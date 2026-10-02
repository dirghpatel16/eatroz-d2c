import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Eatroz | Magnesium Gummies | Drop 01",
  description: "Meet Eatroz Magnesium Gummies: a pouch-format chewable ritual. Drop 01 preview for India. Full product and ordering details will be published before launch.",
  robots: { index: false, follow: false },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en-IN"><body>{children}</body></html>;
}
