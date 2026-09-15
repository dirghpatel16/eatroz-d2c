"use client";
import Image from "next/image";
import { useState } from "react";
import { product } from "@/content/product";
const images = [
  { src: product.media.pouch, alt: "Provisional Eatroz pouch in warm studio light", label: "Pouch" },
  { src: product.media.gummy, alt: "Macro view of a translucent deep-red gummy", label: "Gummy" },
  { src: product.media.detail, alt: "Close detail of the provisional pouch material and artwork", label: "Material" },
];
export function ProductGallery() {
  const [selected, setSelected] = useState(0); const image = images[selected];
  return <section className="gallery section" aria-labelledby="gallery-title"><div className="wrap"><div className="section-head"><p className="eyebrow">PRODUCT STUDY</p><h2 id="gallery-title" className="display">A closer look.</h2><p>Texture, material, appetite. Provisional images today; deterministic production photography before launch.</p></div><figure className="gallery__stage"><Image src={image.src} alt={image.alt} fill sizes="100vw" /><figcaption className="data">0{selected + 1} / 03 — PROVISIONAL CAMPAIGN VISUAL</figcaption></figure><div className="gallery__nav" aria-label="Choose product view">{images.map((item, index) => <button type="button" aria-pressed={selected === index} onClick={() => setSelected(index)} key={item.src}><span className="data">0{index + 1}</span><span>{item.label}</span></button>)}</div></div></section>;
}
