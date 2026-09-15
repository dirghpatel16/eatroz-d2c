type PendingFact = { status: "verification_pending"; value: null };
type VerifiedFact<T> = { status: "verified"; value: T };

export type ProductFact<T> = PendingFact | VerifiedFact<T>;

type Product = {
  name: string;
  eyebrow: string;
  headline: string;
  launchLabel: string;
  price: ProductFact<number>;
  formulaIntent: readonly string[];
  chemicalForms: ProductFact<readonly string[]>;
  elementalMagnesium: ProductFact<number>;
  servingCount: ProductFact<number>;
  percentRda: ProductFact<number>;
  oxide: ProductFact<number>;
  delivery: ProductFact<string>;
  returns: ProductFact<string>;
  subscription: ProductFact<boolean>;
  reviews: ProductFact<{ count: number; average: number }>;
  supplementFactsUrl: ProductFact<string>;
  certificateOfAnalysisUrl: ProductFact<string>;
  contactEmail: ProductFact<string>;
  formulationPendingCopy: string;
  media: {
    heroPoster: string;
    pouch: string;
    gummy: string;
    detail: string;
  };
};

export const product: Product = {
  name: "Eatroz Magnesium Gummies",
  eyebrow: "MAGNESIUM, FULLY NAMED",
  headline: "Your evening ritual, rethought.",
  launchLabel: "DROP 01",
  price: { status: "verification_pending", value: null },
  formulaIntent: ["Glycinate", "Citrate", "Malate", "Taurate"],
  chemicalForms: { status: "verification_pending", value: null },
  elementalMagnesium: { status: "verification_pending", value: null },
  servingCount: { status: "verification_pending", value: null },
  percentRda: { status: "verification_pending", value: null },
  oxide: { status: "verification_pending", value: null },
  delivery: { status: "verification_pending", value: null },
  returns: { status: "verification_pending", value: null },
  subscription: { status: "verification_pending", value: null },
  reviews: { status: "verification_pending", value: null },
  supplementFactsUrl: { status: "verification_pending", value: null },
  certificateOfAnalysisUrl: { status: "verification_pending", value: null },
  contactEmail: { status: "verification_pending", value: null },
  formulationPendingCopy:
    "Final formulation details will be published before orders open.",
  media: {
    heroPoster: "/media/eatroz/hero-four-forms-fall-poster.webp",
    pouch: "/media/eatroz/pouch-beauty.webp",
    gummy: "/media/eatroz/gummy-macro.webp",
    detail: "/media/eatroz/packaging-detail.webp",
  },
} as const;
