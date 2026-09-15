import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..", "public", "media", "eatroz");
const sourceFile = "source/eatroz-pouch-reference.png";
const inputs = [
  ["hero-four-forms-fall-poster.webp", "hero poster"],
  ["pouch-beauty.webp", "product beauty"],
  ["gummy-macro.webp", "gummy macro"],
  ["packaging-detail.webp", "packaging detail"],
];

const hash = (path) => createHash("sha256").update(readFileSync(path)).digest("hex");
const assets = inputs.map(([file, role]) => {
  const path = join(root, file);
  const probe = JSON.parse(execFileSync("ffprobe", ["-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "json", path], { encoding: "utf8" }));
  const { width, height } = probe.streams[0];
  return { file, role, sha256: hash(path), width, height };
});

writeFileSync(join(root, "manifest.json"), `${JSON.stringify({
  provisional: true,
  source: { file: sourceFile, sha256: hash(join(root, sourceFile)) },
  generator: "Runway Agent",
  creditBudget: 500,
  creditFloor: 100,
  motionStrategy: "browser-native still animation; Runway video unavailable on current plan",
  assets,
}, null, 2)}\n`);
