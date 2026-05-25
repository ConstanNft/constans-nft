/**
 * Withdraw all ETH from contract to deployer.
 */
const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

async function main() {
  const net = hre.network.name;
  const file = path.resolve(__dirname, `../deployment.${net}.json`);
  const d = JSON.parse(fs.readFileSync(file, "utf8"));
  const c = await hre.ethers.getContractAt("Constants", d.address);
  const bal = await hre.ethers.provider.getBalance(d.address);
  console.log(`→ Contract balance: ${hre.ethers.formatEther(bal)} ETH`);
  if (bal === 0n) { console.log("Nothing to withdraw."); return; }
  const tx = await c.withdraw();
  console.log(`  tx: ${tx.hash}`);
  await tx.wait();
  console.log(`✓ Withdrawn`);
}
main().catch(err => { console.error(err); process.exit(1); });
