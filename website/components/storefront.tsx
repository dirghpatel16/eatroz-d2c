"use client";
import { useState } from "react";
import type { CommerceConfig } from "@/lib/commerce/config";
import { product } from "@/content/product";
import { HeroFilm } from "@/components/hero/hero-film";
import { PurchaseDock } from "@/components/commerce/purchase-dock";
import { LeadDrawer } from "@/components/commerce/lead-drawer";
import { CartDrawer } from "@/components/commerce/cart-drawer";
import { StickyMobileCta } from "@/components/commerce/sticky-mobile-cta";
import { ExplodedFormula } from "@/components/formula/exploded-formula";
import { OxideProof } from "@/components/proof/oxide-proof";
import { ProductGallery } from "@/components/gallery/product-gallery";
import { FactsDisclosure } from "@/components/facts/facts-disclosure";
import { TrustSection } from "@/components/trust/trust-section";

export function Storefront({ commerce }: { commerce: CommerceConfig }) {
  const [open, setOpen] = useState(false); const action = () => setOpen(true);
  const canSell = commerce.mode === "live" && product.price.status === "verified";
  const actionLabel = canSell ? `Add to Bag — ₹${product.price.value}` : "Join the First Drop";
  return <><main id="main-content" data-commerce-mode={commerce.mode}><HeroFilm mode={commerce.mode} onAction={action}/><PurchaseDock mode={commerce.mode} onAction={action}/><ExplodedFormula/><OxideProof/><ProductGallery/><FactsDisclosure/><TrustSection/><section className="final-cta section" aria-labelledby="final-title"><div className="wrap"><p className="eyebrow">DROP 01 / EARLY ACCESS</p><h2 id="final-title" className="display">Meet your evening magnesium ritual.</h2><p>{product.delivery.status === "verified" ? product.delivery.value : "Delivery timing and returns terms will be published before orders open."}</p><button className="button button--light" onClick={action}>{actionLabel}</button><div className="faq"><details><summary>Is the formula final?</summary><p>No. Every unresolved formulation field remains visibly pending until the approved label is available.</p></details><details><summary>Are these final product photographs?</summary><p>No. They are provisional AI-generated campaign concepts based on a provisional pouch design.</p></details><details><summary>Can I order now?</summary><p>{canSell ? "Yes—use Add to Bag to continue to checkout." : "Not yet. Join the First Drop for the launch update."}</p></details></div></div></section></main><footer className="site-footer"><div className="wrap"><a className="wordmark" href="#hero">Eatroz</a><nav aria-label="Footer"><span>Contact pending</span><a href="/privacy">Privacy</a><a href="/terms">Terms</a></nav><p className="data">PRODUCT AND CAMPAIGN VISUALS ARE PROVISIONAL AI-GENERATED CONCEPTS.</p></div></footer><StickyMobileCta mode={commerce.mode} onAction={action}/>{commerce.mode === "live" && commerce.checkoutUrl ? <CartDrawer open={open} checkoutUrl={commerce.checkoutUrl} onClose={() => setOpen(false)}/> : <LeadDrawer open={open} onClose={() => setOpen(false)}/>}</>;
}
