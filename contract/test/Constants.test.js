const { expect } = require("chai");
const hre = require("hardhat");

describe("Constants", function(){
  let c, owner, alice;
  const BASE_URI = "ipfs://bafybeitest/";

  beforeEach(async ()=>{
    [owner, alice] = await hre.ethers.getSigners();
    const F = await hre.ethers.getContractFactory("Constants");
    c = await F.deploy(owner.address, 500, BASE_URI);
    await c.waitForDeployment();
  });

  it("starts with mint closed", async ()=>{
    expect(await c.mintOpen()).to.eq(false);
    await expect(c.connect(alice).mint(1, {value: hre.ethers.parseEther("0.001")}))
      .to.be.revertedWithCustomError(c, "MintClosed");
  });

  it("mints when opened, charges price, returns tokenURI", async ()=>{
    await c.setMintOpen(true);
    await c.connect(alice).mint(2, {value: hre.ethers.parseEther("0.002")});
    expect(await c.totalMinted()).to.eq(2);
    expect(await c.balanceOf(alice.address)).to.eq(2);
    expect(await c.tokenURI(1)).to.eq(BASE_URI + "1.json");
    expect(await c.tokenURI(2)).to.eq(BASE_URI + "2.json");
  });

  it("rejects wrong payment", async ()=>{
    await c.setMintOpen(true);
    await expect(c.connect(alice).mint(1, {value: hre.ethers.parseEther("0.0009")}))
      .to.be.revertedWithCustomError(c, "WrongPayment");
  });

  it("enforces wallet limit (10)", async ()=>{
    await c.setMintOpen(true);
    await c.connect(alice).mint(10, {value: hre.ethers.parseEther("0.01")});
    await expect(c.connect(alice).mint(1, {value: hre.ethers.parseEther("0.001")}))
      .to.be.revertedWithCustomError(c, "WalletLimitReached");
  });

  it("ownerMint bypasses price/state but respects supply", async ()=>{
    await c.ownerMint(alice.address, 5);
    expect(await c.balanceOf(alice.address)).to.eq(5);
  });

  it("withdraw sends ETH to owner", async ()=>{
    await c.setMintOpen(true);
    await c.connect(alice).mint(3, {value: hre.ethers.parseEther("0.003")});
    const before = await hre.ethers.provider.getBalance(owner.address);
    const tx = await c.withdraw();
    const r = await tx.wait();
    const gas = r.gasUsed * r.gasPrice;
    const after = await hre.ethers.provider.getBalance(owner.address);
    expect(after - before + gas).to.eq(hre.ethers.parseEther("0.003"));
  });

  it("ERC2981 royalty info correct", async ()=>{
    const [recv, amt] = await c.royaltyInfo(1, hre.ethers.parseEther("1"));
    expect(recv).to.eq(owner.address);
    expect(amt).to.eq(hre.ethers.parseEther("0.05"));
  });

  it("starts token id at 1", async ()=>{
    await c.setMintOpen(true);
    const tx = await c.connect(alice).mint(1, {value: hre.ethers.parseEther("0.001")});
    const r = await tx.wait();
    const ev = r.logs.find(l => l.fragment && l.fragment.name === "Transfer");
    expect(ev.args.tokenId).to.eq(1n);
  });

  it("non-owner cannot pause/setBaseURI", async ()=>{
    await expect(c.connect(alice).setMintOpen(true)).to.be.reverted;
    await expect(c.connect(alice).setBaseURI("ipfs://x/")).to.be.reverted;
  });
});
