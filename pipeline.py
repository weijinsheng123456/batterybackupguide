#!/usr/bin/env python3
"""Niche Site Content Pipeline — Battery Backup Guide

用法:
    python3 pipeline.py [--all] [--content-dir DIR] [--site-dir DIR]

路径优先级:
    1. --content-dir / --site-dir 命令行参数
    2. NICHE_CONTENT_DIR / NICHE_SITE_DIR 环境变量
    3. ~/.hermes/content-toolkit/niche-site（默认）"""
import argparse
import datetime
import glob
import json
import os
import re

from deep_content import enrich_buying_guide

DEFAULT_NICHE_HOME = os.path.expanduser("~/.hermes/content-toolkit/niche-site")

# 从环境变量读取，支持覆盖
CONTENT_DIR = os.environ.get("NICHE_CONTENT_DIR",
                             os.path.join(DEFAULT_NICHE_HOME, "content"))
SITE_DIR = os.environ.get("NICHE_SITE_DIR", DEFAULT_NICHE_HOME)
TODAY = datetime.date.today().isoformat()

# Product → image mapping (name_prefix: image_file)
PRODUCT_IMAGE_MAP = {
    "ecoflow delta 2": "ecoflow-delta-2",
    "ecoflow delta 2 max": "ecoflow-delta-2-max",
    "ecoflow delta pro": "ecoflow-delta-pro",
    "ecoflow river 2 pro": "ecoflow-river-2-pro",
    "ecoflow river 2": "ecoflow-river-2",
    "jackery explorer 500": "jackery-explorer-500",
    "jackery explorer 1000 v2": "jackery-explorer-1000-v2",
    "jackery explorer 300": "jackery-explorer-300-plus",
    "jackery explorer 2000 plus": "jackery-explorer-2000-plus",
    "bluetti ac70": "bluetti-ac70",
    "bluetti ac180": "bluetti-ac180",
    "bluetti ac200l": "bluetti-ac200l",
    "bluetti eb55": "bluetti-eb55",
    "anker solix f2000": "anker-solix-f2000",
    "anker solix c800 plus": "anker-solix-c800-plus",
    "anker solix c300 dc": "anker-solix-c300-dc",
    "anker c800": "anker-solix-c800-plus",
    "goal zero yeti 1500x": "goal-zero-yeti-1500x",
    "goal zero yeti 1500 x": "goal-zero-yeti-1500x",
}


def normalize_product_name(name):
    """Clean emoji/prefix/dash from product heading, return lowercase name.
    Handles formats: '🥇 Product Name — desc', '⚡ Our Pick: Product Name', '1. Name'"""
    clean = re.sub(r'^[^a-zA-Z]+', '', name)  # Remove emoji/number prefixes
    parts = re.split(r'\s*[—–:]\s*', clean, maxsplit=1)
    candidate = parts[0].strip().lower()
    # If first part isn't a known product, try the second part
    if len(parts) > 1:
        known_products = {"ecoflow", "jackery", "bluetti", "anker", "goal zero", "goal"}
        is_product = any(candidate.startswith(k) for k in known_products)
        if not is_product:
            candidate = parts[1].strip().lower()
    return candidate


def find_product_image(prod_name_lower):
    """Find matching image for a product name. Returns (image_file, display_name) or None."""
    for prefix, img_file in PRODUCT_IMAGE_MAP.items():
        if prod_name_lower.startswith(prefix) or prefix.startswith(prod_name_lower):
            return img_file, prod_name_lower.title()
    return None, None


def inject_product_images(body):
    """Insert product images after each product recommendation heading.
    Handles multiple formats: h2/h3, with/without Specs prefix, medals/numbers."""
    # Normalize literal \n to actual newlines
    body = body.replace('\\n', '\n')

    def insert_after_tag(match):
        tag = match.group(1)  # h2 or h3
        content = match.group(2)  # heading text
        after = match.group(3)  # content after > before next heading
        prod_name = normalize_product_name(content)
        img_file, display = find_product_image(prod_name)
        if not img_file:
            return match.group(0)
        alt_text = f"{display} portable power station"
        img_html = (f'<div class="product-image-wrap">'
                    f'<img src="/assets/images/{img_file}-thumb.webp" '
                    f'alt="{alt_text}" '
                    f'loading="lazy" width="200" height="200">'
                    f'</div>')
        # Insert image after the first <p> after the heading
        p_match = re.search(r'(<p>.*?</p>)', after, re.DOTALL)
        if p_match:
            p_end = p_match.end()
            return f'<{tag}>{content}</{tag}>{after[:p_end]}\n{img_html}{after[p_end:]}'
        # Fallback: insert right after heading
        return f'<{tag}>{content}</{tag}>\n{img_html}{after}'

    # Match h2 or h3 containing medal/number/emoji + product name
    return re.sub(
        r'<(h[23])[^>]*>([⚡🌟🔋📱🥇🥈🥉\d.][^<]*)</\1>(.*?)(?=<(?:h[23])|\Z)',
        insert_after_tag,
        body,
        flags=re.DOTALL
    )


def cat_badge(category):
    m = {"Buying Guide": "buying-guide", "Guide": "guide", "Comparison": "comparison"}
    cls = m.get(category, "guide")
    return f'<span class="cat-badge {cls}">{category}</span>'


def render_post_html(post, all_posts=None):
    t = post
    badge = cat_badge(t["category"])

    # Determine og:image — smart product-aware fallback
    body = t.get("body", "")
    img_match = re.search(r'<img[^>]+src="/assets/images/([^"]+)"', body)
    if img_match:
        og_image = f"https://batterybackupguide.com/assets/images/{img_match.group(1)}"
    else:
        KEYWORD_MAP = {
            "jackery": "jackery-explorer-500",
            "explorer": "jackery-explorer-500",
            "ecoflow": "ecoflow-delta-2",
            "bluetti": "bluetti-ac70",
            "anker": "anker-solix-f2000",
            "goal-zero": "goal-zero-yeti-1500x",
            "goal zero": "goal-zero-yeti-1500x",
            "yet": "goal-zero-yeti-1500x",
        }
        SLUG_MAP = {
            "apartment": "ecoflow-delta-2",
            "camping": "ecoflow-river-2-pro",
            "gaming": "ecoflow-river-2-pro",
            "senior": "jackery-explorer-300-plus",
            "comparison": "ecoflow-delta-2",
            "safety": "bluetti-ac70",
            "medical": "bluetti-ac70",
            "summer": "ecoflow-delta-2",
            "winter": "ecoflow-delta-2-max",
            "specs": "ecoflow-delta-2",
            "dual": "ecoflow-river-2-pro",
            "ups": "ecoflow-delta-2",
            "generator": "ecoflow-delta-2",
            "guide": "ecoflow-delta-2",
            "checklist": "bluetti-ac180",
            "survival": "ecoflow-delta-2-max",
            "prepared": "ecoflow-delta-2",
            "recharg": "ecoflow-delta-2",
        }
        slug = t.get("slug", "")
        body_lower = body.lower()
        img_key = None
        for kw, img in SLUG_MAP.items():
            if kw in slug:
                img_key = img
                break
        if not img_key:
            for kw, img in KEYWORD_MAP.items():
                if kw in body_lower:
                    img_key = img
                    break
        if not img_key:
            img_key = "ecoflow-delta-2"
        og_image = f"https://batterybackupguide.com/assets/images/{img_key}.webp"

    # Related articles
    related_html = ""
    if all_posts:
        same_cat = [p for p in all_posts if p["category"] == t["category"] and p["slug"] != t["slug"]]
        related = same_cat[:3]
        if len(related) < 3:
            others = [p for p in all_posts if p["slug"] != t["slug"] and p not in related]
            related += others[:3 - len(related)]
        if related:
            related_html = '<div class="related-section"><h2>Related Guides</h2><div class="related-grid">'
            for r in related:
                related_html += f'<a href="/posts/{r["slug"]}" class="related-card"><div class="related-icon">⚡</div><div class="related-title">{r["title"][:50]}</div><div class="related-cat">{r["category"]}</div></a>'
            related_html += '</div></div>'

    # Table of Contents
    toc_items = [(m.group(1).strip().lower().replace(' ', '-').replace('?', '').replace(',', '').replace('—', '-')[:40], m.group(1)) for m in re.finditer(r'<h2>(.*?)</h2>', body)]
    toc_html = ''
    if len(toc_items) >= 3:
        items = ''.join(f'<li><a href="#{h_id}" class="toc-link">{label}</a></li>' for h_id, label in toc_items)
        toc_html = '<nav class="toc-sidebar" id="tocSidebar"><div class="toc-header" onclick="toggleTOC()">☰ On this page <span class="toc-toggle">▼</span></div><div class="toc-body" id="tocBody"><ol>' + items + '</ol></div></nav>'

    # Enrich content depth for Buying Guide / Comparison articles
    body = enrich_buying_guide(body, t.get("category", ""))

    # Inject product images into body
    body = inject_product_images(body)

    # Add h2 IDs
    def add_h2_ids(m):
        txt = m.group(1)
        hid = txt.strip().lower().replace(' ', '-').replace('?', '').replace(',', '').replace('—', '-')[:40]
        return f'<h2 id="{hid}">{txt}</h2>'
    body_with_ids = re.sub(r'<h2>(.*?)</h2>', add_h2_ids, body)

    # Add article-level Amazon affiliate CTA
    TAG = "batteryback08-20"
    prod_names = [m.group(1).strip() for m in re.finditer(r'<h2[^>]*>([🥇🥈🥉\d][^<]*)</h2>', body)]
    clean_names = []
    for name in prod_names:
        clean = re.sub(r'^[^a-zA-Z]+', '', name)
        clean = re.split(r'\s*[—–:]\s*', clean)[0].strip()
        if clean and len(clean) > 3:
            clean_names.append(clean)

    amz_links = []
    for pname in clean_names[:5]:
        search = re.sub(r'[^a-z0-9+]', '', pname.lower().replace(' ', '+'))
        url = f"https://www.amazon.com/s?k={search}+power+station&tag={TAG}"
        amz_links.append(f'<a href="{url}" class="btn" target="_blank" rel="noopener sponsored" style="margin:4px">{pname}</a>')

    if amz_links:
        cta = '\n<div class="callout"><p><strong>Ready to buy?</strong> Check the latest prices on Amazon:</p><p style="margin-top:10px">' + ' '.join(amz_links) + '</p></div>'
        body_with_ids = body_with_ids + cta

    # Determine category link for breadcrumbs
    cat_links = {"Buying Guide": "/posts/best-home-battery-backup-2026",
                 "Guide": "/posts/how-to-prepare-for-power-outages-home",
                 "Comparison": "/posts/jackery-vs-ecoflow-vs-bluetti-home-backup"}
    cat_link = cat_links.get(t["category"], "/")

    # Social sharing
    surl = f'https://batterybackupguide.com/posts/{t["slug"]}'
    stitle = t['title'].replace('"', '')
    share_html = '<div class="share-section"><h3>Share this guide</h3><div class="share-buttons">'
    share_html += f'<a href="https://twitter.com/intent/tweet?text={stitle}&url={surl}" target="_blank" rel="noopener" class="share-btn share-twitter" aria-label="Share on Twitter">𝕏 Twitter</a>'
    share_html += f'<a href="https://www.facebook.com/sharer/sharer.php?u={surl}" target="_blank" rel="noopener" class="share-btn share-facebook" aria-label="Share on Facebook">f Facebook</a>'
    share_html += f'<a href="https://www.reddit.com/submit?title={stitle}&url={surl}" target="_blank" rel="noopener" class="share-btn share-reddit" aria-label="Share on Reddit">● Reddit</a>'
    share_html += f'<a href="mailto:?subject={stitle}&body=Check this out: {surl}" class="share-btn share-email" aria-label="Share via Email">✉ Email</a>'
    share_html += '</div></div>'

    # Back to top
    back_top = '<button id="backTop" class="back-top" onclick=\'window.scrollTo({top:0,behavior:"smooth"})\' aria-label="Back to top">↑</button>'
    back_top_js = '<script>window.addEventListener("scroll",function(){var b=document.getElementById("backTop");if(b){if(window.scrollY>400){b.classList.add("visible")}else{b.classList.remove("visible")}}});</script>'
    progress_js = '<script>window.addEventListener("scroll",function(){var s=document.body.scrollTop||document.documentElement.scrollTop;var h=document.documentElement.scrollHeight-document.documentElement.clientHeight;document.getElementById("progressBar").style.width=(s/h)*100+"%"});</script>'

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
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t['title']}">
<meta name="twitter:description" content="{t['description']}">
<meta name="twitter:image" content="{og_image}">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":"{t['title'].replace(chr(34), '')}","description":"{t['description'][:200].replace(chr(34), '')}","url":"https://batterybackupguide.com/posts/{t['slug']}"}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
<link rel="preload" href="/assets/style.css" as="style">
<link rel="preload" href="{og_image}" as="image">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><text y='28' font-size='28'>&#x26a1;</text></svg>">
</head>
<body>
<div class="progress-bar" id="progressBar"></div>
<a href="#article-content" class="skip-link">Skip to content</a>
<nav class="nav" role="navigation" aria-label="Main navigation"><div class="container"><span class="logo">⚡ Battery<span>Backup</span>Guide</span>
<a href="/">Home</a><a href="/about">About</a></div></nav>
<main id="article-content" class="container post-content" role="main">
<div class="breadcrumbs"><a href="/">Home</a> <span>›</span> <a href="{cat_link}">{t['category']}</a></div>
{toc_html}
{body_with_ids}
{related_html}
{share_html}
</main>
{back_top}
{back_top_js}
{progress_js}
<footer class="footer" role="contentinfo"><div class="container">
<div class="footer-grid">
<div>
<h3>⚡ BatteryBackupGuide</h3>
<p>Independent reviews and guides for home battery backup solutions. We research, test, and compare portable power stations, solar generators, and battery systems so you can make an informed decision.</p>
</div>
<div>
<h3>Categories</h3>
<ul>
<li><a href="/posts/best-home-battery-backup-2026">Buying Guides</a></li>
<li><a href="/posts/jackery-vs-ecoflow-vs-bluetti-home-backup">Comparisons</a></li>
<li><a href="/posts/how-to-prepare-for-power-outages-home">How-To Guides</a></li>
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
<p>BatteryBackupGuide.com — Independent reviews and guides for home battery backup solutions.</p>
<p class="disclosure">We participate in the Amazon Services LLC Associates Program. As an Amazon Associate we earn from qualifying purchases.</p>
<p>&copy; 2026 Battery Backup Guide. All rights reserved.</p>
</div>
</div></footer>
</body>
</html>"""


def sync_plan_status():
    """Sync content-plan.json: mark any existing content JSONs as published."""
    plan_path = f"{SITE_DIR}/content-plan.json"
    if not os.path.exists(plan_path):
        return
    with open(plan_path) as fh:
        plan = json.load(fh)
    existing_slugs = {os.path.splitext(os.path.basename(f))[0] for f in glob.glob(f"{CONTENT_DIR}/*.json")}
    changed = 0
    for p in plan["plan"]:
        if p["slug"] in existing_slugs and p["status"] in ("pending", "planned"):
            p["status"] = "published"
            changed += 1
    if changed:
        with open(plan_path, "w") as fh:
            json.dump(plan, fh, indent=2)
        print(f"📋 content-plan.json: {changed} pending → published")


def update_sitemap(posts):
    urls = []
    urls.append(f"  <url>\n    <loc>https://batterybackupguide.com/</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>1.0</priority>\n  </url>")
    for p in posts:
        pri = "0.9" if p.get("order", 9) <= 2 else "0.8" if p.get("order", 9) <= 5 else "0.7"
        urls.append(f"  <url>\n    <loc>https://batterybackupguide.com/posts/{p['slug']}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>{pri}</priority>\n  </url>")
    urls.append(f"  <url>\n    <loc>https://batterybackupguide.com/about</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.3</priority>\n  </url>")

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>"""
    with open(f"{SITE_DIR}/sitemap.xml", "w") as fh:
        fh.write(sitemap)
    print(f"📄 sitemap.xml updated ({len(posts) + 2} URLs)")


def generate_all(force_all=False, content_dir=None, site_dir=None):
    """Generate all articles. If force_all=False, only regenerates changed ones.
    
    Args:
        force_all: If True, regenerate all articles regardless of modification time
        content_dir: Content JSON directory (default: CONTENT_DIR module var)
        site_dir: Site output directory (default: SITE_DIR module var)
    """
    _content_dir = content_dir or CONTENT_DIR
    _site_dir = site_dir or SITE_DIR

    sync_plan_status()
    posts = []
    json_files = sorted(glob.glob(os.path.join(_content_dir, "*.json")))
    for f in json_files:
        with open(f) as fh:
            posts.append(json.load(fh))
    posts.sort(key=lambda x: x.get("order", 999))

    os.makedirs(f"{_site_dir}/posts", exist_ok=True)

    changed_count = 0
    for p in posts:
        slug = p["slug"]
        json_path = os.path.join(CONTENT_DIR, f"{slug}.json")
        html_path = f"{_site_dir}/posts/{slug}.html"

        # Determine if this article needs regeneration
        needs_regenerate = force_all
        if not needs_regenerate and os.path.exists(html_path):
            json_mtime = os.path.getmtime(json_path)
            html_mtime = os.path.getmtime(html_path)
            if json_mtime > html_mtime:
                needs_regenerate = True
        if not needs_regenerate and not os.path.exists(html_path):
            needs_regenerate = True

        if needs_regenerate:
            html = render_post_html(p, posts)
            with open(html_path, "w") as fh:
                fh.write(html)
            print(f"✅ posts/{slug}.html")
            changed_count += 1
        else:
            print(f"⏭️  posts/{slug}.html (unchanged)")

    if changed_count > 0 or force_all:
        update_sitemap(posts)
        print(f"📋 Generated {changed_count} changed article(s)")
    else:
        print("📋 No changes detected — sitemap unchanged")

    return changed_count


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Battery Backup Guide Content Pipeline")
    parser.add_argument("--all", "-a", action="store_true", help="强制全量重建所有文章")
    parser.add_argument("--content-dir", help="内容 JSON 目录（覆盖环境变量 NICHE_CONTENT_DIR）")
    parser.add_argument("--site-dir", help="站点输出目录（覆盖环境变量 NICHE_SITE_DIR）")
    args = parser.parse_args()

    generate_all(force_all=args.all, content_dir=args.content_dir, site_dir=args.site_dir)
