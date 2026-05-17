#!/usr/bin/env python3
"""Generate search-index.json for batterybackupguide.com.

Scans all post HTML files and extracts:
  - title (from <title> or <h1>)
  - url (permalink)
  - excerpt (first meaningful paragraph)
  - category (from nav/category-hub reference)

Usage: python3 generate_search_index.py
"""

import json, re, os
from pathlib import Path

POSTS_DIR = Path("/home/xiaobai/batterybackupguide/posts")
OUTPUT = Path("/home/xiaobai/batterybackupguide/assets/search-index.json")

CATEGORY_MAP = {
    "anker": "comparison", "jackery": "comparison", "ecoflow": "comparison",
    "bluetti": "comparison", "goal-zero": "comparison", "vs-": "comparison",
    "buying": "buying-guide", "best-": "buying-guide", "budget": "buying-guide",
    "under-": "buying-guide", "top-picks": "buying-guide",
    "survival": "survival", "outage": "survival", "emergency": "survival",
    "safety": "survival", "winter": "survival", "summer": "survival",
    "how-to": "how-to", "guide": "how-to", "specs": "how-to", "runtime": "how-to",
    "cpap": "medical", "medical": "medical", "seniors": "medical",
    "solar": "specialized", "balcony": "specialized", "safety": "specialized",
    "camping": "buying-guide", "gaming": "buying-guide", "home-office": "buying-guide",
    "refrigerator": "buying-guide", "quiet": "buying-guide",
    "generator": "comparison", "ups": "comparison",
}


def infer_category(slug: str) -> str:
    for keyword, cat in CATEGORY_MAP.items():
        if keyword in slug:
            return cat
    return "general"


def extract_excerpt(html: str) -> str:
    """Extract first meaningful text paragraph."""
    # Remove script/style
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)

    # Find first <p> with substantial text
    paras = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
    for p in paras:
        text = re.sub(r'<[^>]+>', '', p).strip()
        text = re.sub(r'\s+', ' ', text)
        if len(text) > 60:
            return text[:200]
    return ""


def extract_title(html: str, slug: str) -> str:
    """Extract article title."""
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    if m:
        return re.sub(r'<[^>]+>', '', m.group(1)).strip()
    m = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
    if m:
        return m.group(1).strip()
    return slug.replace("-", " ").title()


def main():
    entries = []
    files = sorted(POSTS_DIR.glob("*.html"))

    for path in files:
        slug = path.stem
        html = path.read_text(encoding="utf-8")

        title = extract_title(html, slug)
        excerpt = extract_excerpt(html)
        category = infer_category(slug)

        entries.append({
            "title": title,
            "url": f"/posts/{slug}",
            "excerpt": excerpt,
            "category": category,
            "slug": slug,
        })

    # Sort: buying-guide first, then alphabetical
    cat_order = {"buying-guide": 0, "comparison": 1, "survival": 2, "how-to": 3, "medical": 4, "specialized": 5, "general": 6}
    entries.sort(key=lambda e: (cat_order.get(e["category"], 9), e["title"]))

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(entries, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"✅ search-index.json generated: {len(entries)} entries")
    print(f"   Categories: {sorted(set(e['category'] for e in entries))}")
    print(f"   Size: {OUTPUT.stat().st_size} bytes")


if __name__ == "__main__":
    main()
