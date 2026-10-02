"use client";

import Image from "next/image";
import { type FormEvent, useCallback, useEffect, useRef, useState } from "react";
import { displayFact, product } from "../content/product";

const packOptions = [1, 2, 3] as const;

function Arrow({ diagonal = false }: { diagonal?: boolean }) {
  return <span aria-hidden="true" className="arrow-icon">{diagonal ? "↗" : "→"}</span>;
}

function Header({ onAccess }: { onAccess: () => void }) {
  return <>
    <div className="announcement"><span>DROP 01 / PRE-LAUNCH</span><span>Magnesium Gummies · pouch format</span><button onClick={onAccess}>Get first access <Arrow diagonal /></button></div>
    <header className="site-header"><div className="site-header-inner">
      <a className="wordmark" href="#top" aria-label="Eatroz home">eatroz<span>.</span></a>
      <nav className="main-nav" aria-label="Main navigation"><a href="#product">The product</a><a href="#texture">The texture</a><a href="#details">Product details</a></nav>
      <button className="header-action" onClick={onAccess}>First access <Arrow diagonal /></button>
    </div></header>
  </>;
}

function ProductGallery() {
  const [active, setActive] = useState(0);
  const [zoomed, setZoomed] = useState(false);
  const image = product.images[active];
  return <section className="gallery" aria-label="Product images">
    <div className="gallery-main"><span className="gallery-count">{String(active + 1).padStart(2, "0")} — {String(product.images.length).padStart(2, "0")}</span>
      <button type="button" className={`gallery-image-button ${zoomed ? "is-zoomed" : ""}`} aria-label={zoomed ? "Close enlarged image" : "Enlarge product image"} onClick={() => setZoomed((value) => !value)}>
        <Image data-testid="active-product-image" className={image.kind === "cutout" ? "gallery-active cutout" : "gallery-active"} src={image.src} alt={image.alt} width={1122} height={1402} sizes="(max-width: 760px) 100vw, 54vw" priority={active === 0} />
      </button><span className="gallery-caption">{image.label.replace("View ", "")}</span><span className="gallery-zoom">{zoomed ? "Tap to close" : "Tap to inspect"}</span>
    </div>
    <div className="gallery-thumbs" role="group" aria-label="Select product image">{product.images.map((item, index) => <button key={item.src} type="button" className={`gallery-thumb ${active === index ? "active" : ""}`} aria-label={item.label} aria-pressed={active === index} onClick={() => { setActive(index); setZoomed(false); }}><Image src={item.src} alt="" width={150} height={150} sizes="(max-width: 760px) 30vw, 150px" /></button>)}</div>
    <p className="gallery-legal">Editorial product visualization. Final pouch artwork, formula and label details will be confirmed before sale.</p>
  </section>;
}

function ProductIntro() {
  return <div className="product-intro"><span className="kicker"><i /> EATROZ / DROP 01</span><h1>Magnesium Gummies<span>.</span></h1><p>Bead-like chewable gummies in a resealable pouch — an easy, no-mixing part of an evening routine.</p><ul className="hero-facts" aria-label="Product highlights"><li>Chew directly</li><li>Pouch format</li><li>Formula details pending</li></ul></div>;
}

function BuyBox({ onAccess, packs, onPacksChange }: { onAccess: () => void; packs: (typeof packOptions)[number]; onPacksChange: (count: (typeof packOptions)[number]) => void }) {
  const price = displayFact<number>(product.price);
  return <aside className="buybox" id="buybox" aria-label="First access"><div className="buybox-top"><span className="field-label">AVAILABILITY</span><span className="status-chip">PRE-LAUNCH</span></div><p className="price-line">{price === null ? "Price to be revealed" : new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 }).format(price)}</p><p className="buybox-support">This is an editorial preview. No product order or payment is being collected.</p><div className="plan-header"><span className="field-label">POUCH PLAN PREVIEW</span><span>Select a starting point</span></div><div className="pack-options" role="group" aria-label="Pouch plan preview">{packOptions.map((count) => <button key={count} type="button" className={`pack-option ${packs === count ? "selected" : ""}`} aria-pressed={packs === count} aria-label={`${count} ${count === 1 ? "pouch" : "pouches"}`} onClick={() => onPacksChange(count)}><strong>{count}</strong><span>{count === 1 ? "Pouch" : "Pouches"}</span></button>)}</div><p className="selection-summary">Your preview selection: {packs} {packs === 1 ? "pouch" : "pouches"}. Bundle details will be published at launch.</p><button type="button" className="primary-button" onClick={onAccess}>Get first access <Arrow /></button><p className="cta-note">First access is not live until signup is connected.</p><div className="buybox-note"><span>WHAT WE&apos;LL PUBLISH</span><p>Approved serving directions, full ingredients, pricing, delivery and final pack information.</p></div></aside>;
}

function AccessDialog({ onClose, registrationEnabled, privacyUrl, packs }: { onClose: () => void; registrationEnabled: boolean; privacyUrl: string | null; packs: (typeof packOptions)[number] }) {
  const dialogRef = useRef<HTMLElement>(null); const [email, setEmail] = useState(""); const [consent, setConsent] = useState(false); const [status, setStatus] = useState<"idle" | "saving" | "registered" | "local" | "error">("idle"); const [message, setMessage] = useState("");
  useEffect(() => { const previousFocus = document.activeElement as HTMLElement | null; const previousOverflow = document.body.style.overflow; document.body.style.overflow = "hidden"; dialogRef.current?.focus(); const onKeyDown = (event: KeyboardEvent) => { if (event.key === "Escape") onClose(); if (event.key !== "Tab") return; const focusables = Array.from(dialogRef.current?.querySelectorAll<HTMLElement>("button:not([disabled]), input:not([disabled]), a[href]") ?? []); if (!focusables.length) return; const first = focusables[0]; const last = focusables[focusables.length - 1]; if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); } if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); } }; window.addEventListener("keydown", onKeyDown); return () => { window.removeEventListener("keydown", onKeyDown); document.body.style.overflow = previousOverflow; previousFocus?.focus(); }; }, [onClose]);
  const saveLocal = () => { try { window.localStorage.setItem("eatroz-drop01-preview-interest", JSON.stringify({ interested: true, selectedPouches: packs })); setStatus("local"); } catch { setStatus("error"); setMessage("This browser could not save your preview interest. No registration was made."); } };
  const submit = async (event: FormEvent<HTMLFormElement>) => { event.preventDefault(); setStatus("saving"); setMessage(""); try { const response = await fetch("/api/first-access", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ email, consent, selectedPouches: packs }) }); if (!response.ok) throw new Error("Provider did not confirm registration"); setStatus("registered"); } catch { setStatus("error"); setMessage("We could not confirm registration. Please try again later; you are not on the list yet."); } };
  return <div className="modal-backdrop" onMouseDown={(event) => { if (event.target === event.currentTarget) onClose(); }}><section ref={dialogRef} tabIndex={-1} className="access-dialog" role="dialog" aria-modal="true" aria-labelledby="access-title"><button className="dialog-close" aria-label="Close first access" onClick={onClose}>×</button><span className="field-label">DROP 01 / EARLY ACCESS</span><h2 id="access-title">First access,<br />when it&apos;s ready.</h2>{registrationEnabled && privacyUrl ? <>{status === "registered" ? <p className="access-status" role="status">You&apos;re registered for Drop 01 updates. We&apos;ll contact you using the email you provided.</p> : <form className="access-form" onSubmit={submit}><p>Join for launch updates. No payment or product order is taken here.</p><label htmlFor="access-email">Email address</label><input id="access-email" type="email" autoComplete="email" required value={email} onChange={(event) => setEmail(event.target.value)} placeholder="you@example.com" /><label className="access-consent"><input type="checkbox" required checked={consent} onChange={(event) => setConsent(event.target.checked)} /><span>I agree to receive Drop 01 updates and have read the <a href={privacyUrl} target="_blank" rel="noopener noreferrer">privacy notice</a>.</span></label><button className="secondary-button" type="submit" disabled={status === "saving"}>{status === "saving" ? "Confirming…" : "Join first access"} <Arrow /></button></form>}</> : <>{status === "local" ? <p className="access-status" role="status">Saved on this device only. This is not a registered waitlist signup; we cannot contact you from this preview.</p> : <><p>Registration is not connected yet. We won&apos;t ask for your email or imply you&apos;re on a list until the signup service is live.</p><button className="secondary-button" type="button" onClick={saveLocal}>Save interest on this device <Arrow /></button></>}</>}{status === "error" && <p className="access-error" role="alert">{message}</p>}<p className="dialog-small">Final formula, price, delivery terms and first-access details will be published before orders open.</p><button className="dialog-back" onClick={onClose}>Back to the product <Arrow /></button></section></div>;
}

export function Storefront({ sections, footer, registrationEnabled, privacyUrl }: { sections: React.ReactNode; footer: React.ReactNode; registrationEnabled: boolean; privacyUrl: string | null }) {
  const [dialogOpen, setDialogOpen] = useState(false); const [showMobileBar, setShowMobileBar] = useState(false); const [packs, setPacks] = useState<(typeof packOptions)[number]>(1); const openAccess = () => setDialogOpen(true); const closeAccess = useCallback(() => setDialogOpen(false), []);
  useEffect(() => { const action = document.querySelector(".buybox .primary-button"); if (!action || typeof IntersectionObserver === "undefined") return; const observer = new IntersectionObserver(([entry]) => setShowMobileBar(!entry.isIntersecting && entry.boundingClientRect.bottom < 0)); observer.observe(action); return () => observer.disconnect(); }, []);
  return <div id="top" className="site-shell"><a className="skip-link" href="#main-content">Skip to main content</a><Header onAccess={openAccess} /><main id="main-content"><div className="breadcrumb page-container"><a href="#top">Home</a><span>/</span><span>Drop 01</span></div><section className="product-section page-container" id="product"><div className="hero-copy"><ProductIntro /><BuyBox onAccess={openAccess} packs={packs} onPacksChange={setPacks} /></div><ProductGallery /></section>{sections}</main>{footer}<div className="mobile-buy-bar" hidden={!showMobileBar}><div><span>DROP 01</span><strong>Magnesium Gummies</strong></div><button onClick={openAccess}>First access <Arrow /></button></div>{dialogOpen && <AccessDialog onClose={closeAccess} registrationEnabled={registrationEnabled} privacyUrl={privacyUrl} packs={packs} />}</div>;
}
