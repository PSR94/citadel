import type { Metadata } from "next";
import { IBM_Plex_Mono, Space_Grotesk } from "next/font/google";

import { Providers } from "@/components/providers";
import RuntimeShell from "@/components/runtime-shell";

import "./globals.css";

const sans = Space_Grotesk({
  subsets: ["latin"],
  variable: "--font-sans",
});

const mono = IBM_Plex_Mono({
  subsets: ["latin"],
  weight: ["400", "500", "600"],
  variable: "--font-mono",
});

export const metadata: Metadata = {
  title: "CITADEL",
  description: "Enterprise Retrieval Intelligence Platform",
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${sans.variable} ${mono.variable}`}>
      <body className="font-[family-name:var(--font-sans)] antialiased">
        <Providers>
          <RuntimeShell>{children}</RuntimeShell>
        </Providers>
      </body>
    </html>
  );
}
