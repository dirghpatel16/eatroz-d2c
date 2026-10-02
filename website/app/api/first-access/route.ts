import { NextRequest, NextResponse } from "next/server";
import { firstAccessConfig, parseSignup } from "@/lib/first-access";

export async function POST(request: NextRequest) {
  const config = firstAccessConfig();
  if (!config) return NextResponse.json({ error: "Registration is not connected yet." }, { status: 503, headers: { "Cache-Control": "no-store" } });

  let payload: unknown;
  try {
    const raw = await request.text();
    if (raw.length > 4096) return NextResponse.json({ error: "Submission is too large." }, { status: 413 });
    payload = JSON.parse(raw);
  } catch {
    return NextResponse.json({ error: "Invalid submission." }, { status: 400 });
  }
  const signup = parseSignup(payload);
  if (!signup) return NextResponse.json({ error: "Enter a valid email and agree to the privacy notice." }, { status: 400 });

  try {
    const headers: Record<string, string> = { "Content-Type": "application/json" };
    if (config.token) headers.Authorization = `Bearer ${config.token}`;
    const provider = await fetch(config.webhook, {
      method: "POST",
      headers,
      body: JSON.stringify({ ...signup, source: "eatroz-drop-01", consentAt: new Date().toISOString(), consentVersion: "v1" }),
      cache: "no-store",
      signal: AbortSignal.timeout(8000),
    });
    if (!provider.ok) return NextResponse.json({ error: "We could not confirm registration. Please try again later." }, { status: 502 });
    return NextResponse.json({ status: "registered" }, { headers: { "Cache-Control": "no-store" } });
  } catch {
    return NextResponse.json({ error: "We could not confirm registration. Please try again later." }, { status: 502 });
  }
}
