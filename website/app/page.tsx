import { Storefront } from "@/components/storefront";
import { StorefrontFooter, StorefrontSections } from "@/components/storefront-content";
import { firstAccessConfig } from "@/lib/first-access";

export default function Page() {
  const config = firstAccessConfig();
  return <Storefront sections={<StorefrontSections />} footer={<StorefrontFooter />} registrationEnabled={Boolean(config)} privacyUrl={config?.privacyUrl ?? null} />;
}
