// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "erc721a/contracts/ERC721A.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/common/ERC2981.sol";
import "@openzeppelin/contracts/utils/Strings.sol";

/**
 * @title Constants — Genesis 333
 * @notice 333 generative NFT cards rendered from mathematical constants.
 *         Each token deterministic by seed. Rarity sealed at mint.
 *         "Constants stay constant."
 *
 *         Single-phase public mint. Instant reveal.
 *         Per-token tokenURI: baseURI + tokenId + ".json"
 */
contract Constants is ERC721A, Ownable, ERC2981 {
    using Strings for uint256;

    // ─── CONFIG ──────────────────────────────────────────────
    uint256 public constant MAX_SUPPLY    = 333;
    uint256 public constant MAX_PER_WALLET = 10;
    uint256 public mintPrice              = 0.001 ether;

    // ipfs://<CID>/   — set after metadata upload
    string  private _baseTokenURI;
    bool    public  mintOpen = false;

    // ─── EVENTS ──────────────────────────────────────────────
    event MintPriceUpdated(uint256 newPrice);
    event MintStateUpdated(bool open);
    event BaseURIUpdated(string newBase);
    event Withdraw(address indexed to, uint256 amount);

    // ─── ERRORS ──────────────────────────────────────────────
    error MintClosed();
    error SoldOut();
    error WrongPayment();
    error WalletLimitReached();
    error WithdrawFailed();
    error NonexistentToken();

    constructor(
        address royaltyReceiver,
        uint96  royaltyBps,        // e.g. 500 = 5%
        string memory initialBaseURI
    )
        ERC721A("Constants", "CONST")
        Ownable(msg.sender)
    {
        _setDefaultRoyalty(royaltyReceiver, royaltyBps);
        _baseTokenURI = initialBaseURI;
    }

    // ─── MINT ────────────────────────────────────────────────
    function mint(uint256 quantity) external payable {
        if (!mintOpen)                                    revert MintClosed();
        if (_totalMinted() + quantity > MAX_SUPPLY)        revert SoldOut();
        if (_numberMinted(msg.sender) + quantity > MAX_PER_WALLET)
                                                          revert WalletLimitReached();
        if (msg.value != mintPrice * quantity)             revert WrongPayment();
        _mint(msg.sender, quantity);
    }

    /// @notice Owner mint for team / giveaways.
    function ownerMint(address to, uint256 quantity) external onlyOwner {
        if (_totalMinted() + quantity > MAX_SUPPLY) revert SoldOut();
        _mint(to, quantity);
    }

    // ─── METADATA ────────────────────────────────────────────
    function _baseURI() internal view override returns (string memory) {
        return _baseTokenURI;
    }

    function _startTokenId() internal pure override returns (uint256) {
        return 1; // tokens 1..333
    }

    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        if (!_exists(tokenId)) revert NonexistentToken();
        return string(abi.encodePacked(_baseTokenURI, tokenId.toString(), ".json"));
    }

    // ─── ADMIN ───────────────────────────────────────────────
    function setMintOpen(bool open) external onlyOwner {
        mintOpen = open;
        emit MintStateUpdated(open);
    }

    function setMintPrice(uint256 newPrice) external onlyOwner {
        mintPrice = newPrice;
        emit MintPriceUpdated(newPrice);
    }

    function setBaseURI(string calldata newBase) external onlyOwner {
        _baseTokenURI = newBase;
        emit BaseURIUpdated(newBase);
    }

    function setRoyalty(address receiver, uint96 bps) external onlyOwner {
        _setDefaultRoyalty(receiver, bps);
    }

    function withdraw() external onlyOwner {
        uint256 bal = address(this).balance;
        (bool ok, ) = msg.sender.call{value: bal}("");
        if (!ok) revert WithdrawFailed();
        emit Withdraw(msg.sender, bal);
    }

    // ─── VIEWS ───────────────────────────────────────────────
    function totalMinted() external view returns (uint256) {
        return _totalMinted();
    }

    function mintedBy(address wallet) external view returns (uint256) {
        return _numberMinted(wallet);
    }

    // ─── INTERFACE OVERRIDES ─────────────────────────────────
    function supportsInterface(bytes4 interfaceId)
        public view override(ERC721A, ERC2981) returns (bool)
    {
        return ERC721A.supportsInterface(interfaceId) ||
               ERC2981.supportsInterface(interfaceId);
    }
}
