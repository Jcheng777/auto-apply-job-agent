import "./globals.css";
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import Link from "next/link";
import { Button } from "@/components/ui/button";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Job Application Autofiller",
  description: "Automate your job applications with intelligent form filling",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className + " bg-blue-50 min-h-screen"}>
        <nav className="w-full bg-white shadow-sm py-4 mb-8">
          <div className="max-w-4xl mx-auto flex gap-4 px-4">
            <Link href="/applications">
              <Button variant="link" className="text-lg px-2">
                Applications
              </Button>
            </Link>
            <Link href="/profile">
              <Button variant="link" className="text-lg px-2">
                Profile
              </Button>
            </Link>
          </div>
        </nav>
        {children}
      </body>
    </html>
  );
}
