export async function submitLead(email: string): Promise<void> {
  const response = await fetch("/api/leads", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ email }) });
  if (!response.ok) throw new Error("lead_submission_failed");
}
