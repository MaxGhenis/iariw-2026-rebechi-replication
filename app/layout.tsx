import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'What Can Money Buy? — IARIW 2026 discussant slides',
  description:
    'Discussant presentation of Rebechi, Van Kerm, Paradowski, Lepinteur & Rohde (2026), Citizens United and state tax progressivity',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
