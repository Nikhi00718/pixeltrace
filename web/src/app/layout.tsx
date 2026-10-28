import type { Metadata } from "next";
import { JetBrains_Mono, Press_Start_2P } from "next/font/google";
import Link from "next/link";
import "./globals.css";

const pixel = Press_Start_2P({ weight: "400", subsets: ["latin"], variable: "--font-pixel" });
const mono = JetBrains_Mono({ subsets: ["latin"], variable: "--font-mono" });

export const metadata: Metadata = {
  title: "PixelTrace — watch your C++ solve it",
  description: "Write C++ for classic interview problems and watch each line play out as a pixel-art scene.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className={`${pixel.variable} ${mono.variable}`}>
      <body>
        <header className="topbar">
          <Link href="/" className="brand">
            <span className="brand-mark" aria-hidden>▣</span> PIXELTRACE
          </Link>
          <nav>
            <Link href="/">Worlds</Link>
            <Link href="/about">How it works</Link>
          </nav>
        </header>
        <main>{children}</main>
      </body>
    </html>
  );
}
