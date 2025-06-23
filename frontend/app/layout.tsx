import './globals.css'

export const metadata = {
  title: 'Prompt Analyzer',
  description: 'Write better prompts with AI-powered feedback',
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
