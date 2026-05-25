/**
 * Build OpenSea-compatible metadata for the 333 Constants cards.
 *
 * Reads /home/ubuntu/formula-nft/output_v2/collection.json (source of truth)
 * and emits one JSON per token at metadata/<id>.json, plus a manifest.
 *
 * Image URI is constructed once you set IMAGES_CID in .env.
 * If IMAGES_CID is empty, images point to a placeholder so you can iterate.
 */
const fs = require("fs");
const path = require("path");
require("dotenv").config();

const SRC = "/home/ubuntu/formula-nft/output_v2/collection.json";
const OUT = path.resolve(__dirname, "../metadata");

const IMAGES_CID = (process.env.IMAGES_CID || "").trim();
const IMAGE_BASE = IMAGES_CID
  ? `ipfs://${IMAGES_CID}/`
  : "ipfs://__SET_IMAGES_CID_FIRST__/";

const COLLECTION_NAME = "Constants — Genesis 333";
const COLLECTION_DESC =
  "333 generative cards rendered from mathematical constants — formulas, attractors, equations that don't bend, don't fade. " +
  "Each token is deterministic from its seed. Rarity is sealed at mint. Constants stay constant.";
const EXTERNAL_URL = "https://x.com/ConstantsNft";

if (!fs.existsSync(SRC)) {
  console.error(`✗ Source not found: ${SRC}`);
  process.exit(1);
}
fs.mkdirSync(OUT, { recursive: true });

const src = JSON.parse(fs.readFileSync(SRC, "utf8"));
console.log(`→ Source: ${src.items.length} items`);
console.log(`→ Image base: ${IMAGE_BASE}`);

let written = 0;
for (const it of src.items) {
  const tokenId = it.token_id;
  // Image filename inside images CID dir = nft_0001.png ... nft_0333.png
  // Pinata preserves the original filenames when you upload a folder.
  const imageFile = `nft_${String(tokenId).padStart(4, "0")}.png`;

  const meta = {
    name: it.name,                  // "Formula #0001 — Sierpinski Triangle"
    description: `${it.description}\n\n${COLLECTION_DESC}`,
    image: `${IMAGE_BASE}${imageFile}`,
    external_url: EXTERNAL_URL,
    attributes: it.attributes,      // already in OpenSea trait_type/value format
    seed: it.seed,
    signature: it.signature,
  };

  fs.writeFileSync(
    path.join(OUT, `${tokenId}.json`),
    JSON.stringify(meta, null, 2)
  );
  written++;
}

// Collection-level manifest (some marketplaces read this)
const manifest = {
  name: COLLECTION_NAME,
  description: COLLECTION_DESC,
  external_link: EXTERNAL_URL,
  image: `${IMAGE_BASE}nft_0001.png`,
  seller_fee_basis_points: parseInt(process.env.ROYALTY_BPS || "500", 10),
  fee_recipient: process.env.ROYALTY_RECEIVER || "",
  total_supply: src.items.length,
};
fs.writeFileSync(
  path.join(OUT, "_collection.json"),
  JSON.stringify(manifest, null, 2)
);

console.log(`✓ Wrote ${written} metadata files to ${OUT}`);
console.log(`✓ Wrote _collection.json (collection-level manifest)`);
if (!IMAGES_CID) {
  console.log("");
  console.log("⚠ IMAGES_CID is not set yet. Run:");
  console.log("    npm run ipfs:images");
  console.log("  then paste the CID into .env and re-run this script.");
}
