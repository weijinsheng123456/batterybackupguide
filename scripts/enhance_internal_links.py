#!/usr/bin/env python3
"""
batterybackupguide — 内链网络增强脚本
为每篇文章生成 4-6 条高质量相关文章推荐，按相关性排序。

分类体系：
  - comparison: 品牌对比
  - best-of: 最佳选购
  - survival: 应急指南
  - how-to: 教程类
  - specialized: 特定场景

用法: python3 enhance_internal_links.py
"""

import json, re, os
from pathlib import Path

POSTS_DIR = Path("/home/xiaobai/batterybackupguide/posts")
INDEX_FILE = Path("/tmp/article_index.json")

# ── 文章元数据（手工标注分类和关键词） ──────────────────
ARTICLES = {
    # ── comparison (品牌对比) ──
    "anker-vs-jackery-portable-power-station": {
        "title": "Anker vs Jackery Portable Power Stations — Which Brand Wins in 2026?",
        "cat": "comparison", "tags": ["anker", "jackery", "brand-comparison"],
    },
    "anker-vs-ecoflow-vs-goal-zero-comparison": {
        "title": "Anker Solix vs EcoFlow Delta vs Goal Zero Yeti — Which Brand Is Best?",
        "cat": "comparison", "tags": ["anker", "ecoflow", "goal-zero", "brand-comparison"],
    },
    "jackery-vs-ecoflow-vs-bluetti-home-backup": {
        "title": "Jackery vs EcoFlow vs Bluetti: Home Backup Comparison 2026",
        "cat": "comparison", "tags": ["jackery", "ecoflow", "bluetti", "brand-comparison"],
    },
    "bluetti-ac180-vs-ecoflow-delta-2": {
        "title": "Bluetti AC180 vs EcoFlow Delta 2 — Detailed Comparison (2026)",
        "cat": "comparison", "tags": ["bluetti", "ecoflow", "delta-2", "ac180"],
    },
    "power-station-vs-gas-generator-comprehensive": {
        "title": "Power Station vs Gas Generator — Which Is Right for Your Apartment?",
        "cat": "comparison", "tags": ["generator", "gas", "comparison"],
    },
    "power-station-vs-ups-vs-generator-apartment": {
        "title": "Power Station vs UPS vs Generator for Apartments — Which Do You Need?",
        "cat": "comparison", "tags": ["ups", "generator", "comparison", "apartment"],
    },

    # ── best-of (选购指南) ──
    "best-home-battery-backup-2026": {
        "title": "Best Home Battery Backup Systems 2026 — Top 7 Picks Reviewed",
        "cat": "best-of", "tags": ["home-backup", "top-picks", "whole-house"],
    },
    "best-portable-power-station-apartment-dwellers": {
        "title": "Best Portable Power Station for Apartment Dwellers 2026 — Top 6 Picks",
        "cat": "best-of", "tags": ["apartment", "top-picks", "portable"],
    },
    "best-portable-power-station-under-300": {
        "title": "Best Portable Power Station Under $300 — Budget Picks That Don't Suck (2026)",
        "cat": "best-of", "tags": ["budget", "under-300", "cheap"],
    },
    "best-power-station-dual-use-camping-home": {
        "title": "Best Power Station for Camping and Home — Dual-Use Picks (2026)",
        "cat": "best-of", "tags": ["camping", "dual-use", "versatile"],
    },
    "best-power-station-for-seniors-easy-to-use": {
        "title": "Best Portable Power Station for Seniors (2026)",
        "cat": "best-of", "tags": ["seniors", "easy-to-use", "simple"],
    },
    "best-power-station-gaming-setup": {
        "title": "Best Power Station for Gaming Setup — Keep Playing During Outages (2026)",
        "cat": "best-of", "tags": ["gaming", "pc", "electronics"],
    },
    "best-power-station-home-office-backup": {
        "title": "Best Power Station for Home Office & Work From Home Backup (2026)",
        "cat": "best-of", "tags": ["home-office", "wfh", "work"],
    },
    "best-power-station-refrigerator-backup": {
        "title": "Best Portable Power Station for Refrigerator Backup (2026)",
        "cat": "best-of", "tags": ["refrigerator", "appliance", "food"],
    },
    "best-power-station-under-500-apartment": {
        "title": "Best Portable Power Station Under $500 for Apartments (2026)",
        "cat": "best-of", "tags": ["apartment", "under-500", "budget"],
    },
    "best-quiet-backup-power-solutions-apartments": {
        "title": "Best Quiet Backup Power Solutions for Apartments (2026)",
        "cat": "best-of", "tags": ["quiet", "noise", "apartment"],
    },
    "best-generator-for-apartment-2026": {
        "title": "Best Generator for Apartments (No Gas) — 2026 Guide",
        "cat": "best-of", "tags": ["generator", "no-gas", "apartment"],
    },
    "how-to-choose-portable-power-station-apartment": {
        "title": "How to Choose a Portable Power Station for Your Apartment (2026)",
        "cat": "best-of", "tags": ["buyers-guide", "choosing", "apartment"],
    },

    # ── survival (应急指南) ──
    "apartment-power-outage-survival-guide": {
        "title": "Apartment Power Outage Survival Guide (No Generator Needed)",
        "cat": "survival", "tags": ["outage", "survival", "no-generator"],
    },
    "summer-power-outage-survival-apartment": {
        "title": "Summer Power Outage Survival Guide for Apartments (2026)",
        "cat": "survival", "tags": ["summer", "outage", "heat"],
    },
    "winter-power-outage-survival-apartment": {
        "title": "Winter Power Outage Survival Guide for Apartments (2026)",
        "cat": "survival", "tags": ["winter", "outage", "cold"],
    },
    "apartment-emergency-kit-power-outage": {
        "title": "The Complete Apartment Emergency Kit for Power Outages (2026)",
        "cat": "survival", "tags": ["emergency-kit", "preparedness", "checklist"],
    },
    "apartment-power-outage-safety-checklist": {
        "title": "Apartment Power Outage Safety Checklist — What Every Renter Needs",
        "cat": "survival", "tags": ["safety", "checklist", "preparedness"],
    },

    # ── how-to (教程类) ──
    "how-long-power-station-run-appliances": {
        "title": "How Long Will a Power Station Run My Appliances? — Runtime Guide",
        "cat": "how-to", "tags": ["runtime", "calculation", "appliances"],
    },
    "how-to-prepare-for-power-outages-home": {
        "title": "How to Prepare for Power Outages at Home: Complete Guide 2026",
        "cat": "how-to", "tags": ["preparedness", "planning", "home"],
    },
    "how-to-recharge-power-station-without-grid": {
        "title": "How to Recharge Your Power Station Without Grid Power (Solar, Car)",
        "cat": "how-to", "tags": ["solar", "recharge", "off-grid"],
    },
    "how-to-keep-food-cold-during-power-outage-apartment": {
        "title": "How to Keep Food Cold During a Power Outage in Your Apartment",
        "cat": "how-to", "tags": ["food", "cooler", "refrigerator"],
    },
    "understanding-power-station-specs": {
        "title": "Understanding Power Station Specs — Wh, Watts, Inverters, Battery Types",
        "cat": "how-to", "tags": ["specs", "education", "beginner"],
    },
    "can-portable-power-station-power-whole-apartment": {
        "title": "Can a Portable Power Station Power a Whole Apartment?",
        "cat": "how-to", "tags": ["capacity", "realistic", "expectations"],
    },

    # ── specialized (特定场景) ──
    "battery-backup-cpap-apartment": {
        "title": "Battery Backup for CPAP in Apartment — 2026 Life-Saving Guide",
        "cat": "specialized", "tags": ["cpap", "medical", "sleep-apnea"],
    },
    "battery-backup-medical-devices-apartment": {
        "title": "Battery Backup for Medical Devices in Apartments (Beyond CPAP)",
        "cat": "specialized", "tags": ["medical", "health", "devices"],
    },
    "balcony-solar-setup-apartment": {
        "title": "Balcony Solar Generator Setup for Apartments — Complete 2026 Guide",
        "cat": "specialized", "tags": ["solar", "balcony", "renewable"],
    },
    "power-station-safety-what-not-to-do": {
        "title": "Power Station Safety — 10 Things You Should Never Do",
        "cat": "specialized", "tags": ["safety", "warning", "danger"],
    },
}


def slug_to_title(slug: str) -> str:
    """Convert filename slug to display title."""
    a = ARTICLES.get(slug, {})
    return a.get("title", slug.replace("-", " ").title())


def score_article(a_slug: str, b_slug: str) -> int:
    """Score how related article B is to article A (higher = more related)."""
    a = ARTICLES.get(a_slug)
    b = ARTICLES.get(b_slug)
    if not a or not b:
        return 0

    score = 0
    # Same category = strong match
    if a["cat"] == b["cat"]:
        score += 3
    # Shared tags
    shared = set(a["tags"]) & set(b["tags"])
    score += len(shared) * 2
    # Cross-category diversity bonus (prevent same-cluster saturation)
    return score


def get_related(slug: str, max_count: int = 5) -> list:
    """Get top related articles for a given slug."""
    all_slugs = [s for s in ARTICLES if s != slug]
    scored = [(score_article(slug, s), s) for s in all_slugs]
    scored.sort(key=lambda x: -x[0])

    # Diversity: pick top from same cat, then fill with cross-cat
    same_cat = [(s, sc) for sc, s in scored if ARTICLES[s]["cat"] == ARTICLES[slug]["cat"]]
    other_cat = [(s, sc) for sc, s in scored if ARTICLES[s]["cat"] != ARTICLES[slug]["cat"]]

    selected = []
    # 60% same category
    same_count = min(3, len(same_cat))
    for i in range(same_count):
        selected.append(same_cat[i][0])
    # 40% cross category
    other_count = min(max_count - same_count, len(other_cat))
    for i in range(other_count):
        selected.append(other_cat[i][0])

    return selected[:max_count]


def inject_related_section(html: str, slug: str) -> str:
    """Replace existing Related Guides section with enhanced version."""
    related_slugs = get_related(slug)

    if not related_slugs:
        return html

    # Build new section
    cards_html = ""
    for rs in related_slugs:
        title = slug_to_title(rs)
        cards_html += f"""<a href="/posts/{rs}" class="related-card"><div class="related-icon">⚡</div><div class="related-title">{title[:50]}</div></a>\n"""

    new_section = f"""<div class="related-section"><h2>Related Guides</h2><div class="related-grid">
{cards_html}</div></div>"""

    # Replace existing Related Guides section
    old_pattern = r'<div class="related-section"><h2>Related Guides</h2>.*?</div>\s*</div>'
    count = 0
    new_html, count = re.subn(old_pattern, new_section, html, count=1, flags=re.DOTALL)

    if count == 0:
        print(f"  ⚠️  {slug}: No existing Related Guides section found")
        return html

    print(f"  ✅ {slug}: {len(related_slugs)} related articles injected")
    return new_html


def main():
    posts_dir = POSTS_DIR
    files = sorted(posts_dir.glob("*.html"))

    print(f"🔗 Enhancing internal links for {len(files)} articles...\n")

    for path in files:
        slug = path.stem
        if slug not in ARTICLES:
            print(f"  ⏭  {slug}: No metadata (skipping)")
            continue

        html = path.read_text(encoding="utf-8")
        new_html = inject_related_section(html, slug)

        if new_html != html:
            path.write_text(new_html, encoding="utf-8")

    print(f"\n✨ Done! All articles updated.")

    # Print summary stats
    print(f"\n📊 Link distribution:")
    for slug in sorted(ARTICLES):
        related = get_related(slug)
        print(f"  {slug}: {len(related)} links")


if __name__ == "__main__":
    main()
