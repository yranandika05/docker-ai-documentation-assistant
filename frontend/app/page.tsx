'use client'

import { useState } from 'react'

export default function Home() {
  const [question, setQuestion] = useState('')
  const [messages, setMessages] = useState<{question: string, answer: string, citations: string[]}[]>([])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    // TODO: call backend /chat
    const response = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question })
    })
    const data = await response.json()
    setMessages([...messages, { question, answer: data.answer, citations: data.citations }])
    setQuestion('')
  }

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <h1 className="text-2xl font-bold mb-4">Docker AI Documentation Assistant</h1>
      <div className="max-w-2xl mx-auto">
        <div className="bg-white p-4 rounded shadow mb-4">
          {messages.map((msg, i) => (
            <div key={i} className="mb-4">
              <p className="font-semibold">Q: {msg.question}</p>
              <p>A: {msg.answer}</p>
              {msg.citations.length > 0 && (
                <div>
                  <p className="font-semibold">Citations:</p>
                  <ul>
                    {msg.citations.map((cit, j) => <li key={j}>{cit}</li>)}
                  </ul>
                </div>
              )}
            </div>
          ))}
        </div>
        <form onSubmit={handleSubmit} className="flex">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask about Docker..."
            className="flex-1 p-2 border rounded-l"
          />
          <button type="submit" className="bg-blue-500 text-white p-2 rounded-r">Ask</button>
        </form>
      </div>
    </div>
  )
}