import type { Metadata } from "next";
import { Cormorant_Garamond, DM_Mono, Manrope } from "next/font/google";
import { SmoothScroll } from "@/components/motion/smooth-scroll";
import "./globals.css";

const display = Cormorant_Garamond({ subsets: ["latin"], weight: ["400", "500", "600"], variable: "--font-display" });
const body = Manrope({ subsets: ["latin"], variable: "--font-body" });
const data = DM_Mono({ subsets: ["latin"], weight: ["400", "500"], variable: "--font-data" });

export const metadata: Metadata = {
  title: "Eatroz — Magnesium, fully named",
  description: "A transparent first look at Eatroz Magnesium Gummies. Final formulation details publish before orders open.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en" className={`${display.variable} ${body.variable} ${data.variable}`}><body><SmoothScroll>{children}</SmoothScroll></body></html>;
}
