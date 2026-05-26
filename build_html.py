"""Build single-file HTML with embedded base64 gallery."""
import json, os, hashlib

with open('/home/ubuntu/formula-nft-web/items_hd.json') as f:
    thumbs = json.load(f)

# Compact items array for JS
items_json = json.dumps(thumbs['items'], separators=(',', ':'))

# Provenance hash: sha256 of concatenated signatures, ordered by token_id
with open('/home/ubuntu/formula-nft/output_v2/collection.json') as f:
    coll = json.load(f)
sigs = ''.join(it['signature'] for it in sorted(coll['items'], key=lambda x: x['token_id']))
provenance_hash = hashlib.sha256(sigs.encode()).hexdigest()

html = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Constants — Genesis 333</title>
<meta name="description" content="333 generative cards. 21 mathematical constants. Sealed rarity. Constants stay constant.">
<meta property="og:title" content="Constants — Genesis 333">
<meta property="og:description" content="333 generative cards. 21 mathematical constants. Sealed rarity.">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@ConstantsNft">
<link rel="icon" href="data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' fill='%230a0c12'/><text x='16' y='23' font-family='ui-monospace,monospace' font-size='22' font-weight='700' text-anchor='middle' fill='%23a8ff60'>%E2%9F%81</text></svg>">
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

/* === SPLASH === */
.splash{
  position:fixed;inset:0;z-index:9999;
  background:var(--bg);
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  gap:32px;
  transition:opacity .45s ease, visibility .45s;
}
.splash.gone{opacity:0;visibility:hidden;pointer-events:none}
.splash::before{
  content:'';position:absolute;inset:0;pointer-events:none;
  background-image:
    linear-gradient(rgba(255,255,255,0.02) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,255,255,0.02) 1px,transparent 1px);
  background-size:40px 40px;
}
.splash-mark{
  font-family:var(--mono);color:var(--accent);
  font-size:11px;letter-spacing:0.25em;text-transform:uppercase;
  position:relative;z-index:2;
}
.splash-mark::before{content:'◆ ';color:var(--gold)}
.splash-eq{
  font-family:var(--mono);font-size:34px;color:var(--ink);
  letter-spacing:0;line-height:1;
  position:relative;z-index:2;
  text-align:center;
  text-shadow:0 0 24px rgba(168,255,96,0.18);
}
.splash-eq .accent{color:var(--accent)}
.splash-sub{
  font-family:var(--mono);font-size:10px;color:var(--ink3);
  letter-spacing:0.18em;text-transform:uppercase;
  position:relative;z-index:2;
}
.splash-bar{
  width:min(360px,72vw);height:1px;background:var(--line2);
  position:relative;z-index:2;overflow:hidden;
}
.splash-bar::after{
  content:'';position:absolute;top:0;left:-40%;width:40%;height:100%;
  background:linear-gradient(90deg,transparent,var(--accent),transparent);
  animation:splash-sweep 1.4s ease-in-out infinite;
}
.splash-status{
  font-family:var(--mono);font-size:9px;color:var(--ink3);
  letter-spacing:0.2em;text-transform:uppercase;
  position:relative;z-index:2;font-variant-numeric:tabular-nums;
}
.splash-status b{color:var(--accent2);font-weight:500}
@keyframes splash-sweep{
  0%{left:-40%}
  100%{left:100%}
}
@media (max-width:640px){
  .splash-eq{font-size:24px}
  .splash-bar{width:80vw}
}

/* Reduce hero/scroll flicker pre-paint */
body.loading{overflow:hidden}

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
.modal-nav{
  position:absolute;top:50%;transform:translateY(-50%);z-index:5;
  width:40px;height:64px;
  background:rgba(10,12,18,0.7);border:1px solid var(--line2);color:var(--ink2);
  cursor:pointer;font-size:28px;line-height:1;font-weight:300;
  display:flex;align-items:center;justify-content:center;
  transition:all .2s;
  font-family:var(--mono);
}
.modal-nav:hover{background:var(--bg);border-color:var(--accent);color:var(--accent)}
.modal-nav-prev{left:-50px}
.modal-nav-next{right:-50px}
.modal-hint{
  margin-top:18px;font-family:var(--mono);font-size:9px;letter-spacing:0.18em;
  color:var(--ink3);text-transform:uppercase;
  display:flex;justify-content:center;align-items:center;gap:10px;
  padding-top:14px;border-top:1px solid var(--line);
}
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
  cursor:pointer;
}
.const-card:hover{border-color:var(--accent);transform:translateY(-2px)}
.const-card:hover .const-strip img{filter:saturate(1.1)}
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
.const-strip{
  display:grid;grid-template-columns:repeat(4,1fr);gap:4px;margin-top:4px;
}
.const-strip img{
  width:100%;aspect-ratio:1;object-fit:contain;
  border:1px solid var(--line);transition:filter .2s, border-color .2s;
  background:var(--bg);padding:2px;
}
.const-meta{font-family:var(--mono);font-size:10px;color:var(--ink3);letter-spacing:0.08em;margin-top:auto;padding-top:6px;display:flex;justify-content:space-between;align-items:center;gap:8px}
.const-meta .const-cta{
  color:var(--accent);font-weight:500;
  white-space:nowrap;font-size:9px;
}
.const-card:hover .const-cta{text-decoration:underline}

/* === FORMULA DEEP-DIVE MODAL === */
.fmodal-bg{
  position:fixed;inset:0;background:rgba(5,7,11,0.88);backdrop-filter:blur(8px);
  z-index:200;display:none;align-items:center;justify-content:center;padding:24px;
}
.fmodal-bg.open{display:flex}
.fmodal{
  background:var(--panel);border:1px solid var(--line2);
  max-width:780px;width:100%;max-height:88vh;overflow:auto;
  position:relative;
}
.fmodal-close{
  position:absolute;top:14px;right:14px;
  width:32px;height:32px;border:1px solid var(--line2);background:var(--bg);
  color:var(--ink2);font-size:18px;cursor:pointer;line-height:1;
  display:flex;align-items:center;justify-content:center;z-index:2;
  transition:all .2s;
}
.fmodal-close:hover{color:var(--accent);border-color:var(--accent)}
.fmodal-head{
  padding:32px 36px 24px;border-bottom:1px solid var(--line);
  position:relative;
}
.fmodal-tag{
  font-family:var(--mono);font-size:10px;letter-spacing:0.2em;
  color:var(--accent);text-transform:uppercase;margin-bottom:10px;
}
.fmodal-tag::before{content:'◆ ';color:var(--gold)}
.fmodal-name{
  font-size:30px;font-weight:700;letter-spacing:-0.02em;color:var(--ink);
  margin-bottom:14px;line-height:1.1;
}
.fmodal-eq{
  font-family:var(--mono);font-size:14px;color:var(--accent2);
  padding:14px 16px;background:var(--bg);border:1px dashed var(--line2);
  word-break:break-word;line-height:1.5;
}
.fmodal-meta{
  display:flex;flex-wrap:wrap;gap:8px;margin-top:14px;
  font-family:var(--mono);font-size:10px;
}
.fmodal-meta span{
  padding:4px 10px;background:var(--bg);border:1px solid var(--line);
  color:var(--ink2);letter-spacing:0.08em;text-transform:uppercase;
}
.fmodal-body{padding:28px 36px}
.fmodal-section{margin-bottom:24px}
.fmodal-section:last-child{margin-bottom:0}
.fmodal-h{
  font-family:var(--mono);font-size:10px;letter-spacing:0.18em;
  color:var(--ink3);text-transform:uppercase;margin-bottom:10px;
}
.fmodal-h::before{content:'╱╱ '}
.fmodal-text{color:var(--ink2);font-size:14px;line-height:1.7}
.fmodal-text b{color:var(--ink);font-weight:500}
.fmodal-variants{
  display:grid;grid-template-columns:repeat(6,1fr);gap:6px;
}
.fmodal-variants img{
  width:100%;aspect-ratio:1;object-fit:contain;
  border:1px solid var(--line);background:var(--bg);padding:3px;
  transition:transform .2s, border-color .2s;cursor:pointer;
}
.fmodal-variants img:hover{transform:scale(1.04);border-color:var(--accent)}
.fmodal-stats{
  display:grid;grid-template-columns:repeat(3,1fr);gap:10px;
  font-family:var(--mono);
}
.fmodal-stats .fst{
  background:var(--bg);border:1px solid var(--line);padding:12px 14px;
}
.fmodal-stats .fst-v{font-size:18px;font-weight:600;color:var(--ink);line-height:1}
.fmodal-stats .fst-l{font-size:9px;color:var(--ink3);letter-spacing:0.15em;text-transform:uppercase;margin-top:6px}
.fmodal-cta{
  display:flex;gap:10px;flex-wrap:wrap;margin-top:8px;
}

/* === PROVENANCE VERIFIER === */
.verifier{
  margin-top:28px;padding:24px;background:var(--bg);
  border:1px solid var(--line);
}
.verifier-head{
  font-family:var(--mono);font-size:11px;letter-spacing:0.15em;
  color:var(--accent);text-transform:uppercase;margin-bottom:6px;
}
.verifier-head::before{content:'◆ ';color:var(--gold)}
.verifier-desc{
  color:var(--ink2);font-size:13px;line-height:1.6;margin-bottom:14px;
}
.verifier textarea{
  width:100%;min-height:90px;padding:12px;
  background:var(--bg2);border:1px solid var(--line2);color:var(--ink);
  font-family:var(--mono);font-size:11px;line-height:1.5;
  resize:vertical;outline:none;
}
.verifier textarea:focus{border-color:var(--accent2)}
.verifier-row{
  display:flex;gap:10px;margin-top:10px;flex-wrap:wrap;align-items:center;
}
.verifier .btn{padding:10px 18px;font-size:11px}
.verifier-result{
  font-family:var(--mono);font-size:12px;padding:10px 14px;
  border:1px solid var(--line2);color:var(--ink2);
  flex:1;min-width:200px;word-break:break-all;line-height:1.4;
}
.verifier-result.ok{color:var(--accent);border-color:var(--accent)}
.verifier-result.bad{color:#ff7070;border-color:#ff7070}
.verifier-result.busy{color:var(--accent2);border-color:var(--accent2)}
.verifier-snip{
  margin-top:14px;padding:12px 14px;background:var(--bg2);
  border:1px solid var(--line);font-family:var(--mono);
  font-size:11px;color:var(--ink2);line-height:1.6;
  white-space:pre;overflow-x:auto;
}
.verifier-snip b{color:var(--accent2);font-weight:500}

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

/* === COUNTDOWN === */
.countdown{
  display:grid;grid-template-columns:repeat(4,1fr);gap:12px;
  margin-top:18px;margin-bottom:24px;
  position:relative;z-index:2;
}
.cd-cell{
  background:var(--bg);border:1px solid var(--line2);
  padding:18px 12px;text-align:center;
  position:relative;overflow:hidden;
}
.cd-cell::before{
  content:'';position:absolute;top:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,var(--accent),transparent);
  opacity:0.5;
}
.cd-num{
  font-family:var(--mono);font-size:32px;font-weight:700;
  color:var(--ink);line-height:1;letter-spacing:-0.02em;
  font-variant-numeric:tabular-nums;
}
.cd-lbl{
  font-family:var(--mono);font-size:9px;letter-spacing:0.2em;
  color:var(--ink3);text-transform:uppercase;margin-top:8px;
}
.cd-target{
  font-family:var(--mono);font-size:10px;color:var(--ink2);
  letter-spacing:0.08em;margin-bottom:14px;text-transform:uppercase;
  position:relative;z-index:2;
}
.cd-target b{color:var(--accent2);font-weight:500}

/* === MANIFESTO === */
.manifesto{
  background:var(--panel);border:1px solid var(--line);
  padding:48px 44px;margin-top:40px;
  position:relative;
}
.manifesto::before{
  content:'⟁';position:absolute;top:24px;right:32px;
  font-size:48px;color:var(--line2);font-weight:300;
}
.manifesto p{
  color:var(--ink2);font-size:16px;line-height:1.8;
  max-width:680px;margin-bottom:18px;
}
.manifesto p:last-child{margin-bottom:0}
.manifesto p b{color:var(--ink);font-weight:500}
.manifesto-sig{
  font-family:var(--mono);font-size:11px;letter-spacing:0.15em;
  color:var(--accent);text-transform:uppercase;margin-top:24px;
}

/* === HOW IT'S MADE === */
.process{
  display:grid;grid-template-columns:1.2fr 1fr;gap:40px;
  margin-top:40px;align-items:start;
}
.process-text p{
  color:var(--ink2);font-size:15px;line-height:1.75;margin-bottom:16px;
}
.process-text p b{color:var(--accent2);font-weight:500;font-family:var(--mono);font-size:13px}
.code-block{
  background:var(--bg);border:1px solid var(--line2);
  padding:20px 22px;
  font-family:var(--mono);font-size:12px;line-height:1.7;
  color:var(--ink2);overflow-x:auto;
  position:relative;
}
.code-block::before{
  content:'render.py';
  position:absolute;top:0;right:0;
  padding:4px 12px;font-size:10px;letter-spacing:0.15em;
  background:var(--panel);color:var(--ink3);border-left:1px solid var(--line2);border-bottom:1px solid var(--line2);
}
.code-block .k{color:var(--accent)}
.code-block .s{color:var(--gold)}
.code-block .c{color:var(--ink3);font-style:italic}
.code-block .n{color:var(--accent2)}

/* === PROVENANCE === */
.provenance{
  background:var(--bg2);border:1px solid var(--line);
  padding:32px 36px;margin-top:40px;
  font-family:var(--mono);
}
.prov-row{
  display:grid;grid-template-columns:140px 1fr;gap:16px;
  padding:12px 0;border-bottom:1px dashed var(--line);
  font-size:13px;align-items:start;
}
.prov-row:last-child{border-bottom:none}
.prov-key{
  color:var(--ink3);letter-spacing:0.1em;text-transform:uppercase;font-size:10px;
  padding-top:2px;
}
.prov-val{color:var(--ink);word-break:break-all;line-height:1.5}
.prov-val.hash{color:var(--accent2);font-size:11px}
.prov-val.pending{color:var(--ink3);font-style:italic}
.prov-val a{color:var(--accent);text-decoration:none;border-bottom:1px dashed var(--accent)}
.prov-val a:hover{color:#bfff80}

/* === KIND PRIMER === */
.primer-grid{
  display:grid;grid-template-columns:repeat(5,1fr);gap:10px;
  margin-top:32px;margin-bottom:8px;
}
.primer-card{
  background:var(--panel);border:1px solid var(--line);
  padding:18px 16px 16px;
  display:flex;flex-direction:column;gap:8px;
  transition:border-color .2s, transform .2s;
  position:relative;
}
.primer-card:hover{border-color:var(--accent);transform:translateY(-2px)}
.primer-glyph{
  font-family:var(--mono);font-size:22px;color:var(--accent2);
  line-height:1;letter-spacing:-0.02em;
  font-variant-numeric:tabular-nums;
}
.primer-name{
  font-family:var(--mono);font-size:11px;letter-spacing:0.15em;
  color:var(--ink);text-transform:uppercase;font-weight:500;
}
.primer-text{
  font-size:12px;color:var(--ink2);line-height:1.55;
}
.primer-count{
  font-family:var(--mono);font-size:9px;letter-spacing:0.15em;
  color:var(--ink3);text-transform:uppercase;margin-top:auto;padding-top:4px;
}

/* === TIMELINE === */
.timeline-wrap{
  margin-top:36px;
  background:var(--panel);border:1px solid var(--line);
  padding:24px 0 28px;
  position:relative;overflow:hidden;
}
.timeline-head{
  display:flex;justify-content:space-between;align-items:baseline;
  padding:0 28px;margin-bottom:20px;
  font-family:var(--mono);font-size:10px;letter-spacing:0.15em;
  color:var(--ink3);text-transform:uppercase;
}
.timeline-head .tl-span{color:var(--accent2)}
.timeline-scroll{
  overflow-x:auto;overflow-y:hidden;
  padding:36px 28px 24px;
  scrollbar-color:var(--line2) transparent;
}
.timeline-scroll::-webkit-scrollbar{height:8px}
.timeline-scroll::-webkit-scrollbar-track{background:transparent}
.timeline-scroll::-webkit-scrollbar-thumb{background:var(--line2);border-radius:0}
.timeline-track{
  position:relative;height:120px;min-width:1100px;
}
.timeline-line{
  position:absolute;left:0;right:0;top:50%;
  height:1px;background:linear-gradient(90deg,transparent,var(--line2) 4%,var(--line2) 96%,transparent);
}
.timeline-era{
  position:absolute;top:50%;transform:translateY(-50%);
  font-family:var(--mono);font-size:9px;letter-spacing:0.18em;
  color:var(--ink3);text-transform:uppercase;
  background:var(--panel);padding:2px 8px;
}
.tl-node{
  position:absolute;top:50%;transform:translate(-50%,-50%);
  display:flex;flex-direction:column;align-items:center;gap:4px;
  cursor:pointer;width:auto;
}
.tl-dot{
  width:11px;height:11px;border-radius:50%;
  background:var(--bg);border:1.5px solid var(--accent);
  transition:all .2s;
  box-shadow:0 0 0 3px var(--bg);
}
.tl-node:hover .tl-dot{transform:scale(1.4);background:var(--accent);box-shadow:0 0 0 4px rgba(168,255,96,0.15)}
.tl-label{
  position:absolute;bottom:18px;left:50%;transform:translateX(-50%);
  font-family:var(--mono);font-size:10px;color:var(--ink2);
  letter-spacing:0.08em;white-space:nowrap;
  background:var(--panel);padding:2px 6px;
  border:1px solid var(--line);
}
.tl-year{
  position:absolute;top:18px;left:50%;transform:translateX(-50%);
  font-family:var(--mono);font-size:9px;color:var(--ink3);
  letter-spacing:0.1em;white-space:nowrap;
}
.tl-node:hover .tl-label{color:var(--accent);border-color:var(--accent)}
.tl-node.alt .tl-label{bottom:auto;top:18px}
.tl-node.alt .tl-year{top:auto;bottom:18px}

/* === AMBIENT GRAIN === */
body::after{
  content:'';position:fixed;inset:0;pointer-events:none;z-index:0;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200' viewBox='0 0 200 200'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0.4 0'/></filter><rect width='100%25' height='100%25' filter='url(%23n)'/></svg>");
  opacity:0.025;mix-blend-mode:overlay;
}

/* === FAQ === */
.faq-list{
  display:flex;flex-direction:column;gap:8px;margin-top:36px;
  max-width:880px;
}
.faq-item{
  background:var(--panel);border:1px solid var(--line);
  transition:border-color .2s;
}
.faq-item:hover{border-color:var(--line2)}
.faq-item[open]{border-color:var(--accent)}
.faq-q{
  list-style:none;cursor:pointer;
  padding:18px 22px;
  font-family:var(--display);font-size:15px;font-weight:500;color:var(--ink);
  display:flex;justify-content:space-between;align-items:center;gap:16px;
  user-select:none;
}
.faq-q::-webkit-details-marker{display:none}
.faq-q::after{
  content:'+';font-family:var(--mono);font-size:20px;color:var(--accent);
  font-weight:300;line-height:1;transition:transform .2s;
  flex-shrink:0;
}
.faq-item[open] .faq-q::after{transform:rotate(45deg)}
.faq-q .faq-tag{
  font-family:var(--mono);font-size:9px;letter-spacing:0.15em;
  color:var(--ink3);text-transform:uppercase;margin-right:auto;
  padding:3px 8px;border:1px solid var(--line2);
}
.faq-q .faq-text{flex:1}
.faq-a{
  padding:0 22px 22px 22px;
  color:var(--ink2);font-size:14px;line-height:1.7;
}
.faq-a code{
  font-family:var(--mono);font-size:12px;color:var(--accent2);
  background:var(--bg);padding:2px 6px;border:1px solid var(--line);
}
.faq-a a{color:var(--accent);text-decoration:none;border-bottom:1px solid var(--line2)}
.faq-a a:hover{border-bottom-color:var(--accent)}
.faq-a p{margin-bottom:10px}
.faq-a p:last-child{margin-bottom:0}
.faq-a ul{list-style:none;margin:8px 0;padding:0}
.faq-a ul li{padding:4px 0 4px 18px;position:relative}
.faq-a ul li::before{content:'▸';position:absolute;left:0;color:var(--accent);font-size:11px;top:6px}

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
  .modal-nav{width:36px;height:48px;font-size:22px}
  .modal-nav-prev{left:8px;top:auto;bottom:8px;transform:none}
  .modal-nav-next{right:8px;top:auto;bottom:8px;transform:none}
  .modal-hint{font-size:8px;gap:6px}
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
  .countdown{grid-template-columns:repeat(4,1fr);gap:6px}
  .cd-cell{padding:14px 4px}
  .cd-num{font-size:22px}
  .cd-lbl{font-size:8px;letter-spacing:0.12em}
  .manifesto{padding:32px 24px}
  .manifesto p{font-size:15px;line-height:1.75}
  .manifesto::before{font-size:32px;top:18px;right:20px}
  .process{grid-template-columns:1fr;gap:24px}
  .code-block{font-size:11px;padding:18px 16px}
  .provenance{padding:24px 20px}
  .prov-row{grid-template-columns:1fr;gap:4px;padding:10px 0}
  .prov-key{padding-top:0;font-size:9px}
  .faq-q{padding:14px 16px;font-size:14px;flex-wrap:wrap}
  .faq-q .faq-tag{font-size:8px;padding:2px 6px}
  .faq-a{padding:0 16px 18px 16px;font-size:13px}
  .const-strip{grid-template-columns:repeat(4,1fr)}
  .fmodal-head{padding:24px 22px 20px}
  .fmodal-name{font-size:22px}
  .fmodal-body{padding:22px}
  .fmodal-eq{font-size:12px;padding:10px 12px}
  .fmodal-variants{grid-template-columns:repeat(4,1fr)}
  .fmodal-stats{grid-template-columns:repeat(3,1fr);gap:6px}
  .fmodal-stats .fst{padding:10px 10px}
  .fmodal-stats .fst-v{font-size:15px}
  .verifier{padding:18px}
  .verifier-row{flex-direction:column;align-items:stretch}
  .verifier-result{min-width:0}
  .primer-grid{grid-template-columns:repeat(2,1fr);gap:8px}
  .primer-card{padding:14px 14px 12px}
  .primer-glyph{font-size:18px}
  .timeline-wrap{margin-top:28px}
  .timeline-head{padding:0 18px;flex-wrap:wrap;gap:6px}
  .timeline-scroll{padding:36px 18px 24px}
  .timeline-track{min-width:1400px}
  .tl-label{font-size:9px;padding:2px 5px}
  .tl-year{font-size:8px}
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
<body class="loading">

<div class="splash" id="splash" aria-hidden="true">
  <div class="splash-mark">Constants · Genesis 333</div>
  <div class="splash-eq">e<sup>iπ</sup> + 1 = <span class="accent">0</span></div>
  <div class="splash-sub">rendering 333 deterministic constants</div>
  <div class="splash-bar"></div>
  <div class="splash-status" id="splashStatus">parsing the universe · <b>0%</b></div>
</div>

<nav>
  <div class="brand">CONSTANTS<b>·</b>NFT</div>
  <div class="nav-links">
    <a href="#lore">Lore</a>
    <a href="#how">Process</a>
    <a href="#provenance">Proof</a>
    <a href="#gallery">Gallery</a>
    <a href="#mint">Mint</a>
    <a href="#faq">FAQ</a>
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

    <div class="primer-grid" id="primerGrid"></div>

    <div class="constants-grid" id="constantsGrid"></div>

    <div class="timeline-wrap">
      <div class="timeline-head">
        <span>Timeline · 21 constants across <span class="tl-span">2,517 years</span></span>
        <span>← scroll →</span>
      </div>
      <div class="timeline-scroll" id="timelineScroll">
        <div class="timeline-track" id="timelineTrack">
          <div class="timeline-line"></div>
        </div>
      </div>
    </div>
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

  <div class="manifesto">
    <p>The chart will paint. Liquidity will rotate. Narratives will turn over by lunchtime.</p>
    <p><b>π</b> will still equal <b>π</b>.</p>
    <p>Constants is built on the things that don't move. Twenty-one equations that survived empires, gods, paradigm shifts, and every market cycle since markets were invented. We rendered each one as a parametric artifact and sealed 333 of them on-chain.</p>
    <p>No roadmap. No utility theater. No "based on engagement." The math is the utility. The proof is the proof. Mint, or don't — the constants don't care either way.</p>
    <p><b>Constants stay constant.</b></p>
    <div class="manifesto-sig">⟁ Genesis · 333 · sealed</div>
  </div>
</section>

<section id="how">
  <div class="section-tag">How It's Made</div>
  <h2 class="section-title">Determinism, all the way down.</h2>
  <p class="section-desc">Every card is the output of a pure function. Same seed, same constant, same render — forever. Nothing in the pipeline is improvised.</p>

  <div class="process">
    <div class="process-text">
      <p><b>// 01 · seed</b><br>Each token has a 64-bit seed derived from a base seed plus its token ID. Deterministic. Reproducible. Pre-computed.</p>
      <p><b>// 02 · constant</b><br>The seed picks one of 21 mathematical constants — Sierpinski, Lorenz, Mandelbrot, Schrödinger, and the rest of the canon.</p>
      <p><b>// 03 · palette</b><br>Same seed picks one of 10 palettes. Some warm. Some void. Some so rare they only show up in single digits across the supply.</p>
      <p><b>// 04 · render</b><br>The constant's renderer takes 4-6 randomized parameters — rotation, density, zoom, position, color depth — and produces a 880×1210 frame. Pinned to IPFS. Hashed into the provenance.</p>
    </div>
    <pre class="code-block">
<span class="c"># pseudo-code · the whole pipeline</span>
<span class="k">def</span> <span class="n">render</span>(token_id):
    seed     = sha256(<span class="s">"constants"</span> + token_id)
    rng      = Random(seed)
    constant = rng.pick(<span class="n">CONSTANTS_21</span>)
    palette  = rng.pick(<span class="n">PALETTES_10</span>)
    params   = constant.params(rng)
    rarity   = rng.tier()  <span class="c"># sealed</span>
    <span class="k">return</span> constant.draw(params, palette)

<span class="c"># Same input → same output, forever.</span>
<span class="c"># That's the whole promise.</span>
    </pre>
  </div>
</section>

<section id="provenance">
  <div class="section-tag">On-Chain · Provenance</div>
  <h2 class="section-title">Verifiable, immutable, math.</h2>
  <p class="section-desc">Every render is hashed before deploy. The provenance hash below is computed from the concatenated signatures of all 333 tokens, in order. Anyone can re-derive it from the metadata and verify nothing was swapped after launch.</p>

  <div class="provenance">
    <div class="prov-row">
      <div class="prov-key">Standard</div>
      <div class="prov-val">ERC-721A · ERC-2981 royalties</div>
    </div>
    <div class="prov-row">
      <div class="prov-key">Chain</div>
      <div class="prov-val">Ethereum mainnet (chainId 1)</div>
    </div>
    <div class="prov-row">
      <div class="prov-key">Supply</div>
      <div class="prov-val">333 · sealed at deploy</div>
    </div>
    <div class="prov-row">
      <div class="prov-key">Mint price</div>
      <div class="prov-val">0.001 ETH · max 10 / wallet</div>
    </div>
    <div class="prov-row">
      <div class="prov-key">Royalty</div>
      <div class="prov-val">5% (500 bps) · ERC-2981</div>
    </div>
    <div class="prov-row">
      <div class="prov-key">Provenance</div>
      <div class="prov-val hash">__PROVENANCE_HASH__</div>
    </div>
    <div class="prov-row">
      <div class="prov-key">Method</div>
      <div class="prov-val">sha256( sig₁ ‖ sig₂ ‖ … ‖ sig₃₃₃ ) · ordered by token_id</div>
    </div>
    <div class="prov-row">
      <div class="prov-key">Contract</div>
      <div class="prov-val pending">pending deploy · address will appear here</div>
    </div>
    <div class="prov-row">
      <div class="prov-key">Etherscan</div>
      <div class="prov-val pending">pending deploy</div>
    </div>
    <div class="prov-row">
      <div class="prov-key">Metadata</div>
      <div class="prov-val pending">ipfs://… · pinned at launch</div>
    </div>
  </div>

  <div class="verifier">
    <div class="verifier-head">Verify it yourself</div>
    <p class="verifier-desc">Paste a JSON array of all 333 signatures (or any subset, in token-id order) and we'll hash them in your browser. No server. Just <code style="font-family:var(--mono);color:var(--accent2)">sha256(sig₁ ‖ sig₂ ‖ …)</code>.</p>
    <textarea id="verifierInput" placeholder='[ "sig_token_1", "sig_token_2", ... ]' spellcheck="false"></textarea>
    <div class="verifier-row">
      <button class="btn btn-primary" id="verifierBtn">Compute hash</button>
      <button class="btn btn-ghost" id="verifierLoad">Load all 333</button>
      <div class="verifier-result" id="verifierResult">awaiting input · sha256 computed in-browser</div>
    </div>
    <div class="verifier-snip"><b># python verification:</b>
import json, hashlib
sigs = json.load(open('signatures.json'))
print(hashlib.sha256(''.join(sigs).encode()).hexdigest())
<b># expected:</b> __PROVENANCE_HASH__</div>
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
    <div class="cd-target">Genesis · target window · <b id="cdTarget">TBA</b></div>
    <div class="countdown" id="countdown">
      <div class="cd-cell"><div class="cd-num" id="cdD">--</div><div class="cd-lbl">Days</div></div>
      <div class="cd-cell"><div class="cd-num" id="cdH">--</div><div class="cd-lbl">Hours</div></div>
      <div class="cd-cell"><div class="cd-num" id="cdM">--</div><div class="cd-lbl">Minutes</div></div>
      <div class="cd-cell"><div class="cd-num" id="cdS">--</div><div class="cd-lbl">Seconds</div></div>
    </div>
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

<section id="faq">
  <div class="section-tag">Questions · Answered</div>
  <h2 class="section-title">The fine print,<br><span style="color:var(--accent);font-style:italic;font-weight:300">in plain language.</span></h2>
  <p class="section-desc">Everything we get asked, written down once. If something's missing, ping us on X.</p>

  <div class="faq-list">

    <details class="faq-item" open>
      <summary class="faq-q"><span class="faq-tag">01 · Mint</span><span class="faq-text">When does the mint go live?</span></summary>
      <div class="faq-a">
        <p>The launch window is announced first on <a href="https://x.com/ConstantsNft" target="_blank" rel="noopener">@ConstantsNft</a>. Whitelist gets the first window. Public window opens 24 hours later if any supply remains. The countdown on this page updates the moment the date is locked.</p>
      </div>
    </details>

    <details class="faq-item">
      <summary class="faq-q"><span class="faq-tag">02 · Mint</span><span class="faq-text">What's the price and wallet limit?</span></summary>
      <div class="faq-a">
        <p><code>0.001 ETH</code> per card. <code>10</code> max per wallet. No tiered pricing, no Dutch auction — same price for whitelist and public.</p>
      </div>
    </details>

    <details class="faq-item">
      <summary class="faq-q"><span class="faq-tag">03 · Chain</span><span class="faq-text">Which chain? Why mainnet and not L2?</span></summary>
      <div class="faq-a">
        <p>Ethereum mainnet, <code>chainId 1</code>, <code>ERC-721A</code> for cheap batched mints. We chose mainnet because the thesis is permanence — these are constants. They live where the strongest consensus is.</p>
      </div>
    </details>

    <details class="faq-item">
      <summary class="faq-q"><span class="faq-tag">04 · Supply</span><span class="faq-text">Is supply really capped at 333?</span></summary>
      <div class="faq-a">
        <p>Yes. The cap is enforced at the contract level and sealed at deploy. No team-mint reserve hidden in the source. No "Volume II of Genesis 333." Anything we ship later is a separate collection on a separate contract.</p>
      </div>
    </details>

    <details class="faq-item">
      <summary class="faq-q"><span class="faq-tag">05 · Rarity</span><span class="faq-text">How does rarity work?</span></summary>
      <div class="faq-a">
        <p>Five tiers exist across the 333 cards. The exact distribution is sealed in the metadata at deploy and verifiable through the provenance hash. We're not publishing per-formula odds — we don't want anyone reverse-engineering which constants are most likely to land high tiers. Mint, then look.</p>
        <p><b>Constants stay constant.</b> The rarity is the rarity. Nobody re-rolls.</p>
      </div>
    </details>

    <details class="faq-item">
      <summary class="faq-q"><span class="faq-tag">06 · Reveal</span><span class="faq-text">Is there a delayed reveal?</span></summary>
      <div class="faq-a">
        <p>No delay. Your card is fully revealed the moment the mint transaction confirms. The image is already on IPFS, the metadata is already pinned. We don't run a "blind box, wait 48 hours" cycle.</p>
      </div>
    </details>

    <details class="faq-item">
      <summary class="faq-q"><span class="faq-tag">07 · Art</span><span class="faq-text">Are the renders generated at mint, or pre-rendered?</span></summary>
      <div class="faq-a">
        <p>Pre-rendered, deterministically. Every card is the output of a pure function of <code>(formula, palette, seed)</code> — same inputs, same image, every time. We render once, hash, pin to IPFS, then deploy. The provenance hash on this page proves nothing was swapped.</p>
      </div>
    </details>

    <details class="faq-item">
      <summary class="faq-q"><span class="faq-tag">08 · Royalty</span><span class="faq-text">What's the royalty?</span></summary>
      <div class="faq-a">
        <p><code>5%</code> via <code>ERC-2981</code>. Honored on marketplaces that respect on-chain royalties. We don't run an enforcement allowlist — if a marketplace ignores 2981, that's their call.</p>
      </div>
    </details>

    <details class="faq-item">
      <summary class="faq-q"><span class="faq-tag">09 · Bot</span><span class="faq-text">How are you stopping bots?</span></summary>
      <div class="faq-a">
        <p>Per-wallet cap of 10, EOA-only mint guard, and the whitelist window is signature-gated. We won't pretend bots are impossible — but cost-per-bot is high enough that organic minters won't get squeezed out.</p>
      </div>
    </details>

    <details class="faq-item">
      <summary class="faq-q"><span class="faq-tag">10 · Trust</span><span class="faq-text">Who's behind Constants?</span></summary>
      <div class="faq-a">
        <p>The contract is verified on Etherscan at deploy. The provenance hash on this page lets anyone independently verify that the metadata wasn't reordered after launch — no team, no privileged keys can swap the renders after the fact.</p>
        <p>No DAO, no team token, no roadmap dependency on a third party. Just one set of math, one drop, signed.</p>
      </div>
    </details>

    <details class="faq-item">
      <summary class="faq-q"><span class="faq-tag">11 · Refund</span><span class="faq-text">Can I get a refund or sell back?</span></summary>
      <div class="faq-a">
        <p>No buybacks, no team-side refunds. Once the mint transaction confirms, the card is yours and the ETH is committed. Secondary trading happens on OpenSea, Blur, or any marketplace that supports ERC-721 — we don't gate that.</p>
      </div>
    </details>

    <details class="faq-item">
      <summary class="faq-q"><span class="faq-tag">12 · License</span><span class="faq-text">What can I do with a card I own?</span></summary>
      <div class="faq-a">
        <p>You hold the token, you hold a non-exclusive license to display and remix the artwork for personal and commercial use. The underlying mathematical constants belong to no one — we're just the renderers.</p>
      </div>
    </details>

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
    <button class="modal-nav modal-nav-prev" id="modalPrev" aria-label="Previous card">‹</button>
    <button class="modal-nav modal-nav-next" id="modalNext" aria-label="Next card">›</button>
    <div class="modal-img"><img id="modalImg" alt=""></div>
    <div class="modal-body">
      <div class="modal-tag" id="modalTag">FORMULA · ####</div>
      <h2 id="modalName">—</h2>
      <p class="modal-sub" id="modalDesc">—</p>
      <div class="modal-traits" id="modalTraits"></div>
      <div class="modal-sig" id="modalSig"></div>
      <div class="modal-hint">← → navigate · esc to close</div>
    </div>
  </div>
</div>

<div class="fmodal-bg" id="fmodalBg">
  <div class="fmodal" id="fmodal">
    <button class="fmodal-close" id="fmodalClose" aria-label="Close">×</button>
    <div class="fmodal-head">
      <div class="fmodal-tag" id="fmodalTag">CONSTANT · ####</div>
      <h2 class="fmodal-name" id="fmodalName">—</h2>
      <div class="fmodal-eq" id="fmodalEq">—</div>
      <div class="fmodal-meta" id="fmodalMeta"></div>
    </div>
    <div class="fmodal-body">
      <div class="fmodal-section">
        <div class="fmodal-h">What it is</div>
        <p class="fmodal-text" id="fmodalLore">—</p>
      </div>
      <div class="fmodal-section">
        <div class="fmodal-h">Why it matters</div>
        <p class="fmodal-text" id="fmodalWhy">—</p>
      </div>
      <div class="fmodal-section">
        <div class="fmodal-h">Cards rendered</div>
        <div class="fmodal-stats" id="fmodalStats"></div>
      </div>
      <div class="fmodal-section">
        <div class="fmodal-h">Sample variants — same equation, different parameters</div>
        <div class="fmodal-variants" id="fmodalVariants"></div>
      </div>
      <div class="fmodal-section">
        <div class="fmodal-cta">
          <button class="btn btn-primary" id="fmodalGoGallery">View all in gallery →</button>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
const ITEMS = __ITEMS_JSON__;

// === Splash bootstrap ===
(function splashBoot(){
  const splash = document.getElementById('splash');
  const status = document.getElementById('splashStatus');
  if (!splash) return;
  const stages = [
    'parsing the universe',
    'computing 333 signatures',
    'verifying provenance',
    'almost there',
  ];
  const start = performance.now();
  const minDuration = 1100; // ms — keep splash visible long enough to read
  let pct = 0;
  const tick = setInterval(()=>{
    pct = Math.min(99, pct + Math.random()*9 + 3);
    const stage = stages[Math.min(stages.length-1, Math.floor(pct/25))];
    if (status) status.innerHTML = `${stage} · <b>${Math.floor(pct)}%</b>`;
  }, 90);
  function dismiss(){
    clearInterval(tick);
    if (status) status.innerHTML = 'rendering complete · <b>100%</b>';
    splash.classList.add('gone');
    document.body.classList.remove('loading');
    setTimeout(()=>splash.remove(), 600);
  }
  function ready(){
    const elapsed = performance.now() - start;
    const wait = Math.max(0, minDuration - elapsed);
    setTimeout(dismiss, wait);
  }
  if (document.readyState === 'complete' || document.readyState === 'interactive'){
    requestAnimationFrame(ready);
  } else {
    window.addEventListener('DOMContentLoaded', ()=>requestAnimationFrame(ready));
  }
  // Hard fallback — never trap user
  setTimeout(dismiss, 6000);
})();

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
let currentItem = null;
function openModal(it){
  currentItem = it;
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
  currentItem = null;
}
function navModal(dir){
  if (!currentItem) return;
  const filtered = filter();
  if (!filtered.length) return;
  const idx = filtered.findIndex(it=>it.id===currentItem.id);
  if (idx < 0){
    // Current item not in current filter — open first match instead
    openModal(filtered[0]);
    return;
  }
  const next = filtered[(idx + dir + filtered.length) % filtered.length];
  openModal(next);
}
modalClose.addEventListener('click',closeModal);
document.getElementById('modalPrev').addEventListener('click',e=>{e.stopPropagation();navModal(-1)});
document.getElementById('modalNext').addEventListener('click',e=>{e.stopPropagation();navModal(+1)});
modalBg.addEventListener('click',e=>{if(e.target===modalBg) closeModal()});
document.addEventListener('keydown',e=>{
  if (!modalBg.classList.contains('open')) return;
  if (e.key==='Escape'){ closeModal(); return; }
  if (e.key==='ArrowRight'){ e.preventDefault(); navModal(+1); }
  else if (e.key==='ArrowLeft'){ e.preventDefault(); navModal(-1); }
});

// === Hero featured card === (random pick that's not super spoilery — just shows it's a card)
const featImg=ITEMS[Math.floor(Math.random()*ITEMS.length)].img;
const featEl=document.getElementById('heroFeat');
featEl.style.background=`url(data:image/jpeg;base64,${featImg}) center/cover, linear-gradient(135deg,#1a1f2c,#0e1118)`;
featEl.style.backgroundBlendMode='luminosity';

// === Initial render ===
render();

// === Constants Index ===
const CONSTANTS_INDEX = [
  {code:'SIER', name:'Sierpinski Triangle',     eq:'(x,y) → midpoint to one of 3 vertices', who:'W. Sierpinski',     yr:1915, kind:'fractal',
   lore:"A triangle made by jumping halfway to a random vertex, over and over. Three rules, infinite detail. The chaos game's first proof that randomness can build perfect order.",
   why:"Showed mathematicians that simple iterative rules can carve self-similar structure out of pure noise — a foundational moment in fractal geometry."},
  {code:'LRNZ', name:'Lorenz Attractor',        eq:'dx/dt = σ(y−x), dy/dt = x(ρ−z)−y, dz/dt = xy−βz', who:'E. Lorenz', yr:1963, kind:'chaos',
   lore:"A weather model that bent into butterfly wings. Three coupled ODEs that never repeat, never escape, never settle — bounded but eternally restless.",
   why:"The image of chaos itself. Lorenz proved deterministic systems can be unpredictable, and the butterfly effect entered every scientific vocabulary on Earth."},
  {code:'CLIF', name:'Clifford Attractor',      eq:'xₙ₊₁ = sin(a·yₙ) + c·cos(a·xₙ)',         who:'C. Pickover',     yr:1989, kind:'attractor',
   lore:"A four-parameter strange attractor by Cliff Pickover — short loop, long memory. Every parameter shift redraws the universe.",
   why:"A staple of generative art. Tiny coefficient nudges flip topology entirely, making it the perfect canvas for parametric exploration."},
  {code:'MAND', name:'Mandelbrot Set',          eq:'zₙ₊₁ = zₙ² + c',                          who:'B. Mandelbrot',   yr:1980, kind:'fractal',
   lore:"The complex-plane test: pick a point c, iterate z² + c, ask if it stays bounded. The boundary between yes and no is infinite, jagged, alive.",
   why:"The most photographed equation in mathematics. Proved fractals weren't a curiosity — they're how nature actually draws coastlines, lungs, and lightning."},
  {code:'JULA', name:'Julia Set',               eq:'zₙ₊₁ = zₙ² + c (fixed c)',                who:'G. Julia',        yr:1918, kind:'fractal',
   lore:"Same iteration as Mandelbrot, but c is locked and z₀ varies. Each c value is its own universe — connected, dust, dendrite, spiral.",
   why:"Predates Mandelbrot by 60 years. The Julia set is the parameter slice that taught us a single number can encode an entire fractal continent."},
  {code:'EULR', name:"Euler's Identity",        eq:'eⁱᵖⁱ + 1 = 0',                            who:'L. Euler',        yr:1748, kind:'identity',
   lore:"Five fundamental constants in one statement. e, i, π, 1, and 0 — multiplication, exponentiation, addition, identity, nothing — all bound by a single equality.",
   why:"Routinely voted the most beautiful equation ever written. It's not a tool, it's a proof that the universe's constants know each other intimately."},
  {code:'LISS', name:'Lissajous Curve',         eq:'x = A·sin(at + δ), y = B·sin(bt)',        who:'J. Lissajous',    yr:1857, kind:'curve',
   lore:"Two perpendicular sine waves, woven by a frequency ratio. Rational ratios close the loop. Irrational ratios trace forever without repeating.",
   why:"The first instrument for visualizing audio frequency. Every oscilloscope still draws Lissajous figures when fed a tone."},
  {code:'FERN', name:'Barnsley Fern',           eq:'IFS · 4 affine transforms',               who:'M. Barnsley',     yr:1988, kind:'fractal',
   lore:"Four affine transformations, applied probabilistically. From four rules and a dice roll, a fern leaf emerges — stem, fronds, every detail.",
   why:"Proved that biological complexity can be compressed into 24 numbers. The IFS theorem became the basis for fractal image compression."},
  {code:'HART', name:'Heart Curve',             eq:'r = 1 − sin(θ)',                          who:'classical',       yr:1741, kind:'curve',
   lore:"A polar cardioid. Plot r against θ in standard form, get a heart. The math knew before the emoji did.",
   why:"The cardioid appears in epicycloids, in microphone pickup patterns, in the central bulb of the Mandelbrot set. Same shape, different physics."},
  {code:'NAVI', name:'Navier-Stokes',           eq:'∂v/∂t + (v·∇)v = −∇p/ρ + ν∇²v + f',       who:'C-L. Navier',     yr:1822, kind:'physics',
   lore:"The equation that governs every flowing fluid — air around a wing, blood in an artery, ocean currents around a continent.",
   why:"One of the seven Millennium Prize problems. Whether smooth solutions always exist in 3D is unproven; a million-dollar question for 200 years and counting."},
  {code:'FIBO', name:'Fibonacci Spiral',        eq:'Fₙ = Fₙ₋₁ + Fₙ₋₂',                        who:'Leonardo of Pisa', yr:1202, kind:'sequence',
   lore:"Each term is the sum of the previous two. Squares with Fibonacci side lengths tile a golden spiral. The ratio Fₙ/Fₙ₋₁ converges to φ.",
   why:"Found in sunflower seeds, pinecone spirals, nautilus shells, hurricane arms. Nature's preferred packing strategy, written in a 13th-century rabbit puzzle."},
  {code:'WAVE', name:'Wave Equation',           eq:'∂²u/∂t² = c²·∇²u',                        who:"d'Alembert",      yr:1747, kind:'physics',
   lore:"A second-order PDE that describes anything propagating at speed c — sound, light, water ripples, vibrating strings, gravitational waves.",
   why:"Solving the wave equation taught humanity Fourier analysis, and through it, every signal-processing technique we have today."},
  {code:'PYTH', name:'Pythagorean Theorem',     eq:'a² + b² = c²',                            who:'Pythagoras',      yr:-530, kind:'theorem',
   lore:"In any right triangle, the square on the hypotenuse equals the sum of the squares on the other two sides. 2,500 years old. Still true.",
   why:"The first formula most humans ever learn. It seeded geometry, irrational numbers, and the Euclidean distance metric used everywhere from GPS to ML."},
  {code:'SPIR', name:'Spirograph',              eq:'x = (R−r)cos(t) + d·cos((R−r)t/r)',       who:'D. Cohen',        yr:1965, kind:'curve',
   lore:"A point on a small circle rolling inside a larger one — hypotrochoid. Tweak the radii and you tile the plane with rosettes, stars, knots.",
   why:"The toy taught a generation what parametric curves felt like. Same math powers gear design, planetary orbits, and the engine of every wankel rotary."},
  {code:'GAUS', name:'Gaussian Distribution',   eq:'f(x) = e^(−(x−μ)²/2σ²) / σ√(2π)',         who:'C.F. Gauss',      yr:1809, kind:'statistics',
   lore:"The bell curve. The shape that errors fall into when you average enough independent measurements. The Central Limit Theorem made tangible.",
   why:"Underpins statistics, signal processing, machine learning, finance, and quantum mechanics. The normal distribution is anything but normal — it's foundational."},
  {code:'LGST', name:'Logistic Map',            eq:'xₙ₊₁ = r·xₙ(1−xₙ)',                       who:'P. Verhulst',     yr:1838, kind:'chaos',
   lore:"A toy population model. Sweep the parameter r from 0 to 4 and watch fixed points split into 2-cycles, 4-cycles, then chaos — the famous bifurcation diagram.",
   why:"The simplest equation that exhibits the route to chaos via period doubling. Feigenbaum constants emerged here; chaos theory grew up around it."},
  {code:'FOUR', name:'Fourier Series',          eq:'f(x) = Σ aₙ·cos(nx) + bₙ·sin(nx)',        who:'J. Fourier',      yr:1807, kind:'series',
   lore:"Any periodic function can be written as a sum of sines and cosines. Decomposing complexity into pure tones — that's the entire idea.",
   why:"Powers MP3, JPEG, MRI, radar, voice recognition, and quantum mechanics. Every modern signal we encode passes through Fourier's lens."},
  {code:'ROSE', name:'Rose Curve',              eq:'r = a·cos(kθ)',                           who:'G. Grandi',       yr:1728, kind:'curve',
   lore:"A polar plot that draws petals. Integer k gives k petals (odd) or 2k petals (even). Rational k gives exotic stars. Irrational k never closes.",
   why:"A textbook case of how a single integer can completely change a curve's symmetry. Antenna engineers still use rose patterns to model directional gain."},
  {code:'SCHR', name:'Schrödinger Equation',    eq:'iℏ·∂ψ/∂t = Ĥψ',                           who:'E. Schrödinger',  yr:1926, kind:'physics',
   lore:"The wave function ψ evolves under the Hamiltonian operator. Linear, complex, deterministic — until you measure, and probability collapses out of it.",
   why:"The cornerstone of quantum mechanics. Every transistor on Earth — every phone, every GPU — works because someone solved this equation in the 1940s."},
  {code:'KOCH', name:'Koch Snowflake',          eq:'L = 3·(4/3)ⁿ',                            who:'H. von Koch',     yr:1904, kind:'fractal',
   lore:"Take a triangle. Replace the middle third of every edge with two edges of a smaller triangle. Repeat. The perimeter grows without bound while the area stays finite.",
   why:"The first published fractal with infinite length and finite area. It broke 19th-century intuitions about what 'length' even meant."},
  {code:'GRAV', name:"Newton's Gravitation",    eq:'F = G·m₁m₂/r²',                           who:'I. Newton',       yr:1687, kind:'physics',
   lore:"Two masses, a distance, and a constant. Apples fall, moons orbit, galaxies cluster — all from one inverse-square law that holds across 40 orders of magnitude.",
   why:"The first universal law. Newton's gravity was the prototype for every physical theory that followed, including the one Einstein wrote to replace it."},
];

// Build per-formula lookup of cards for variant strips
const ITEMS_BY_CODE = {};
ITEMS.forEach(it=>{
  if(!ITEMS_BY_CODE[it.code]) ITEMS_BY_CODE[it.code]=[];
  ITEMS_BY_CODE[it.code].push(it);
});

const cgrid = document.getElementById('constantsGrid');
CONSTANTS_INDEX.forEach(c=>{
  const el = document.createElement('div');
  el.className = 'const-card';
  el.dataset.code = c.code;
  const pool = ITEMS_BY_CODE[c.code] || [];
  // Pick 4 deterministic samples (palette diversity if possible)
  const samples = [];
  const seenP = new Set();
  for (const it of pool){
    if (samples.length>=4) break;
    if (!seenP.has(it.palette)){ seenP.add(it.palette); samples.push(it); }
  }
  while (samples.length<4 && samples.length<pool.length) samples.push(pool[samples.length]);
  const stripHtml = samples.length
    ? '<div class="const-strip">'+samples.map(s=>`<img src="data:image/jpeg;base64,${s.img}" alt="${c.code} variant" loading="lazy">`).join('')+'</div>'
    : '';
  el.innerHTML = `
    <div class="const-name">${c.name}</div>
    <div class="const-eq">${c.eq}</div>
    ${stripHtml}
    <div class="const-meta">
      <span>${c.who} · ${c.yr < 0 ? Math.abs(c.yr)+' BCE' : c.yr} · ${c.kind}</span>
      <span class="const-cta">read →</span>
    </div>
  `;
  el.addEventListener('click',()=>openFormulaModal(c));
  cgrid.appendChild(el);
});

// === Formula Deep-Dive Modal ===
const fmodalBg   = document.getElementById('fmodalBg');
const fmodalTag  = document.getElementById('fmodalTag');
const fmodalName = document.getElementById('fmodalName');
const fmodalEq   = document.getElementById('fmodalEq');
const fmodalMeta = document.getElementById('fmodalMeta');
const fmodalLore = document.getElementById('fmodalLore');
const fmodalWhy  = document.getElementById('fmodalWhy');
const fmodalStats= document.getElementById('fmodalStats');
const fmodalVars = document.getElementById('fmodalVariants');
const fmodalGo   = document.getElementById('fmodalGoGallery');
let fmodalCurrentCode = null;

function openFormulaModal(c){
  fmodalCurrentCode = c.code;
  fmodalTag.textContent = `CONSTANT · ${c.code}`;
  fmodalName.textContent = c.name;
  fmodalEq.textContent = c.eq;
  fmodalMeta.innerHTML = `
    <span>${c.who}</span>
    <span>${c.yr < 0 ? Math.abs(c.yr)+' BCE' : c.yr+' CE'}</span>
    <span>${c.kind}</span>
  `;
  fmodalLore.textContent = c.lore;
  fmodalWhy.textContent  = c.why;

  const pool = ITEMS_BY_CODE[c.code] || [];
  const palettes = new Set(pool.map(p=>p.palette));
  fmodalStats.innerHTML = `
    <div class="fst"><div class="fst-v">${pool.length}</div><div class="fst-l">cards</div></div>
    <div class="fst"><div class="fst-v">${palettes.size}</div><div class="fst-l">palettes</div></div>
    <div class="fst"><div class="fst-v">${c.code}</div><div class="fst-l">code</div></div>
  `;

  // Build variant grid: spread across palettes, up to 12
  const byPalette = {};
  pool.forEach(p=>{ if(!byPalette[p.palette]) byPalette[p.palette]=[]; byPalette[p.palette].push(p); });
  const picks = [];
  const palKeys = Object.keys(byPalette);
  let round = 0;
  while (picks.length < 12 && palKeys.some(k=>byPalette[k].length > round)){
    for (const k of palKeys){
      if (byPalette[k].length > round){
        picks.push(byPalette[k][round]);
        if (picks.length >= 12) break;
      }
    }
    round++;
  }
  fmodalVars.innerHTML = picks.map(p=>
    `<img src="data:image/jpeg;base64,${p.img}" alt="${c.code} #${p.id}" data-id="${p.id}" title="#${String(p.id).padStart(4,'0')} · ${p.palette}" loading="lazy">`
  ).join('');
  fmodalVars.querySelectorAll('img').forEach(img=>{
    img.addEventListener('click',()=>{
      const id = parseInt(img.dataset.id);
      const it = ITEMS.find(x=>x.id===id);
      if (it){ closeFormulaModal(); openModal(it); }
    });
  });

  fmodalBg.classList.add('open');
  document.body.style.overflow='hidden';
}
function closeFormulaModal(){
  fmodalBg.classList.remove('open');
  document.body.style.overflow='';
  fmodalCurrentCode = null;
}
document.getElementById('fmodalClose').addEventListener('click',closeFormulaModal);
fmodalBg.addEventListener('click',e=>{ if(e.target===fmodalBg) closeFormulaModal(); });
fmodalGo.addEventListener('click',()=>{
  if (!fmodalCurrentCode) return;
  state.formula = fmodalCurrentCode;
  state.shown = PAGE;
  fGroup.querySelectorAll('.chip').forEach(ch=>{
    ch.classList.toggle('active', ch.dataset.f === fmodalCurrentCode);
  });
  render();
  closeFormulaModal();
  document.getElementById('gallery').scrollIntoView({behavior:'smooth'});
});
window.addEventListener('keydown',e=>{
  if (e.key==='Escape' && fmodalBg.classList.contains('open')) closeFormulaModal();
});

// === Concept Primer (5 kinds) ===
const PRIMER = [
  {kind:'fractal',    glyph:'∞',  text:"Self-similar shapes that repeat detail at every scale. Zoom in, see the same structure again."},
  {kind:'attractor',  glyph:'∮',  text:"Bounded paths that a chaotic system traces forever — never settling, never escaping."},
  {kind:'curve',      glyph:'∿',  text:"Parametric or polar plots — sine, polar, polar-rose. Geometry written as a single line."},
  {kind:'physics',    glyph:'∂',  text:"Equations that govern reality — gravity, fluid flow, quantum waves. The universe's running source code."},
  {kind:'theorem',    glyph:'∑',  text:"Identities, theorems, sequences. The pure-math foundations everything else stands on."},
];
const KIND_MAP = {
  fractal:'fractal', chaos:'fractal',
  attractor:'attractor',
  curve:'curve', sequence:'curve', series:'curve',
  physics:'physics', identity:'physics',
  theorem:'theorem', statistics:'theorem',
};
const primerCounts = {};
CONSTANTS_INDEX.forEach(c=>{
  const k = KIND_MAP[c.kind] || c.kind;
  primerCounts[k] = (primerCounts[k]||0) + 1;
});
const pgrid = document.getElementById('primerGrid');
PRIMER.forEach(p=>{
  const el = document.createElement('div');
  el.className='primer-card';
  el.innerHTML = `
    <div style="display:flex;align-items:baseline;gap:10px">
      <span class="primer-glyph">${p.glyph}</span>
      <span class="primer-name">${p.kind}</span>
    </div>
    <p class="primer-text">${p.text}</p>
    <div class="primer-count">${primerCounts[p.kind]||0} constants</div>
  `;
  pgrid.appendChild(el);
});

// === Timeline (21 constants over time) ===
(function timeline(){
  const track = document.getElementById('timelineTrack');
  const scroll = document.getElementById('timelineScroll');
  const sorted = CONSTANTS_INDEX.slice().sort((a,b)=>a.yr-b.yr);
  const minYr = sorted[0].yr;
  const maxYr = sorted[sorted.length-1].yr;
  const span = maxYr - minYr;

  // Era markers (BCE / CE start / 1900)
  const eras = [
    {yr: minYr,  label:`${Math.abs(minYr)} BCE`, side:'left'},
    {yr: 1,      label:'CE 1', side:'mid'},
    {yr: 1700,   label:'1700', side:'mid'},
    {yr: 1900,   label:'1900', side:'mid'},
    {yr: maxYr,  label:`${maxYr}`, side:'right'},
  ];

  function pct(yr){
    return ((yr - minYr) / span) * 100;
  }

  eras.forEach(e=>{
    if (e.yr < minYr || e.yr > maxYr) return;
    const el = document.createElement('div');
    el.className='timeline-era';
    if (e.side==='left'){ el.style.left='0'; }
    else if (e.side==='right'){ el.style.right='0'; }
    else { el.style.left = pct(e.yr) + '%'; el.style.transform = 'translate(-50%,-50%)'; }
    el.textContent = e.label;
    track.appendChild(el);
  });

  // Place nodes; alternate label position to reduce overlap
  let lastPct = -10;
  sorted.forEach((c,i)=>{
    const p = pct(c.yr);
    const node = document.createElement('div');
    node.className = 'tl-node' + (i%2===1 ? ' alt' : '');
    node.style.left = p + '%';
    const yrLabel = c.yr < 0 ? Math.abs(c.yr)+' BCE' : c.yr;
    node.innerHTML = `
      <div class="tl-dot"></div>
      <div class="tl-label">${c.code}</div>
      <div class="tl-year">${yrLabel}</div>
    `;
    node.title = `${c.name} · ${yrLabel}`;
    node.addEventListener('click',()=>openFormulaModal(c));
    track.appendChild(node);
    lastPct = p;
  });
})();

// === Provenance verifier ===
(function verifier(){
  const inp = document.getElementById('verifierInput');
  const btn = document.getElementById('verifierBtn');
  const loadBtn = document.getElementById('verifierLoad');
  const out = document.getElementById('verifierResult');
  const expected = (document.querySelector('.prov-val.hash')?.textContent || '').trim();

  async function sha256Hex(str){
    const buf = new TextEncoder().encode(str);
    const dig = await crypto.subtle.digest('SHA-256', buf);
    return Array.from(new Uint8Array(dig)).map(b=>b.toString(16).padStart(2,'0')).join('');
  }
  function setResult(cls, txt){
    out.className = 'verifier-result ' + (cls||'');
    out.textContent = txt;
  }
  btn.addEventListener('click', async ()=>{
    const raw = inp.value.trim();
    if (!raw){ setResult('bad', 'paste a JSON array of signatures first'); return; }
    let arr;
    try { arr = JSON.parse(raw); } catch(e){ setResult('bad', 'not valid JSON: '+e.message); return; }
    if (!Array.isArray(arr) || !arr.every(x=>typeof x==='string')){
      setResult('bad', 'expected a JSON array of strings'); return;
    }
    setResult('busy', `hashing ${arr.length} signatures…`);
    try {
      const hash = await sha256Hex(arr.join(''));
      if (arr.length===333 && expected && hash.toLowerCase()===expected.toLowerCase()){
        setResult('ok', `✓ MATCH · ${hash}`);
      } else if (arr.length===333){
        setResult('bad', `✗ MISMATCH · got ${hash}`);
      } else {
        setResult('busy', `(${arr.length}/333) sha256 = ${hash}`);
      }
    } catch(e){ setResult('bad', 'hashing failed: '+e.message); }
  });
  loadBtn.addEventListener('click',()=>{
    const sigs = ITEMS.slice().sort((a,b)=>a.id-b.id).map(it=>it.sig);
    inp.value = JSON.stringify(sigs);
    setResult('busy', `loaded ${sigs.length} signatures from gallery · click Compute hash`);
  });
})();

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

// === Countdown ===
// Set CONSTANTS_LAUNCH to a future ISO timestamp to start the countdown.
// Leave null and "TBA" copy stays visible.
const CONSTANTS_LAUNCH = null; // e.g. '2026-06-21T18:00:00Z'

(function countdown(){
  const target = CONSTANTS_LAUNCH ? new Date(CONSTANTS_LAUNCH) : null;
  const elD = document.getElementById('cdD');
  const elH = document.getElementById('cdH');
  const elM = document.getElementById('cdM');
  const elS = document.getElementById('cdS');
  const elT = document.getElementById('cdTarget');
  const pad = n => String(Math.max(0,n)).padStart(2,'0');

  if (!target || isNaN(target.getTime())){
    // Keep dashes, show "TBA · follow @ConstantsNft"
    elT.innerHTML = '<b>TBA · follow @ConstantsNft</b>';
    return;
  }

  // Format target in user's locale
  try {
    elT.innerHTML = 'Genesis · target window · <b>' +
      target.toLocaleString(undefined,{
        year:'numeric',month:'short',day:'2-digit',
        hour:'2-digit',minute:'2-digit',timeZoneName:'short'
      }) + '</b>';
  } catch(e){}

  function tick(){
    const diff = target - new Date();
    if (diff <= 0){
      elD.textContent='00';elH.textContent='00';
      elM.textContent='00';elS.textContent='00';
      elT.innerHTML = '<b style="color:var(--accent)">live · check the contract</b>';
      return;
    }
    const d = Math.floor(diff / 86400000);
    const h = Math.floor((diff % 86400000) / 3600000);
    const m = Math.floor((diff % 3600000) / 60000);
    const s = Math.floor((diff % 60000) / 1000);
    elD.textContent = pad(d);
    elH.textContent = pad(h);
    elM.textContent = pad(m);
    elS.textContent = pad(s);
  }
  tick();
  setInterval(tick, 1000);
})();

// === Console signature + easter eggs ===
(function easter(){
  const ascii = `
   ╱╱  CONSTANTS · GENESIS 333
   ╱╱  ──────────────────────────
   ╱╱  e^(iπ) + 1 = 0
   ╱╱  21 formulas · 10 palettes · 5 tiers
   ╱╱  signed · anonymous
   ╱╱  https://x.com/ConstantsNft
`;
  try {
    console.log('%c'+ascii,
      'color:#a8ff60;font-family:monospace;font-size:11px;line-height:1.4');
    console.log('%cwhisper a constant to summon it · try: pi · phi · e · lorenz · mandelbrot · fibonacci',
      'color:#60d4ff;font-family:monospace;font-size:10px;font-style:italic');
  } catch(e){}

  // Keystroke easter egg: type a keyword anywhere on the page
  const SUMMONS = {
    'pi':         ['EULR'],
    'phi':        ['FIBO'],
    'e':          ['EULR'],
    'lorenz':     ['LRNZ'],
    'butterfly':  ['LRNZ'],
    'mandelbrot': ['MAND'],
    'julia':      ['JULA'],
    'fibonacci':  ['FIBO'],
    'golden':     ['FIBO'],
    'sierpinski': ['SIER'],
    'fern':       ['FERN'],
    'newton':     ['GRAV'],
    'gravity':    ['GRAV'],
    'wave':       ['WAVE'],
    'fourier':    ['FOUR'],
    'rose':       ['ROSE'],
    'koch':       ['KOCH'],
    'snow':       ['KOCH'],
    'quantum':    ['SCHR'],
    'schrodinger':['SCHR'],
    'gauss':      ['GAUS'],
    'bell':       ['GAUS'],
    'logistic':   ['LGST'],
    'chaos':      ['LRNZ','LGST'],
    'pythagoras': ['PYTH'],
    'spiro':      ['SPIR'],
    'spirograph': ['SPIR'],
    'lissajous':  ['LISS'],
    'navier':     ['NAVI'],
    'flow':       ['NAVI'],
    'clifford':   ['CLIF'],
    'heart':      ['HART'],
  };
  const longest = Math.max(...Object.keys(SUMMONS).map(k=>k.length));
  let buf = '';
  let timer = null;

  function summon(codes){
    const code = codes[Math.floor(Math.random()*codes.length)];
    const pool = ITEMS_BY_CODE[code] || [];
    if (!pool.length) return false;
    const pick = pool[Math.floor(Math.random()*pool.length)];
    // If a modal is open, close first
    if (fmodalBg.classList.contains('open')) closeFormulaModal();
    if (modalBg.classList.contains('open')) closeModal();
    setTimeout(()=>openModal(pick), 50);
    try {
      console.log(`%c◆ summoned ${code} · #${String(pick.id).padStart(4,'0')}`,
        'color:#ffcc66;font-family:monospace;font-size:11px');
    } catch(e){}
    return true;
  }

  document.addEventListener('keydown', e=>{
    // Ignore if user is typing in an input/textarea
    const tag = (e.target && e.target.tagName) || '';
    if (tag === 'INPUT' || tag === 'TEXTAREA') return;
    if (e.metaKey || e.ctrlKey || e.altKey) return;

    const ch = e.key;
    if (ch && ch.length === 1 && /[a-zA-Z]/.test(ch)){
      buf = (buf + ch.toLowerCase()).slice(-longest);
      clearTimeout(timer);
      timer = setTimeout(()=>{ buf=''; }, 1500);
      // Match longest suffix
      for (let len = Math.min(longest, buf.length); len >= 2; len--){
        const tail = buf.slice(-len);
        if (SUMMONS[tail]){
          if (summon(SUMMONS[tail])){ buf=''; clearTimeout(timer); }
          return;
        }
      }
    }
  });
})();
</script>

</body>
</html>
'''

html = html.replace('__ITEMS_JSON__', items_json)
html = html.replace('__PROVENANCE_HASH__', provenance_hash)

out = '/home/ubuntu/formula-nft-web/index.html'
with open(out, 'w') as f:
    f.write(html)

print(f'wrote {out}')
print(f'size: {os.path.getsize(out)/1048576:.2f}MB')
