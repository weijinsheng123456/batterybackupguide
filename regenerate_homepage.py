#!/usr/bin/env python3
"""Regenerate batterybackupguide.com index.html posts grid from content JSON files"""
import json, os, glob, datetime

BASE = os.path.expanduser("~/.hermes/content-toolkit/niche-site")
CONTENT = f"{BASE}/content"
TODAY = datetime.date.today().isoformat()


def smart_truncate(text, max_chars=120):
    if len(text) <= max_chars:
        return text
    truncated = text[:max_chars]
    last_space = truncated.rfind(' ')
    if last_space > max_chars * 0.6:
        truncated = text[:last_space]
    return truncated.rstrip(',.;:') + '...'


def get_icon(slug):
    icons = {'best-home-battery-backup-2026': '🏆', 'best-generator-for-apartment-2026': '⚡',
             'apartment-power-outage-survival-guide': '🆘', 'jackery-vs-ecoflow-vs-bluetti-home-backup': '⚔️',
             'how-to-prepare-for-power-outages-home': '📋', 'best-portable-power-station-apartment-dwellers': '🔋',
             'battery-backup-cpap-apartment': '🏥', 'can-portable-power-station-power-whole-apartment': '🤔',
             'best-quiet-backup-power-solutions-apartments': '🔇', 'how-to-keep-food-cold-during-power-outage-apartment': '🧊',
             'best-power-station-under-500-apartment': '💰', 'how-to-choose-portable-power-station-apartment': '🎯',
             'balcony-solar-setup-apartment': '☀️', 'power-station-vs-ups-vs-generator-apartment': '⚖️',
             'best-power-station-home-office-backup': '💻', 'best-power-station-refrigerator-backup': '📦',
             'apartment-power-outage-safety-checklist': '✅', 'how-long-power-station-run-appliances': '⏱️',
             'anker-vs-ecoflow-vs-goal-zero-comparison': '🥊', 'winter-power-outage-survival-apartment': '❄️'}
    return icons.get(slug, '⚡')


def load_posts():
    posts = []
    for f in sorted(glob.glob(f"{CONTENT}/*.json")):
        with open(f) as fh:
            posts.append(json.load(fh))
    posts.sort(key=lambda x: x.get("order", 999))
    return posts


def update_sitemap(posts):
    """Re-generate sitemap.xml from posts (shared with pipeline.py logic)."""
    urls = []
    urls.append(
        f"  <url>\n    <loc>https://batterybackupguide.com/</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>1.0</priority>\n  </url>")
    for p in posts:
        pri = "0.9" if p.get("order", 9) <= 2 else "0.8" if p.get("order", 9) <= 5 else "0.7"
        urls.append(
            f"  <url>\n    <loc>https://batterybackupguide.com/posts/{p['slug']}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>{pri}</priority>\n  </url>")
    urls.append(
        f"  <url>\n    <loc>https://batterybackupguide.com/about</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.3</priority>\n  </url>")

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>"""
    with open(f"{BASE}/sitemap.xml", "w") as fh:
        fh.write(sitemap)
    print(f"📄 sitemap.xml updated ({len(posts) + 2} URLs)")


posts = load_posts()
cls_map = {"Buying Guide": "buying", "Guide": "guide", "Comparison": "comparison"}

# Generate cards for all posts (including top 3 for consistency)
cards = []
for p in posts:
    cls = cls_map.get(p['category'], "guide")
    excerpt = smart_truncate(p['excerpt'], 120)
    cards.append(f'''<article class="post-card card-{cls}" data-cat="{cls}">
<div class="card-icon">{get_icon(p['slug'])}</div>
<div class="card-body">
<div class="card-cat cat-{cls}">{p['category']}</div>
<h2><a href="/posts/{p['slug']}">{p['title']}</a></h2>
<div class="card-meta">{p['read_time']} min read</div>
<p>{excerpt}</p>
<a href="/posts/{p['slug']}" class="read-more">Read Review →</a>
</div>
</article>''')

with open(f"{BASE}/index.html") as f:
    html = f.read()

# Replace posts-grid section (everything between <div class="posts-grid"> and <div class="cta-section">)
old_start = html.find('<div class="posts-grid">')
old_end = html.find('<div class="cta-section">')
if old_start == -1 or old_end == -1:
    print("❌ Could not find posts-grid or cta-section markers in index.html")
else:
    html = html[:old_start] + f'<div class="posts-grid">\n{chr(10).join(cards)}\n</div>\n' + html[old_end:]

    with open(f"{BASE}/index.html", "w") as f:
        f.write(html)

    print(f"🎯 首页已更新: {len(posts)} 篇文章")

# Also update sitemap
update_sitemap(posts)
