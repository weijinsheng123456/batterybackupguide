#!/usr/bin/env python3
"""Niche Site Content Pipeline — Battery Backup Guide"""
import json, os, glob, re

CONTENT_DIR = os.path.expanduser("~/.hermes/content-toolkit/niche-site/content")
SITE_DIR = os.path.expanduser("~/.hermes/content-toolkit/niche-site")

CSS = """:root { --primary: #2563eb; --primary-dark: #1d4ed8; --accent: #f59e0b; --bg: #f8fafc; --card: #ffffff; --text: #1e293b; --text-light: #64748b; --border: #e2e8f0; }
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, system-ui, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: var(--bg); color: var(--text); line-height: 1.7; }
.container { max-width: 800px; margin: 0 auto; padding: 0 20px; }
.nav { background: white; border-bottom: 1px solid var(--border); padding: 12px 0; position: sticky; top: 0; z-index: 100; }
.nav .container { display: flex; gap: 24px; align-items: center; }
.nav a { color: var(--text-light); text-decoration: none; font-size: 0.9rem; font-weight: 500; }
.nav a:hover { color: var(--primary); }
.nav .logo { font-weight: 700; color: var(--text); font-size: 1rem; margin-right: auto; }
.post-content { padding: 40px 0; }
.post-content h1 { font-size: 2rem; margin-bottom: 10px; }
.post-content .post-meta { color: var(--text-light); font-size: 0.9rem; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 1px solid var(--border); }
.post-content h2 { font-size: 1.5rem; margin: 30px 0 12px; }
.post-content h3 { font-size: 1.2rem; margin: 24px 0 10px; }
.post-content p { margin-bottom: 16px; }
.post-content ul, .post-content ol { margin: 0 0 16px 20px; }
.post-content li { margin-bottom: 8px; }
.post-content .product-box { background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 10px; padding: 20px; margin: 20px 0; }
.post-content .product-box h3 { margin-top: 0; }
.post-content .pros-cons { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 20px 0; }
.post-content .pros, .post-content .cons { padding: 16px; border-radius: 8px; }
.post-content .pros { background: #f0fdf4; border: 1px solid #bbf7d0; }
.post-content .cons { background: #fef2f2; border: 1px solid #fecaca; }
.post-content table { width: 100%; border-collapse: collapse; margin: 20px 0; }
.post-content th, .post-content td { padding: 10px 12px; text-align: left; border-bottom: 1px solid var(--border); font-size: 0.9rem; }
.post-content th { background: #f1f5f9; font-weight: 600; }
.skip-link { position: absolute; top: -40px; left: 0; background: var(--primary); color: #fff; padding: 8px 16px; z-index: 999; }
.skip-link:focus { top: 0; }
.footer { background: #1e293b; color: #94a3b8; padding: 30px 0; text-align: center; font-size: 0.85rem; }
.footer .aff-disclosure { margin-top: 10px; font-size: 0.8rem; }
@media (max-width: 640px) { .post-content .pros-cons { grid-template-columns: 1fr; } }
"""

def render_post_html(post):
    t = post
    # Build Article JSON-LD
    json_ld_article = f'''{{"@context":"https://schema.org","@type":"Article","headline":"{t['title'].replace(chr(34),'')}","description":"{t['description'][:200].replace(chr(34),'')}","url":"https://batterybackupguide.com/posts/{t['slug']}","dateModified":"2026-05-02","author":{{"@type":"Organization","name":"Battery Backup Guide"}}}}'''
    
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
<script type="application/ld+json">{json_ld_article}</script>
<style>
{CSS}</style>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><text y='28' font-size='28'>⚡</text></svg>">
</head>
<body>
<a href="#article-content" class="skip-link">Skip to content</a>
<nav class="nav" role="navigation" aria-label="Main navigation"><div class="container"><span class="logo">&#x26a1; BatteryBackupGuide</span>
<a href="/">Home</a><a href="/about">About</a></div></nav>
<main id="article-content" class="container post-content" role="main">
{t['body']}
</main>
<footer class="footer" role="contentinfo"><div class="container">
<p>BatteryBackupGuide.com &mdash; Independent reviews and guides for home battery backup solutions.</p>
<p class="aff-disclosure">We participate in the Amazon Services LLC Associates Program. As an Amazon Associate we earn from qualifying purchases.</p>
<p>&copy; 2026 Battery Backup Guide. All rights reserved.</p>
</div></footer>
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
    with open(f"{SITE_DIR}/sitemap.xml", "w") as f:
        f.write(sitemap)
    print(f"📄 sitemap.xml updated ({len(posts)+2} URLs)")

def generate_all():
    # Load all posts
    posts = []
    for f in sorted(glob.glob(f"{CONTENT_DIR}/*.json")):
        with open(f) as fh:
            posts.append(json.load(fh))
    posts.sort(key=lambda x: x.get("order", 999))
    
    # Generate HTML for each post
    os.makedirs(f"{SITE_DIR}/posts", exist_ok=True)
    for p in posts:
        html = render_post_html(p)
        with open(f"{SITE_DIR}/posts/{p['slug']}.html", "w") as f:
            f.write(html)
        print(f"✅ posts/{p['slug']}.html")
    
    # Update sitemap
    update_sitemap(posts)
    
    print(f"🎯 全部生成完成: {len(posts)} 篇文章")

if __name__ == "__main__":
    generate_all()
