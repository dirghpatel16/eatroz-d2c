import { expect, test } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

test("prelaunch journey is complete and claim-safe", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator("main")).toHaveAttribute("data-commerce-mode", "prelaunch");
  await expect(page.getByRole("button", { name: "Join the First Drop" }).first()).toBeVisible();
  await expect(page.getByText("Final formulation details will be published before orders open.").first()).toBeVisible();
  await expect(page.getByText(/in stock/i)).toHaveCount(0);
  await expect(page.getByText(/customer reviews/i)).toHaveCount(0);
  const results = await new AxeBuilder({ page }).disableRules(["color-contrast"]).analyze();
  expect(results.violations).toEqual([]);
});

test("gallery and lead drawer work", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: /02 gummy/i }).click();
  await expect(page.getByAltText(/macro view of a translucent/i)).toBeVisible();
  await page.getByRole("button", { name: "Join the First Drop" }).first().click();
  await expect(page.getByRole("heading", { name: "Be first to know." })).toBeVisible();
  await expect(page.getByLabel("Email address")).toBeVisible();
});

test("mobile retains a first-screen CTA and reveals the sticky action", async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== "mobile", "mobile-only assertion");
  await page.goto("/");
  await expect(page.getByRole("heading", { name: /your evening ritual/i })).toBeVisible();
  await expect(page.getByRole("button", { name: "Join the First Drop" }).first()).toBeVisible();
  await page.locator("#formula").scrollIntoViewIfNeeded();
  await expect(page.locator(".sticky-cta")).toHaveAttribute("data-visible", "true");
});
