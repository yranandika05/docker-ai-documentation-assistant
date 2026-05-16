import glob
import os
import re


def remove_yaml_frontmatter(text: str) -> str:
    """Remove YAML frontmatter at the top of a Markdown/MDX file."""
    if not text.startswith("---"):
        return text

    lines = text.splitlines(keepends=True)
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return "".join(lines[index + 1 :]).lstrip("\n")

    return text


def clean_text(text: str) -> str:
    """Normalize whitespace and remove excessive blank lines."""
    text = remove_yaml_frontmatter(text)
    lines = [line.strip() for line in text.splitlines()]

    cleaned = []
    blank = False
    for line in lines:
        if line:
            cleaned.append(line)
            blank = False
        elif not blank:
            cleaned.append("")
            blank = True

    return "\n".join(cleaned).strip()


def find_split_point(text: str, start: int, end: int) -> int:
    """Find a good split point near the end of the chunk."""
    if end >= len(text):
        return len(text)

    window = text[start:end]

    # Prefer heading boundaries first
    heading_positions = [m.start() for m in re.finditer(r"(?m)^(#{2,4} .*)", window)]
    if heading_positions:
        pos = heading_positions[-1]
        if pos >= 200:
            return start + pos

    # Prefer paragraph break
    para_pos = window.rfind("\n\n")
    if para_pos != -1 and para_pos >= 200:
        return start + para_pos

    # Prefer sentence ending punctuation
    sentence_match = re.search(r"([\.\!\?][\"']?)(\s+)$", window)
    if sentence_match:
        pos = sentence_match.start(1)
        if pos >= 200:
            return start + pos + len(sentence_match.group(1))

    # Prefer last whitespace before the cutoff
    whitespace_pos = window.rfind(" ")
    if whitespace_pos != -1 and whitespace_pos >= 200:
        return start + whitespace_pos

    return end


def adjust_start(text: str, position: int) -> int:
    """Avoid starting a chunk in the middle of a word."""
    if position <= 0 or position >= len(text):
        return position

    if text[position].isspace():
        while position < len(text) and text[position].isspace():
            position += 1
        return position

    if text[position - 1].isalnum() and text[position].isalnum():
        forward = text.find(" ", position, min(len(text), position + 50))
        if forward != -1:
            return forward + 1

        backward = text.rfind(" ", max(0, position - 50), position)
        if backward != -1:
            return backward + 1

    return position


def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[str]:
    """Chunk text with overlap, preferring heading, paragraph, and sentence boundaries."""
    text = text.strip()
    if not text:
        return []

    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        split = find_split_point(text, start, end)
        if split <= start:
            split = end

        chunk = text[start:split].strip()
        if not chunk:
            break

        if len(chunk) >= 200 or start == 0:
            chunks.append(chunk)
        elif chunks:
            chunks[-1] += "\n\n" + chunk

        if split >= len(text):
            break

        start = max(split - chunk_overlap, start + 1)
        start = adjust_start(text, start)

    if len(chunks) > 1 and len(chunks[-1]) < 200:
        chunks[-2] += "\n\n" + chunks.pop()

    return chunks


def print_chunks():
    docs_dir = os.path.join(os.path.dirname(__file__), "../../data/sample-docs")
    patterns = ["**/*.md", "**/*.mdx"]
    file_paths = []

    for pattern in patterns:
        file_paths.extend(glob.glob(os.path.join(docs_dir, pattern), recursive=True))

    file_paths.sort()
    chunk_count = 0

    for file_path in file_paths:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        content = clean_text(content)
        chunks = chunk_text(content)

        for index, chunk in enumerate(chunks):
            if not chunk.strip():
                continue

            preview_start = chunk.replace("\n", " ")[:150]
            preview_end = chunk.replace("\n", " ")[-150:]
            print(f"source: {file_path}")
            print(f"chunk: {index}")
            print(f"len: {len(chunk)}")
            print(f"start: {preview_start}...")
            print(f"end: ...{preview_end}")
            print()

            chunk_count += 1
            if chunk_count >= 10:
                return


def main():
    print_chunks()


if __name__ == "__main__":
    main()
