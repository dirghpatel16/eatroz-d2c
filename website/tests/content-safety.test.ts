import { describe, expect, it } from "vitest";
import { product } from "@/content/product";

describe("product content", () => {
  it("keeps unresolved facts explicitly pending", () => {
    expect(product.price.status).toBe("verification_pending");
    expect(product.chemicalForms.status).toBe("verification_pending");
    expect(product.elementalMagnesium.status).toBe("verification_pending");
    expect(product.servingCount.status).toBe("verification_pending");
    expect(product.percentRda.status).toBe("verification_pending");
    expect(product.oxide.status).toBe("verification_pending");
    expect(product.delivery.status).toBe("verification_pending");
    expect(product.returns.status).toBe("verification_pending");
    expect(product.subscription.status).toBe("verification_pending");
    expect(product.reviews.status).toBe("verification_pending");
    expect(product.supplementFactsUrl.status).toBe("verification_pending");
    expect(product.certificateOfAnalysisUrl.status).toBe(
      "verification_pending",
    );
    expect(product.contactEmail.status).toBe("verification_pending");
  });

  it("contains no unsupported delivery or clinical claims", () => {
    const serialized = JSON.stringify(product).toLowerCase();
    expect(serialized).not.toContain("liposomal delivery");
    expect(serialized).not.toContain("clinically proven");
    expect(serialized).not.toContain("muscle recovery");
  });
});
