"""
Formula NFT Generator v2 — 333 collection with rarity in JSON
"""
import os, json, hashlib, sys, time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.patches import Rectangle
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.collections import LineCollection

rcParams['mathtext.fontset'] = 'cm'
OUT = "/home/ubuntu/formula-nft/output_v2"
os.makedirs(OUT, exist_ok=True)

# ---- Palettes (10) ----
PALETTES = {
    "void":     {"bg": "#0a0a14", "fg": "#e8e8ff", "accent": "#7c5cff", "glow": "#00ffd0"},
    "ember":    {"bg": "#160a08", "fg": "#ffe8d6", "accent": "#ff5c3a", "glow": "#ffaa00"},
    "lab":      {"bg": "#06141a", "fg": "#d4f5ff", "accent": "#00d4ff", "glow": "#a8ff60"},
    "rose":     {"bg": "#1a0612", "fg": "#ffd6e8", "accent": "#ff3d8a", "glow": "#ffd700"},
    "forest":   {"bg": "#0a1410", "fg": "#d8ffe8", "accent": "#3dffaa", "glow": "#fff066"},
    "noir":     {"bg": "#000000", "fg": "#ffffff", "accent": "#aaaaaa", "glow": "#ffcc00"},
    "magma":    {"bg": "#100208", "fg": "#fff0e0", "accent": "#ff2266", "glow": "#ff8800"},
    "arctic":   {"bg": "#0a1828", "fg": "#e0f8ff", "accent": "#5cc8ff", "glow": "#ffffff"},
    "neon":     {"bg": "#0d0518", "fg": "#fffaff", "accent": "#ff00aa", "glow": "#00ffff"},
    "gold":     {"bg": "#181208", "fg": "#fff5d6", "accent": "#d4a020", "glow": "#fff0a0"},
}
# Palette rarity weights — some palettes harder to roll
PALETTE_WEIGHTS = {
    "void": 0.15, "ember": 0.13, "lab": 0.13, "rose": 0.11, "forest": 0.11,
    "noir": 0.13, "magma": 0.08, "arctic": 0.08, "neon": 0.05, "gold": 0.03,
}

# ---- Visualizers (high variation) ----
def _rot(ax, rng):
    """Apply random rotation via Affine2D for axes that support it."""
    return rng.uniform(0, 2*np.pi)

def viz_mandelbrot(ax, p, rng):
    # Curated zoom regions across the boundary
    regions = [(-0.745, 0.10), (-0.7269, 0.1889), (-1.25, 0.0),
               (-0.16, 1.04), (-0.235, 0.827), (0.275, 0.0),
               (-1.768, -0.001), (-0.5, 0.6), (-0.105, 0.92)]
    cx, cy = regions[int(rng.integers(0, len(regions)))]
    cx += rng.uniform(-0.005, 0.005); cy += rng.uniform(-0.005, 0.005)
    zoom = 10**rng.uniform(-2.5, -0.3)
    res = 500
    x = np.linspace(cx-zoom, cx+zoom, res); y = np.linspace(cy-zoom, cy+zoom, res)
    X, Y = np.meshgrid(x, y); C = X + 1j*Y; Z = np.zeros_like(C); M = np.zeros(C.shape)
    max_iter = int(rng.integers(80, 200))
    for i in range(max_iter):
        m = np.abs(Z) <= 2; Z[m] = Z[m]**2 + C[m]; M[m] = i
    # Random colormap order
    cols = [p["bg"], p["accent"], p["glow"], p["fg"]]
    if rng.random() < 0.5: cols = cols[::-1]
    cmap = LinearSegmentedColormap.from_list("m", cols)
    ax.imshow(M**rng.uniform(0.5, 1.2), cmap=cmap,
              extent=[cx-zoom,cx+zoom,cy-zoom,cy+zoom], origin="lower")
    ax.set_xticks([]); ax.set_yticks([])

def viz_lorenz(ax, p, rng):
    sigma = rng.uniform(8, 14); rho = rng.uniform(22, 35); beta = rng.uniform(2, 4)
    dt = rng.uniform(0.005, 0.015); n = int(rng.integers(7000, 12000))
    xs, ys, zs = np.zeros(n), np.zeros(n), np.zeros(n)
    xs[0], ys[0], zs[0] = rng.uniform(-5,5), rng.uniform(-5,5), rng.uniform(-5,5)
    for i in range(n-1):
        xs[i+1] = xs[i] + sigma*(ys[i]-xs[i])*dt
        ys[i+1] = ys[i] + (xs[i]*(rho-zs[i])-ys[i])*dt
        zs[i+1] = zs[i] + (xs[i]*ys[i]-beta*zs[i])*dt
    # Rotate viewport — pick xy / xz / yz projection
    proj = int(rng.integers(0, 3))
    a, b = [(xs, ys), (xs, zs), (ys, zs)][proj]
    # Random rotation
    th = rng.uniform(0, 2*np.pi)
    ar = a*np.cos(th) - b*np.sin(th); br = a*np.sin(th) + b*np.cos(th)
    pts = np.array([ar, br]).T
    seg = np.concatenate([pts[:-1, None], pts[1:, None]], axis=1)
    cols = [p["accent"], p["glow"], p["fg"]]
    if rng.random() < 0.5: cols = cols[::-1]
    cmap = LinearSegmentedColormap.from_list("l", cols)
    lw = rng.uniform(0.4, 0.9)
    lc = LineCollection(seg, cmap=cmap, linewidth=lw, alpha=rng.uniform(0.7, 0.95))
    lc.set_array(np.linspace(0,1,n-1)); ax.add_collection(lc)
    pad = rng.uniform(1.5, 4)
    ax.set_xlim(ar.min()-pad, ar.max()+pad); ax.set_ylim(br.min()-pad, br.max()+pad)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])

def viz_fibonacci(ax, p, rng):
    phi = (1+5**0.5)/2; n = int(rng.integers(200, 1200))
    angle_div = rng.choice([phi**2, phi, np.sqrt(5), 137.5*np.pi/180/(2*np.pi)*2*np.pi])
    theta = np.arange(n) * 2*np.pi / angle_div + rng.uniform(0, 2*np.pi)
    r = np.sqrt(np.arange(n)) * rng.uniform(0.7, 1.3)
    x, y = r*np.cos(theta), r*np.sin(theta)
    smin, smax = sorted([rng.uniform(2, 30), rng.uniform(30, 90)])
    sizes = np.linspace(smax, smin, n)
    cols = [p["accent"], p["glow"], p["fg"]]
    rng.shuffle(cols)
    cmap = LinearSegmentedColormap.from_list("f", cols)
    phase = rng.uniform(0, 1)
    c_arr = (np.linspace(0,1,n) + phase) % 1
    marker = rng.choice(['o', 'h', '*', 'D', 's'])
    ax.scatter(x, y, s=sizes, c=c_arr, cmap=cmap, alpha=rng.uniform(0.7, 0.95),
               edgecolors='none', marker=marker)
    lim = r.max()*1.1
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])

def viz_fourier(ax, p, rng):
    t = np.linspace(0, rng.uniform(2, 6)*np.pi, 2200)
    n_terms = int(rng.integers(3, 15))
    wave_type = rng.choice(['square', 'sawtooth', 'triangle'])
    cmap = LinearSegmentedColormap.from_list("fr", [p["accent"], p["glow"]])
    cum = np.zeros_like(t)
    phase = rng.uniform(0, 2*np.pi)
    for k in range(1, n_terms+1):
        if wave_type == 'square':
            cum += (4/np.pi)*np.sin((2*k-1)*t + phase)/(2*k-1)
        elif wave_type == 'sawtooth':
            cum += -(2/np.pi)*((-1)**k)*np.sin(k*t + phase)/k
        else:  # triangle
            cum += (8/np.pi**2)*((-1)**((k-1)//2)) * np.sin((2*k-1)*t+phase)/((2*k-1)**2) if k%2 else cum
        ax.plot(t, cum, color=cmap(k/n_terms), lw=rng.uniform(0.6, 1.3),
                alpha=rng.uniform(0.3, 0.7))
    ax.plot(t, cum, color=p["fg"], lw=rng.uniform(1.5, 2.5))
    ax.set_xlim(t[0], t[-1]); ax.set_ylim(-1.6, 1.6)
    ax.set_xticks([]); ax.set_yticks([])

def viz_rose(ax, p, rng):
    k_n, k_d = int(rng.integers(2,12)), int(rng.integers(1,7))
    k = k_n / k_d
    theta = np.linspace(0, 2*np.pi*k_d*2, 4000)
    phase = rng.uniform(0, 2*np.pi)
    r_offset = rng.uniform(0, 0.3)
    r = np.cos(k*theta) + r_offset
    rot = rng.uniform(0, 2*np.pi)
    x = r*np.cos(theta+rot); y = r*np.sin(theta+rot)
    glow_layers = [(rng.uniform(6,12),0.06),(rng.uniform(3,5),0.18),
                   (rng.uniform(1.5,2.5),0.4),(rng.uniform(0.7,1.1),1.0)]
    for lw, a in glow_layers:
        ax.plot(x, y, color=p["glow"] if lw>1 else p["fg"], lw=lw, alpha=a)
    lim = (abs(r).max())*1.15
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])

def viz_julia(ax, p, rng):
    candidates = [(-0.8,0.156),(-0.4,0.6),(0.285,0.01),(-0.7269,0.1889),
                  (-0.835,-0.2321),(0.355,0.355),(-0.123,0.745),(0.45,-0.1428),
                  (-0.391,-0.587),(-0.75,0.11),(-0.2,0.78),(0.4,0.4)]
    cre, cim = candidates[int(rng.integers(0, len(candidates)))]
    cre += rng.uniform(-0.04,0.04); cim += rng.uniform(-0.04,0.04)
    res = 500
    span = rng.uniform(1.2, 1.8)
    cx_off, cy_off = rng.uniform(-0.3, 0.3), rng.uniform(-0.3, 0.3)
    x = np.linspace(-span+cx_off, span+cx_off, res)
    y = np.linspace(-span+cy_off, span+cy_off, res)
    X, Y = np.meshgrid(x, y); Z = X + 1j*Y; M = np.zeros(Z.shape); C = complex(cre, cim)
    max_iter = int(rng.integers(80, 200))
    for i in range(max_iter):
        m = np.abs(Z) <= 2; Z[m] = Z[m]**2 + C; M[m] = i
    cols = [p["bg"], p["accent"], p["glow"], p["fg"]]
    if rng.random() < 0.5: cols = cols[::-1]
    cmap = LinearSegmentedColormap.from_list("j", cols)
    ax.imshow(M**rng.uniform(0.6, 1.1), cmap=cmap,
              extent=[-span+cx_off,span+cx_off,-span+cy_off,span+cy_off], origin="lower")
    ax.set_xticks([]); ax.set_yticks([])

def viz_pythag(ax, p, rng):
    ang_split = rng.uniform(np.pi/8, np.pi/2.5)
    base_size = rng.uniform(20, 38)
    base_angle = rng.uniform(-0.2, 0.2)
    depth = int(rng.integers(8, 11))
    def branch(x, y, size, angle, d):
        if d == 0 or size < 0.4: return
        c, s = np.cos(angle), np.sin(angle)
        p0 = np.array([x,y]); p1 = p0 + size*np.array([c,s])
        p2 = p1 + size*np.array([-s,c]); p3 = p0 + size*np.array([-s,c])
        sq = plt.Polygon([p0,p1,p2,p3], closed=True, facecolor=p["accent"],
                         edgecolor=p["glow"], alpha=0.25+0.7*(d/depth), linewidth=0.7)
        ax.add_patch(sq)
        nl = size*np.cos(ang_split); nr = size*np.sin(ang_split)
        branch(p3[0], p3[1], nl, angle+ang_split, d-1)
        mid = p3 + nl*np.array([np.cos(angle+ang_split), np.sin(angle+ang_split)])
        branch(mid[0], mid[1], nr, angle-(np.pi/2-ang_split), d-1)
    branch(-base_size/2, -base_size, base_size, base_angle, depth)
    ax.set_xlim(-90, 90); ax.set_ylim(-50, 130)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])

def viz_gauss(ax, p, rng):
    x = np.linspace(-5, 5, 500); n = int(rng.integers(2, 9))
    cols = [p["accent"], p["glow"]]
    if rng.random() < 0.5: cols = cols[::-1]
    cmap = LinearSegmentedColormap.from_list("g", cols)
    for i in range(n):
        mu = rng.uniform(-2.5, 2.5); sigma = rng.uniform(0.3, 1.5)
        amp = rng.uniform(0.5, 1.4)
        y = amp * np.exp(-(x-mu)**2/(2*sigma**2))/(sigma*np.sqrt(2*np.pi))
        a = rng.uniform(0.2, 0.5)
        ax.fill_between(x, 0, y, color=cmap(i/n), alpha=a)
        ax.plot(x, y, color=cmap(i/n), lw=rng.uniform(1, 2))
    ax.plot(x, np.exp(-x**2/2)/np.sqrt(2*np.pi), color=p["fg"], lw=rng.uniform(1.8, 2.5))
    ax.set_xlim(-5, 5); ax.set_xticks([]); ax.set_yticks([])

def viz_sierpinski(ax, p, rng):
    n = int(rng.integers(20000, 50000))
    n_verts = int(rng.choice([3, 4, 5, 6]))
    rot = rng.uniform(0, 2*np.pi)
    verts = np.array([[np.cos(2*np.pi*i/n_verts + rot),
                       np.sin(2*np.pi*i/n_verts + rot)] for i in range(n_verts)])
    ratio = rng.uniform(0.4, 0.55) if n_verts == 3 else rng.uniform(0.5, 0.65)
    pts = np.zeros((n,2)); pts[0] = rng.uniform(-0.3, 0.3, 2)
    idx = rng.integers(0, n_verts, n-1)
    for i in range(1, n):
        pts[i] = pts[i-1] + ratio*(verts[idx[i-1]] - pts[i-1])
    color = rng.choice([p["glow"], p["accent"], p["fg"]])
    ax.scatter(pts[:,0], pts[:,1], s=rng.uniform(0.3, 1.0), c=color,
               alpha=rng.uniform(0.5, 0.85), edgecolors='none')
    ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])

def viz_koch(ax, p, rng):
    def koch(p1, p2, depth):
        if depth == 0: return [p1, p2]
        p1, p2 = np.array(p1), np.array(p2)
        a = p1 + (p2-p1)/3; b = p1 + 2*(p2-p1)/3
        v = b - a; angle = np.pi/3
        rot = np.array([[np.cos(angle),-np.sin(angle)],[np.sin(angle),np.cos(angle)]])
        peak = a + rot @ v
        return (koch(p1,a,depth-1)[:-1] + koch(a,peak,depth-1)[:-1]
                + koch(peak,b,depth-1)[:-1] + koch(b,p2,depth-1))
    depth = int(rng.integers(3, 7))
    n_sides = int(rng.choice([3, 4, 5, 6, 8]))
    L = 1.0; pts = []
    base_rot = rng.uniform(0, 2*np.pi)
    poly = [np.array([np.cos(2*np.pi*i/n_sides+base_rot)*L/2,
                      np.sin(2*np.pi*i/n_sides+base_rot)*L/2]) for i in range(n_sides)]
    for i in range(n_sides):
        pts += koch(poly[i], poly[(i+1)%n_sides], depth)[:-1]
    pts.append(pts[0]); pts = np.array(pts)
    ax.fill(pts[:,0], pts[:,1], color=p["accent"], alpha=rng.uniform(0.2, 0.4))
    ax.plot(pts[:,0], pts[:,1], color=p["glow"], lw=rng.uniform(0.8, 1.5))
    ax.set_xlim(-0.8, 0.8); ax.set_ylim(-0.8, 0.8)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])

def viz_lissajous(ax, p, rng):
    a = int(rng.integers(2, 13)); b = int(rng.integers(2, 13))
    delta = rng.uniform(0, 2*np.pi)
    t = np.linspace(0, 2*np.pi, 4000)
    x = np.sin(a*t + delta); y = np.sin(b*t + rng.uniform(0,np.pi))
    rot = rng.uniform(0, 2*np.pi)
    xr = x*np.cos(rot) - y*np.sin(rot); yr = x*np.sin(rot) + y*np.cos(rot)
    glow_layers = [(rng.uniform(4,7),0.1),(rng.uniform(2,3.5),0.25),(rng.uniform(0.8,1.4),0.95)]
    for lw, alph in glow_layers:
        ax.plot(xr, yr, color=p["glow"] if lw>1.5 else p["fg"], lw=lw, alpha=alph)
    ax.set_xlim(-1.2,1.2); ax.set_ylim(-1.2,1.2)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])

def viz_heart(ax, p, rng):
    t = np.linspace(0, 2*np.pi, 1500)
    x = 16*np.sin(t)**3
    y = 13*np.cos(t) - 5*np.cos(2*t) - 2*np.cos(3*t) - np.cos(4*t)
    # Full random rotation (was ±0.3 rad — way too narrow)
    rot = rng.uniform(0, 2*np.pi)
    scale = rng.uniform(0.7, 1.3)
    x, y = x*scale, y*scale
    xr = x*np.cos(rot) - y*np.sin(rot); yr = x*np.sin(rot) + y*np.cos(rot)
    # Random offset
    offx, offy = rng.uniform(-5, 5), rng.uniform(-3, 3)
    xr += offx; yr += offy
    glow_layers = [(rng.uniform(15,28),0.04),(rng.uniform(7,13),0.12),
                   (rng.uniform(2.5,5),0.32),(rng.uniform(1.0,2.0),1.0)]
    for lw, a in glow_layers:
        ax.plot(xr, yr, color=p["glow"] if lw>1.5 else p["fg"], lw=lw, alpha=a)
    n_ripple = int(rng.integers(0, 10))
    ripple_style = rng.choice(['concentric', 'spiral', 'broken'])
    for i in range(n_ripple):
        s = 1 + (i+1)*rng.uniform(0.08, 0.22)
        if ripple_style == 'spiral':
            phase = i * rng.uniform(0.1, 0.4)
            cx_off = np.cos(phase) * 2; cy_off = np.sin(phase) * 2
            ax.plot(xr*s + cx_off, yr*s + cy_off, color=p["accent"],
                    lw=rng.uniform(0.3, 0.9), alpha=rng.uniform(0.15, 0.4))
        elif ripple_style == 'broken':
            # Plot only 60% of points
            mask = rng.random(len(xr)) < 0.6
            ax.plot(xr[mask]*s, yr[mask]*s, color=p["accent"],
                    lw=rng.uniform(0.3, 0.7), alpha=rng.uniform(0.2, 0.4))
        else:
            ax.plot(xr*s, yr*s, color=p["accent"], lw=rng.uniform(0.3, 0.8),
                    alpha=rng.uniform(0.2, 0.4))
    ax.set_xlim(-30,30); ax.set_ylim(-25,25)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])

def viz_attractor_clifford(ax, p, rng):
    # Use known-good parameter regions to avoid degenerate attractors
    # Clifford attractor needs |a|, |b|, |c|, |d| roughly in [1.0, 1.9]
    # to produce visible structure (outside that range often diverges or collapses)
    presets = [
        (-1.7, 1.3, -0.1, -1.21), (-1.4, 1.6, 1.0, 0.7), (1.6, -0.6, -1.2, 1.6),
        (1.5, -1.8, 1.6, 0.9), (-1.8, -2.0, -0.5, -0.9), (-1.7, -1.3, -0.5, -0.7),
        (1.8, 1.7, -0.6, 1.0), (1.6, 1.6, 0.6, -1.2), (-1.5, 1.4, 1.7, -1.5),
        (-1.24, -1.25, -1.81, -1.91), (1.7, -1.6, 1.0, -1.9),
    ]
    a, b, cc, d = presets[int(rng.integers(0, len(presets)))]
    # Tiny perturbation only
    a += rng.uniform(-0.05, 0.05); b += rng.uniform(-0.05, 0.05)
    cc += rng.uniform(-0.05, 0.05); d += rng.uniform(-0.05, 0.05)
    n = int(rng.integers(50000, 90000))
    xs, ys = np.zeros(n), np.zeros(n)
    xs[0], ys[0] = rng.uniform(-0.3, 0.3), rng.uniform(-0.3, 0.3)
    for i in range(1, n):
        xs[i] = np.sin(a*ys[i-1]) + cc*np.cos(a*xs[i-1])
        ys[i] = np.sin(b*xs[i-1]) + d*np.cos(b*ys[i-1])
    # Sanity check — if attractor collapsed to single point, skip rotation
    rng_x = xs.max() - xs.min(); rng_y = ys.max() - ys.min()
    if rng_x < 0.5 or rng_y < 0.5:
        # Fallback to known-good preset
        a, b, cc, d = -1.4, 1.6, 1.0, 0.7
        for i in range(1, n):
            xs[i] = np.sin(a*ys[i-1]) + cc*np.cos(a*xs[i-1])
            ys[i] = np.sin(b*xs[i-1]) + d*np.cos(b*ys[i-1])
    rot = rng.uniform(0, 2*np.pi)
    xr = xs*np.cos(rot) - ys*np.sin(rot); yr = xs*np.sin(rot) + ys*np.cos(rot)
    color = rng.choice([p["glow"], p["accent"], p["fg"]])
    ax.scatter(xr, yr, s=rng.uniform(1.5, 3.0), c=color,
               alpha=rng.uniform(0.55, 0.85), edgecolors='none')
    lim = max(abs(xr).max(), abs(yr).max())*1.1
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])

def viz_logistic(ax, p, rng):
    # Mode variation: full bifurcation OR zoomed window
    mode = rng.choice(['full', 'zoom_3to4', 'zoom_chaos', 'zoom_window'])
    if mode == 'full':
        r_min, r_max = 2.4, 4.0
    elif mode == 'zoom_3to4':
        r_min, r_max = rng.uniform(2.8, 3.2), rng.uniform(3.7, 4.0)
    elif mode == 'zoom_chaos':
        r_min, r_max = rng.uniform(3.55, 3.65), rng.uniform(3.85, 4.0)
    else:  # zoom_window — zoom into a periodic window
        windows = [(3.82, 3.86), (3.626, 3.635), (3.738, 3.745), (3.55, 3.59)]
        r_min, r_max = windows[int(rng.integers(0, len(windows)))]
        r_min += rng.uniform(-0.005, 0.005); r_max += rng.uniform(-0.005, 0.005)
    rs = np.linspace(r_min, r_max, int(rng.integers(600, 1200)))
    n_iter = int(rng.integers(500, 900)); n_drop = int(n_iter*rng.uniform(0.6, 0.8))
    xs, ys = [], []
    for r in rs:
        x = rng.uniform(0.2, 0.8)
        for _ in range(n_drop): x = r*x*(1-x)
        for _ in range(n_iter-n_drop):
            x = r*x*(1-x); xs.append(r); ys.append(x)
    color = rng.choice([p["glow"], p["accent"], p["fg"]])
    ax.scatter(xs, ys, s=rng.uniform(0.08, 0.35), c=color,
               alpha=rng.uniform(0.35, 0.7), edgecolors='none')
    ax.set_xlim(r_min, r_max); ax.set_ylim(0, 1)
    ax.set_xticks([]); ax.set_yticks([])

def viz_euler(ax, p, rng):
    theta = np.linspace(0, 2*np.pi, 400)
    phase = rng.uniform(0, 2*np.pi)
    rot_fn = lambda x, y: (x*np.cos(phase)-y*np.sin(phase),
                           x*np.sin(phase)+y*np.cos(phase))
    cx, cy = np.cos(theta), np.sin(theta)
    ax.plot(cx, cy, color=p["accent"], lw=rng.uniform(2, 4), alpha=0.9)
    n_rays = int(rng.integers(8, 64))
    spoke_len = rng.uniform(0.7, 1.0)
    for i in range(n_rays):
        a = 2*np.pi*i/n_rays + phase
        ax.plot([0, np.cos(a)*spoke_len], [0, np.sin(a)*spoke_len],
                color=p["glow"], lw=rng.uniform(0.3, 0.9), alpha=rng.uniform(0.3, 0.7))
    # Spiral overlay (always — was 50%)
    n_spirals = int(rng.integers(1, 4))
    for sp_i in range(n_spirals):
        st = np.linspace(0, rng.uniform(2,8)*np.pi, 600)
        sr = np.exp(st * rng.uniform(-0.18, -0.04))
        sphase = phase + sp_i * 2*np.pi/n_spirals
        ax.plot(sr*np.cos(st+sphase), sr*np.sin(st+sphase),
                color=p["glow"], lw=rng.uniform(0.6, 1.5), alpha=rng.uniform(0.4, 0.7))
    # Inner concentric circles
    n_inner = int(rng.integers(0, 5))
    for i in range(n_inner):
        radius = rng.uniform(0.2, 0.85)
        ax.plot(cx*radius, cy*radius, color=p["accent"],
                lw=rng.uniform(0.3, 0.8), alpha=rng.uniform(0.3, 0.6))
    pts = [(1,0),(-1,0),(0,1),(0,-1)]
    labels = ["1", "-1", "i", "-i"]
    for (px, py), lbl in zip(pts, labels):
        rpx, rpy = rot_fn(px, py)
        ax.scatter([rpx],[rpy], s=rng.uniform(120, 250),
                   c=[p["fg"]], edgecolors=p["glow"],
                   linewidths=rng.uniform(1.5, 3), zorder=5)
        ax.text(rpx*1.18, rpy*1.18, lbl, color=p["fg"], fontsize=14,
                ha='center', va='center', style='italic', weight='bold')
    ax.set_xlim(-1.55,1.55); ax.set_ylim(-1.55,1.55)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])

def viz_spiro(ax, p, rng):
    # Larger parameter ranges + rotation + scale
    R = rng.uniform(3, 8); r = rng.uniform(0.5, R-0.3); d = rng.uniform(0.5, R+1)
    cycles = rng.uniform(2, 20)
    n_pts = int(rng.integers(3000, 7000))
    t = np.linspace(0, 2*np.pi*cycles, n_pts)
    x = (R-r)*np.cos(t) + d*np.cos((R-r)/r*t)
    y = (R-r)*np.sin(t) - d*np.sin((R-r)/r*t)
    rot = rng.uniform(0, 2*np.pi)
    xr = x*np.cos(rot) - y*np.sin(rot); yr = x*np.sin(rot) + y*np.cos(rot)
    cols = [p["accent"], p["glow"], p["fg"]]
    if rng.random() < 0.5: cols = cols[::-1]
    cmap = LinearSegmentedColormap.from_list("sp", cols)
    seg = np.array([np.column_stack([xr[:-1], yr[:-1]]),
                    np.column_stack([xr[1:], yr[1:]])]).transpose(1,0,2)
    lc = LineCollection(seg, cmap=cmap, linewidth=rng.uniform(0.5, 1.5),
                        alpha=rng.uniform(0.6, 0.95))
    lc.set_array(np.linspace(0,1,len(t)-1))
    ax.add_collection(lc)
    lim = max(abs(xr).max(), abs(yr).max())*1.1
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])

def viz_fern(ax, p, rng):
    n = int(rng.integers(30000, 70000))
    pert = lambda v, s: v + rng.uniform(-s, s)
    pts = np.zeros((n, 2))
    for i in range(1, n):
        r = rng.random()
        x, y = pts[i-1]
        if r < 0.01:
            pts[i] = [0, pert(0.16, 0.05)*y]
        elif r < 0.86:
            pts[i] = [pert(0.85,0.05)*x + pert(0.04,0.04)*y,
                      pert(-0.04,0.04)*x + pert(0.85,0.05)*y + pert(1.6,0.2)]
        elif r < 0.93:
            pts[i] = [pert(0.2,0.08)*x - pert(0.26,0.08)*y,
                      pert(0.23,0.08)*x + pert(0.22,0.08)*y + pert(1.6,0.2)]
        else:
            pts[i] = [pert(-0.15,0.08)*x + pert(0.28,0.08)*y,
                      pert(0.26,0.08)*x + pert(0.24,0.08)*y + pert(0.44,0.1)]
    # Random rotation full 0-2pi (was ±pi/8 — too narrow)
    rot = rng.uniform(0, 2*np.pi)
    px, py = pts[:,0], pts[:,1]
    pxr = px*np.cos(rot) - py*np.sin(rot); pyr = px*np.sin(rot) + py*np.cos(rot)
    color = rng.choice([p["glow"], p["accent"], p["fg"]])
    ax.scatter(pxr, pyr, s=rng.uniform(0.15, 0.55), c=color,
               alpha=rng.uniform(0.45, 0.75), edgecolors='none')
    pad = 0.5
    ax.set_xlim(pxr.min()-pad, pxr.max()+pad)
    ax.set_ylim(pyr.min()-pad, pyr.max()+pad)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])

def viz_wave(ax, p, rng):
    n_sources = int(rng.integers(2, 7))
    res = 300
    x = np.linspace(-5, 5, res); y = np.linspace(-5, 5, res)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X)
    for i in range(n_sources):
        sx, sy = rng.uniform(-3.5, 3.5, 2)
        k = rng.uniform(1.5, 6); phase = rng.uniform(0, 2*np.pi)
        Z += np.cos(k*np.sqrt((X-sx)**2 + (Y-sy)**2) + phase)
    cols = [p["bg"], p["accent"], p["glow"]]
    if rng.random() < 0.5: cols = cols[::-1]
    cmap = LinearSegmentedColormap.from_list("w", cols)
    ax.imshow(Z, cmap=cmap, extent=[-5,5,-5,5], origin="lower")
    ax.set_xticks([]); ax.set_yticks([])

def viz_einstein(ax, p, rng):
    theta = np.linspace(0, 2*np.pi, 500)
    cmap = LinearSegmentedColormap.from_list("e", [p["accent"], p["glow"]])
    n_orbits = int(rng.integers(8, 18))
    for i, e in enumerate(np.linspace(rng.uniform(0.05, 0.25),
                                       rng.uniform(0.7, 0.92), n_orbits)):
        a_axis = 1 + i*rng.uniform(0.2, 0.4)
        phase = rng.uniform(0, 2*np.pi)
        r = a_axis*(1-e**2)/(1+e*np.cos(theta + phase))
        ax.plot(r*np.cos(theta), r*np.sin(theta),
                color=cmap(i/n_orbits), lw=rng.uniform(0.6, 1.2),
                alpha=rng.uniform(0.5, 0.85))
    ax.scatter([0],[0], s=rng.uniform(300, 500), c=[p["fg"]],
               edgecolors=p["glow"], linewidths=rng.uniform(1.5, 3), zorder=5)
    lim = rng.uniform(7, 10)
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])

def viz_schrodinger(ax, p, rng):
    res = 400
    span = rng.uniform(10, 20)
    x = np.linspace(-span, span, res); y = np.linspace(-span, span, res)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2) + 1e-9
    n = int(rng.integers(2, 6)); l = int(rng.integers(0, n))
    m = int(rng.integers(0, l+1))
    psi = np.exp(-R/n) * (R/n)**l * np.cos(m * np.arctan2(Y, X) + rng.uniform(0, 2*np.pi))
    cols = [p["bg"], p["accent"], p["glow"], p["fg"]]
    if rng.random() < 0.3: cols = cols[::-1]
    cmap = LinearSegmentedColormap.from_list("s", cols)
    ax.imshow(psi**2, cmap=cmap, extent=[-span,span,-span,span], origin="lower")
    ax.set_xticks([]); ax.set_yticks([])

def viz_navierstokes(ax, p, rng):
    res = int(rng.integers(20, 32))
    x = np.linspace(-3, 3, res); y = np.linspace(-3, 3, res)
    X, Y = np.meshgrid(x, y)
    n_swirl = int(rng.integers(2, 6))
    U = np.zeros_like(X); V = np.zeros_like(Y)
    for _ in range(n_swirl):
        cx, cy = rng.uniform(-2.5, 2.5, 2)
        s = rng.choice([-1, 1]) * rng.uniform(0.6, 1.5)
        dx, dy = X - cx, Y - cy
        d2 = dx**2 + dy**2 + rng.uniform(0.3, 0.8)
        U += s*(-dy)/d2; V += s*(dx)/d2
    mag = np.sqrt(U**2 + V**2)
    cols = [p["accent"], p["glow"]]
    if rng.random() < 0.5: cols = cols[::-1]
    cmap = LinearSegmentedColormap.from_list("ns", cols)
    ax.streamplot(X, Y, U, V, color=mag, cmap=cmap,
                  linewidth=rng.uniform(0.7, 1.2),
                  density=rng.uniform(1.0, 1.6),
                  arrowsize=rng.uniform(0.5, 0.9))
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])

# ---- Formula catalog (20 entries) ----
FORMULAS = [
    {"name":"Mandelbrot Set",         "code":"MAND", "formula":r"$z_{n+1} = z_n^2 + c$",
     "tagline":"the boundary of chaos",        "viz":viz_mandelbrot,           "year":1980,  "discoverer":"B. Mandelbrot"},
    {"name":"Lorenz Attractor",       "code":"LRNZ", "formula":r"$\dot{x}=\sigma(y-x),\ \dot{y}=x(\rho-z)-y,\ \dot{z}=xy-\beta z$",
     "tagline":"butterfly effect",             "viz":viz_lorenz,               "year":1963,  "discoverer":"E. Lorenz"},
    {"name":"Fibonacci Spiral",       "code":"FIBO", "formula":r"$F_n = F_{n-1} + F_{n-2}$",
     "tagline":"nature's signature",           "viz":viz_fibonacci,            "year":1202,  "discoverer":"Fibonacci"},
    {"name":"Euler's Identity",       "code":"EULR", "formula":r"$e^{i\pi} + 1 = 0$",
     "tagline":"the most beautiful equation",  "viz":viz_euler,                "year":1748,  "discoverer":"L. Euler"},
    {"name":"Fourier Series",         "code":"FOUR", "formula":r"$f(x)=\sum \frac{4}{\pi}\frac{\sin((2k-1)x)}{2k-1}$",
     "tagline":"any wave, any signal",         "viz":viz_fourier,              "year":1822,  "discoverer":"J. Fourier"},
    {"name":"Rose Curve",             "code":"ROSE", "formula":r"$r = \cos(k\theta)$",
     "tagline":"polar petals",                 "viz":viz_rose,                 "year":1727,  "discoverer":"G. Grandi"},
    {"name":"Julia Set",              "code":"JULA", "formula":r"$z_{n+1}=z_n^2 + c,\ c\in\mathbb{C}$",
     "tagline":"fractal companion",            "viz":viz_julia,                "year":1918,  "discoverer":"G. Julia"},
    {"name":"Pythagoras Tree",        "code":"PYTH", "formula":r"$a^2 + b^2 = c^2$",
     "tagline":"ancient geometry blooms",      "viz":viz_pythag,               "year":-500,  "discoverer":"Pythagoras"},
    {"name":"Gaussian Distribution",  "code":"GAUS", "formula":r"$f(x)=\frac{1}{\sigma\sqrt{2\pi}}e^{-\frac{(x-\mu)^2}{2\sigma^2}}$",
     "tagline":"the bell of probability",      "viz":viz_gauss,                "year":1809,  "discoverer":"C.F. Gauss"},
    {"name":"Sierpinski Triangle",    "code":"SIER", "formula":r"$\dim_H = \frac{\log 3}{\log 2}$",
     "tagline":"chaos game",                   "viz":viz_sierpinski,           "year":1915,  "discoverer":"W. Sierpinski"},
    {"name":"Koch Snowflake",         "code":"KOCH", "formula":r"$P_n = 3 \cdot 4^n / 3^n$",
     "tagline":"infinite perimeter",           "viz":viz_koch,                 "year":1904,  "discoverer":"H. von Koch"},
    {"name":"Logistic Map",           "code":"LGST", "formula":r"$x_{n+1} = r x_n (1 - x_n)$",
     "tagline":"path to chaos",                "viz":viz_logistic,             "year":1976,  "discoverer":"R. May"},
    {"name":"Lissajous Curve",        "code":"LISS", "formula":r"$x=\sin(at+\delta),\ y=\sin(bt)$",
     "tagline":"harmonic dance",               "viz":viz_lissajous,            "year":1857,  "discoverer":"J. Lissajous"},
    {"name":"Barnsley Fern",          "code":"FERN", "formula":r"$f_i(\mathbf{x}) = A_i \mathbf{x} + b_i$",
     "tagline":"IFS botanical",                "viz":viz_fern,                 "year":1988,  "discoverer":"M. Barnsley"},
    {"name":"Cardioid Heart",         "code":"HART", "formula":r"$x=16\sin^3 t,\ y=13\cos t - \dots$",
     "tagline":"polar romance",                "viz":viz_heart,                "year":1741,  "discoverer":"J. Castillon"},
    {"name":"Spirograph",             "code":"SPIR", "formula":r"$x=(R-r)\cos t + d\cos(\frac{R-r}{r}t)$",
     "tagline":"hypotrochoid",                 "viz":viz_spiro,                "year":1827,  "discoverer":"E. Suardi"},
    {"name":"Wave Interference",      "code":"WAVE", "formula":r"$\psi = \sum A_i \cos(k_i r_i)$",
     "tagline":"superposition",                "viz":viz_wave,                 "year":1801,  "discoverer":"T. Young"},
    {"name":"Einstein Field Eqs",     "code":"GRAV", "formula":r"$G_{\mu\nu} + \Lambda g_{\mu\nu} = \frac{8\pi G}{c^4} T_{\mu\nu}$",
     "tagline":"spacetime curves",             "viz":viz_einstein,             "year":1915,  "discoverer":"A. Einstein"},
    {"name":"Schrödinger Equation",   "code":"SCHR", "formula":r"$i\hbar\frac{\partial \psi}{\partial t} = \hat{H}\psi$",
     "tagline":"quantum probability",          "viz":viz_schrodinger,          "year":1925,  "discoverer":"E. Schrödinger"},
    {"name":"Clifford Attractor",     "code":"CLIF", "formula":r"$x'=\sin(ay)+c\cos(ax),\ y'=\sin(bx)+d\cos(by)$",
     "tagline":"strange beauty",               "viz":viz_attractor_clifford,   "year":1980,  "discoverer":"C. Pickover"},
    {"name":"Navier-Stokes Flow",     "code":"NAVI", "formula":r"$\rho(\partial_t \mathbf{u} + \mathbf{u}\cdot\nabla\mathbf{u}) = -\nabla p + \mu\nabla^2\mathbf{u}$",
     "tagline":"the unsolved millennium",      "viz":viz_navierstokes,         "year":1845,  "discoverer":"Navier & Stokes"},
]

# Formula rarity weights (lower = rarer)
FORMULA_WEIGHTS = {
    "MAND":12,"LRNZ":10,"FIBO":12,"EULR":8,"FOUR":10,"ROSE":12,"JULA":7,"PYTH":12,"GAUS":11,
    "SIER":9,"KOCH":9,"LGST":7,"LISS":10,"FERN":7,"HART":11,"SPIR":10,"WAVE":8,
    "GRAV":3,"SCHR":4,"CLIF":6,"NAVI":2
}

RARITIES = [
    ("Common",    0.55, "—"),
    ("Rare",      0.25, "✦"),
    ("Epic",      0.13, "✦✦"),
    ("Legendary", 0.06, "✦✦✦"),
    ("Mythic",    0.01, "✦✦✦✦"),
]

def weighted_pick(items, weights, rng):
    arr = list(items); w = np.array([weights[i] for i in arr], dtype=float)
    w = w / w.sum()
    return arr[int(rng.choice(len(arr), p=w))]

def pick_rarity(rng):
    r = rng.random(); cum = 0
    for name, weight, mark in RARITIES:
        cum += weight
        if r <= cum: return name, mark
    return RARITIES[0][0], RARITIES[0][2]

def make_card(token_id, formula, palette_name, rarity, mark, seed):
    rng = np.random.default_rng(seed)
    p = PALETTES[palette_name]

    fig = plt.figure(figsize=(8, 11), facecolor=p["bg"])
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    border = fig.add_axes([0,0,1,1]); border.set_facecolor(p["bg"])
    border.set_xticks([]); border.set_yticks([])
    for s in border.spines.values(): s.set_visible(False)

    rect = Rectangle((0.025,0.02), 0.95, 0.96, fill=False,
                     edgecolor=p["accent"], linewidth=2.5, transform=fig.transFigure)
    fig.add_artist(rect)
    rect2 = Rectangle((0.04,0.034), 0.92, 0.932, fill=False,
                      edgecolor=p["glow"], linewidth=0.6, alpha=0.5, transform=fig.transFigure)
    fig.add_artist(rect2)

    fig.text(0.06, 0.945, f"#{token_id:04d}", color=p["glow"], fontsize=11,
             family="monospace", weight="bold")
    fig.text(0.94, 0.945, f"{formula['code']} · {palette_name.upper()}",
             color=p["accent"], fontsize=11, family="monospace", weight="bold", ha="right")
    fig.text(0.5, 0.895, formula["name"], color=p["fg"], fontsize=22, weight="bold",
             ha="center", family="serif")
    fig.text(0.5, 0.868, formula["tagline"].upper(), color=p["accent"], fontsize=9,
             ha="center", family="monospace", style="italic", alpha=0.85)

    ax = fig.add_axes([0.1, 0.32, 0.8, 0.52]); ax.set_facecolor(p["bg"])
    for s in ax.spines.values():
        s.set_color(p["accent"]); s.set_linewidth(0.8); s.set_alpha(0.4)
    formula["viz"](ax, p, rng)

    fig.text(0.5, 0.245, formula["formula"], color=p["fg"], fontsize=16, ha="center", va="center")

    year_str = f"{abs(formula['year'])} {'BCE' if formula['year']<0 else 'CE'}"
    fig.text(0.06, 0.155, "DISCOVERED", color=p["accent"], fontsize=8,
             family="monospace", weight="bold")
    fig.text(0.06, 0.13, f"{formula['discoverer']} · {year_str}",
             color=p["fg"], fontsize=10, family="monospace")
    fig.text(0.94, 0.155, "RARITY", color=p["accent"], fontsize=8,
             family="monospace", weight="bold", ha="right")
    fig.text(0.94, 0.13, f"{rarity} {mark}", color=p["glow"], fontsize=10,
             family="monospace", weight="bold", ha="right")

    sig = hashlib.sha256(f"{token_id}-{formula['code']}-{palette_name}-{seed}".encode()).hexdigest()[:16]
    fig.text(0.5, 0.06, f"0x{sig}", color=p["fg"], fontsize=8,
             family="monospace", ha="center", alpha=0.5)
    fig.text(0.5, 0.04, "FORMULA · ON-CHAIN MATH", color=p["accent"], fontsize=7,
             family="monospace", ha="center", weight="bold", alpha=0.7)

    out_path = os.path.join(OUT, f"nft_{token_id:04d}.png")
    fig.savefig(out_path, dpi=110, facecolor=p["bg"])
    plt.close(fig)

    return {
        "token_id": token_id,
        "name": f"Formula #{token_id:04d} — {formula['name']}",
        "description": f"{formula['name']}. {formula['tagline'].capitalize()}. Discovered by {formula['discoverer']} in {year_str}.",
        "image": f"nft_{token_id:04d}.png",
        "attributes": [
            {"trait_type": "Formula",    "value": formula["name"]},
            {"trait_type": "Code",       "value": formula["code"]},
            {"trait_type": "Palette",    "value": palette_name},
            {"trait_type": "Rarity",     "value": rarity},
            {"trait_type": "Year",       "value": formula["year"]},
            {"trait_type": "Discoverer", "value": formula["discoverer"]},
        ],
        "rarity": rarity,
        "rarity_mark": mark,
        "signature": f"0x{sig}",
        "seed": int(seed),
    }


def main(count=333, seed_base=20260521):
    rng = np.random.default_rng(seed_base)
    formula_codes = [f["code"] for f in FORMULAS]
    formula_by_code = {f["code"]: f for f in FORMULAS}

    catalog = []; t0 = time.time()
    for i in range(1, count+1):
        seed = seed_base + i*97 + 1
        local_rng = np.random.default_rng(seed)
        code = weighted_pick(formula_codes, FORMULA_WEIGHTS, local_rng)
        palette = weighted_pick(list(PALETTES.keys()), PALETTE_WEIGHTS, local_rng)
        rarity, mark = pick_rarity(local_rng)
        meta = make_card(i, formula_by_code[code], palette, rarity, mark, seed)
        catalog.append(meta)
        if i % 25 == 0 or i == count:
            elapsed = time.time() - t0
            print(f"  {i:>3}/{count}  [{elapsed:6.1f}s]  last: {code} {palette:<7} {rarity}")

    # Rarity rollups
    from collections import Counter
    rar = Counter(m["rarity"] for m in catalog)
    pal = Counter(m["attributes"][2]["value"] for m in catalog)
    cod = Counter(m["attributes"][1]["value"] for m in catalog)

    manifest = {
        "name": "Formula NFT — Genesis 333",
        "description": "333 famous mathematical formulas as generative NFT cards. Each card is deterministic from its seed; rarity is rolled at mint time.",
        "supply": count,
        "seed_base": seed_base,
        "rarity_distribution": dict(rar),
        "palette_distribution": dict(pal),
        "formula_distribution": dict(cod),
        "items": catalog,
    }
    with open(os.path.join(OUT, "collection.json"), "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"\nDone: {count} cards in {OUT}")
    print(f"Rarity: {dict(rar)}")
    print(f"Manifest: {OUT}/collection.json")

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 333
    main(count=n)
