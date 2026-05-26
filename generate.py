"""
Formula NFT Generator
Generates NFT-style cards featuring famous mathematical formulas
with corresponding visualizations.
"""
import os
import json
import hashlib
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import rcParams
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib.colors import LinearSegmentedColormap

# ---- Setup ----
rcParams['mathtext.fontset'] = 'cm'
OUT = "/home/ubuntu/formula-nft/output"
os.makedirs(OUT, exist_ok=True)

# Curated palettes — cyberpunk / cosmic / lab vibes
PALETTES = {
    "void":     {"bg": "#0a0a14", "fg": "#e8e8ff", "accent": "#7c5cff", "glow": "#00ffd0"},
    "ember":    {"bg": "#160a08", "fg": "#ffe8d6", "accent": "#ff5c3a", "glow": "#ffaa00"},
    "lab":      {"bg": "#06141a", "fg": "#d4f5ff", "accent": "#00d4ff", "glow": "#a8ff60"},
    "rose":     {"bg": "#1a0612", "fg": "#ffd6e8", "accent": "#ff3d8a", "glow": "#ffd700"},
    "forest":   {"bg": "#0a1410", "fg": "#d8ffe8", "accent": "#3dffaa", "glow": "#fff066"},
    "noir":     {"bg": "#000000", "fg": "#ffffff", "accent": "#aaaaaa", "glow": "#ffcc00"},
}

# ---- Visualizers ----
def viz_mandelbrot(ax, p, seed):
    rng = np.random.default_rng(seed)
    cx = rng.uniform(-0.75, -0.7)
    cy = rng.uniform(0.0, 0.15)
    zoom = rng.uniform(0.005, 0.05)
    res = 600
    x = np.linspace(cx - zoom, cx + zoom, res)
    y = np.linspace(cy - zoom, cy + zoom, res)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y
    Z = np.zeros_like(C)
    M = np.zeros(C.shape)
    for i in range(120):
        mask = np.abs(Z) <= 2
        Z[mask] = Z[mask]**2 + C[mask]
        M[mask] = i
    cmap = LinearSegmentedColormap.from_list("m", [p["bg"], p["accent"], p["glow"], p["fg"]])
    ax.imshow(M, cmap=cmap, extent=[cx-zoom, cx+zoom, cy-zoom, cy+zoom], origin="lower")
    ax.set_xticks([]); ax.set_yticks([])

def viz_lorenz(ax, p, seed):
    rng = np.random.default_rng(seed)
    sigma, rho, beta = 10.0, 28.0, 8/3
    dt = 0.01
    n = 8000
    xs, ys, zs = np.zeros(n), np.zeros(n), np.zeros(n)
    xs[0] = rng.uniform(-1, 1); ys[0] = rng.uniform(-1, 1); zs[0] = rng.uniform(-1, 1)
    for i in range(n-1):
        dx = sigma * (ys[i] - xs[i])
        dy = xs[i] * (rho - zs[i]) - ys[i]
        dz = xs[i] * ys[i] - beta * zs[i]
        xs[i+1] = xs[i] + dx*dt
        ys[i+1] = ys[i] + dy*dt
        zs[i+1] = zs[i] + dz*dt
    pts = np.array([xs, zs]).T
    seg = np.concatenate([pts[:-1, None], pts[1:, None]], axis=1)
    from matplotlib.collections import LineCollection
    t = np.linspace(0, 1, n-1)
    cmap = LinearSegmentedColormap.from_list("l", [p["accent"], p["glow"], p["fg"]])
    lc = LineCollection(seg, cmap=cmap, linewidth=0.6, alpha=0.85)
    lc.set_array(t)
    ax.add_collection(lc)
    ax.set_xlim(xs.min()-2, xs.max()+2); ax.set_ylim(zs.min()-2, zs.max()+2)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])

def viz_fibonacci(ax, p, seed):
    rng = np.random.default_rng(seed)
    phi = (1 + 5**0.5) / 2
    n = rng.integers(300, 800)
    theta = np.arange(n) * 2 * np.pi / phi**2
    r = np.sqrt(np.arange(n))
    x = r * np.cos(theta); y = r * np.sin(theta)
    sizes = np.linspace(60, 8, n)
    colors = np.linspace(0, 1, n)
    cmap = LinearSegmentedColormap.from_list("f", [p["accent"], p["glow"], p["fg"]])
    ax.scatter(x, y, s=sizes, c=colors, cmap=cmap, alpha=0.85, edgecolors='none')
    lim = r.max() * 1.1
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])

def viz_euler(ax, p, seed):
    rng = np.random.default_rng(seed)
    # Unit circle with e^{i*theta} traced
    theta = np.linspace(0, 2*np.pi, 400)
    ax.plot(np.cos(theta), np.sin(theta), color=p["accent"], lw=2.5, alpha=0.9)
    # Spinning radii
    n_rays = rng.integers(12, 32)
    for i in range(n_rays):
        a = 2*np.pi * i / n_rays + rng.uniform(0, 0.3)
        ax.plot([0, np.cos(a)], [0, np.sin(a)], color=p["glow"], lw=0.6, alpha=0.5)
    # The famous points
    ax.scatter([1, -1, 0, 0], [0, 0, 1, -1], s=180,
               c=[p["fg"], p["fg"], p["fg"], p["fg"]],
               edgecolors=p["glow"], linewidths=2, zorder=5)
    for (px, py, lbl) in [(1, 0, "1"), (-1, 0, "-1"), (0, 1, "i"), (0, -1, "-i")]:
        ax.text(px*1.18, py*1.18, lbl, color=p["fg"], fontsize=14,
                ha='center', va='center', style='italic', weight='bold')
    ax.set_xlim(-1.45, 1.45); ax.set_ylim(-1.45, 1.45)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    ax.axhline(0, color=p["fg"], lw=0.4, alpha=0.3)
    ax.axvline(0, color=p["fg"], lw=0.4, alpha=0.3)

def viz_fourier(ax, p, seed):
    rng = np.random.default_rng(seed)
    t = np.linspace(0, 4*np.pi, 2000)
    n_terms = rng.integers(3, 9)
    y = np.zeros_like(t)
    for k in range(1, n_terms+1):
        y += np.sin((2*k-1)*t) / (2*k-1)
    y *= 4/np.pi
    # Draw layered partial sums
    cmap = LinearSegmentedColormap.from_list("fr", [p["accent"], p["glow"]])
    cum = np.zeros_like(t)
    for k in range(1, n_terms+1):
        cum += (4/np.pi) * np.sin((2*k-1)*t) / (2*k-1)
        ax.plot(t, cum, color=cmap(k/n_terms), lw=1, alpha=0.5)
    ax.plot(t, y, color=p["fg"], lw=2)
    ax.set_xlim(0, 4*np.pi); ax.set_ylim(-1.6, 1.6)
    ax.set_xticks([]); ax.set_yticks([])

def viz_rose(ax, p, seed):
    rng = np.random.default_rng(seed)
    k_num = rng.integers(2, 9)
    k_den = rng.integers(1, 5)
    k = k_num / k_den
    theta = np.linspace(0, 2*np.pi*k_den*2, 4000)
    r = np.cos(k * theta)
    x = r * np.cos(theta); y = r * np.sin(theta)
    # Glow effect — draw multiple times with decreasing alpha
    for lw, a in [(8, 0.08), (4, 0.18), (2, 0.4), (0.9, 1.0)]:
        ax.plot(x, y, color=p["glow"] if lw > 1 else p["fg"], lw=lw, alpha=a)
    ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])

def viz_julia(ax, p, seed):
    rng = np.random.default_rng(seed)
    # Pick a c on the boundary of nice Julia sets
    candidates = [(-0.8, 0.156), (-0.4, 0.6), (0.285, 0.01),
                  (-0.7269, 0.1889), (-0.835, -0.2321), (0.355, 0.355)]
    cre, cim = candidates[seed % len(candidates)]
    cre += rng.uniform(-0.02, 0.02); cim += rng.uniform(-0.02, 0.02)
    res = 600
    x = np.linspace(-1.6, 1.6, res); y = np.linspace(-1.6, 1.6, res)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j*Y
    M = np.zeros(Z.shape)
    C = complex(cre, cim)
    for i in range(120):
        mask = np.abs(Z) <= 2
        Z[mask] = Z[mask]**2 + C
        M[mask] = i
    cmap = LinearSegmentedColormap.from_list("j", [p["bg"], p["accent"], p["glow"], p["fg"]])
    ax.imshow(M, cmap=cmap, extent=[-1.6,1.6,-1.6,1.6], origin="lower")
    ax.set_xticks([]); ax.set_yticks([])

def viz_pythag(ax, p, seed):
    rng = np.random.default_rng(seed)
    # Pythagoras tree
    def branch(x, y, size, angle, depth):
        if depth == 0 or size < 0.5:
            return
        # Square corners
        c, s = np.cos(angle), np.sin(angle)
        p0 = np.array([x, y])
        p1 = p0 + size * np.array([c, s])
        p2 = p1 + size * np.array([-s, c])
        p3 = p0 + size * np.array([-s, c])
        sq = plt.Polygon([p0, p1, p2, p3], closed=True,
                         facecolor=p["accent"], edgecolor=p["glow"],
                         alpha=0.3 + 0.7*(depth/10), linewidth=0.8)
        ax.add_patch(sq)
        # Two children — left and right
        new_size_l = size * np.cos(np.pi/4)
        new_size_r = size * np.sin(np.pi/4)
        branch(p3[0], p3[1], new_size_l, angle + np.pi/4, depth-1)
        # Right square top
        mid = p3 + new_size_l * np.array([np.cos(angle+np.pi/4), np.sin(angle+np.pi/4)])
        branch(mid[0], mid[1], new_size_r, angle - np.pi/4, depth-1)
    branch(-15, -25, 30, 0, 9)
    ax.set_xlim(-60, 60); ax.set_ylim(-30, 90)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])

def viz_gauss(ax, p, seed):
    rng = np.random.default_rng(seed)
    x = np.linspace(-4, 4, 500)
    # Multiple gaussians stacked
    n = rng.integers(3, 7)
    cmap = LinearSegmentedColormap.from_list("g", [p["accent"], p["glow"]])
    for i in range(n):
        mu = rng.uniform(-2, 2)
        sigma = rng.uniform(0.4, 1.2)
        y = np.exp(-(x-mu)**2 / (2*sigma**2)) / (sigma*np.sqrt(2*np.pi))
        ax.fill_between(x, 0, y, color=cmap(i/n), alpha=0.35)
        ax.plot(x, y, color=cmap(i/n), lw=1.5)
    # Bell curve markers
    main = np.exp(-x**2/2) / np.sqrt(2*np.pi)
    ax.plot(x, main, color=p["fg"], lw=2.2)
    ax.set_xlim(-4, 4)
    ax.set_xticks([]); ax.set_yticks([])

# ---- Formulas catalog ----
FORMULAS = [
    {
        "name": "Mandelbrot Set",
        "code": "MAND",
        "formula": r"$z_{n+1} = z_n^2 + c$",
        "tagline": "the boundary of chaos",
        "viz": viz_mandelbrot,
        "year": 1980,
        "discoverer": "B. Mandelbrot",
    },
    {
        "name": "Lorenz Attractor",
        "code": "LRNZ",
        "formula": r"$\dot{x}=\sigma(y-x),\ \dot{y}=x(\rho-z)-y,\ \dot{z}=xy-\beta z$",
        "tagline": "butterfly effect",
        "viz": viz_lorenz,
        "year": 1963,
        "discoverer": "E. Lorenz",
    },
    {
        "name": "Fibonacci Spiral",
        "code": "FIBO",
        "formula": r"$F_n = F_{n-1} + F_{n-2},\ \ \varphi = \frac{1+\sqrt{5}}{2}$",
        "tagline": "nature's signature",
        "viz": viz_fibonacci,
        "year": 1202,
        "discoverer": "Fibonacci",
    },
    {
        "name": "Euler's Identity",
        "code": "EULR",
        "formula": r"$e^{i\pi} + 1 = 0$",
        "tagline": "the most beautiful equation",
        "viz": viz_euler,
        "year": 1748,
        "discoverer": "L. Euler",
    },
    {
        "name": "Fourier Series",
        "code": "FOUR",
        "formula": r"$f(x) = \sum_{k=1}^{\infty} \frac{4}{\pi} \frac{\sin((2k-1)x)}{2k-1}$",
        "tagline": "any wave, any signal",
        "viz": viz_fourier,
        "year": 1822,
        "discoverer": "J. Fourier",
    },
    {
        "name": "Rose Curve",
        "code": "ROSE",
        "formula": r"$r = \cos(k\theta)$",
        "tagline": "polar petals",
        "viz": viz_rose,
        "year": 1727,
        "discoverer": "G. Grandi",
    },
    {
        "name": "Julia Set",
        "code": "JULA",
        "formula": r"$z_{n+1} = z_n^2 + c,\ \ c \in \mathbb{C}$",
        "tagline": "fractal companion",
        "viz": viz_julia,
        "year": 1918,
        "discoverer": "G. Julia",
    },
    {
        "name": "Pythagoras Tree",
        "code": "PYTH",
        "formula": r"$a^2 + b^2 = c^2$",
        "tagline": "ancient geometry blooms",
        "viz": viz_pythag,
        "year": -500,
        "discoverer": "Pythagoras",
    },
    {
        "name": "Gaussian Distribution",
        "code": "GAUS",
        "formula": r"$f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}$",
        "tagline": "the bell of probability",
        "viz": viz_gauss,
        "year": 1809,
        "discoverer": "C.F. Gauss",
    },
]

RARITIES = [
    ("Common",    0.55, "—"),
    ("Rare",      0.25, "✦"),
    ("Epic",      0.13, "✦✦"),
    ("Legendary", 0.06, "✦✦✦"),
    ("Mythic",    0.01, "✦✦✦✦"),
]

def pick_rarity(rng):
    r = rng.random()
    cum = 0
    for name, weight, mark in RARITIES:
        cum += weight
        if r <= cum:
            return name, mark
    return RARITIES[0][0], RARITIES[0][2]

def make_card(token_id, formula, palette_name, seed):
    rng = np.random.default_rng(seed)
    p = PALETTES[palette_name]
    rarity, mark = pick_rarity(rng)

    fig = plt.figure(figsize=(8, 11), facecolor=p["bg"])
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    # Outer border
    border = fig.add_axes([0, 0, 1, 1])
    border.set_facecolor(p["bg"])
    border.set_xticks([]); border.set_yticks([])
    for spine in border.spines.values():
        spine.set_visible(False)
    # Frame
    rect = Rectangle((0.025, 0.02), 0.95, 0.96, fill=False,
                     edgecolor=p["accent"], linewidth=2.5, transform=fig.transFigure)
    fig.add_artist(rect)
    rect2 = Rectangle((0.04, 0.034), 0.92, 0.932, fill=False,
                      edgecolor=p["glow"], linewidth=0.6, alpha=0.5, transform=fig.transFigure)
    fig.add_artist(rect2)

    # --- Header ---
    fig.text(0.06, 0.945, f"#{token_id:04d}", color=p["glow"],
             fontsize=11, family="monospace", weight="bold")
    fig.text(0.94, 0.945, f"{formula['code']} · {palette_name.upper()}",
             color=p["accent"], fontsize=11, family="monospace",
             weight="bold", ha="right")

    # --- Title ---
    fig.text(0.5, 0.895, formula["name"], color=p["fg"],
             fontsize=22, weight="bold", ha="center",
             family="serif")
    fig.text(0.5, 0.868, formula["tagline"].upper(), color=p["accent"],
             fontsize=9, ha="center", family="monospace",
             style="italic", alpha=0.85)

    # --- Visualization ---
    ax = fig.add_axes([0.1, 0.32, 0.8, 0.52])
    ax.set_facecolor(p["bg"])
    for spine in ax.spines.values():
        spine.set_color(p["accent"])
        spine.set_linewidth(0.8)
        spine.set_alpha(0.4)
    formula["viz"](ax, p, seed)

    # --- Formula ---
    fig.text(0.5, 0.245, formula["formula"], color=p["fg"],
             fontsize=18, ha="center", va="center")

    # --- Footer info ---
    year_str = f"{abs(formula['year'])} {'BCE' if formula['year']<0 else 'CE'}"
    fig.text(0.06, 0.155, "DISCOVERED", color=p["accent"],
             fontsize=8, family="monospace", weight="bold")
    fig.text(0.06, 0.13, f"{formula['discoverer']} · {year_str}",
             color=p["fg"], fontsize=10, family="monospace")

    fig.text(0.94, 0.155, "RARITY", color=p["accent"],
             fontsize=8, family="monospace", weight="bold", ha="right")
    fig.text(0.94, 0.13, f"{rarity} {mark}", color=p["glow"],
             fontsize=10, family="monospace", weight="bold", ha="right")

    # --- Hash signature ---
    sig = hashlib.sha256(f"{token_id}-{formula['code']}-{palette_name}-{seed}".encode()).hexdigest()[:16]
    fig.text(0.5, 0.06, f"0x{sig}", color=p["fg"],
             fontsize=8, family="monospace", ha="center", alpha=0.5)
    fig.text(0.5, 0.04, "FORMULA · ON-CHAIN MATH", color=p["accent"],
             fontsize=7, family="monospace", ha="center",
             weight="bold", alpha=0.7)

    out_path = os.path.join(OUT, f"nft_{token_id:04d}_{formula['code']}.png")
    fig.savefig(out_path, dpi=120, facecolor=p["bg"])
    plt.close(fig)

    metadata = {
        "token_id": token_id,
        "name": f"Formula #{token_id:04d} — {formula['name']}",
        "description": f"{formula['name']}. {formula['tagline'].capitalize()}. Discovered by {formula['discoverer']} in {year_str}.",
        "image": f"nft_{token_id:04d}_{formula['code']}.png",
        "attributes": [
            {"trait_type": "Formula", "value": formula["name"]},
            {"trait_type": "Code", "value": formula["code"]},
            {"trait_type": "Palette", "value": palette_name},
            {"trait_type": "Rarity", "value": rarity},
            {"trait_type": "Year", "value": formula["year"]},
            {"trait_type": "Discoverer", "value": formula["discoverer"]},
        ],
        "signature": f"0x{sig}",
    }
    return out_path, metadata


def main(count=12, seed_base=1337):
    random.seed(seed_base)
    rng = np.random.default_rng(seed_base)
    palette_names = list(PALETTES.keys())

    catalog = []
    for i in range(1, count+1):
        formula = FORMULAS[(i-1) % len(FORMULAS)]
        palette = palette_names[rng.integers(0, len(palette_names))]
        seed = seed_base + i*97
        path, meta = make_card(i, formula, palette, seed)
        print(f"  → #{i:04d} {formula['name']:<25} [{palette:<7}] {meta['attributes'][3]['value']}")
        catalog.append(meta)

    with open(os.path.join(OUT, "collection.json"), "w") as f:
        json.dump({"name": "Formula NFT Collection",
                   "description": "Famous mathematical formulas as generative NFT cards.",
                   "items": catalog}, f, indent=2)
    print(f"\nGenerated {count} cards in {OUT}")
    print(f"Manifest: {OUT}/collection.json")

if __name__ == "__main__":
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    main(count=n)
