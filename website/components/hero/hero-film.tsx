"use client";
import Image from "next/image";
import { useState } from "react";
import { product } from "@/content/product";
import type { CommerceMode } from "@/lib/commerce/config";

export function HeroFilm({ mode, onAction }: { mode: CommerceMode; onAction: () => void }) {
  const [playing, setPlaying] = useState(true);
  const canSell = mode === "live" && product.price.status === "verified";
  return <section id="hero" className="hero" data-playing={playing} aria-labelledby="hero-title">
    <Image className="hero__media" src={product.media.heroPoster} alt="Provisional Eatroz pouch with red gummies suspended in warm light" fill priority sizes="100vw" />
    <div className="hero__wash" aria-hidden="true" />
    <header className="site-header wrap"><a className="wordmark" href="#hero" aria-label="Eatroz home">Eatroz</a><nav aria-label="Primary"><a href="#formula">Formula</a><a href="#product">Product</a><a href="#proof">Proof</a></nav><button className="header-action" onClick={onAction}>{canSell ? "Bag" : "First drop"}</button></header>
    <div className="hero__content wrap">
      <p className="eyebrow">{product.eyebrow}</p>
      <p className="hero__drop data">{product.launchLabel}</p>
      <h1 id="hero-title" className="display">{product.headline}</h1>
      <p className="hero__intro">A magnesium gummy built around named ingredients, considered ritual, and radical clarity—before the first order opens.</p>
      <button className="button button--light" onClick={onAction}>{canSell ? `Add to Bag — ₹${product.price.value}` : "Join the First Drop"}</button>
    </div>
    <div className="hero__meta data"><span>01 / PRE-LAUNCH</span><button onClick={() => setPlaying(value => !value)} aria-label={`${playing ? "Pause" : "Play"} motion`}>{playing ? "PAUSE MOTION" : "PLAY MOTION"}</button></div>
  </section>;
}
