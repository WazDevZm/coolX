import type { Metadata } from 'next'
import { Inter, Poppins } from 'next/font/google'
import './globals.css'

const inter = Inter({ 
  subsets: ['latin'],
  variable: '--font-inter',
})

const poppins = Poppins({ 
  subsets: ['latin'],
  weight: ['300', '400', '500', '600', '700', '800', '900'],
  variable: '--font-poppins',
})

export const metadata: Metadata = {
  title: 'TriviaMaster - Test Your Knowledge',
  description: 'Challenge yourself with thousands of trivia questions across multiple categories. Compete with friends and climb the leaderboards!',
  keywords: 'trivia, quiz, knowledge, brain games, education, fun',
  authors: [{ name: 'TriviaMaster Team' }],
  openGraph: {
    title: 'TriviaMaster - Test Your Knowledge',
    description: 'Challenge yourself with thousands of trivia questions across multiple categories.',
    type: 'website',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={`${inter.variable} ${poppins.variable}`}>
      <body className="font-sans antialiased">
        {children}
      </body>
    </html>
  )
}
