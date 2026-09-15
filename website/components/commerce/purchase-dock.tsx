import Image from "next/image";
import { product } from "@/content/product";
import type { CommerceMode } from "@/lib/commerce/config";

export function PurchaseDock({ mode, onAction }: { mode: CommerceMode; onAction: () => void }) {
  const canSell = mode === "live" && product.price.status === "verified";
  return <section id="product" className="purchase section" aria-labelledby="purchase-title">
    <div className="purchase__visual"><Image src={product.media.pouch} alt="Provisional Eatroz Magnesium Gummies pouch" fill sizes="(max-width: 760px) 100vw, 50vw" /><span className="visual-note data">PROVISIONAL CAMPAIGN VISUAL</span></div>
    <div className="purchase__copy"><p className="eyebrow">THE FIRST DROP</p><h2 id="purchase-title" className="display">Magnesium, without the mystery.</h2><p className="lede">One considered nightly ritual. Every final formulation detail will be named before orders open.</p><dl className="status-list"><div><dt>Formula</dt><dd>Final confirmation pending</dd></div><div><dt>Serving</dt><dd>Final label pending</dd></div><div><dt>Launch price</dt><dd>{product.price.status === "verified" ? `₹${product.price.value}` : "To be announced"}</dd></div></dl><button className="button" onClick={onAction}>{canSell ? `Add to Bag — ₹${product.price.value}` : "Join the First Drop"}</button></div>
  </section>;
}
