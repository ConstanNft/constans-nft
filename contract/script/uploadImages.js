/**
 * Upload the 333 source PNGs to IPFS via Pinata as a single directory.
 *
 *   .env:  PINATA_JWT=eyJhbGc...
 *   Source: /home/ubuntu/formula-nft/output_v2/nft_*.png
 *
 * Pinata "pinFileToIPFS" with multiple files preserves directory structure,
 * which is exactly what we need so metadata can reference
 *   ipfs://<CID>/nft_0001.png
 */
const fs = require("fs");
const path = require("path");
const axios = require("axios");
const FormData = require("form-data");
require("dotenv").config();

const SRC_DIR = "/home/ubuntu/formula-nft/output_v2";
const JWT = (process.env.PINATA_JWT || "").trim();

if (!JWT) {
  console.error("✗ PINATA_JWT missing in .env");
  process.exit(1);
}

(async () => {
  const files = fs.readdirSync(SRC_DIR)
    .filter(f => f.startsWith("nft_") && f.endsWith(".png"))
    .sort();
  console.log(`→ Found ${files.length} images in ${SRC_DIR}`);
  if (files.length !== 333) {
    console.error(`✗ Expected 333 PNGs, found ${files.length}`);
    process.exit(1);
  }

  const form = new FormData();
  for (const f of files) {
    const full = path.join(SRC_DIR, f);
    // filepath flag tells Pinata to keep folder structure: images/nft_0001.png
    form.append("file", fs.createReadStream(full), {
      filepath: `images/${f}`,
    });
  }
  form.append("pinataMetadata", JSON.stringify({
    name: "constants-genesis-images",
  }));
  form.append("pinataOptions", JSON.stringify({ cidVersion: 1 }));

  console.log("→ Uploading to Pinata… (this may take 1-3 minutes)");

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
  console.log("  ✓ Images pinned to IPFS");
  console.log("─────────────────────────────────────────────");
  console.log(`  CID         : ${cid}`);
  console.log(`  Sample      : ipfs://${cid}/nft_0001.png`);
  console.log(`  Gateway     : https://gateway.pinata.cloud/ipfs/${cid}/nft_0001.png`);
  console.log(`  Size        : ${(res.data.PinSize / 1048576).toFixed(2)} MB`);
  console.log("─────────────────────────────────────────────");
  console.log("");
  console.log("Now update .env:");
  console.log(`  IMAGES_CID=${cid}`);
  console.log("Then run: npm run metadata && npm run ipfs:metadata");
})().catch(err => {
  console.error("✗ Upload failed:", err.response?.data || err.message);
  process.exit(1);
});
