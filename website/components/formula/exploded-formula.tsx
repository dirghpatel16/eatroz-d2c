"use client";
import Image from "next/image";
import { useEffect, useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { product } from "@/content/product";

export function ExplodedFormula() {
  const root = useRef<HTMLElement>(null);
  useEffect(() => { if (matchMedia("(prefers-reduced-motion: reduce)").matches) return; gsap.registerPlugin(ScrollTrigger); const context = gsap.context(() => { gsap.fromTo("[data-form]", { y: 48, opacity: 0 }, { y: 0, opacity: 1, stagger: .12, scrollTrigger: { trigger: root.current, start: "top 70%", end: "bottom 72%", scrub: true } }); }, root); return () => context.revert(); }, []);
  return <section id="formula" ref={root} className="formula section" aria-labelledby="formula-title"><div className="wrap formula__grid"><div className="formula__visual"><div className="formula__image"><Image src={product.media.gummy} alt="Macro view of a provisional deep-red Eatroz gummy" fill sizes="(max-width: 760px) 100vw, 45vw" /><span className="orb orb--one"/><span className="orb orb--two"/></div></div><div className="formula__copy"><p className="eyebrow">FORMULA INTENT — FINAL CONFIRMATION PENDING</p><h2 id="formula-title" className="display">Four forms. One considered direction.</h2><p className="lede">The intended formulation is being developed around four named forms. Final chemistry and quantities will appear here only after approval.</p><ol>{product.formulaIntent.map((form, index) => <li data-form key={form}><span className="data">0{index + 1}</span><strong className="display">{form}</strong></li>)}</ol></div></div></section>;
}
