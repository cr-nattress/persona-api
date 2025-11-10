import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Person Aggregate Root API - Test App",
  description: "Test application for Person Aggregate Root API",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
