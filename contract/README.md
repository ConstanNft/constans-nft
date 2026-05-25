# Constants — Genesis 333

ERC-721A NFT collection on **Ethereum mainnet**. 333 supply · 0.001 ETH mint · instant reveal · 5% royalty.

```
═══════════════════════════════════════════════════
  STACK
═══════════════════════════════════════════════════
  Contract  : ERC-721A + ERC-2981 (royalty)
  Chain     : Ethereum mainnet (chainId 1)
  Storage   : IPFS via Pinata (images + metadata)
  Tooling   : Hardhat 2.22 · Solidity 0.8.27
  Frontend  : single-file mint.html (ethers v6)
═══════════════════════════════════════════════════
  COSTS — Ethereum mainnet
═══════════════════════════════════════════════════
  Deploy contract        : ~ 0.05–0.20 ETH
                           ($150–$600 depending
                           on gas. Watch
                           etherscan.io/gastracker
                           and deploy when sub-15 gwei)
  Verify on Etherscan    : free
  IPFS pinning           : free (Pinata 1GB)
  Per-mint gas (user)    : ~ $4–15 at 20 gwei
  Withdraw / setMintOpen : ~ $1–3 each
═══════════════════════════════════════════════════
```

> Lu pilih mainnet sendiri. Numbers di atas asli, gak bisa di-cheat. Kalau gas
> tinggi waktu mau deploy, **tunggu** — pagi WIB / weekend US biasanya paling
> rendah. `hardhat run` tetep aman, kontrak gak ke-broadcast sebelum lu konfirm
> di terminal.

## Files

```
constants-contract/
├── contracts/Constants.sol      ← ERC-721A contract
├── script/
│   ├── deploy.js                ← deploy + save deployment.json
│   ├── verify.js                ← verify on Etherscan
│   ├── openMint.js              ← toggle mint open/closed
│   ├── withdraw.js              ← pull ETH out
│   ├── buildMetadata.js         ← gen 333 token JSONs
│   ├── uploadImages.js          ← pin PNGs to IPFS
│   └── uploadMetadata.js        ← pin JSONs to IPFS
├── mint.html                    ← single-file mint dApp
├── hardhat.config.js
├── package.json
└── .env.example                 ← copy to .env and fill
```

## One-Time Setup

```bash
cd constants-contract
npm install
cp .env.example .env
```

Edit `.env`:
- `DEPLOYER_PRIVATE_KEY` — fresh wallet's private key. Must hold **at least 0.25 ETH** for safety on mainnet.
- `ROYALTY_RECEIVER` — wallet that gets royalty + mint payments.
- `ETHERSCAN_API_KEY` — free at [etherscan.io/apis](https://etherscan.io/apis).
- `PINATA_JWT` — free at [pinata.cloud](https://app.pinata.cloud/developers/api-keys).
- `MAINNET_RPC_URL` — public works, but for safety bump to Alchemy / Infura free tier.

## Deploy Steps (~30 minutes total)

### 1. Pin images to IPFS

```bash
npm run ipfs:images
```

Output: a CID like `bafybeih...`. Paste it into `.env` as `IMAGES_CID=`.

### 2. Build + pin metadata

```bash
npm run metadata          # writes metadata/1.json … 333.json
npm run ipfs:metadata     # pins folder, prints CID
```

Paste the metadata CID into `.env` as `METADATA_CID=`.

### 3. Test on Sepolia FIRST (recommended, free)

Get Sepolia ETH from [sepoliafaucet.com](https://sepoliafaucet.com) or [coinbase.com/faucets/ethereum-sepolia-faucet](https://www.coinbase.com/faucets/ethereum-sepolia-faucet).

```bash
npm run deploy:sepolia
```

Open `mint.html`, set `CHAIN_ID = 11155111`, `EXPLORER = "https://sepolia.etherscan.io"`, `RPC_URL = "https://ethereum-sepolia-rpc.publicnode.com"`. Mint a few. If everything works → step 4.

### 4. Deploy to Ethereum mainnet

**Watch gas first.** Open [etherscan.io/gastracker](https://etherscan.io/gastracker). Wait until "Low" or "Average" is below 15 gwei. Then:

```bash
npm run deploy:mainnet
```

The script prints estimated gas + asks via the wallet provider before broadcasting. After it confirms it auto-saves `deployment.mainnet.json` and patches `CONTRACT_ADDRESS` in `.env`.

### 5. Verify on Etherscan

```bash
npm run verify:mainnet
```

Source becomes public + OpenSea picks it up automatically (~1 hour).

### 6. Pre-mint smoke test

Before opening mint, sanity-check that metadata loads:

```bash
npx hardhat console --network mainnet
> const c = await ethers.getContractAt("Constants", "0xDEPLOYED")
> await c.ownerMint("0xYOUR_WALLET", 1)        // mints token #1 to you
> await c.tokenURI(1)
# should print: ipfs://bafy.../1.json
# fetch via https://gateway.pinata.cloud/ipfs/<cid>/1.json
# verify the image URL renders the right card
```

### 7. Open mint

```bash
npm run open:mainnet
```

### 8. Wire frontend

Edit `mint.html` near the top of `<script>`:

```js
const CONTRACT_ADDRESS = "0xYOUR_DEPLOYED_ADDRESS";
```

Host anywhere — Vercel, Netlify, IPFS, your own VPS. Single file, no backend.

## Operations

```bash
# pause minting
CLOSE=1 npm run open:mainnet

# pull ETH out of contract
npm run withdraw:mainnet

# adjust price
npx hardhat console --network mainnet
> const c = await ethers.getContractAt("Constants", "0x...")
> await c.setMintPrice(ethers.parseEther("0.002"))
```

## What you can change later

Owner-only functions on the deployed contract:

- `setMintPrice(uint)`     — adjust price
- `setMintOpen(bool)`      — pause/resume
- `setBaseURI(string)`     — repoint metadata if you migrate IPFS pin
- `setRoyalty(addr, bps)`  — change royalty
- `ownerMint(addr, qty)`   — team allocation / giveaways
- `withdraw()`             — pull funds

## Security notes

- Use a **fresh deployer wallet** funded only with what you need for gas. Never use a wallet that holds significant assets.
- Double-check Pinata pinning persists. If you ever switch pinning service, redeploy `setBaseURI()`.
- Keep `.env` out of git (`.gitignore` already excludes it).
- `mintOpen` defaults to `false` so you can verify metadata loads before exposing the mint.
- Etherscan verification is irreversible — your source code becomes permanently public. That's the point: trust.

---

`Constants stay constant.`  ·  [@ConstantsNft](https://x.com/ConstantsNft)
