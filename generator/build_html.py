"""Build single-file HTML with embedded base64 gallery."""
import json, os

with open('/home/ubuntu/formula-nft-web/items_hd.json') as f:
    thumbs = json.load(f)

# Compact items array for JS
items_json = json.dumps(thumbs['items'], separators=(',', ':'))

html = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Constants — Genesis 333</title>
<style>
:root{
  --bg:#0a0c12; --bg2:#0e1118; --panel:#12161f; --panel2:#1a1f2c;
  --ink:#e8eaf0; --ink2:#9aa0b0; --ink3:#5a6072;
  --accent:#a8ff60; --accent2:#60d4ff; --gold:#ffcc66;
  --line:#1f2532; --line2:#2a3142;
  --mono:'JetBrains Mono','SF Mono',ui-monospace,Menlo,Consolas,monospace;
  --display:'Inter',system-ui,-apple-system,sans-serif;
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:var(--bg);color:var(--ink);font-family:var(--display);font-size:15px;line-height:1.5;-webkit-font-smoothing:antialiased}
body{overflow-x:hidden}

/* === GRID NOISE BG === */
body::before{
  content:'';position:fixed;inset:0;pointer-events:none;z-index:0;
  background-image:
    linear-gradient(rgba(255,255,255,0.015) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,255,255,0.015) 1px,transparent 1px);
  background-size:40px 40px;
}

/* === NAV === */
nav{
  position:sticky;top:0;z-index:50;
  background:rgba(10,12,18,0.85);backdrop-filter:blur(12px);
  border-bottom:1px solid var(--line);
  padding:14px 32px;
  display:flex;justify-content:space-between;align-items:center;gap:24px;
}
.brand{font-family:var(--mono);font-weight:600;font-size:14px;letter-spacing:0.05em;color:var(--ink)}
.brand b{color:var(--accent)}
.nav-links{display:flex;gap:20px;font-family:var(--mono);font-size:12px;color:var(--ink2);letter-spacing:0.08em;text-transform:uppercase}
.nav-links a{color:var(--ink2);text-decoration:none;transition:color .2s}
.nav-links a:hover{color:var(--accent)}

.nav-wallet{display:flex;align-items:center;gap:10px;font-family:var(--mono);font-size:11px}
.chain-pill{padding:5px 10px;border:1px solid var(--line2);color:var(--ink2);letter-spacing:0.1em;font-size:10px}
.chain-pill.ok{border-color:var(--accent);color:var(--accent)}
.chain-pill.bad{border-color:#ff7070;color:#ff7070}
.btn-sm{padding:7px 12px;font-size:11px;width:auto}

/* === HERO === */
.hero{
  position:relative;z-index:1;
  padding:90px 32px 60px;
  max-width:1280px;margin:0 auto;
  display:grid;grid-template-columns:1.2fr 1fr;gap:60px;align-items:center;
}
.hero-left h1{
  font-family:var(--display);font-size:64px;font-weight:800;letter-spacing:-0.03em;line-height:1.02;
  margin-bottom:24px;
}
.hero-left h1 .accent{color:var(--accent);font-style:italic;font-weight:300}
.hero-tag{
  font-family:var(--mono);font-size:11px;letter-spacing:0.2em;color:var(--accent);
  margin-bottom:20px;text-transform:uppercase;
}
.hero-tag::before{content:'◆ ';color:var(--gold)}
.hero-desc{
  color:var(--ink2);font-size:17px;line-height:1.6;max-width:520px;margin-bottom:32px;
}
.hero-stats{display:flex;gap:32px;margin-bottom:36px;font-family:var(--mono)}
.stat{border-left:2px solid var(--accent);padding-left:14px}
.stat-val{font-size:24px;font-weight:600;color:var(--ink)}
.stat-lbl{font-size:10px;color:var(--ink3);letter-spacing:0.15em;text-transform:uppercase;margin-top:2px}
.hero-cta{display:flex;gap:14px;flex-wrap:wrap}
.btn{
  display:inline-flex;align-items:center;gap:10px;
  padding:14px 26px;
  font-family:var(--mono);font-size:12px;letter-spacing:0.12em;text-transform:uppercase;
  border:none;cursor:pointer;text-decoration:none;
  transition:all .2s;
}
.btn-primary{background:var(--accent);color:var(--bg);font-weight:600}
.btn-primary:hover{background:#bfff80;transform:translate(-2px,-2px);box-shadow:4px 4px 0 var(--accent)}
.btn-ghost{background:transparent;color:var(--ink);border:1px solid var(--line2)}
.btn-ghost:hover{border-color:var(--accent);color:var(--accent)}

/* === HERO CARD VAULT === */
.hero-right{
  position:relative;
  height:480px;
  display:flex;align-items:center;justify-content:center;
}
.vault-card{
  position:absolute;
  width:240px;height:330px;
  background:var(--panel);
  border:1px solid var(--line2);
  display:flex;align-items:center;justify-content:center;
  font-family:var(--mono);font-size:10px;color:var(--ink3);
  transition:transform .8s cubic-bezier(.2,.8,.2,1);
}
.vault-card::after{
  content:'? ? ?';font-size:60px;color:var(--line2);font-weight:700;
  position:absolute;
}
.vault-card:nth-child(1){transform:rotate(-12deg) translateX(-90px)}
.vault-card:nth-child(2){transform:rotate(-3deg) translateX(-30px) translateY(10px);z-index:2}
.vault-card:nth-child(3){transform:rotate(6deg) translateX(50px) translateY(-5px);z-index:3}
.vault-card:nth-child(4){transform:rotate(15deg) translateX(110px) translateY(15px);z-index:1}
.vault-card.featured{
  z-index:10;
  width:280px;height:380px;
  background:linear-gradient(135deg,#1a1f2c,#0e1118);
  border:1px solid var(--accent);
  box-shadow:0 0 80px rgba(168,255,96,0.15);
  transform:rotate(0) translateY(-20px);
}
.vault-card.featured::after{
  content:'';
  width:90%;height:90%;
  background:url('') center/contain no-repeat;
}
.vault-stamp{
  position:absolute;top:14px;left:14px;
  font-family:var(--mono);font-size:9px;letter-spacing:0.15em;color:var(--accent);
}
.vault-stamp-r{position:absolute;bottom:14px;right:14px;font-family:var(--mono);font-size:9px;color:var(--ink3)}

/* === DIVIDER STRIPE === */
.stripe{
  background:var(--accent);color:var(--bg);
  padding:14px 0;overflow:hidden;white-space:nowrap;
  font-family:var(--mono);font-weight:600;font-size:13px;letter-spacing:0.2em;
  border-top:1px solid var(--bg);border-bottom:1px solid var(--bg);
  position:relative;z-index:1;
}
.stripe-track{display:inline-block;animation:scroll 40s linear infinite}
.stripe-track span{margin-right:48px}
@keyframes scroll{from{transform:translateX(0)}to{transform:translateX(-50%)}}

/* === SECTION === */
section{padding:80px 32px;max-width:1280px;margin:0 auto;position:relative;z-index:1}
.section-tag{
  font-family:var(--mono);font-size:11px;letter-spacing:0.2em;color:var(--accent);
  text-transform:uppercase;margin-bottom:14px;
}
.section-tag::before{content:'╱╱ '}
.section-title{
  font-size:40px;font-weight:700;letter-spacing:-0.02em;line-height:1.1;
  margin-bottom:18px;
}
.section-desc{color:var(--ink2);font-size:16px;max-width:640px;line-height:1.65}

/* === LORE GRID === */
.lore-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-top:48px}
.lore-card{
  background:var(--panel);border:1px solid var(--line);
  padding:28px 24px;
  transition:border-color .2s,transform .2s;
}
.lore-card:hover{border-color:var(--accent);transform:translateY(-4px)}
.lore-num{
  font-family:var(--mono);font-size:11px;color:var(--accent);letter-spacing:0.15em;
  margin-bottom:14px;
}
.lore-card h3{font-size:20px;font-weight:600;margin-bottom:10px}
.lore-card p{color:var(--ink2);font-size:14px;line-height:1.65}

/* === GALLERY === */
.gallery-section{padding-top:60px}
.gallery-header{
  display:flex;justify-content:space-between;align-items:flex-end;
  flex-wrap:wrap;gap:24px;margin-bottom:36px;
}
.gallery-counter{
  font-family:var(--mono);font-size:13px;color:var(--ink2);
}
.gallery-counter b{color:var(--accent);font-weight:600}

.filters{
  display:flex;flex-wrap:wrap;gap:10px;margin-bottom:32px;
  padding:18px 20px;background:var(--panel);border:1px solid var(--line);
}
.filter-group{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.filter-group label{
  font-family:var(--mono);font-size:10px;color:var(--ink3);
  letter-spacing:0.15em;text-transform:uppercase;margin-right:6px;
}
.chip{
  padding:6px 12px;
  font-family:var(--mono);font-size:11px;letter-spacing:0.05em;
  background:transparent;border:1px solid var(--line2);color:var(--ink2);
  cursor:pointer;transition:all .15s;
}
.chip:hover{border-color:var(--ink2);color:var(--ink)}
.chip.active{background:var(--accent);border-color:var(--accent);color:var(--bg);font-weight:600}
.search-box{
  display:flex;align-items:center;gap:8px;
  background:var(--bg);border:1px solid var(--line2);
  padding:8px 14px;margin-left:auto;
}
.search-box input{
  background:transparent;border:none;outline:none;color:var(--ink);
  font-family:var(--mono);font-size:12px;width:120px;
}
.search-box span{font-family:var(--mono);font-size:11px;color:var(--ink3)}

.grid{
  display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));
  gap:14px;
}
.card{
  background:var(--panel);border:1px solid var(--line);
  cursor:pointer;overflow:hidden;
  transition:all .2s;position:relative;
  aspect-ratio:88/121;
}
.card:hover{border-color:var(--accent);transform:translateY(-3px)}
.card img{width:100%;height:100%;object-fit:cover;display:block;background:var(--bg2)}
.card-tag{
  position:absolute;top:8px;left:8px;
  font-family:var(--mono);font-size:9px;color:var(--accent);
  background:rgba(10,12,18,0.85);padding:3px 7px;letter-spacing:0.1em;
  backdrop-filter:blur(4px);
}
.card-id{
  position:absolute;bottom:8px;right:8px;
  font-family:var(--mono);font-size:9px;color:var(--ink2);
  background:rgba(10,12,18,0.85);padding:3px 7px;
  backdrop-filter:blur(4px);
}
.empty-state{
  grid-column:1/-1;text-align:center;padding:80px 0;color:var(--ink3);
  font-family:var(--mono);font-size:13px;
}
.load-more{
  margin:48px auto 0;display:block;
}

/* === MODAL === */
.modal-bg{
  position:fixed;inset:0;background:rgba(5,7,12,0.92);backdrop-filter:blur(8px);
  z-index:100;display:none;align-items:center;justify-content:center;padding:40px;
}
.modal-bg.open{display:flex}
.modal{
  background:var(--panel);border:1px solid var(--line2);
  max-width:880px;width:100%;max-height:90vh;overflow:auto;
  display:grid;grid-template-columns:1fr 1fr;gap:0;
  position:relative;
}
.modal-close{
  position:absolute;top:12px;right:12px;z-index:5;
  background:rgba(10,12,18,0.8);border:1px solid var(--line2);color:var(--ink);
  width:32px;height:32px;cursor:pointer;font-size:18px;font-family:var(--mono);
  display:flex;align-items:center;justify-content:center;
}
.modal-close:hover{border-color:var(--accent);color:var(--accent)}
.modal-img{background:var(--bg);display:flex;align-items:center;justify-content:center;padding:24px}
.modal-img img{width:100%;max-width:340px;height:auto;display:block}
.modal-body{padding:36px 32px;display:flex;flex-direction:column;justify-content:center}
.modal-tag{font-family:var(--mono);font-size:10px;letter-spacing:0.2em;color:var(--accent);text-transform:uppercase;margin-bottom:10px}
.modal h2{font-size:26px;font-weight:700;line-height:1.2;margin-bottom:8px;letter-spacing:-0.01em}
.modal-sub{color:var(--ink2);font-size:14px;line-height:1.6;margin-bottom:24px}
.modal-traits{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.trait{
  background:var(--bg2);border:1px solid var(--line);padding:12px 14px;
}
.trait-lbl{font-family:var(--mono);font-size:9px;color:var(--ink3);letter-spacing:0.15em;text-transform:uppercase;margin-bottom:4px}
.trait-val{font-family:var(--mono);font-size:13px;color:var(--ink);font-weight:500}
.modal-sig{
  margin-top:20px;padding:10px 14px;background:var(--bg2);border:1px dashed var(--line2);
  font-family:var(--mono);font-size:11px;color:var(--ink3);word-break:break-all;
}
.modal-sig b{color:var(--accent2);font-weight:500}

/* === MINT CARD (legacy, unused in soon mode) ===
   Kept for safety so older bookmarks don't break.
*/

/* === SOON CARD === */
.soon-card{
  position:relative;
  margin:40px 0 56px;padding:36px 32px;
  background:linear-gradient(135deg,rgba(168,255,96,0.04),rgba(96,212,255,0.04));
  border:1px solid var(--line2);
  overflow:hidden;
}
.soon-card::before{
  content:'';position:absolute;inset:0;
  background-image:
    radial-gradient(circle at 20% 30%,rgba(168,255,96,0.12),transparent 60%),
    radial-gradient(circle at 80% 70%,rgba(96,212,255,0.10),transparent 55%);
  pointer-events:none;
}
.soon-tag{
  display:inline-flex;align-items:center;gap:8px;
  font-family:var(--mono);font-size:11px;letter-spacing:0.25em;
  color:var(--accent);margin-bottom:24px;
  padding:6px 12px;border:1px solid var(--accent);background:rgba(168,255,96,0.08);
  position:relative;z-index:2;
}
.soon-dot{width:6px;height:6px;border-radius:50%;background:var(--accent);animation:dotpulse 1.4s ease-in-out infinite}
@keyframes dotpulse{0%,100%{opacity:.4}50%{opacity:1}}
.soon-grid{
  display:grid;grid-template-columns:repeat(4,1fr);gap:24px;
  margin-bottom:28px;position:relative;z-index:2;
}
.soon-stat{border-left:2px solid var(--accent);padding-left:16px}
.soon-val{font-family:var(--mono);font-size:30px;font-weight:600;color:var(--ink);line-height:1.05}
.soon-unit{font-size:14px;color:var(--ink2);margin-left:4px;font-weight:400}
.soon-lbl{font-family:var(--mono);font-size:10px;letter-spacing:0.15em;text-transform:uppercase;color:var(--ink3);margin-top:6px}
.soon-meta{
  font-family:var(--mono);font-size:11px;color:var(--ink2);
  letter-spacing:0.05em;line-height:1.85;margin-bottom:24px;
  padding-top:20px;border-top:1px dashed var(--line2);
  position:relative;z-index:2;
}
.soon-cta{position:relative;z-index:2;display:inline-flex;width:auto}

/* === CONSTANTS INDEX (formula list section) === */
.constants-section{
  background:var(--bg2);border-top:1px solid var(--line);border-bottom:1px solid var(--line);
  margin:0 -32px;padding:80px 32px;position:relative;z-index:1;
}
.constants-inner{max-width:1280px;margin:0 auto}
.constants-grid{
  display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));
  gap:14px;margin-top:40px;
}
.const-card{
  background:var(--panel);border:1px solid var(--line);
  padding:18px 20px;transition:all .2s;
  display:flex;flex-direction:column;gap:8px;
  position:relative;overflow:hidden;
}
.const-card:hover{border-color:var(--accent);transform:translateY(-2px)}
.const-card::before{
  content:attr(data-code);
  position:absolute;top:14px;right:14px;
  font-family:var(--mono);font-size:9px;color:var(--ink3);letter-spacing:0.15em;
  background:var(--bg2);padding:3px 8px;border:1px solid var(--line);
}
.const-name{font-size:15px;font-weight:600;color:var(--ink);padding-right:60px}
.const-eq{
  font-family:var(--mono);font-size:13px;color:var(--accent2);
  letter-spacing:0;line-height:1.4;
  padding:10px 12px;background:var(--bg);border:1px dashed var(--line);
  word-break:break-word;
}
.const-meta{font-family:var(--mono);font-size:10px;color:var(--ink3);letter-spacing:0.08em;margin-top:auto;padding-top:6px}

/* === FLOATING MATH BG === */
.math-bg{
  position:absolute;inset:0;overflow:hidden;pointer-events:none;z-index:0;
}
.math-bg span{
  position:absolute;
  font-family:var(--mono);font-size:13px;color:var(--ink);
  opacity:0.04;letter-spacing:0.05em;white-space:nowrap;
  user-select:none;
}

/* === FOOTER === */
footer{
  border-top:1px solid var(--line);padding:48px 32px;margin-top:60px;
  position:relative;z-index:1;
  display:flex;justify-content:space-between;flex-wrap:wrap;gap:24px;
}
footer .col{font-family:var(--mono);font-size:12px;color:var(--ink3);line-height:1.8}
footer h4{font-size:11px;letter-spacing:0.2em;color:var(--ink);text-transform:uppercase;margin-bottom:12px}
footer a{color:var(--ink2);text-decoration:none}
footer a:hover{color:var(--accent)}

@media (max-width:880px){
  nav{padding:12px 16px;gap:12px}
  .nav-links{gap:14px;font-size:11px}
  .hero{grid-template-columns:1fr;gap:30px;padding:40px 18px 30px}
  .hero-left h1{font-size:38px}
  .hero-stats{flex-wrap:wrap;gap:16px 24px;margin-bottom:28px}
  .hero-cta{flex-direction:column;align-items:stretch}
  .hero-cta .btn{justify-content:center}
  .hero-right{height:300px}
  .vault-card{width:140px;height:195px}
  .vault-card.featured{width:170px;height:235px}
  .vault-card:nth-child(1){transform:rotate(-12deg) translateX(-65px)}
  .vault-card:nth-child(2){transform:rotate(-3deg) translateX(-22px) translateY(8px);z-index:2}
  .vault-card:nth-child(3){transform:rotate(6deg) translateX(35px) translateY(-3px);z-index:3}
  .vault-card:nth-child(4){transform:rotate(15deg) translateX(75px) translateY(10px);z-index:1}
  section{padding:48px 18px}
  .section-title{font-size:28px}
  .section-desc{font-size:15px}
  .lore-grid{grid-template-columns:1fr;gap:14px}
  .modal{grid-template-columns:1fr;max-height:95vh}
  .modal-img{padding:14px}
  .modal-img img{max-width:260px}
  .modal-body{padding:24px 22px}
  .modal h2{font-size:22px}
  .modal-traits{grid-template-columns:1fr 1fr;gap:10px}
  .grid{grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:10px}
  .filters{flex-direction:column;align-items:stretch;padding:14px;gap:14px}
  .filter-group{width:100%;margin-left:0 !important}
  .filter-group label{margin-bottom:4px;width:100%}
  .search-box{margin-left:0;width:100%}
  .search-box input{width:100%}
  .gallery-header{flex-direction:column;align-items:flex-start}
  .soon-card{padding:24px 20px}
  .soon-grid{grid-template-columns:repeat(2,1fr);gap:18px}
  .soon-val{font-size:24px}
  .soon-meta{font-size:10px}
  .soon-cta{width:100%;justify-content:center;text-align:center}
  .constants-section{margin:0 -18px;padding:56px 18px}
  .constants-grid{grid-template-columns:1fr;gap:12px}
  .const-card{padding:16px 16px}
  footer{padding:32px 18px;gap:20px}
  .stripe{font-size:11px;padding:11px 0}
  .math-bg span{font-size:11px}
}
@media (max-width:480px){
  .hero-left h1{font-size:30px}
  .section-title{font-size:24px}
  .grid{grid-template-columns:repeat(2,1fr)}
  .modal-traits{grid-template-columns:1fr}
  .nav-links{display:none}
  .brand{font-size:12px}
}
</style>
</head>
<body>

<nav>
  <div class="brand">CONSTANTS<b>·</b>NFT</div>
  <div class="nav-links">
    <a href="#lore">Lore</a>
    <a href="#gallery">Gallery</a>
    <a href="#mint">Mint</a>
    <a href="https://x.com/ConstantsNft" target="_blank" rel="noopener">X</a>
  </div>
</nav>

<header class="hero">
  <div class="hero-left">
    <div class="hero-tag">Genesis Drop · 333 Constants</div>
    <h1>The math that <span class="accent">stays</span><br>constant.</h1>
    <p class="hero-desc">A generative collection of 333 constants — every famous formula, attractor, and equation that ever shaped human thought, rendered as a unique parametric artifact. Each card is deterministic from its seed. Rarity is sealed inside the chain.</p>
    <div class="hero-stats">
      <div class="stat"><div class="stat-val">333</div><div class="stat-lbl">Total Supply</div></div>
      <div class="stat"><div class="stat-val">21</div><div class="stat-lbl">Formulas</div></div>
      <div class="stat"><div class="stat-val">10</div><div class="stat-lbl">Palettes</div></div>
      <div class="stat"><div class="stat-val">5</div><div class="stat-lbl">Rarity Tiers</div></div>
    </div>
    <div class="hero-cta">
      <a href="#gallery" class="btn btn-primary">Explore Gallery →</a>
      <a href="#mint" class="btn btn-ghost">Mint Info</a>
    </div>
  </div>
  <div class="hero-right">
    <div class="vault-card"><span class="vault-stamp">SIER · 1915</span></div>
    <div class="vault-card"><span class="vault-stamp">LRNZ · 1963</span></div>
    <div class="vault-card featured" id="heroFeat"><span class="vault-stamp">EULR · 1748</span><span class="vault-stamp-r">#???</span></div>
    <div class="vault-card"><span class="vault-stamp">MAND · 1980</span></div>
    <div class="vault-card"><span class="vault-stamp">FIBO · 1202</span></div>
  </div>
</header>

<div class="stripe">
  <div class="stripe-track">
    <span>◆ MINT TO REVEAL</span><span>◆ CONSTANTS STAY CONSTANT</span><span>◆ SEALED RARITY</span><span>◆ ON-CHAIN PROOF</span><span>◆ GENESIS 333</span>
    <span>◆ MINT TO REVEAL</span><span>◆ CONSTANTS STAY CONSTANT</span><span>◆ SEALED RARITY</span><span>◆ ON-CHAIN PROOF</span><span>◆ GENESIS 333</span>
  </div>
</div>

<section class="constants-section" id="constants-index">
  <div class="math-bg" id="mathBg"></div>
  <div class="constants-inner" style="position:relative;z-index:2">
    <div class="section-tag">The Index · 21 Constants</div>
    <h2 class="section-title">Twenty-one equations.<br><span style="color:var(--accent);font-style:italic;font-weight:300">Each one renders different.</span></h2>
    <p class="section-desc">Every card in the collection is generated from one of these constants. Same equation, infinite parameter space — palette, rotation, density, zoom, all randomized per token. Math made visible.</p>
    <div class="constants-grid" id="constantsGrid"></div>
  </div>
</section>

<section id="lore">
  <div class="section-tag">The Premise</div>
  <h2 class="section-title">The universe's permanent ink.</h2>
  <p class="section-desc">From Pythagoras to Mandelbrot, from chaos game to Lorenz attractor — these are the equations that don't bend, don't fade, don't get rewritten by time. We rendered each one as a one-of-a-kind card. Some are louder. Some are subtler. Some are myths.</p>
  <div class="lore-grid">
    <div class="lore-card">
      <div class="lore-num">// 01</div>
      <h3>Twenty-one formulas</h3>
      <p>From Sierpinski to Schrödinger. Each card hand-coded as its own renderer with parameter randomization across rotation, density, zoom, and overlay variants.</p>
    </div>
    <div class="lore-card">
      <div class="lore-num">// 02</div>
      <h3>Ten palettes</h3>
      <p>Neon, Magma, Lab, Arctic, Gold, Void, Noir, Ember, Rose, Forest. Some warm and obvious. Some cold and quiet. Some incredibly rare.</p>
    </div>
    <div class="lore-card">
      <div class="lore-num">// 03</div>
      <h3>Sealed rarity</h3>
      <p>Five tiers exist. Their distribution is locked into the seed. We won't tell you which token is what. Mint, hold, and find your number.</p>
    </div>
  </div>
</section>

<section id="gallery" class="gallery-section">
  <div class="gallery-header">
    <div>
      <div class="section-tag">The Collection</div>
      <h2 class="section-title">All 333, on display.</h2>
    </div>
    <div class="gallery-counter">Showing <b id="shownCount">0</b> of <b>333</b></div>
  </div>

  <div class="filters">
    <div class="filter-group" id="formulaFilters">
      <label>Formula</label>
      <button class="chip active" data-f="all">All</button>
    </div>
    <div class="filter-group" id="paletteFilters" style="margin-left:24px">
      <label>Palette</label>
      <button class="chip active" data-p="all">All</button>
    </div>
    <div class="search-box">
      <span>#</span>
      <input id="searchInput" type="number" min="1" max="333" placeholder="ID" />
    </div>
  </div>

  <div class="grid" id="grid"></div>
  <button class="btn btn-ghost load-more" id="loadMore" style="display:none">Load More</button>
</section>

<section id="mint">
  <div class="section-tag">Mint · Coming Soon</div>
  <h2 class="section-title">Pull a card.<br><span style="color:var(--accent);font-style:italic;font-weight:300">Reveal what found you.</span></h2>
  <p class="section-desc">Mint goes live on Ethereum mainnet. Each card is bound to a fixed formula, palette, and seed — generated parametrically, then sealed into IPFS. Token ID is assigned by ERC-721A in mint order, but rarity is randomized into the metadata at deployment. You don't pick. The constant picks you.</p>

  <div class="soon-card">
    <div class="soon-tag"><span class="soon-dot"></span>SOON</div>
    <div class="soon-grid">
      <div class="soon-stat">
        <div class="soon-val">333</div>
        <div class="soon-lbl">Total Supply</div>
      </div>
      <div class="soon-stat">
        <div class="soon-val">0.001<span class="soon-unit">ETH</span></div>
        <div class="soon-lbl">Mint Price</div>
      </div>
      <div class="soon-stat">
        <div class="soon-val">10</div>
        <div class="soon-lbl">Max / Wallet</div>
      </div>
      <div class="soon-stat">
        <div class="soon-val">5<span class="soon-unit">%</span></div>
        <div class="soon-lbl">Royalty</div>
      </div>
    </div>
    <div class="soon-meta">
      ▸ ERC-721A on Ethereum mainnet · ▸ Instant reveal · ▸ IPFS metadata · ▸ Verified contract on Etherscan
    </div>
    <a href="https://x.com/ConstantsNft" target="_blank" rel="noopener" class="btn btn-primary soon-cta">Follow @ConstantsNft for launch →</a>
  </div>

  <div class="lore-grid">
    <div class="lore-card">
      <div class="lore-num">// step 01</div>
      <h3>Wait for the bell</h3>
      <p>Mint date drops on X first. Whitelist holders get the first window. Public window opens 24 hours later if any supply remains.</p>
    </div>
    <div class="lore-card">
      <div class="lore-num">// step 02</div>
      <h3>Roll your number</h3>
      <p>Token ID is assigned by ERC-721A in mint order. The formula × palette × rarity pairing is sealed in metadata. Five tiers exist. We won't tell you which is which.</p>
    </div>
    <div class="lore-card">
      <div class="lore-num">// step 03</div>
      <h3>Reveal</h3>
      <p>Within seconds your card materializes — the parametric render of the constant that found you. View on OpenSea, hold, or trade.</p>
    </div>
  </div>
</section>

<footer>
  <div class="col">
    <h4>Constants</h4>
    Genesis Drop · 333 supply<br>
    Ethereum mainnet · ERC-721A<br>
    Constants stay constant.
  </div>
  <div class="col">
    <h4>Find us</h4>
    <a href="https://x.com/ConstantsNft" target="_blank" rel="noopener">Twitter / X · @ConstantsNft</a>
  </div>
  <div class="col">
    <h4>Built</h4>
    Single-file artifact<br>
    Deterministic generation<br>
    All images embedded
  </div>
</footer>

<div class="modal-bg" id="modalBg">
  <div class="modal" id="modal">
    <button class="modal-close" id="modalClose">×</button>
    <div class="modal-img"><img id="modalImg" alt=""></div>
    <div class="modal-body">
      <div class="modal-tag" id="modalTag">FORMULA · ####</div>
      <h2 id="modalName">—</h2>
      <p class="modal-sub" id="modalDesc">—</p>
      <div class="modal-traits" id="modalTraits"></div>
      <div class="modal-sig" id="modalSig"></div>
    </div>
  </div>
</div>

<script>
const ITEMS = __ITEMS_JSON__;

// === Build filter chips ===
const formulas = [...new Set(ITEMS.map(i=>i.code))].sort();
const palettes = [...new Set(ITEMS.map(i=>i.palette))].sort();
const fGroup = document.getElementById('formulaFilters');
const pGroup = document.getElementById('paletteFilters');
formulas.forEach(c=>{
  const b=document.createElement('button');
  b.className='chip';b.dataset.f=c;b.textContent=c;
  fGroup.appendChild(b);
});
palettes.forEach(p=>{
  const b=document.createElement('button');
  b.className='chip';b.dataset.p=p;b.textContent=p;
  pGroup.appendChild(b);
});

// === State ===
const state={formula:'all',palette:'all',search:'',shown:60};
const PAGE=60;

// === Render gallery ===
const grid=document.getElementById('grid');
const counter=document.getElementById('shownCount');
const loadMore=document.getElementById('loadMore');

function filter(){
  return ITEMS.filter(it=>{
    if(state.formula!=='all' && it.code!==state.formula) return false;
    if(state.palette!=='all' && it.palette!==state.palette) return false;
    if(state.search && !String(it.id).includes(state.search)) return false;
    return true;
  });
}

function render(){
  const filtered=filter();
  const slice=filtered.slice(0,state.shown);
  grid.innerHTML='';
  if(filtered.length===0){
    grid.innerHTML='<div class="empty-state">No cards match these filters. Try clearing them.</div>';
    counter.textContent='0';
    loadMore.style.display='none';
    return;
  }
  slice.forEach(it=>{
    const c=document.createElement('div');
    c.className='card';
    c.dataset.id=it.id;
    c.innerHTML=`
      <img src="data:image/jpeg;base64,${it.img}" alt="${it.name}" loading="lazy">
      <div class="card-tag">${it.code}</div>
      <div class="card-id">#${String(it.id).padStart(4,'0')}</div>
    `;
    c.addEventListener('click',()=>openModal(it));
    grid.appendChild(c);
  });
  counter.textContent=slice.length;
  loadMore.style.display=filtered.length>state.shown?'inline-flex':'none';
}

// === Filter handlers ===
fGroup.addEventListener('click',e=>{
  if(!e.target.classList.contains('chip')) return;
  fGroup.querySelectorAll('.chip').forEach(c=>c.classList.remove('active'));
  e.target.classList.add('active');
  state.formula=e.target.dataset.f;
  state.shown=PAGE;
  render();
});
pGroup.addEventListener('click',e=>{
  if(!e.target.classList.contains('chip')) return;
  pGroup.querySelectorAll('.chip').forEach(c=>c.classList.remove('active'));
  e.target.classList.add('active');
  state.palette=e.target.dataset.p;
  state.shown=PAGE;
  render();
});
document.getElementById('searchInput').addEventListener('input',e=>{
  state.search=e.target.value.trim();
  state.shown=PAGE;
  render();
});
loadMore.addEventListener('click',()=>{
  state.shown+=PAGE;
  render();
});

// === Modal ===
const modalBg=document.getElementById('modalBg');
const modalClose=document.getElementById('modalClose');
function openModal(it){
  document.getElementById('modalImg').src=`data:image/jpeg;base64,${it.img}`;
  document.getElementById('modalName').textContent=`${it.formula} · #${String(it.id).padStart(4,'0')}`;
  document.getElementById('modalTag').textContent=`${it.code} · ${it.palette.toUpperCase()}`;
  document.getElementById('modalDesc').textContent=it.desc;
  document.getElementById('modalTraits').innerHTML=`
    <div class="trait"><div class="trait-lbl">Formula Code</div><div class="trait-val">${it.code}</div></div>
    <div class="trait"><div class="trait-lbl">Palette</div><div class="trait-val">${it.palette}</div></div>
    <div class="trait"><div class="trait-lbl">Year</div><div class="trait-val">${it.year}</div></div>
    <div class="trait"><div class="trait-lbl">Discoverer</div><div class="trait-val">${it.discoverer}</div></div>
  `;
  document.getElementById('modalSig').innerHTML=`Signature · <b>${it.sig}</b>`;
  modalBg.classList.add('open');
  document.body.style.overflow='hidden';
}
function closeModal(){
  modalBg.classList.remove('open');
  document.body.style.overflow='';
}
modalClose.addEventListener('click',closeModal);
modalBg.addEventListener('click',e=>{if(e.target===modalBg) closeModal()});
document.addEventListener('keydown',e=>{if(e.key==='Escape') closeModal()});

// === Hero featured card === (random pick that's not super spoilery — just shows it's a card)
const featImg=ITEMS[Math.floor(Math.random()*ITEMS.length)].img;
const featEl=document.getElementById('heroFeat');
featEl.style.background=`url(data:image/jpeg;base64,${featImg}) center/cover, linear-gradient(135deg,#1a1f2c,#0e1118)`;
featEl.style.backgroundBlendMode='luminosity';

// === Initial render ===
render();

// === Constants Index ===
const CONSTANTS_INDEX = [
  {code:'SIER', name:'Sierpinski Triangle',     eq:'(x,y) → midpoint to one of 3 vertices', who:'W. Sierpinski',     yr:1915, kind:'fractal'},
  {code:'LRNZ', name:'Lorenz Attractor',        eq:'dx/dt = σ(y−x), dy/dt = x(ρ−z)−y, dz/dt = xy−βz', who:'E. Lorenz', yr:1963, kind:'chaos'},
  {code:'CLIF', name:'Clifford Attractor',      eq:'xₙ₊₁ = sin(a·yₙ) + c·cos(a·xₙ)',         who:'C. Pickover',     yr:1989, kind:'attractor'},
  {code:'MAND', name:'Mandelbrot Set',          eq:'zₙ₊₁ = zₙ² + c',                          who:'B. Mandelbrot',   yr:1980, kind:'fractal'},
  {code:'JULA', name:'Julia Set',               eq:'zₙ₊₁ = zₙ² + c (fixed c)',                who:'G. Julia',        yr:1918, kind:'fractal'},
  {code:'EULR', name:"Euler's Identity",        eq:'eⁱᵖⁱ + 1 = 0',                            who:'L. Euler',        yr:1748, kind:'identity'},
  {code:'LISS', name:'Lissajous Curve',         eq:'x = A·sin(at + δ), y = B·sin(bt)',        who:'J. Lissajous',    yr:1857, kind:'curve'},
  {code:'FERN', name:'Barnsley Fern',           eq:'IFS · 4 affine transforms',               who:'M. Barnsley',     yr:1988, kind:'fractal'},
  {code:'HART', name:'Heart Curve',             eq:'r = 1 − sin(θ)',                          who:'classical',       yr:1741, kind:'curve'},
  {code:'NAVI', name:'Navier-Stokes',           eq:'∂v/∂t + (v·∇)v = −∇p/ρ + ν∇²v + f',       who:'C-L. Navier',     yr:1822, kind:'physics'},
  {code:'FIBO', name:'Fibonacci Spiral',        eq:'Fₙ = Fₙ₋₁ + Fₙ₋₂',                        who:'Leonardo of Pisa', yr:1202, kind:'sequence'},
  {code:'WAVE', name:'Wave Equation',           eq:'∂²u/∂t² = c²·∇²u',                        who:"d'Alembert",      yr:1747, kind:'physics'},
  {code:'PYTH', name:'Pythagorean Theorem',     eq:'a² + b² = c²',                            who:'Pythagoras',      yr:-530, kind:'theorem'},
  {code:'SPIR', name:'Spirograph',              eq:'x = (R−r)cos(t) + d·cos((R−r)t/r)',       who:'D. Cohen',        yr:1965, kind:'curve'},
  {code:'GAUS', name:'Gaussian Distribution',   eq:'f(x) = e^(−(x−μ)²/2σ²) / σ√(2π)',         who:'C.F. Gauss',      yr:1809, kind:'statistics'},
  {code:'LGST', name:'Logistic Map',            eq:'xₙ₊₁ = r·xₙ(1−xₙ)',                       who:'P. Verhulst',     yr:1838, kind:'chaos'},
  {code:'FOUR', name:'Fourier Series',          eq:'f(x) = Σ aₙ·cos(nx) + bₙ·sin(nx)',        who:'J. Fourier',      yr:1807, kind:'series'},
  {code:'ROSE', name:'Rose Curve',              eq:'r = a·cos(kθ)',                           who:'G. Grandi',       yr:1728, kind:'curve'},
  {code:'SCHR', name:'Schrödinger Equation',    eq:'iℏ·∂ψ/∂t = Ĥψ',                           who:'E. Schrödinger',  yr:1926, kind:'physics'},
  {code:'KOCH', name:'Koch Snowflake',          eq:'L = 3·(4/3)ⁿ',                            who:'H. von Koch',     yr:1904, kind:'fractal'},
  {code:'GRAV', name:"Newton's Gravitation",    eq:'F = G·m₁m₂/r²',                           who:'I. Newton',       yr:1687, kind:'physics'},
];

const cgrid = document.getElementById('constantsGrid');
CONSTANTS_INDEX.forEach(c=>{
  const el = document.createElement('div');
  el.className = 'const-card';
  el.dataset.code = c.code;
  el.innerHTML = `
    <div class="const-name">${c.name}</div>
    <div class="const-eq">${c.eq}</div>
    <div class="const-meta">${c.who} · ${c.yr < 0 ? Math.abs(c.yr)+' BCE' : c.yr} · ${c.kind}</div>
  `;
  el.addEventListener('click',()=>{
    // Filter gallery by this code
    state.formula = c.code;
    state.shown = PAGE;
    fGroup.querySelectorAll('.chip').forEach(ch=>{
      ch.classList.toggle('active', ch.dataset.f === c.code);
    });
    render();
    document.getElementById('gallery').scrollIntoView({behavior:'smooth'});
  });
  cgrid.appendChild(el);
});

// === Floating math background ===
(function mathBg(){
  const symbols = [
    'eⁱᵖⁱ + 1 = 0', 'a² + b² = c²', 'F = m·a', 'E = mc²',
    '∇·E = ρ/ε₀', '∫f(x)dx', 'Σ Fₙ = Fₙ₋₁ + Fₙ₋₂',
    'r = a·cos(kθ)', 'π ≈ 3.14159', 'φ = 1.61803', 'e ≈ 2.71828',
    '∂u/∂t = c²·∇²u', 'zₙ₊₁ = zₙ² + c', 'iℏ∂ψ/∂t = Ĥψ',
    '√−1 = i', '0! = 1', 'lim(n→∞)', 'Σ 1/n²= π²/6',
    '∮E·dl = −dΦ/dt', 'P(A∩B)', '⟨ψ|H|ψ⟩', 'dx/dt = σ(y−x)',
  ];
  const wrap = document.getElementById('mathBg');
  const N = window.innerWidth < 700 ? 12 : 22;
  for (let i=0; i<N; i++){
    const s = document.createElement('span');
    s.textContent = symbols[i % symbols.length];
    s.style.top = Math.random()*100 + '%';
    s.style.left = Math.random()*100 + '%';
    s.style.transform = `rotate(${(Math.random()*40-20).toFixed(1)}deg)`;
    s.style.fontSize = (10 + Math.random()*8) + 'px';
    wrap.appendChild(s);
  }
})();
</script>

</body>
</html>
'''

html = html.replace('__ITEMS_JSON__', items_json)

out = '/home/ubuntu/formula-nft-web/index.html'
with open(out, 'w') as f:
    f.write(html)

print(f'wrote {out}')
print(f'size: {os.path.getsize(out)/1048576:.2f}MB')
