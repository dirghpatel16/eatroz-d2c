"use client";
import { useEffect, useRef, useState } from "react";
import { product } from "@/content/product";
import { buildCheckoutUrl } from "@/lib/commerce/checkout";

export function CartDrawer({ open, checkoutUrl, onClose }: { open: boolean; checkoutUrl: string; onClose: () => void }) {
  const dialog = useRef<HTMLDialogElement>(null); const [quantity, setQuantity] = useState(1);
  useEffect(() => { if (open && !dialog.current?.open) dialog.current?.showModal(); if (!open && dialog.current?.open) dialog.current.close(); }, [open]);
  if (product.price.status !== "verified") return null;
  return <dialog ref={dialog} className="drawer" onClose={onClose} aria-labelledby="cart-title"><button className="drawer__close data" onClick={onClose} aria-label="Close bag">CLOSE</button><h2 id="cart-title" className="display">Your bag</h2><p>{product.name}</p><label>Quantity<input type="number" min="1" max="12" value={quantity} onChange={event => setQuantity(Number(event.target.value))} /></label><a className="button" href={buildCheckoutUrl(checkoutUrl, quantity)}>Checkout — ₹{product.price.value * quantity}</a></dialog>;
}
