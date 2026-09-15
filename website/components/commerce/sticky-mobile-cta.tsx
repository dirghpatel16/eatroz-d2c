"use client";
import { useEffect, useState } from "react";
import { product } from "@/content/product";
import type { CommerceMode } from "@/lib/commerce/config";

export function StickyMobileCta({ mode, onAction }: { mode: CommerceMode; onAction: () => void }) {
  const [pastHero, setPastHero] = useState(false);
  useEffect(() => { const update = () => setPastHero((document.getElementById("hero")?.getBoundingClientRect().bottom ?? 1) <= 0); update(); window.addEventListener("scroll", update, { passive: true }); return () => window.removeEventListener("scroll", update); }, []);
  const canSell = mode === "live" && product.price.status === "verified";
  return <div className="sticky-cta" data-visible={pastHero} aria-hidden={!pastHero}><span className="data">DROP 01</span><button className="button" onClick={onAction} tabIndex={pastHero ? 0 : -1}>{canSell ? `Add to Bag — ₹${product.price.value}` : "Join the First Drop"}</button></div>;
}
