import Image from "next/image";
import { displayFact, product } from "../content/product";

function Arrow() { return <span aria-hidden="true" className="arrow-icon">→</span>; }

const detailRows = [
  { name: "Format", context: "How you take it", value: product.format },
  { name: "Packaging", context: "How it is kept", value: product.packaging },
  { name: "Pouch dimensions", context: "Length × breadth × width", value: `${product.pouchDimensions.length} × ${product.pouchDimensions.breadth} × ${product.pouchDimensions.width}` },
  { name: "Elemental magnesium", context: "Amount per serving", value: displayFact<number>(product.elementalMagnesium) ?? "To be published" },
  { name: "Full ingredient panel", context: "Complete formula and excipients", value: displayFact<string>(product.ingredients) ?? "To be published" },
];

const faq = [
  { question: "Is this a gummy or a drink mix?", answer: "It is a chewable gummy. There is no water or mixing step in the intended ritual." },
  { question: "What are the pouch dimensions?", answer: "The current package visualization is 25.5 cm long × 21.5 cm broad × 8 cm wide. Final manufactured pouch details will be confirmed before sale." },
  { question: "How many gummies should I take?", answer: "Serving guidance is being verified. We will publish approved on-pack directions before orders open; this preview is not dosing guidance." },
  { question: "Can I buy it now?", answer: "Not yet. This is a pre-launch product preview, not a live checkout. Price, shipping and returns will be published before an order is accepted." },
];

export function StorefrontSections() {
  return <>
    <section className="proof-rail"><div className="page-container proof-rail-inner"><span>Chew directly <b>—</b> no water</span><span>Bead-like texture</span><span>Resealable pouch</span><span>Full label before sale</span></div></section>

    <section className="ritual-section page-container" id="ritual"><div className="ritual-copy"><span className="section-eyebrow">THE EVENING EDIT</span><h2>Made to fit a full day, not add to it.</h2><p>The format is intentionally simple: take a bead-like gummy directly, then get on with your evening. No shaker, glass or elaborate routine required.</p><a href="#texture" className="text-link">See the texture <Arrow /></a></div><div className="ritual-image media-frame"><Image src="/media/eatroz/eatroz-evening-ritual-v2.png" alt="Eatroz pouch in a calm evening setting" width={1122} height={1402} sizes="(max-width: 760px) 100vw, 50vw" /></div></section>

    <section className="texture-section" id="texture"><div className="page-container texture-grid"><div className="texture-image"><Image src="/media/eatroz/eatroz-gummy-beads-v3.png" alt="Close-up of bead-like Eatroz Magnesium Gummies" width={1254} height={1254} sizes="(max-width: 760px) 100vw, 50vw" /></div><div className="texture-copy"><span className="section-eyebrow">A CLOSER LOOK</span><h2>Texture with a point of view.</h2><p>Our gummy is shown as a tactile, bead-like chewable — a product detail, not a performance promise. Formula, serving and ingredient information will stay clearly marked until the final pack is verified.</p><div className="texture-notes"><span>01 <b>Chewable format</b></span><span>02 <b>Bead-like visual texture</b></span><span>03 <b>Final label pending</b></span></div></div></div></section>

    <section className="spec-section page-container" id="details"><div className="spec-intro"><span className="section-eyebrow">PRODUCT DETAILS</span><h2>Nothing useful should be hard to find.</h2><p>Facts we can stand behind now, plus the details we will publish before launch.</p></div><dl className="spec-list">{detailRows.map((row, index) => <div key={row.name} className="spec-row"><dt><span>{String(index + 1).padStart(2, "0")}</span>{row.name}</dt><dd><small>{row.context}</small><strong>{row.value}</strong></dd></div>)}</dl><p className="spec-disclaimer">Pouch dimensions describe the current editorial visualization, not a final manufacturing specification. This page makes no health, treatment or dosage claims.</p></section>

    <section className="pouch-section"><div className="page-container pouch-grid"><div><span className="section-eyebrow">THE POUCH, IN VIEW</span><h2>Designed to keep close.</h2><p>A resealable format that is easy to store and carry. The supplied visual is a packaging concept; final regulated on-pack information will appear before sale.</p><a href="#details" className="text-link">Read the product details <Arrow /></a></div><div className="pouch-dimensions" aria-label="Current pouch dimensions"><span>EDITORIAL PACK REFERENCE</span><strong>25.5 <small>cm</small></strong><em>length</em><div><b>21.5 cm</b><span>breadth</span></div><div><b>8 cm</b><span>width</span></div></div></div></section>

    <section className="faq-section" id="faq"><div className="page-container faq-grid"><div><span className="section-eyebrow">QUESTIONS, ANSWERED PLAINLY</span><h2>Good to know.</h2></div><div className="faq-list">{faq.map((item) => <details key={item.question}><summary>{item.question}<span aria-hidden="true">+</span></summary><p>{item.answer}</p></details>)}</div></div></section>

    <section className="closing-section"><div className="page-container closing-inner"><div><span className="section-eyebrow">EATROZ / DROP 01</span><h2>Keep an eye on the details<span>.</span></h2><p>We will publish the final formula, price and ordering information before this becomes a product you can buy.</p><a className="closing-button" href="#buybox">Explore first access <Arrow /></a></div><Image src="/media/eatroz/eatroz-pouch-front-v2.png" alt="Eatroz Magnesium Gummies pouch front" width={1122} height={1402} sizes="(max-width: 760px) 90vw, 40vw" /></div></section>
  </>;
}

export function StorefrontFooter() {
  return <footer><div className="page-container footer-top"><a className="footer-wordmark" href="#top">eatroz<span>.</span></a><p>Details in view, before the sale.</p><nav aria-label="Footer navigation"><a href="#product">The product</a><a href="#texture">The texture</a><a href="#details">Product details</a><a href="#faq">FAQs</a></nav></div><div className="page-container footer-bottom"><span>© 2026 Eatroz. Site preview.</span><span>No product orders or live registration are being accepted on this preview.</span></div></footer>;
}
