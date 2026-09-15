export function buildCheckoutUrl(base: string, quantity: number): string {
  const url = new URL(base);
  const safeQuantity = Number.isFinite(quantity)
    ? Math.max(1, Math.min(12, Math.trunc(quantity)))
    : 1;
  url.searchParams.set("quantity", String(safeQuantity));
  return url.toString();
}
