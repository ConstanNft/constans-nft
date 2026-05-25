/**
 * Upload the metadata/ folder (1.json … 333.json) to IPFS via Pinata.
 *
 * Returns the CID that becomes the contract baseURI.
 *   ipfs://<CID>/  → contract appends "<tokenId>.json"
 */
const fs = require("fs");
const path = require("path");
const axios = require("axios");
const FormData = require("form-data");
require("dotenv").config();

const META_DIR = path.resolve(__dirname, "../metadata");
const JWT = (process.env.PINATA_JWT || "").trim();

if (!JWT) {
  console.error("✗ PINATA_JWT missing in .env");
  process.exit(1);
}

(async () => {
  const files = fs.readdirSync(META_DIR)
    .filter(f => /^\d+\.json$/.test(f))
    .sort((a, b) => parseInt(a) - parseInt(b));
  if (files.length !== 333) {
    console.error(`✗ Expected 333 metadata json files, got ${files.length}.`);
    console.error("  Run: npm run metadata");
    process.exit(1);
  }
  console.log(`→ Uploading ${files.length} metadata files`);

  // Sanity: open file 1 and verify image URI looks sane
  const sample = JSON.parse(fs.readFileSync(path.join(META_DIR, "1.json"), "utf8"));
  if (sample.image.includes("__SET_IMAGES_CID_FIRST__")) {
    console.error("✗ Metadata still has placeholder image URI.");
    console.error("  Set IMAGES_CID in .env then run: npm run metadata");
    process.exit(1);
  }
  console.log(`  Sample image: ${sample.image}`);

  const form = new FormData();
  for (const f of files) {
    form.append("file", fs.createReadStream(path.join(META_DIR, f)), {
      filepath: `metadata/${f}`,
    });
  }
  // also include collection-level manifest (optional)
  if (fs.existsSync(path.join(META_DIR, "_collection.json"))) {
    form.append("file", fs.createReadStream(path.join(META_DIR, "_collection.json")), {
      filepath: `metadata/_collection.json`,
    });
  }
  form.append("pinataMetadata", JSON.stringify({
    name: "constants-genesis-metadata",
  }));
  form.append("pinataOptions", JSON.stringify({ cidVersion: 1 }));

  const res = await axios.post(
    "https://api.pinata.cloud/pinning/pinFileToIPFS",
    form,
    {
      maxBodyLength: Infinity,
      maxContentLength: Infinity,
      headers: {
        ...form.getHeaders(),
        Authorization: `Bearer ${JWT}`,
      },
    }
  );

  const cid = res.data.IpfsHash;
  console.log("");
  console.log("─────────────────────────────────────────────");
  console.log("  ✓ Metadata pinned to IPFS");
  console.log("─────────────────────────────────────────────");
  console.log(`  CID         : ${cid}`);
  console.log(`  baseURI     : ipfs://${cid}/`);
  console.log(`  Token 1     : ipfs://${cid}/1.json`);
  console.log(`  Gateway     : https://gateway.pinata.cloud/ipfs/${cid}/1.json`);
  console.log("─────────────────────────────────────────────");
  console.log("");
  console.log("Now update .env:");
  console.log(`  METADATA_CID=${cid}`);
  console.log("Then run: npm run deploy:base");
})().catch(err => {
  console.error("✗ Upload failed:", err.response?.data || err.message);
  process.exit(1);
});
