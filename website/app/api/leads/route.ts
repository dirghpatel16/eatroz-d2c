import { NextResponse } from "next/server";
const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
export async function POST(request: Request) {
  const webhook = process.env.LEAD_WEBHOOK_URL;
  if (process.env.LEAD_CAPTURE_APPROVED !== "true" || !webhook?.startsWith("https://")) return NextResponse.json({ error: "capture_unavailable" }, { status: 503 });
  const body = await request.json().catch(() => null) as { email?: unknown } | null;
  if (!body || typeof body.email !== "string" || !emailPattern.test(body.email)) return NextResponse.json({ error: "invalid_email" }, { status: 400 });
  const upstream = await fetch(webhook, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ email: body.email, source: "eatroz-first-drop" }), cache: "no-store", signal: AbortSignal.timeout(5000) }).catch(() => null);
  if (!upstream?.ok) return NextResponse.json({ error: "capture_unavailable" }, { status: 503 });
  return NextResponse.json({ ok: true });
}
