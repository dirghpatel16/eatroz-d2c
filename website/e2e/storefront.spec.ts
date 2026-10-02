import { expect, test } from "@playwright/test";

test("commercial product hierarchy is clear while the page remains pre-launch", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: /magnesium gummies/i, level: 1 })).toBeVisible();
  await expect(page.getByRole("region", { name: /product images/i })).toBeVisible();
  await expect(page.getByRole("complementary", { name: /first access/i })).toContainText("Price to be revealed");
  await expect(page.getByRole("button", { name: "Get first access" }).last()).toBeVisible();
  await expect(page.getByText(/no product order or payment is being collected/i)).toBeVisible();
  await expect(page.getByRole("button", { name: /add to cart/i })).toHaveCount(0);
});

test("gallery uses the approved pouch, bead and evening images", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByTestId("active-product-image")).toHaveAttribute("alt", /pouch, front view/i);
  await page.getByRole("button", { name: "View gummy detail" }).click();
  await expect(page.getByTestId("active-product-image")).toHaveAttribute("src", /eatroz-gummy-beads-v3.png/);
  await page.getByRole("button", { name: "View evening ritual" }).click();
  await expect(page.getByTestId("active-product-image")).toHaveAttribute("src", /eatroz-evening-ritual-v2.png/);
});

test("shows the pouch dimensions as editorial information rather than a product claim", async ({ page }) => {
  await page.goto("/");
  const details = page.locator("#details");
  await details.scrollIntoViewIfNeeded();
  await expect(details).toContainText("25.5 cm × 21.5 cm × 8 cm");
  await expect(details).toContainText(/editorial visualization/i);
  await expect(details).toContainText(/no health, treatment or dosage claims/i);
});

test("first-access dialog is accessible and never implies a connected waitlist", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: "Get first access" }).last().click();
  const dialog = page.getByRole("dialog", { name: /first access/i });
  await expect(dialog).toBeVisible();
  await expect(dialog).toContainText(/registration is not connected yet/i);
  await dialog.getByRole("button", { name: /save interest on this device/i }).click();
  await expect(dialog).toContainText(/saved on this device only/i);
  await page.keyboard.press("Escape");
  await expect(dialog).toHaveCount(0);
});

test("mobile layout has no horizontal overflow and retains the commerce action", async ({ page, isMobile }) => {
  test.skip(!isMobile, "Mobile-only layout");
  await page.goto("/");
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1)).toBe(true);
  await page.getByRole("button", { name: "Get first access" }).last().scrollIntoViewIfNeeded();
  await page.evaluate(() => window.scrollBy(0, 550));
  await expect(page.locator(".mobile-buy-bar")).toBeVisible();
});
