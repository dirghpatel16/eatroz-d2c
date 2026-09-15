import { describe, expect, it } from "vitest";
import { buildCheckoutUrl } from "@/lib/commerce/checkout";

describe("buildCheckoutUrl", () => {
  it.each([
    [Number.NaN, "1"],
    [-2, "1"],
    [2.9, "2"],
    [99, "12"],
  ])("normalizes quantity %s to %s", (quantity, expected) => {
    const result = new URL(
      buildCheckoutUrl("https://checkout.example.test/cart", quantity),
    );
    expect(result.searchParams.get("quantity")).toBe(expected);
  });
});
