import { describe, expect, it } from "vitest";
import { displayFact, product } from "../content/product";

describe("product fact contract", () => {
  it("does not promote pending commercial details into approved copy", () => {
    expect(product.price.status).toBe("verification_pending");
    expect(product.reviews.status).toBe("verification_pending");
    expect(product.elementalMagnesium.status).toBe("verification_pending");
    expect(product.servingSize.status).toBe("verification_pending");
    expect(displayFact(product.price)).toBeNull();
    expect(displayFact(product.reviews)).toBeNull();
  });

  it("can display a verified fact", () => {
    expect(displayFact({ status: "verified", value: 899 })).toBe(899);
  });

  it("uses the existing Eatroz pouch and chewable imagery", () => {
    expect(product.images).toHaveLength(3);
    expect(product.images.every((image) => image.src.startsWith("/media/eatroz/"))).toBe(true);
    expect(product.images.some((image) => image.alt.toLowerCase().includes("pouch"))).toBe(true);
    expect(product.images.some((image) => image.src.endsWith("eatroz-gummy-beads-v3.png"))).toBe(true);
  });
});
