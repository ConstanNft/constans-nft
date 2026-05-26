"""
CONSTANTS — Brand Assets v2
Fixed: PFP circle-crop safe, banner PFP-zone clear, mobile-safe.
"""
import os, numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.patches import Circle
from matplotlib.colors import LinearSegmentedColormap

rcParams['mathtext.fontset'] = 'cm'

OUT = "/home/ubuntu/formula-nft/brand"
os.makedirs(OUT, exist_ok=True)

P = {"bg": "#0a0a14", "fg": "#e8e8ff", "accent": "#7c5cff", "glow": "#00ffd0"}

# ============================================================
# PFP — 1024x1024  (circle-crop safe)
# ============================================================
def make_pfp():
    fig = plt.figure(figsize=(10.24, 10.24), facecolor=P["bg"])
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    bg = fig.add_axes([0, 0, 1, 1])
    bg.set_facecolor(P["bg"]); bg.set_xticks([]); bg.set_yticks([])
    for s in bg.spines.values(): s.set_visible(False)

    # Star field — keep within circle area
    rng = np.random.default_rng(42)
    n_stars = 220
    sx = rng.uniform(0, 1, n_stars); sy = rng.uniform(0, 1, n_stars)
    # only stars within visible circle
    mask = (sx-0.5)**2 + (sy-0.5)**2 < 0.48**2
    ss = rng.exponential(0.5, n_stars) * 4
    bg.scatter(sx[mask], sy[mask], s=ss[mask], c=P["fg"], alpha=0.15,
               edgecolors='none', transform=bg.transAxes)

    # Outer rings — pulled inward to survive circle crop
    ring1 = Circle((0.5, 0.5), 0.42, fill=False, edgecolor=P["accent"],
                   linewidth=5, transform=fig.transFigure)
    fig.add_artist(ring1)
    ring2 = Circle((0.5, 0.5), 0.435, fill=False, edgecolor=P["glow"],
                   linewidth=1.2, alpha=0.6, transform=fig.transFigure)
    fig.add_artist(ring2)

    # Visualization area — Euler's identity, slightly larger
    ax = fig.add_axes([0.20, 0.20, 0.60, 0.60])
    ax.set_facecolor(P["bg"]); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)

    theta = np.linspace(0, 2*np.pi, 400)
    for lw, a in [(20, 0.05), (12, 0.10), (6, 0.22), (2.8, 0.95)]:
        ax.plot(np.cos(theta), np.sin(theta),
                color=P["glow"] if lw > 3 else P["accent"],
                lw=lw, alpha=a)

    # Radial spokes
    for i in range(36):
        a = 2*np.pi * i / 36
        ax.plot([0, np.cos(a)], [0, np.sin(a)], color=P["glow"],
                lw=0.5, alpha=0.18)

    # Cardinal points
    for px, py, lbl in [(1,0,"1"),(-1,0,"-1"),(0,1,"i"),(0,-1,"-i")]:
        ax.scatter([px],[py], s=380, c=P["fg"],
                   edgecolors=P["glow"], linewidths=3, zorder=5)
        ax.text(px*1.22, py*1.22, lbl, color=P["fg"], fontsize=24,
                ha='center', va='center', style='italic', weight='bold', zorder=6)

    ax.axhline(0, color=P["fg"], lw=0.5, alpha=0.2)
    ax.axvline(0, color=P["fg"], lw=0.5, alpha=0.2)
    ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.5, 1.5)
    ax.set_aspect("equal")

    # Center equation — bigger, bolder card
    fig.text(0.5, 0.5, r"$e^{i\pi}+1=0$", color=P["fg"], fontsize=56,
             ha='center', va='center', weight='bold',
             bbox=dict(boxstyle="round,pad=0.7", facecolor=P["bg"],
                       edgecolor=P["accent"], linewidth=2.5))

    # Wordmark — bigger, moved INSIDE rings (safe at PFP sizes)
    fig.text(0.5, 0.81, "CONSTANTS", color=P["fg"], fontsize=38,
             ha='center', family='serif', weight='bold')

    # Tagline removed (unreadable at PFP sizes)
    # Bottom mark — small symbol instead of text
    fig.text(0.5, 0.19, "✦   ✦   ✦", color=P["accent"],
             fontsize=18, ha='center', family='monospace', alpha=0.7)

    out = os.path.join(OUT, "pfp.png")
    fig.savefig(out, dpi=100, facecolor=P["bg"])
    plt.close(fig)
    print(f"PFP saved → {out}")


# ============================================================
# BANNER — 1500x500
# ============================================================
def make_banner():
    fig = plt.figure(figsize=(15, 5), facecolor=P["bg"])
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    bg = fig.add_axes([0, 0, 1, 1])
    bg.set_facecolor(P["bg"]); bg.set_xticks([]); bg.set_yticks([])
    for s in bg.spines.values(): s.set_visible(False)

    rng = np.random.default_rng(1337)
    n_stars = 280
    sx = rng.uniform(0, 1, n_stars); sy = rng.uniform(0, 1, n_stars)
    ss = rng.exponential(0.5, n_stars) * 3
    bg.scatter(sx, sy, s=ss, c=P["fg"], alpha=0.1, edgecolors='none', transform=bg.transAxes)

    # PFP safe zone: lower-left circle ~x=[0, 0.18], y=[0, 0.55]
    # We'll keep that whole quadrant clear — only put a faint vis
    # in upper-left, away from the PFP overlap.

    # ---- Upper-left: Lorenz attractor (above PFP zone) ----
    ax1 = fig.add_axes([0.04, 0.55, 0.13, 0.4])
    ax1.set_facecolor(P["bg"])
    sigma, rho, beta = 10.0, 28.0, 8/3
    dt = 0.01; n = 8000
    xs, ys, zs = np.zeros(n), np.zeros(n), np.zeros(n)
    xs[0], ys[0], zs[0] = 0.5, 0.5, 0.5
    for i in range(n-1):
        xs[i+1] = xs[i] + sigma*(ys[i]-xs[i])*dt
        ys[i+1] = ys[i] + (xs[i]*(rho-zs[i])-ys[i])*dt
        zs[i+1] = zs[i] + (xs[i]*ys[i]-beta*zs[i])*dt
    ax1.plot(xs, zs, color=P["glow"], lw=0.4, alpha=0.7)
    ax1.set_aspect("equal"); ax1.set_xticks([]); ax1.set_yticks([])
    for s in ax1.spines.values(): s.set_visible(False)

    # ---- Right side: Rose curve (only — Mandelbrot dropped to give wordmark space) ----
    ax3 = fig.add_axes([0.83, 0.55, 0.13, 0.4])
    ax3.set_facecolor(P["bg"])
    k = 5/2
    th = np.linspace(0, 2*np.pi*4, 3000)
    r = np.cos(k*th); rx, ry = r*np.cos(th), r*np.sin(th)
    for lw, a in [(8,0.08),(4,0.18),(2,0.4),(0.9,1.0)]:
        ax3.plot(rx, ry, color=P["glow"] if lw>1 else P["fg"], lw=lw, alpha=a)
    ax3.set_xlim(-1.2,1.2); ax3.set_ylim(-1.2,1.2)
    ax3.set_aspect("equal"); ax3.set_xticks([]); ax3.set_yticks([])
    for s in ax3.spines.values(): s.set_visible(False)

    # ---- Center: wordmark — full width, no obstacles ----
    fig.text(0.5, 0.62, "CONSTANTS", color=P["fg"], fontsize=80,
             ha='center', va='center', family='serif', weight='bold')

    fig.add_artist(plt.Line2D([0.41, 0.59], [0.43, 0.43],
                              color=P["accent"], linewidth=2.5,
                              transform=fig.transFigure))

    fig.text(0.5, 0.34, "GENESIS · 333", color=P["accent"], fontsize=22,
             ha='center', va='center', family='monospace', weight='bold',
             alpha=0.95)

    fig.text(0.5, 0.22, "some things never change", color=P["fg"],
             fontsize=16, ha='center', va='center', family='serif',
             style='italic', alpha=0.75)

    # Top strip — pulled inside mobile safe area (away from extreme top)
    formula_strip = (
        r"$e^{i\pi}+1=0$" + "      " +
        r"$a^2+b^2=c^2$" + "      " +
        r"$F_n = F_{n-1}+F_{n-2}$" + "      " +
        r"$z_{n+1}=z_n^2+c$"
    )
    fig.text(0.5, 0.90, formula_strip, color=P["accent"], fontsize=11,
             ha='center', va='center', alpha=0.55)

    # Bottom strip — pulled inside safe area
    fig.text(0.5, 0.10, "✦   333 EQUATIONS · ON-CHAIN MATH   ✦",
             color=P["glow"], fontsize=11, ha='center', va='center',
             family='monospace', weight='bold', alpha=0.85)

    out = os.path.join(OUT, "banner.png")
    fig.savefig(out, dpi=100, facecolor=P["bg"])
    plt.close(fig)
    print(f"Banner saved → {out}")


if __name__ == "__main__":
    make_pfp()
    make_banner()
