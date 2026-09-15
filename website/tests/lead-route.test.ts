import { afterEach, describe, expect, it, vi } from "vitest";
import { POST } from "@/app/api/leads/route";

afterEach(() => { vi.unstubAllEnvs(); vi.restoreAllMocks(); });
describe("lead route", () => {
  it("fails closed when capture is unconfigured", async () => {
    vi.stubEnv("LEAD_WEBHOOK_URL", "");
    vi.stubEnv("LEAD_CAPTURE_APPROVED", "");
    const response = await POST(new Request("http://local/api/leads", { method: "POST", body: JSON.stringify({ email: "person@example.com" }) }));
    expect(response.status).toBe(503);
  });
  it("rejects invalid email", async () => {
    vi.stubEnv("LEAD_WEBHOOK_URL", "https://hooks.example.test/eatroz");
    vi.stubEnv("LEAD_CAPTURE_APPROVED", "true");
    const response = await POST(new Request("http://local/api/leads", { method: "POST", body: JSON.stringify({ email: "broken" }) }));
    expect(response.status).toBe(400);
  });
});
