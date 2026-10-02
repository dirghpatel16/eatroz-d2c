export type ProductFact<T> =
  | { status: "verified"; value: T }
  | { status: "verification_pending"; value?: never };

export function displayFact<T>(fact: ProductFact<T>): T | null {
  return fact.status === "verified" ? fact.value : null;
}

export const product = {
  name: "Magnesium Gummies",
  format: "Bead-like chewable gummies",
  packaging: "Resealable pouch",
  edition: "DROP 01",
  price: { status: "verification_pending" },
  reviews: { status: "verification_pending" },
  servingSize: { status: "verification_pending" },
  elementalMagnesium: { status: "verification_pending" },
  ingredients: { status: "verification_pending" },
  fssaiDetails: { status: "verification_pending" },
  pouchDimensions: {
    length: "25.5 cm",
    breadth: "21.5 cm",
    width: "8 cm",
  },
  images: [
    { src: "/media/eatroz/eatroz-pouch-front-v2.png", alt: "Eatroz Magnesium Gummies pouch, front view", label: "View pouch front", kind: "cutout" },
    { src: "/media/eatroz/eatroz-gummy-beads-v3.png", alt: "Close-up of bead-like Eatroz magnesium gummies", label: "View gummy detail", kind: "photo" },
    { src: "/media/eatroz/eatroz-evening-ritual-v2.png", alt: "Eatroz Magnesium Gummies pouch in an evening ritual setting", label: "View evening ritual", kind: "photo" },
  ],
} as const;
