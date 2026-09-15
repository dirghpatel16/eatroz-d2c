"use client";
import { type FormEvent, useEffect, useRef, useState } from "react";
import { submitLead } from "@/lib/leads/submit";

export function LeadDrawer({ open, onClose }: { open: boolean; onClose: () => void }) {
  const dialog = useRef<HTMLDialogElement>(null);
  const [status, setStatus] = useState<"idle" | "sending" | "success" | "error">("idle");
  useEffect(() => { if (open && !dialog.current?.open) dialog.current?.showModal(); if (!open && dialog.current?.open) dialog.current.close(); }, [open]);
  async function submit(event: FormEvent<HTMLFormElement>) { event.preventDefault(); setStatus("sending"); const form = new FormData(event.currentTarget); try { await submitLead(String(form.get("email"))); setStatus("success"); } catch { setStatus("error"); } }
  return <dialog ref={dialog} className="drawer" onClose={onClose} aria-labelledby="lead-title"><button className="drawer__close data" onClick={onClose} aria-label="Close first drop form">CLOSE</button><p className="eyebrow">EARLY ACCESS</p><h2 id="lead-title" className="display">Be first to know.</h2><p>Launch timing, final formulation, and the first order window—nothing else.</p>{status === "success" ? <p className="drawer__success">You&apos;re on the list.</p> : <form onSubmit={submit}><label>Email address<input name="email" type="email" required autoComplete="email" placeholder="you@example.com" /></label><small>By joining, you agree to receive Eatroz launch updates. Read our <a href="/privacy">privacy notice</a>.</small><button className="button" disabled={status === "sending"}>{status === "sending" ? "Joining…" : "Join the First Drop"}</button>{status === "error" && <p role="alert">Capture is not live yet. Your email remains here; please retry later.</p>}</form>}</dialog>;
}
