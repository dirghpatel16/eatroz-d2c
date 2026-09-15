import { describe, expect, it } from "vitest";
import { parseCommerceConfig } from "@/lib/commerce/config";

describe("parseCommerceConfig", () => {
  it("fails closed to prelaunch", () => {
    expect(parseCommerceConfig({}, false)).toEqual({
      mode: "prelaunch",
      checkoutUrl: null,
    });
    expect(
      parseCommerceConfig({ NEXT_PUBLIC_COMMERCE_MODE: "broken" }, false),
    ).toEqual({ mode: "prelaunch", checkoutUrl: null });
  });

  it("rejects incomplete or unsafe live configurations", () => {
    expect(
      parseCommerceConfig(
        {
          NEXT_PUBLIC_COMMERCE_MODE: "live",
          NEXT_PUBLIC_COMMERCE_APPROVED: "true",
          NEXT_PUBLIC_CHECKOUT_URL: "http://unsafe.test",
        },
        true,
      ).mode,
    ).toBe("prelaunch");
    expect(
      parseCommerceConfig(
        {
          NEXT_PUBLIC_COMMERCE_MODE: "live",
          NEXT_PUBLIC_COMMERCE_APPROVED: "true",
          NEXT_PUBLIC_CHECKOUT_URL: "https://checkout.example.test/cart",
        },
        false,
      ).mode,
    ).toBe("prelaunch");
    expect(
      parseCommerceConfig(
        {
          NEXT_PUBLIC_COMMERCE_MODE: "live",
          NEXT_PUBLIC_CHECKOUT_URL: "https://checkout.example.test/cart",
        },
        true,
      ).mode,
    ).toBe("prelaunch");
  });

  it("enables live mode only after explicit approval", () => {
    expect(
      parseCommerceConfig(
        {
          NEXT_PUBLIC_COMMERCE_MODE: "live",
          NEXT_PUBLIC_COMMERCE_APPROVED: "true",
          NEXT_PUBLIC_CHECKOUT_URL: "https://checkout.example.test/cart",
        },
        true,
      ),
    ).toEqual({
      mode: "live",
      checkoutUrl: "https://checkout.example.test/cart",
    });
  });
});
