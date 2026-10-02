export function firstAccessConfig() {
  const webhook = process.env.EATROZ_WAITLIST_WEBHOOK_URL;
  const privacyUrl = process.env.EATROZ_PRIVACY_URL;
  if (!webhook || !privacyUrl) return null;
  try {
    if (new URL(webhook).protocol !== "https:" || new URL(privacyUrl).protocol !== "https:") return null;
  } catch {
    return null;
  }
  return { webhook, privacyUrl, token: process.env.EATROZ_WAITLIST_WEBHOOK_TOKEN };
}

export function parseSignup(value: unknown): { email: string; selectedPouches: 1 | 2 | 3 } | null {
  if (typeof value !== "object" || value === null) return null;
  const candidate = value as Record<string, unknown>;
  const email = typeof candidate.email === "string" ? candidate.email.trim() : "";
  if (email.length < 5 || email.length > 254 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return null;
  if (candidate.consent !== true) return null;
  if (candidate.selectedPouches !== 1 && candidate.selectedPouches !== 2 && candidate.selectedPouches !== 3) return null;
  return { email, selectedPouches: candidate.selectedPouches };
}
