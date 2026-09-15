export type CommerceMode = "prelaunch" | "live";

export type CommerceConfig = {
  mode: CommerceMode;
  checkoutUrl: string | null;
};

export function parseCommerceConfig(
  env: Record<string, string | undefined>,
  saleDataVerified: boolean,
): CommerceConfig {
  const candidate = env.NEXT_PUBLIC_CHECKOUT_URL;
  let checkoutUrl: string | null = null;

  try {
    const parsed = new URL(candidate ?? "");
    if (parsed.protocol === "https:") checkoutUrl = parsed.toString();
  } catch {
    checkoutUrl = null;
  }

  if (
    env.NEXT_PUBLIC_COMMERCE_MODE === "live" &&
    env.NEXT_PUBLIC_COMMERCE_APPROVED === "true" &&
    checkoutUrl &&
    saleDataVerified
  ) {
    return { mode: "live", checkoutUrl };
  }

  return { mode: "prelaunch", checkoutUrl: null };
}
