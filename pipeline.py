#!/usr/bin/env python3
"""Niche Site Content Pipeline — Battery Backup Guide"""
import json, os, glob

CONTENT_DIR = os.path.expanduser("~/.hermes/content-toolkit/niche-site/content")
SITE_DIR = os.path.expanduser("~/.hermes/content-toolkit/niche-site")

CSS = """:root {
  --bg-base: #0a0e1a;
  --bg-card: rgba(255,255,255,0.04);
  --bg-card-hover: rgba(255,255,255,0.08);
  --glow-blue: #00d4ff;
  --glow-purple: #7c3aed;
  --glow-amber: #f59e0b;
  --glow-green: #10b981;
  --text: #f1f5f9;
  --text-secondary: #94a3b8;
  --text-muted: #64748b;
  --border: rgba(255,255,255,0.08);
  --shadow: 0 4px 20px rgba(0,0,0,0.3);
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: var(--bg-base); color: var(--text); line-height: 1.8;
  -webkit-font-smoothing: antialiased;
}
body::before {
  content: '';
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background:
    radial-gradient(ellipse at 20% 50%, rgba(0,212,255,0.06) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 20%, rgba(124,58,237,0.05) 0%, transparent 50%);
  pointer-events: none; z-index: 0;
}
.container { max-width: 860px; margin: 0 auto; padding: 0 24px; position: relative; z-index: 1; }
.skip-link { position: absolute; top: -40px; left: 0; background: var(--glow-blue); color: #000; padding: 8px 16px; z-index: 999; border-radius: 0 0 4px 0; font-weight: 600; font-size: 0.85rem; transition: top 0.2s; }
.skip-link:focus { top: 0; }
.progress-bar { position: fixed; top: 0; left: 0; width: 0; height: 3px; background: linear-gradient(90deg, var(--glow-blue), var(--glow-purple)); z-index: 1000; transition: width 0.1s; }
.nav { background: rgba(10,14,26,0.85); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border-bottom: 1px solid rgba(255,255,255,0.06); padding: 0; position: sticky; top: 0; z-index: 100; height: 56px; }
.nav .container { display: flex; gap: 28px; align-items: center; height: 100%; }
.nav .logo { font-weight: 800; color: #fff; font-size: 1.05rem; margin-right: auto; letter-spacing: -0.3px; }
.nav .logo span { color: var(--glow-blue); }
.nav a { color: var(--text-secondary); text-decoration: none; font-size: 0.875rem; font-weight: 500; transition: color 0.2s; }
.nav a:hover, .nav a:focus { color: var(--glow-blue); }
.breadcrumbs { display: flex; gap: 8px; align-items: center; font-size: 0.8rem; color: var(--text-muted); margin-bottom: 16px; padding: 16px 0 0; }
.breadcrumbs a { color: var(--text-muted); text-decoration: none; }
.breadcrumbs a:hover { color: var(--glow-blue); }
.post-content { padding: 32px 0 48px; }
.post-content h1 { font-size: 2.2rem; font-weight: 800; line-height: 1.3; letter-spacing: -0.5px; margin-bottom: 16px; background: linear-gradient(135deg, #fff, var(--glow-blue)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.post-content .post-meta { color: var(--text-muted); font-size: 0.85rem; margin-bottom: 24px; padding-bottom: 20px; border-bottom: 1px solid var(--border); display: flex; gap: 16px; flex-wrap: wrap; align-items: center; }
.cat-badge { display: inline-block; padding: 3px 12px; border-radius: 20px; font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
.cat-badge.guide { background: rgba(16,185,129,0.15); color: #34d399; }
.cat-badge.buying-guide { background: rgba(0,212,255,0.15); color: #00d4ff; }
.cat-badge.comparison { background: rgba(124,58,237,0.15); color: #a78bfa; }
.post-content h2 { font-size: 1.5rem; font-weight: 700; margin: 40px 0 14px; letter-spacing: -0.3px; color: var(--text); }
.post-content h2::before { content: ''; display: block; width: 40px; height: 3px; background: linear-gradient(90deg, var(--glow-blue), var(--glow-purple)); border-radius: 2px; margin-bottom: 12px; }
.post-content h3 { font-size: 1.15rem; font-weight: 600; margin: 28px 0 10px; color: var(--text); }
.post-content p { margin-bottom: 18px; color: var(--text-secondary); font-size: 1rem; line-height: 1.8; }
.post-content ul, .post-content ol { margin: 0 0 18px 24px; color: var(--text-secondary); }
.post-content li { margin-bottom: 8px; }
.post-content strong { color: var(--text); }
.post-content .product-box { background: linear-gradient(135deg, rgba(0,212,255,0.06), rgba(124,58,237,0.06)); border: 1px solid rgba(0,212,255,0.15); border-radius: 14px; padding: 28px; margin: 28px 0; position: relative; }
.post-content .product-box .rank-badge { position: absolute; top: -10px; left: 20px; background: linear-gradient(135deg, var(--glow-blue), var(--glow-purple)); color: #000; font-size: 0.7rem; font-weight: 800; padding: 4px 14px; border-radius: 20px; text-transform: uppercase; letter-spacing: 0.5px; }
.post-content .product-box h3 { margin-top: 4px; font-size: 1.2rem; color: var(--glow-blue); }
.post-content .product-box p { margin-bottom: 10px; }
.post-content .pros-cons { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 24px 0; }
.post-content .pros, .post-content .cons { padding: 20px; border-radius: 12px; }
.post-content .pros { background: rgba(16,185,129,0.08); border: 1px solid rgba(16,185,129,0.2); }
.post-content .cons { background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.2); }
.post-content .pros h4 { color: #34d399; }
.post-content .cons h4 { color: #f87171; }
.post-content .pros ul, .post-content .cons ul { margin: 0; padding: 0; list-style: none; font-size: 0.9rem; }
.post-content .pros li, .post-content .cons li { padding: 3px 0; position: relative; padding-left: 18px; }
.post-content .pros li::before { content: '+'; color: var(--glow-green); position: absolute; left: 0; font-weight: 700; }
.post-content .cons li::before { content: '-'; color: #f87171; position: absolute; left: 0; font-weight: 700; }
.post-content table { width: 100%; border-collapse: separate; border-spacing: 0; margin: 24px 0; border-radius: 12px; overflow: hidden; }
.post-content th, .post-content td { padding: 12px 14px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 0.85rem; }
.post-content th { background: linear-gradient(135deg, rgba(0,212,255,0.15), rgba(124,58,237,0.15)); color: var(--text); font-weight: 600; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.3px; }
.post-content tr:last-child td { border-bottom: none; }
.post-content tr:hover td { background: rgba(255,255,255,0.03); }
.btn { display: inline-block; background: linear-gradient(135deg, var(--glow-blue), #0284c7); color: #000; padding: 12px 28px; border-radius: 10px; text-decoration: none; font-weight: 700; font-size: 0.9rem; transition: all 0.3s; }
.btn:hover { transform: translateY(-2px); box-shadow: 0 8px 30px rgba(0,212,255,0.3); }
.btn-accent { background: linear-gradient(135deg, var(--glow-amber), #d97706); color: #000; }
.stars { color: var(--glow-amber); font-size: 0.9rem; letter-spacing: 2px; }
.callout { background: rgba(245,158,11,0.1); border-left: 4px solid var(--glow-amber); border-radius: 0 10px 10px 0; padding: 20px 24px; margin: 24px 0; }
.callout p { margin: 0; color: var(--glow-amber); }
.warning { background: rgba(239,68,68,0.1); border-left: 4px solid #f87171; border-radius: 0 10px 10px 0; padding: 20px 24px; margin: 24px 0; }
.warning p { margin: 0; color: #f87171; }
.faq-item { border: 1px solid var(--border); border-radius: 12px; padding: 20px 24px; margin: 16px 0; background: var(--bg-card); }
.faq-item h3 { margin-top: 0; font-size: 1rem; color: var(--text); }
.faq-item p { margin-bottom: 0; }
.footer { background: rgba(255,255,255,0.02); color: var(--text-secondary); padding: 40px 0; margin-top: 48px; border-top: 1px solid var(--border); }
.footer .container { max-width: 900px; }
.footer-grid { display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 32px; margin-bottom: 28px; }
.footer h3 { color: #fff; font-size: 0.9rem; margin-bottom: 12px; }
.footer p { font-size: 0.82rem; line-height: 1.7; }
.footer a { color: var(--glow-blue); text-decoration: none; }
.footer a:hover { text-decoration: underline; }
.footer ul { list-style: none; }
.footer li { margin-bottom: 6px; font-size: 0.82rem; }
.footer li a { color: var(--text-secondary); }
.footer li a:hover { color: var(--glow-blue); }
.footer .footer-bottom { border-top: 1px solid var(--border); padding-top: 20px; text-align: center; font-size: 0.78rem; color: var(--text-muted); }
.footer .disclosure { margin-top: 8px; font-size: 0.75rem; }
@media (max-width: 640px) {
  .container { padding: 0 16px; }
  .post-content h1 { font-size: 1.5rem; }
  .post-content h2 { font-size: 1.2rem; }
  .post-content .pros-cons { grid-template-columns: 1fr; }
  .post-content th, .post-content td { padding: 8px 10px; }
  .footer-grid { grid-template-columns: 1fr; gap: 24px; }
  .post-content .product-box { padding: 20px; }
}
@keyframes fadeUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
.product-box, .callout, .warning { animation: fadeUp 0.4s ease-out; }
.toc-sidebar { background: rgba(255,255,255,0.03); border: 1px solid var(--border); border-radius: 10px; margin-bottom: 28px; overflow: hidden; }
.toc-header { padding: 12px 16px; cursor: pointer; font-size: 0.82rem; font-weight: 600; display: flex; align-items: center; gap: 8px; color: var(--text); user-select: none; }
.toc-header:hover { background: rgba(255,255,255,0.03); }
.toc-toggle { font-size: 0.7rem; transition: transform 0.2s; color: var(--text-muted); }
.toc-body { padding: 0 16px 12px; }
.toc-body.collapsed { display: none; }
.toc-body ol { margin: 0; padding: 0; list-style: none; }
.toc-body li { margin-bottom: 4px; padding-left: 20px; position: relative; }
.toc-body li::before { content: counter(toc-counter); counter-increment: toc-counter; color: var(--glow-blue); font-weight: 600; font-size: 0.72rem; position: absolute; left: 0; }
.toc-body ol { counter-reset: toc-counter; }
.toc-link { color: var(--text-secondary); text-decoration: none; font-size: 0.82rem; transition: color 0.2s; display: inline-block; padding: 3px 0; }
.toc-link:hover { color: var(--glow-blue); }
html { scroll-behavior: smooth; }
.share-section { margin: 32px 0; padding-top: 24px; border-top: 1px solid var(--border); }
.share-section h3 { font-size: 0.9rem; font-weight: 600; margin-bottom: 12px; }
.share-buttons { display: flex; gap: 8px; flex-wrap: wrap; }
.share-btn { display: inline-flex; align-items: center; gap: 6px; padding: 8px 16px; border-radius: 8px; font-size: 0.78rem; font-weight: 600; text-decoration: none; transition: all 0.2s; color: #e2e8f0; background: rgba(0,0,0,0.2); }
.share-btn:hover { transform: translateY(-1px); }
.share-twitter:hover { background: #1da1f2; color: #fff; }
.share-facebook:hover { background: #1877f2; color: #fff; }
.share-reddit:hover { background: #ff4500; color: #fff; }
.share-email:hover { background: var(--glow-blue); color: #000; }
@media print { .nav, .footer, .toc-sidebar, .share-section, .related-section, .back-top, .progress-bar { display: none !important; } body { background: #fff !important; color: #000 !important; } .container { max-width: 100%; } .post-content h1 { -webkit-text-fill-color: #000 !important; color: #000 !important; } }

.related-section { margin-top: 48px; padding-top: 32px; border-top: 1px solid var(--border); }
.related-section h2 { font-size: 1.1rem; font-weight: 700; margin-bottom: 16px; }
.related-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14px; }
.related-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 10px; padding: 16px; text-decoration: none; color: inherit; transition: all 0.2s; }
.related-card:hover { background: var(--bg-card-hover); border-color: rgba(0,212,255,0.2); transform: translateY(-2px); }
.related-icon { font-size: 1.3rem; margin-bottom: 6px; }
.related-title { font-size: 0.82rem; font-weight: 600; line-height: 1.3; margin-bottom: 4px; }
.related-cat { font-size: 0.65rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; }
.back-top { position: fixed; bottom: 30px; right: 30px; width: 44px; height: 44px; border-radius: 50%; border: 1px solid var(--border); background: rgba(10,14,26,0.8); backdrop-filter: blur(8px); color: var(--text-secondary); font-size: 1.2rem; cursor: pointer; display: flex; align-items: center; justify-content: center; opacity: 0; visibility: hidden; transition: all 0.3s; z-index: 999; }
.back-top.visible { opacity: 1; visibility: visible; }
.back-top:hover { background: var(--glow-blue); color: #000; border-color: var(--glow-blue); transform: translateY(-2px); }
@media (max-width: 640px) { .related-grid { grid-template-columns: 1fr; } }
"""


def cat_badge(category):
    m = {"Buying Guide": "buying-guide", "Guide": "guide", "Comparison": "comparison"}
    cls = m.get(category, "guide")
    return f'<span class="cat-badge {cls}">{category}</span>'

def render_post_html(post, all_posts=None):
    t = post
    badge = cat_badge(t["category"])
    
    # Related articles
    related_html = ""
    if all_posts:
        same_cat = [p for p in all_posts if p["category"] == t["category"] and p["slug"] != t["slug"]]
        related = same_cat[:3]
        if len(related) < 3:
            others = [p for p in all_posts if p["slug"] != t["slug"] and p not in related]
            related += others[:3-len(related)]
        if related:
            related_html = '<div class="related-section"><h2>Related Guides</h2><div class="related-grid">'
            for r in related:
                icon = chr(0x26A1)
                related_html += f'<a href="/posts/{r["slug"]}" class="related-card"><div class="related-icon">{icon}</div><div class="related-title">{r["title"][:50]}</div><div class="related-cat">{r["category"]}</div></a>'
            related_html += '</div></div>'
    
    # Table of Contents
    import re as _re
    toc_items = [(m.group(1).strip().lower().replace(' ', '-').replace('?','').replace(',','').replace('—','-')[:40], m.group(1)) for m in _re.finditer(r'<h2>(.*?)</h2>', t.get('body', ''))]
    toc_html = ''
    if len(toc_items) >= 3:
        items = ''.join('<li><a href="#' + h_id + '" class="toc-link">' + label + '</a></li>' for h_id, label in toc_items)
        toc_html = '<nav class="toc-sidebar" id="tocSidebar"><div class="toc-header" onclick="toggleTOC()">\u2630 On this page <span class="toc-toggle">\u25BC</span></div><div class="toc-body" id="tocBody"><ol>' + items + '</ol></div></nav>'
    
    # Add id attributes to h2 tags
    def add_h2_ids(m):
        txt = m.group(1)
        hid = txt.strip().lower().replace(' ', '-').replace('?','').replace(',','').replace('—','-')[:40]
        return '<h2 id="' + hid + '">' + txt + '</h2>'
    body_with_ids = _re.sub(r'<h2>(.*?)</h2>', add_h2_ids, t.get('body', ''))
    
    # Social sharing
    surl = 'https://batterybackupguide.com/posts/' + t['slug']
    stitle = t['title'].replace('"', '')
    share_html = '<div class="share-section"><h3>Share this guide</h3><div class="share-buttons">'
    share_html += '<a href="https://twitter.com/intent/tweet?text=' + stitle + '&url=' + surl + '" target="_blank" rel="noopener" class="share-btn share-twitter" aria-label="Share on Twitter">\U0001d54f Twitter</a>'
    share_html += '<a href="https://www.facebook.com/sharer/sharer.php?u=' + surl + '" target="_blank" rel="noopener" class="share-btn share-facebook" aria-label="Share on Facebook">f Facebook</a>'
    share_html += '<a href="https://www.reddit.com/submit?title=' + stitle + '&url=' + surl + '" target="_blank" rel="noopener" class="share-btn share-reddit" aria-label="Share on Reddit">\u25cf Reddit</a>'
    share_html += '<a href="mailto:?subject=' + stitle + '&body=Check this out: ' + surl + '" class="share-btn share-email" aria-label="Share via Email">\u2709 Email</a>'
    share_html += '</div></div>'
    
    # Back to top button
    back_top = '<button id="backTop" class="back-top" onclick="window.scrollTo({top:0,behavior:&apos;smooth&apos;})">\u2191</button>'
    
    back_top_js = '<script>window.addEventListener("scroll",function(){var b=document.getElementById("backTop");if(b){if(window.scrollY>400){b.classList.add("visible")}else{b.classList.remove("visible")}}});</script>' 
    
    return f"""<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{t['title']} — Battery Backup Guide</title>
<meta name="description" content="{t['description']}">
<link rel="canonical" href="https://batterybackupguide.com/posts/{t['slug']}">
<meta property="og:title" content="{t['title']}">
<meta property="og:description" content="{t['description']}">
<meta property="og:url" content="https://batterybackupguide.com/posts/{t['slug']}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Battery Backup Guide">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t['title']}">
<meta name="twitter:description" content="{t['description']}">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":"{t['title'].replace(chr(34),'')}","description":"{t['description'][:200].replace(chr(34),'')}","url":"https://batterybackupguide.com/posts/{t['slug']}"}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
{CSS}</style>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><text y='28' font-size='28'>&#x26a1;</text></svg>">
</head>
<body>
<div class="progress-bar" id="progressBar"></div>
<a href="#article-content" class="skip-link">Skip to content</a>
<nav class="nav" role="navigation" aria-label="Main navigation"><div class="container"><span class="logo">&#x26a1; BatteryBackupGuide</span>
<a href="/">Home</a><a href="/about">About</a></div></nav>
<main id="article-content" class="container post-content" role="main">
<div class="breadcrumbs"><a href="/">Home</a> <span>&#x203a;</span> <span>{t['category']}</span></div>
{toc_html}
{body_with_ids}
{related_html}
{share_html}
</main>
{back_top}
{back_top_js}
<footer class="footer" role="contentinfo"><div class="container">
<div class="footer-grid">
<div>
<h3>&#x26a1; BatteryBackupGuide</h3>
<p>Independent reviews and guides for home battery backup solutions. We research, test, and compare portable power stations, solar generators, and battery systems so you can make an informed decision.</p>
</div>
<div>
<h3>Categories</h3>
<ul>
<li><a href="/">Buying Guides</a></li>
<li><a href="/">Comparisons</a></li>
<li><a href="/">How-To Guides</a></li>
</ul>
</div>
<div>
<h3>Links</h3>
<ul>
<li><a href="/about">About Us</a></li>
<li><a href="/about#disclosure">Affiliate Disclosure</a></li>
<li><a href="/">Home</a></li>
</ul>
</div>
</div>
<div class="footer-bottom">
<p>BatteryBackupGuide.com &mdash; Independent reviews and guides for home battery backup solutions.</p>
<p class="disclosure">We participate in the Amazon Services LLC Associates Program. As an Amazon Associate we earn from qualifying purchases.</p>
<p>&copy; 2026 Battery Backup Guide. All rights reserved.</p>
</div>
</div></footer>
<script>
window.addEventListener('scroll', function() {{
  var s = document.body.scrollTop || document.documentElement.scrollTop;
  var h = document.documentElement.scrollHeight - document.documentElement.clientHeight;
  document.getElementById("progressBar").style.width = (s / h) * 100 + "%";
}});
</script>
</body>
</html>"""


def update_sitemap(posts):
    urls = []
    urls.append(f"  <url>\n    <loc>https://batterybackupguide.com/</loc>\n    <lastmod>2026-05-02</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>1.0</priority>\n  </url>")
    for p in posts:
        pri = "0.9" if p.get("order", 9) <= 2 else "0.8" if p.get("order", 9) <= 5 else "0.7"
        urls.append(f"  <url>\n    <loc>https://batterybackupguide.com/posts/{p['slug']}</loc>\n    <lastmod>2026-05-02</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>{pri}</priority>\n  </url>")
    urls.append(f"  <url>\n    <loc>https://batterybackupguide.com/about</loc>\n    <lastmod>2026-05-02</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.3</priority>\n  </url>")
    
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>"""
    with open(f"{SITE_DIR}/sitemap.xml", "w") as fh:
        fh.write(sitemap)
    print(f"📄 sitemap.xml updated ({len(posts)+2} URLs)")

def generate_all():
    posts = []
    for f in sorted(glob.glob(f"{CONTENT_DIR}/*.json")):
        with open(f) as fh:
            posts.append(json.load(fh))
    posts.sort(key=lambda x: x.get("order", 999))
    
    os.makedirs(f"{SITE_DIR}/posts", exist_ok=True)
    for p in posts:
        html = render_post_html(p, posts)
        with open(f"{SITE_DIR}/posts/{p['slug']}.html", "w") as fh:
            fh.write(html)
        print(f"✅ posts/{p['slug']}.html")
    
    update_sitemap(posts)

if __name__ == "__main__":
    generate_all()
