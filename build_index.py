import os
import json
import re

# Read original backup
with open('index.html.backup', 'r', encoding='utf-8') as f:
    orig = f.read()

# Extract LOGO
logo_match = re.search(r'var LOGO\s*=\s*(\{[\s\S]*?\});', orig)
logo_str = logo_match.group(0) if logo_match else 'var LOGO={};'

# Build clean works list
def clean_title(name, cat):
    base = os.path.splitext(name)[0]
    t = base.replace('-&-', ' & ').replace('-01', ' 1').replace('-02', ' 2')
    t = t.replace('=', ' - ').replace('_', ' ').replace('-', ' ')
    t = ' '.join(t.split())
    words = []
    for w in t.split():
        if w.lower() in ['&', 'x']:
            words.append(w.lower() if w.lower() == 'x' else '&')
        elif w.upper() in ['CARD', 'TRALOR', 'TAILOR', 'CM']:
            if w.upper() == 'TRALOR':
                words.append('Tailor')
            else:
                words.append(w.capitalize())
        else:
            words.append(w.capitalize())
    return ' '.join(words)

works = []
for cat_name, folder in [('Ladies Tailor', 'Ladies Tailor'), ('Patrika', 'Patrika')]:
    for f in sorted(os.listdir(folder)):
        if not f.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue
        title = clean_title(f, cat_name)
        img_url = f'{folder}/{f}'
        thumb_url = f'thumbnails/{folder}/{f}'
        desc = f'Lagna Patrika / Wedding Card design ({title})' if cat_name == 'Patrika' else f'Ladies Tailor Shop Banner & Board design ({title})'
        works.append({
            't': title,
            'cat': cat_name,
            'price': '₹200',
            'd': desc,
            'img': img_url,
            'thumb': thumb_url
        })

works_json = json.dumps(works, ensure_ascii=False, indent=1)

# Extract CSS section from original
style_end = orig.find('</style>')
pre_style = orig[:style_end]

extra_css = """
.cats{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:28px}
.catcard{display:block;text-decoration:none;color:inherit;background:var(--card);border-radius:14px;overflow:hidden;border:1px solid var(--line);transition:transform .3s,box-shadow .3s}
.catcard:hover{transform:translateY(-6px);box-shadow:0 18px 36px rgba(0,0,0,.12)}
.catcard .art{aspect-ratio:16/10;overflow:hidden;background:var(--card);position:relative}
.catcard .art img{width:100%;height:100%;object-fit:cover;object-position:center;transition:transform .4s}
.catcard:hover .art img{transform:scale(1.05)}
.catcard .body{padding:22px 24px 26px}
.catcard h3{font-size:30px;margin:0 0 6px}
.catcard p{color:var(--muted);font-size:15px;margin:10px 0 0;line-height:1.5}
.back{display:inline-flex;align-items:center;gap:8px;font-weight:700;text-decoration:none;margin-bottom:24px;color:var(--ink);padding:9px 22px;border-radius:999px;border:2px solid var(--line);background:var(--card);transition:all .2s;cursor:pointer}
.back:hover{background:var(--sun);color:#fff;border-color:var(--sun)}
.grid{columns:3 290px;column-gap:22px}
.tile{display:block;width:100%;margin-bottom:22px;break-inside:avoid;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px;text-align:left;color:inherit;cursor:pointer;font:inherit;transition:transform .25s,box-shadow .25s}
.tile:hover{transform:translateY(-4px);box-shadow:0 12px 28px rgba(0,0,0,.09)}
.tile .art{overflow:hidden;border-radius:8px;background:var(--bg);position:relative}
.tile .art img{width:100%;height:auto;display:block;transition:transform .35s}
.tile:hover .art img{transform:scale(1.04)}
.tile h3{font-size:20px;margin:12px 0 4px;font-weight:700}
.meta{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-top:6px}
.meta small{color:var(--muted);font-size:14px}
.pr{background:var(--sun);color:#fff;font:700 13px var(--body);padding:3px 12px;border-radius:999px;text-transform:uppercase}
dialog{border:0;padding:0;background:var(--card);color:var(--ink);border-radius:16px;width:min(960px,94vw);max-height:92vh;overflow:auto;box-shadow:0 24px 64px rgba(0,0,0,.45)}
dialog::backdrop{background:rgba(0,0,0,.85);backdrop-filter:blur(4px)}
.lb{display:grid;grid-template-columns:1fr;position:relative}
.lb .art{background:#0B0B0B;display:flex;align-items:center;justify-content:center;min-height:320px;max-height:72vh;overflow:hidden;position:relative}
.lb .art img{width:100%;height:auto;max-height:72vh;object-fit:contain}
.lb .txt{padding:26px 30px;display:flex;flex-direction:column;gap:10px;align-items:flex-start}
.lb h3{font-size:32px;margin:0}
.lb-actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:14px}
.lb-nav{position:absolute;top:50%;transform:translateY(-50%);background:rgba(0,0,0,.65);color:#fff;border:0;width:46px;height:46px;border-radius:50%;cursor:pointer;font-size:24px;display:flex;align-items:center;justify-content:center;transition:background .2s;z-index:5}
.lb-nav:hover{background:var(--sun)}
.lb-prev{left:14px}
.lb-next{right:14px}
.lb .x{position:absolute;top:14px;right:14px;width:40px;height:40px;border-radius:50%;border:0;background:var(--sun);color:#fff;font:700 18px var(--body);cursor:pointer;z-index:10;display:flex;align-items:center;justify-content:center}

/* --- Section: 3-Step Process --- */
.process{background:var(--card);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.steps-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:24px;margin-top:40px}
.step-card{background:var(--bg);border:1px solid var(--line);border-radius:12px;padding:32px 28px;position:relative;transition:transform .3s}
.step-card:hover{transform:translateY(-4px)}
.step-num{display:inline-block;font:700 32px var(--display);color:var(--sun);margin-bottom:12px;background:rgba(216,31,38,.08);padding:4px 14px;border-radius:8px}
.step-card h3{font-size:24px;margin:0 0 10px}
.step-card p{margin:0;color:var(--muted);font-size:15px;line-height:1.5}

/* --- Section: Printing Setup --- */
.printing{border-bottom:1px solid var(--line)}
.print-grid{display:grid;grid-template-columns:1.1fr 1fr;gap:clamp(30px,5vw,60px);align-items:center}
.print-media{position:relative;border-radius:14px;overflow:hidden;border:1px solid var(--line);box-shadow:0 16px 36px rgba(0,0,0,.08)}
.print-media img{width:100%;height:auto;display:block}
.print-badge{position:absolute;bottom:16px;left:16px;background:rgba(11,11,11,.85);backdrop-filter:blur(6px);color:#fff;padding:8px 18px;border-radius:999px;font:700 14px var(--body);border:1px solid rgba(255,255,255,.2);display:flex;align-items:center;gap:8px}
.print-badge::before{content:"";width:8px;height:8px;border-radius:50%;background:#25D366;display:inline-block}
.print-feats{list-style:none;padding:0;margin:28px 0 0;display:grid;grid-template-columns:1fr 1fr;gap:20px}
.print-feats li{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 20px}
.print-feats b{display:block;font:700 18px var(--display);color:var(--ink);margin-bottom:4px;text-transform:uppercase}
.print-feats p{margin:0;font-size:14px;color:var(--muted);line-height:1.4}
@media(max-width:860px){.print-grid{grid-template-columns:1fr}.print-feats{grid-template-columns:1fr}}

/* --- Section: Happy Clients / Instagram Video Reviews --- */
.reviews{background:var(--bg);border-bottom:1px solid var(--line)}
.reviews-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:32px;margin-top:40px}
.reel-card{background:var(--card);border:1px solid var(--line);border-radius:16px;overflow:hidden;box-shadow:0 12px 28px rgba(0,0,0,.06);transition:transform .3s,box-shadow .3s}
.reel-card:hover{transform:translateY(-6px);box-shadow:0 20px 40px rgba(0,0,0,.12)}
.reel-art{aspect-ratio:9/14;overflow:hidden;position:relative;background:#000}
.reel-art img{width:100%;height:100%;object-fit:cover;transition:transform .4s}
.reel-card:hover .reel-art img{transform:scale(1.03)}
.reel-badge{position:absolute;top:16px;left:16px;background:linear-gradient(45deg,#f09433 0%,#e6683c 25%,#dc2743 50%,#cc2366 75%,#bc1888 100%);color:#fff;font:700 12px var(--body);padding:5px 14px;border-radius:999px;letter-spacing:.04em;text-transform:uppercase;box-shadow:0 4px 12px rgba(0,0,0,.25)}
.reel-body{padding:22px 24px 26px}
.reel-rating{color:#FFB800;font-size:18px;margin-bottom:8px;display:flex;align-items:center;gap:4px}
.reel-client{font-weight:700;font-size:18px;margin:0 0 2px;color:var(--ink)}
.reel-loc{font-size:13px;color:var(--muted);margin-bottom:10px}
.reel-quote{font-size:15px;color:var(--ink);line-height:1.5;margin:0 0 16px;font-style:italic}
.reel-actions{display:flex;gap:10px;align-items:center}
.btn-insta{display:inline-flex;align-items:center;gap:6px;background:transparent;border:2px solid #E1306C;color:#E1306C;font:700 13px var(--body);padding:8px 16px;border-radius:999px;text-decoration:none;transition:all .2s}
.btn-insta:hover{background:#E1306C;color:#fff}
"""

new_html = f"""{pre_style}{extra_css}</style>
</head>
<body>
<header class="nav"><div class="wrap">
  <a class="logo" href="#top" aria-label="Sangharsh Graphic home"><img class="lm" data-logo="mark" alt=""><img class="lw" data-logo="word" alt="Sangharsh Graphic"></a>
  <nav aria-label="Main"><ul>
    <li><a href="#work">Categories</a></li>
    <li><a href="#process">How to Order</a></li>
    <li><a href="#printing">Printing Setup</a></li>
    <li><a href="#reviews">Happy Clients</a></li>
    <li><a href="#services">Services</a></li>
    <li><a href="#about">About</a></li>
    <li><a href="#contact">Contact</a></li>
  </ul></nav>
  <a class="navcall" href="tel:+917875685832">Call 78756 85832</a>
</div></header>

<main id="top">
<div class="hero"><div class="wrap hgrid">
  <div class="htxt">
    <p class="kicker">Graphic design &amp; printing studio · Malegaon Camp, Nashik</p>
    <h1>Wedding invitations, shop banners &amp; logos</h1>
    <p class="lead">Send us your details and photos. We design it in Marathi or English and give you a print-ready file or printed delivery.</p>
    <div class="cta"><a class="btn" href="tel:+917875685832">Call 78756 85832</a><a class="btn ghost" href="https://wa.me/917875685832?text=Hello%20Sangharsh%20Graphics" target="_blank" rel="noopener">Chat on WhatsApp</a></div>
    <ul class="facts"><li><b>From ₹200</b>per design</li><li><b>Marathi + English</b>cards and banners</li><li><b>Print-ready</b>flex &amp; offset press files</li></ul>
  </div>
  <div class="hshow" id="hshow"></div>
</div></div>

<!-- 1. Work by Category -->
<section id="work"><div class="wrap">
  <div class="head">
    <div>
      <h2>Work by Category</h2>
      <p style="margin:8px 0 0;color:var(--muted);font-size:17px">Select a category below to explore all showcase designs</p>
    </div>
  </div>
  <div class="cats" id="cats"></div>
</div></section>

<!-- Category Detail View (Dynamic Gallery) -->
<section id="catview" hidden><div class="wrap">
  <a class="back" href="#work">← Back to All Categories</a>
  <div class="head">
    <div>
      <h2 id="cvTitle"></h2>
      <p id="cvNote" style="margin:8px 0 0;color:var(--muted);font-size:18px"></p>
    </div>
    <b class="pr" id="cvCount" style="font-size:15px;padding:6px 16px"></b>
  </div>
  <div class="grid" id="grid"></div>
</div></section>

<!-- 2. How to Order: 3 Simple Steps -->
<section class="process" id="process"><div class="wrap">
  <div class="head">
    <div>
      <p class="kicker">Fast &amp; hassle-free ordering</p>
      <h2>How It Works in 3 Easy Steps</h2>
      <p style="margin:8px 0 0;color:var(--muted);font-size:17px">सोपी ३-स्टेप ऑर्डर पद्धत — WhatsApp वरून थेट डिझाईन मिळवा</p>
    </div>
  </div>
  <div class="steps-grid">
    <div class="step-card">
      <span class="step-num">01</span>
      <h3>Send Photos &amp; Details</h3>
      <p>Send your shop name, banner size, or bride/groom details with photos directly to <b>+91 78756 85832</b> on WhatsApp.</p>
    </div>
    <div class="step-card">
      <span class="step-num">02</span>
      <h3>Review Proof &amp; Changes</h3>
      <p>We send you a sharp preview in Marathi or English within 2–4 hours. Check spelling, fonts, and request changes freely.</p>
    </div>
    <div class="step-card">
      <span class="step-num">03</span>
      <h3>Print-Ready File &amp; Delivery</h3>
      <p>Receive your press-ready high-resolution CMYK file or pick up your finished printed flex banner from our Malegaon Camp studio.</p>
    </div>
  </div>
  <div style="margin-top:34px;text-align:center">
    <a class="btn" href="https://wa.me/917875685832?text=Hello%20Ajay,%20I%20want%20to%20order%20a%20design" target="_blank" rel="noopener">Start Your Order on WhatsApp</a>
  </div>
</div></section>

<!-- 3. Printing Machine & In-House Quality Setup -->
<section class="printing" id="printing"><div class="wrap">
  <div class="print-grid">
    <div class="print-media">
      <img src="assets/printing_machine.jpg" alt="Large Format Digital Flex Printing Machine at Sangharsh Graphics" loading="lazy">
      <div class="print-badge">SpeedPrint Industrial Digital Flex Press</div>
    </div>
    <div>
      <p class="kicker">In-house printing infrastructure</p>
      <h2>Heavy-Duty Flex &amp; Sharp Card Printing</h2>
      <p class="lead" style="margin:16px 0 20px">We don’t just create digital artwork — we ensure your shop banner has rich, eye-catching colors and withstands harsh weather for years.</p>
      
      <ul class="print-feats">
        <li>
          <b>Sun &amp; Weatherproof</b>
          <p>High-density solvent inks that do not fade in scorching heat or heavy rain.</p>
        </li>
        <li>
          <b>Star Flex Media</b>
          <p>Tear-resistant heavy-duty media tailored for shop signboards &amp; gate banners.</p>
        </li>
        <li>
          <b>Exact Frame Sizing</b>
          <p>Pre-measured with eyelets and border margins for quick iron frame mounting.</p>
        </li>
        <li>
          <b>Same-Day Express</b>
          <p>Urgent flex printing and WhatsApp digital invitation cards within hours.</p>
        </li>
      </ul>
      <div style="margin-top:28px">
        <a class="btn" href="tel:+917875685832">Call for Printing Rates</a>
      </div>
    </div>
  </div>
</div></section>

<!-- 4. Happy Clients & Instagram Video Reviews -->
<section class="reviews" id="reviews"><div class="wrap">
  <div class="head">
    <div>
      <p class="kicker">Real client stories</p>
      <h2>Happy Clients &amp; Instagram Reviews</h2>
      <p style="margin:8px 0 0;color:var(--muted);font-size:17px">आमचे समाधानी ग्राहक — Trusted by 500+ shop owners &amp; families in Malegaon, Nashik &amp; Dhule</p>
    </div>
    <a class="btn-insta" href="https://instagram.com" target="_blank" rel="noopener">Follow on Instagram ★</a>
  </div>

  <div class="reviews-grid">
    <!-- Reel Review 1: Tailor Shop -->
    <div class="reel-card">
      <div class="reel-art">
        <img src="assets/reel_tailor_review.jpg" alt="Instagram Video Review - Suresh Ladies Boutique Banner" loading="lazy">
        <span class="reel-badge">Instagram Reel</span>
      </div>
      <div class="reel-body">
        <div class="reel-rating">★★★★★ <span>5.0</span></div>
        <h4 class="reel-client">Suresh Ladies Boutique</h4>
        <div class="reel-loc">Malegaon Camp, Nashik</div>
        <p class="reel-quote">“The banner design for my boutique is super attractive! Vibrant colors, perfect Marathi font and great printing quality. Footfall increased immediately. Ajay is the best!”</p>
        <div class="reel-actions">
          <a class="btn-insta" href="https://wa.me/917875685832?text=Hello%20Ajay,%20I%20saw%20the%20Ladies%20Tailor%20banner%20review" target="_blank" rel="noopener">Inquire Like This</a>
        </div>
      </div>
    </div>

    <!-- Reel Review 2: Wedding Invitation Card -->
    <div class="reel-card">
      <div class="reel-art">
        <img src="assets/reel_patrika_review.jpg" alt="Instagram Video Review - Sneha and Rahul Wedding Card" loading="lazy">
        <span class="reel-badge">Instagram Reel</span>
      </div>
      <div class="reel-body">
        <div class="reel-rating">★★★★★ <span>5.0</span></div>
        <h4 class="reel-client">Sneha &amp; Rahul</h4>
        <div class="reel-loc">Nashik (Lagna Patrika)</div>
        <p class="reel-quote">“We got our Marathi Lagna Patrika designed here. The Ganesh motif, family details, and paper finish were so elegant. All our relatives appreciated the card!”</p>
        <div class="reel-actions">
          <a class="btn-insta" href="https://wa.me/917875685832?text=Hello%20Ajay,%20I%20saw%20the%20Lagna%20Patrika%20card%20review" target="_blank" rel="noopener">Inquire Like This</a>
        </div>
      </div>
    </div>
  </div>
</div></section>

<!-- 5. What I Design (Services) -->
<section class="services" id="services"><div class="wrap">
  <div class="head"><h2>What I design</h2></div>
  <div class="svc">
    <div><h3>Wedding invitations</h3><p>Marathi and English cards for print and WhatsApp, with photos, family details and venue.</p></div>
    <div><h3>Shop banners &amp; boards</h3><p>Shop signs, gate banners and sale posters, sized and ready for the flex press.</p></div>
    <div><h3>Logo &amp; branding</h3><p>A logo and look that work on a signboard and a phone screen alike.</p></div>
    <div><h3>Social media</h3><p>Post and story designs for offers, festivals and launches.</p></div>
  </div>
</div></section>

<!-- 6. About Section -->
<section class="about" id="about"><div class="wrap">
  <div><img class="abmark" data-logo="mark" alt="Sangharsh Graphic logo"><h2>Design with some fight in it</h2></div>
  <div>
    <p>“Sangharsh” means struggle, and every shop and every family event wants to be noticed. Sangharsh Graphics is a design studio in Malegaon Camp, Nashik, run by Ajay Shewale.</p>
    <p>You deal directly with Ajay, not a middleman. Bring your photos and details, and you get a clear design in Marathi or English, ready to print or share on WhatsApp.</p>
  </div>
</div></section>

<!-- 7. Contact Section -->
<section class="contact" id="contact"><div class="wrap">
  <div>
    <h2>Need a design? Call now.</h2>
    <a class="big" href="tel:+917875685832">+91 78756 85832</a>
    <div class="cta"><a class="btn" href="tel:+917875685832">Call Ajay</a><a class="btn" href="https://wa.me/917875685832?text=Hello%20Sangharsh%20Graphics" target="_blank" rel="noopener">Chat on WhatsApp</a></div>
    <address>Ajay Shewale<br>Jahagirdar Plaza, Shop No. 2, near Malegaon Generic Medical, below Moka Moment Café, Malegaon Camp (Nashik)</address>
  </div>
  <form id="form">
    <label>Your name<input name="n" required autocomplete="name"></label>
    <label>What do you need designed?<textarea name="m" rows="4" required placeholder="Wedding invitation, shop banner, logo…"></textarea></label>
    <button class="btn" type="submit">Send on WhatsApp</button>
    <p id="note" role="status"></p>
  </form>
</div></section>
</main>

<footer><div class="wrap"><span class="flogo"><img class="fl" data-logo="mark" alt=""><span>© 2026 Sangharsh Graphic</span></span><span>Malegaon Camp, Nashik · +91 78756 85832</span></div></footer>

<a class="float" href="https://wa.me/917875685832?text=Hello%20Sangharsh%20Graphics" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">WhatsApp</a>

<dialog id="dlg" aria-label="Project details">
  <button class="x" id="close" aria-label="Close">✕</button>
  <div class="lb">
    <button class="lb-nav lb-prev" id="lbPrev" aria-label="Previous image">‹</button>
    <div class="art" id="lbArt"></div>
    <button class="lb-nav lb-next" id="lbNext" aria-label="Next image">›</button>
    <div class="txt">
      <small id="lbCat" style="color:var(--muted);font-weight:700;text-transform:uppercase;letter-spacing:.05em"></small>
      <h3 id="lbTitle"></h3>
      <b class="pr" id="lbPrice"></b>
      <p id="lbDesc"></p>
      <div class="lb-actions">
        <a class="btn" id="lbWaBtn" href="" target="_blank" rel="noopener">Order on WhatsApp</a>
        <a class="btn ghost" href="tel:+917875685832">Call Ajay</a>
      </div>
    </div>
  </div>
</dialog>

<script>
var WORKS = {works_json};

var CATS = [
  {{
    k: 'ladies-tailor',
    cat: 'Ladies Tailor',
    name: 'Ladies Tailor',
    sub: 'Shop Banners & Boards',
    note: 'Custom banners, flex boards and shop signage designed for ladies tailors and boutiques.',
    cover: 'Ladies Tailor/4 X 2 -Osaka.jpg',
    thumbCover: 'thumbnails/Ladies Tailor/4 X 2 -Osaka.jpg'
  }},
  {{
    k: 'patrika',
    cat: 'Patrika',
    name: 'Lagna Patrika',
    sub: 'Wedding & Invitation Cards',
    note: 'Traditional & modern wedding invitations, Mandav patrika and Mehandi cards in Marathi & English.',
    cover: 'Patrika/Mandav-Patrika.jpg',
    thumbCover: 'thumbnails/Patrika/Mandav-Patrika.jpg'
  }}
];

function media(w, useThumb){{
  var s = (useThumb && w.thumb) ? w.thumb : w.img;
  return '<img src="' + encodeURI(s) + '" alt="' + w.t + '" loading="lazy" onerror="this.onerror=null;this.src=\\'' + encodeURI(w.img) + '\\';">';
}}

var grid = document.getElementById('grid');
var dlg = document.getElementById('dlg');
var currentFilteredWorks = [];
var currentModalIndex = 0;

function render(cat){{
  grid.innerHTML = '';
  currentFilteredWorks = WORKS.filter(function(w){{
    return w.cat === cat;
  }});

  currentFilteredWorks.forEach(function(w, idx){{
    var b = document.createElement('button');
    b.className = 'tile';
    b.setAttribute('aria-label', 'Open ' + w.t);
    b.innerHTML = '<div class="art">' + media(w, true) + '</div>' +
                  '<h3>' + w.t + '</h3>' +
                  '<div class="meta"><small>' + w.cat + '</small><b class="pr">' + w.price + '</b></div>';
    b.onclick = function(){{ openModal(idx); }};
    grid.appendChild(b);
  }});
}}

var cg = document.getElementById('cats');
var cv = document.getElementById('catview');

CATS.forEach(function(c){{
  var list = WORKS.filter(function(w){{ return w.cat === c.cat; }});
  var card = document.createElement('a');
  card.className = 'catcard';
  card.href = '#' + c.k;
  
  var coverWork = {{
    t: c.name,
    img: c.cover,
    thumb: c.thumbCover
  }};

  card.innerHTML = '<div class="art">' + media(coverWork, true) + '</div>' +
                   '<div class="body">' +
                     '<div class="meta"><h3>' + c.name + '</h3><b class="pr">' + list.length + ' Designs</b></div>' +
                     '<p>' + c.note + '</p>' +
                   '</div>';
  cg.appendChild(card);
}});

var HOME_SECTIONS = ['work', 'process', 'printing', 'reviews', 'services', 'about'];

function route(){{
  var h = location.hash.slice(1);
  var c = CATS.filter(function(x){{ return x.k === h; }})[0];
  var isCategoryView = !!c;

  HOME_SECTIONS.forEach(function(id){{
    var el = document.getElementById(id);
    if(el) el.hidden = isCategoryView;
  }});
  
  var heroEl = document.querySelector('.hero');
  if(heroEl) heroEl.hidden = isCategoryView;
  
  cv.hidden = !isCategoryView;

  if(c){{
    document.getElementById('cvTitle').textContent = c.name;
    document.getElementById('cvNote').textContent = c.note;
    document.getElementById('cvCount').textContent = listCount(c.cat) + ' Designs';
    render(c.cat);
    window.scrollTo({{top: 0, behavior: 'smooth'}});
  }} else {{
    if(h && h !== 'work'){{
      var target = document.getElementById(h);
      if(target) target.scrollIntoView({{behavior: 'smooth'}});
    }} else {{
      window.scrollTo({{top: 0, behavior: 'smooth'}});
    }}
  }}
}}

function listCount(cat){{
  return WORKS.filter(function(w){{ return w.cat === cat; }}).length;
}}

window.addEventListener('hashchange', route);

function openModal(idx){{
  currentModalIndex = idx;
  var w = currentFilteredWorks[idx];
  if(!w) return;

  document.getElementById('lbArt').innerHTML = media(w, false);
  document.getElementById('lbCat').textContent = w.cat;
  document.getElementById('lbTitle').textContent = w.t;
  document.getElementById('lbPrice').textContent = 'Starting at ' + w.price;
  document.getElementById('lbDesc').textContent = w.d;

  var waMsg = 'Hello Ajay, I am interested in this design: ' + w.t + ' (' + w.cat + ').';
  document.getElementById('lbWaBtn').href = 'https://wa.me/917875685832?text=' + encodeURIComponent(waMsg);

  dlg.showModal();
}}

document.getElementById('lbPrev').onclick = function(e){{
  e.stopPropagation();
  if(currentFilteredWorks.length === 0) return;
  var newIdx = (currentModalIndex - 1 + currentFilteredWorks.length) % currentFilteredWorks.length;
  openModal(newIdx);
}};

document.getElementById('lbNext').onclick = function(e){{
  e.stopPropagation();
  if(currentFilteredWorks.length === 0) return;
  var newIdx = (currentModalIndex + 1) % currentFilteredWorks.length;
  openModal(newIdx);
}};

document.addEventListener('keydown', function(e){{
  if(!dlg.open) return;
  if(e.key === 'ArrowLeft') document.getElementById('lbPrev').click();
  if(e.key === 'ArrowRight') document.getElementById('lbNext').click();
}});

document.getElementById('close').onclick = function(){{ dlg.close(); }};
dlg.addEventListener('click', function(e){{ if(e.target === dlg) dlg.close(); }});

document.getElementById('form').addEventListener('submit', function(e){{
  e.preventDefault();
  var f = e.target;
  var msg = 'Hello Sangharsh Graphics, I am ' + f.n.value + '.\\n' + f.m.value;
  window.open('https://wa.me/917875685832?text=' + encodeURIComponent(msg), '_blank');
  document.getElementById('note').textContent = 'Opening WhatsApp with your message.';
}});

{logo_str}
document.querySelectorAll('[data-logo]').forEach(function(i){{
  var key = i.getAttribute('data-logo');
  if(LOGO[key]) i.src = LOGO[key];
}});

// Hero featured items
var hs = document.getElementById('hshow');
var heroItems = [
  {{ t: 'Mandav Patrika', img: 'Patrika/Mandav-Patrika.jpg', thumb: 'thumbnails/Patrika/Mandav-Patrika.jpg', tag: 'Patrika', k: 'patrika', cls: 'hi h0' }},
  {{ t: 'Osaka Ladies Tailor', img: 'Ladies Tailor/4 X 2 -Osaka.jpg', thumb: 'thumbnails/Ladies Tailor/4 X 2 -Osaka.jpg', tag: 'Banner', k: 'ladies-tailor', cls: 'hi h1' }},
  {{ t: 'Ladies Tailor Flex', img: 'Ladies Tailor/3 X 4 -111.jpg', thumb: 'thumbnails/Ladies Tailor/3 X 4 -111.jpg', tag: 'Banner', k: 'ladies-tailor', cls: 'hi h2' }}
];

heroItems.forEach(function(item){{
  var a = document.createElement('a');
  a.className = item.cls;
  a.href = '#' + item.k;
  a.innerHTML = media(item, true) + '<span class="tag">' + item.tag + '</span>';
  hs.appendChild(a);
}});

route();
</script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print('Updated index.html successfully with all sections! Size:', len(new_html))
