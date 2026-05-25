/**
 * Deploy Constants.sol to Base.
 *
 *   network: base | baseSepolia
 *   reads:   .env  (DEPLOYER_PRIVATE_KEY, ROYALTY_RECEIVER, ROYALTY_BPS,
 *                   METADATA_CID, MINT_PRICE_ETH)
 */
const hre = require("hardhat");
const fs = require("fs");
const path = require("path");
require("dotenv").config();

async function main() {
  const net = hre.network.name;
  const [deployer] = await hre.ethers.getSigners();
  const balance = await hre.ethers.provider.getBalance(deployer.address);

  const royaltyReceiver = process.env.ROYALTY_RECEIVER || deployer.address;
  const royaltyBps      = parseInt(process.env.ROYALTY_BPS || "500", 10);
  const metadataCid     = (process.env.METADATA_CID || "").trim();
  const mintPriceEth    = process.env.MINT_PRICE_ETH || "0.001";

  if (!metadataCid) {
    console.error("✗ METADATA_CID empty in .env. Upload metadata first.");
    process.exit(1);
  }
  const baseURI = `ipfs://${metadataCid}/`;

  console.log("─────────────────────────────────────────────");
  console.log("  CONSTANTS — DEPLOY");
  console.log("─────────────────────────────────────────────");
  console.log(`  Network         : ${net}`);
  console.log(`  Deployer        : ${deployer.address}`);
  console.log(`  Balance         : ${hre.ethers.formatEther(balance)} ETH`);
  console.log(`  Royalty rcv     : ${royaltyReceiver}`);
  console.log(`  Royalty bps     : ${royaltyBps} (${royaltyBps/100}%)`);
  console.log(`  baseURI         : ${baseURI}`);
  console.log(`  Mint price      : ${mintPriceEth} ETH`);
  console.log("─────────────────────────────────────────────");

  if (balance < hre.ethers.parseEther("0.002")) {
    console.error("✗ Deployer balance too low. Need at least 0.002 ETH on Base for safety.");
    process.exit(1);
  }

  const Factory = await hre.ethers.getContractFactory("Constants");
  const c = await Factory.deploy(royaltyReceiver, royaltyBps, baseURI);
  console.log(`→ Tx submitted: ${c.deploymentTransaction().hash}`);
  await c.waitForDeployment();
  const addr = await c.getAddress();
  console.log(`✓ Deployed at: ${addr}`);

  // If user changed price, set it
  const wantWei = hre.ethers.parseEther(mintPriceEth);
  const onchain = await c.mintPrice();
  if (onchain !== wantWei) {
    console.log(`→ Updating mint price to ${mintPriceEth} ETH…`);
    const tx = await c.setMintPrice(wantWei);
    await tx.wait();
    console.log("  ✓ price updated");
  }

  // Persist artifacts for the frontend
  const out = {
    network: net,
    chainId: hre.network.config.chainId,
    address: addr,
    deployer: deployer.address,
    royaltyReceiver,
    royaltyBps,
    baseURI,
    mintPriceWei: wantWei.toString(),
    mintPriceEth,
    deployedAt: new Date().toISOString(),
  };
  const outPath = path.resolve(__dirname, `../deployment.${net}.json`);
  fs.writeFileSync(outPath, JSON.stringify(out, null, 2));
  console.log(`✓ Saved ${outPath}`);

  // Patch .env with CONTRACT_ADDRESS (idempotent)
  const envPath = path.resolve(__dirname, "../.env");
  if (fs.existsSync(envPath)) {
    let env = fs.readFileSync(envPath, "utf8");
    if (env.match(/^CONTRACT_ADDRESS=/m)) {
      env = env.replace(/^CONTRACT_ADDRESS=.*$/m, `CONTRACT_ADDRESS=${addr}`);
    } else {
      env += `\nCONTRACT_ADDRESS=${addr}\n`;
    }
    fs.writeFileSync(envPath, env);
    console.log(`✓ Patched .env CONTRACT_ADDRESS`);
  }

  console.log("");
  console.log("Next steps:");
  console.log(`  1. Verify on Basescan: npm run verify:base`);
  console.log(`  2. Open mint:          npm run open`);
  console.log(`  3. Visit on Basescan:  https://basescan.org/address/${addr}`);
}

main().catch(err => { console.error(err); process.exit(1); });
