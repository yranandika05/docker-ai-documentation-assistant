import type { Metadata } from 'next'

import './globals.css'

export const metadata: Metadata = {
  title: 'Docker AI Assistant',
  description: 'AI-powered Docker documentation assistant',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}