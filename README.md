# Constants — Genesis 333

> 333 generative NFT cards rendered from mathematical constants. Each card is deterministic from its seed. Rarity is sealed inside the chain. **Constants stay constant.**

[![X](https://img.shields.io/badge/X-@ConstantsNft-1da1f2?style=flat&logo=x)](https://x.com/ConstantsNft)
![Chain](https://img.shields.io/badge/chain-Ethereum%20Mainnet-627eea)
![Standard](https://img.shields.io/badge/standard-ERC--721A-a8ff60)
![Supply](https://img.shields.io/badge/supply-333-ffcc66)
![License](https://img.shields.io/badge/license-MIT-blue)

## What is this

A NFT collection of 333 cards. Every card is a generative parametric render of a famous mathematical constant — Sierpinski triangle, Lorenz attractor, Mandelbrot set, Euler's identity, Schrödinger equation, and 16 others.

- **21 formulas** × **10 palettes** × **5 rarity tiers**
- Each token deterministic from a seed sealed at deployment
- ERC-721A on Ethereum mainnet · 0.001 ETH mint · 5% royalty
- Metadata + images on IPFS (Pinata)
- Single-file mint dApp (no backend)

## Repository layout

```
constans-nft/
├── contract/         Smart contract + Hardhat + deploy/verify scripts
│   ├── contracts/Constants.sol     ERC-721A + ERC-2981 royalty
│   ├── script/                     deploy, verify, mint open, withdraw
│   ├── test/                       9/9 unit tests passing
│   ├── mint.html                   standalone mint dApp (alt to web/)
│   ├── package.json
│   ├── hardhat.config.js
│   └── README.md                   full deploy walkthrough
│
└── web/              Marketing + gallery + mint site
    └── index.html                  single-file site
                                    (333 HD thumbs base64-embedded ~28MB)
````
## The 21 constants

| Code | Name | Discoverer | Year |
|------|------|-----------|------|
| SIER | Sierpinski Triangle | W. Sierpinski | 1915 |
| LRNZ | Lorenz Attractor | E. Lorenz | 1963 |
| CLIF | Clifford Attractor | C. Pickover | 1989 |
| MAND | Mandelbrot Set | B. Mandelbrot | 1980 |
| JULA | Julia Set | G. Julia | 1918 |
| EULR | Euler's Identity | L. Euler | 1748 |
| LISS | Lissajous Curve | J. Lissajous | 1857 |
| FERN | Barnsley Fern | M. Barnsley | 1988 |
| HART | Heart Curve | classical | 1741 |
| NAVI | Navier-Stokes | C-L. Navier | 1822 |
| FIBO | Fibonacci Spiral | Leonardo of Pisa | 1202 |
| WAVE | Wave Equation | d'Alembert | 1747 |
| PYTH | Pythagorean Theorem | Pythagoras | -530 |
| SPIR | Spirograph | D. Cohen | 1965 |
| GAUS | Gaussian Distribution | C.F. Gauss | 1809 |
| LGST | Logistic Map | P. Verhulst | 1838 |
| FOUR | Fourier Series | J. Fourier | 1807 |
| ROSE | Rose Curve | G. Grandi | 1728 |
| SCHR | Schrödinger Equation | E. Schrödinger | 1926 |
| KOCH | Koch Snowflake | H. von Koch | 1904 |
| GRAV | Newton's Gravitation | I. Newton | 1687 |

## Rarity distribution (333 supply)

```
Common      183
Rare         80
Epic         46
Legendary    23
Mythic        1
```

We don't reveal which token is which tier. Mint and find out.

## Links

- **X**: [@ConstantsNft](https://x.com/ConstantsNft)
- **Contract**: TBA after mainnet deploy
- **OpenSea**: TBA after deploy

## License

MIT for code. Art and brand are © Constants. Holders may use their cards as PFP and for personal/commercial use within reasonable scope.
