/**
 * Toggle mint open. Run after verifying frontend + tokenURI works.
 * Usage:  npm run open    (opens mint)
 *         CLOSE=1 npm run open  (closes it)
 */
const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

async function main() {
  const net = hre.network.name;
  const file = path.resolve(__dirname, `../deployment.${net}.json`);
  const d = JSON.parse(fs.readFileSync(file, "utf8"));
  const c = await hre.ethers.getContractAt("Constants", d.address);
  const open = !process.env.CLOSE;
  console.log(`→ setMintOpen(${open}) on ${d.address}`);
  const tx = await c.setMintOpen(open);
  console.log(`  tx: ${tx.hash}`);
  await tx.wait();
  console.log(`✓ Mint ${open ? "OPEN" : "CLOSED"}`);
}
main().catch(err => { console.error(err); process.exit(1); });
