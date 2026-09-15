import { Storefront } from "@/components/storefront";
import { product } from "@/content/product";
import { parseCommerceConfig } from "@/lib/commerce/config";

export default function Home() {
  const saleDataVerified = product.price.status === "verified"
    && product.chemicalForms.status === "verified"
    && product.elementalMagnesium.status === "verified"
    && product.servingCount.status === "verified"
    && product.percentRda.status === "verified"
    && product.oxide.status === "verified";
  return <Storefront commerce={parseCommerceConfig(process.env, saleDataVerified)} />;
}
