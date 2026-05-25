/**
 * Verify the deployed Constants contract on Basescan.
 * Reads contract address + constructor args from deployment.<network>.json.
 */
const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

async function main() {
  const net = hre.network.name;
  const file = path.resolve(__dirname, `../deployment.${net}.json`);
  if (!fs.existsSync(file)) {
    console.error(`✗ ${file} not found. Deploy first: npm run deploy:${net}`);
    process.exit(1);
  }
  const d = JSON.parse(fs.readFileSync(file, "utf8"));
  console.log(`→ Verifying ${d.address} on ${net}…`);

  await hre.run("verify:verify", {
    address: d.address,
    constructorArguments: [d.royaltyReceiver, d.royaltyBps, d.baseURI],
  });
  console.log(`✓ Verified: https://basescan.org/address/${d.address}#code`);
}

main().catch(err => { console.error(err); process.exit(1); });
