// @vitest-environment node
import { afterEach, describe, expect, it, vi } from "vitest";
import { NextRequest } from "next/server";
import { POST } from "../app/api/first-access/route";

afterEach(() => { vi.unstubAllEnvs(); vi.unstubAllGlobals(); });

function request(body: unknown) {
  return new NextRequest("http://localhost:3000/api/first-access", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(body),
  });
}

describe("first-access signup endpoint", () => {
  it("refuses to collect email without a provider and privacy URL", async () => {
    vi.stubEnv("EATROZ_WAITLIST_WEBHOOK_URL", "");
    vi.stubEnv("EATROZ_PRIVACY_URL", "");
    const send = vi.fn();
    vi.stubGlobal("fetch", send);
    const response = await POST(request({ email: "buyer@example.com", consent: true, selectedPouches: 1 }));
    expect(response.status).toBe(503);
    expect(send).not.toHaveBeenCalled();
  });

  it("rejects invalid or unconsented submissions", async () => {
    vi.stubEnv("EATROZ_WAITLIST_WEBHOOK_URL", "https://example.com/hook");
    vi.stubEnv("EATROZ_PRIVACY_URL", "https://example.com/privacy");
    const response = await POST(request({ email: "not-an-email", consent: false, selectedPouches: 2 }));
    expect(response.status).toBe(400);
  });

  it("confirms only after the provider accepts the lead", async () => {
    vi.stubEnv("EATROZ_WAITLIST_WEBHOOK_URL", "https://example.com/hook");
    vi.stubEnv("EATROZ_PRIVACY_URL", "https://example.com/privacy");
    const send = vi.fn().mockResolvedValue({ ok: true });
    vi.stubGlobal("fetch", send);
    const response = await POST(request({ email: "buyer@example.com", consent: true, selectedPouches: 2 }));
    expect(response.status).toBe(200);
    expect(await response.json()).toEqual({ status: "registered" });
    expect(send).toHaveBeenCalledOnce();
    expect(JSON.parse(send.mock.calls[0][1].body)).toMatchObject({ email: "buyer@example.com", selectedPouches: 2, source: "eatroz-drop-01" });
  });

  it("does not claim registration when the provider fails", async () => {
    vi.stubEnv("EATROZ_WAITLIST_WEBHOOK_URL", "https://example.com/hook");
    vi.stubEnv("EATROZ_PRIVACY_URL", "https://example.com/privacy");
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: false }));
    const response = await POST(request({ email: "buyer@example.com", consent: true, selectedPouches: 3 }));
    expect(response.status).toBe(502);
  });
});
