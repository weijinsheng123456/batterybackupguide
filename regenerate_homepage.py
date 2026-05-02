#!/usr/bin/env python3
"""Regenerate bubblebackupguide.com index.html from content JSON files"""
import json, os, glob

BASE = os.path.expanduser("~/.hermes/content-toolkit/niche-site")
CONTENT = f"{BASE}/content"

def smart_truncate(text, max_chars=120):
    if len(text) <= max_chars: return text
    truncated = text[:max_chars]
    last_space = truncated.rfind(' ')
    if last_space > max_chars * 0.6:
        truncated = text[:last_space]
    return truncated.rstrip(',.;:') + '...'

def get_icon(slug):
    icons = {'best-home-battery-backup-2026':'🏆','best-generator-for-apartment-2026':'⚡','apartment-power-outage-survival-guide':'🆘',
             'jackery-vs-ecoflow-vs-bluetti-home-backup':'⚔️','how-to-prepare-for-power-outages-home':'📋','best-portable-power-station-apartment-dwellers':'🔋',
             'battery-backup-cpap-apartment':'🏥','can-portable-power-station-power-whole-apartment':'🤔','best-quiet-backup-power-solutions-apartments':'🔇',
             'how-to-keep-food-cold-during-power-outage-apartment':'🧊','best-power-station-under-500-apartment':'💰','how-to-choose-portable-power-station-apartment':'🎯',
             'balcony-solar-setup-apartment':'☀️','power-station-vs-ups-vs-generator-apartment':'⚖️','best-power-station-home-office-backup':'💻',
             'best-power-station-refrigerator-backup':'📦','apartment-power-outage-safety-checklist':'✅','how-long-power-station-run-appliances':'⏱️',
             'anker-vs-ecoflow-vs-goal-zero-comparison':'🥊','winter-power-outage-survival-apartment':'❄️'}
    return icons.get(slug, '⚡')

posts = []
for f in sorted(glob.glob(f"{CONTENT}/*.json")):
    with open(f) as fh:
        posts.append(json.load(fh))
posts.sort(key=lambda x: x.get("order", 999))

cls_map = {"Buying Guide":"buying","Guide":"guide","Comparison":"comparison"}

# Top 3
top3 = ''
for i, p in enumerate(posts[:3]):
    medals = ['🥇', '🥈', '🥉']
    top3 += f'''<a href="/posts/{p['slug']}" class="top-card">
<div class="top-rank">{medals[i]}</div>
<div class="top-icon">{get_icon(p['slug'])}</div>
<div class="top-title">{p['title'][:40]}{'...' if len(p['title'])>40 else ''}</div>
<div class="top-cat">{p['category']} · {p['read_time']} min</div>
</a>'''

# Cards
cards = []
for p in posts[3:]:
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

# Replace top picks section
old_top = html[html.find('<div class="top-picks">'):html.find('</div>', html.find('class="top-picks"')) + 6]
html = html.replace(old_top, f'<div class="top-picks"><div class="section-label">⚡ Top Picks at a Glance</div><div class="top-grid">{top3}</div></div>')

# Replace card grid
old_start = html.find('<div class="posts-grid">')
old_end = html.find('<div class="cta-section">')
html = html[:old_start] + f'<div class="posts-grid">\n{chr(10).join(cards)}\n</div>\n' + html[old_end:]

with open(f"{BASE}/index.html", "w") as f:
    f.write(html)

print(f"🎯 首页已更新: {len(posts)} 篇文章")
