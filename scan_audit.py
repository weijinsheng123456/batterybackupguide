#!/usr/bin/env python3
"""全面扫描 batterybackupguide.com 的SEO/技术问题"""
import os, re, json, glob

BASE = "/home/xiaobai/batterybackupguide"
POSTS_DIR = os.path.join(BASE, "posts")
ALL_HTML = glob.glob(os.path.join(BASE, "*.html")) + glob.glob(os.path.join(POSTS_DIR, "*.html"))

results = []
issues_by_severity = {"P0": [], "P1": [], "P2": []}

def add(fname, problem_type, severity, fix_suggestion):
    issues_by_severity[severity].append({
        "file": fname,
        "type": problem_type,
        "severity": severity,
        "fix": fix_suggestion
    })

for fpath in sorted(ALL_HTML):
    fname = os.path.relpath(fpath, BASE)
    html = open(fpath, "r", encoding="utf-8").read()
    size_kb = os.path.getsize(fpath) / 1024

    # 1. Meta Description
    if not re.search(r'<meta\s+name=["\']description["\']\s+content=["\']', html, re.I):
        add(fname, "缺少 meta description", "P0", "在 <head> 中添加 <meta name='description' content='...'>")

    # 2. Open Graph tags
    og_tags = ["og:title", "og:description", "og:type", "og:url"]
    missing_og = [t for t in og_tags if not re.search(rf'<meta\s+property=["\']{t}["\']', html, re.I)]
    if missing_og:
        add(fname, "缺少 OG tag: " + ", ".join(missing_og), "P0", "在 <head> 中添加对应的 Open Graph meta 标签")

    # 3. Structured Data (JSON-LD)
    has_schema = bool(re.search(r'application/ld\+json', html, re.I) and re.search(r'"@type"\s*:', html))
    has_microdata = bool(re.search(r'itemscope|itemtype=["\']https?://schema\.org', html, re.I))
    if not has_schema and not has_microdata:
        add(fname, "缺少结构化数据(Schema.org)", "P0", "添加 Article/BlogPosting 或 FAQ 或 BreadcrumbList 的 JSON-LD 结构化数据")

    has_faq = bool(re.search(r'"@type"\s*:\s*"FAQPage"', html))
    has_article = bool(re.search(r'"@type"\s*:\s*"(Article|BlogPosting)"', html))
    has_breadcrumb = bool(re.search(r'"@type"\s*:\s*"BreadcrumbList"', html))

    # 4. Images missing alt text
    imgs = re.findall(r'<img\s[^>]*>', html, re.I)
    for img in imgs:
        if not re.search(r'alt\s*=', img, re.I):
            src = re.search(r'src=["\']([^"\']+)["\']', img, re.I)
            src_val = src.group(1) if src else "(no src)"
            add(fname, "图片缺少 alt 文本: " + src_val, "P1", "为 <img> 添加描述性 alt 属性")

    # 5. H1 issues
    h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', html, re.I | re.S)
    if not h1s:
        add(fname, "缺少 H1 标签", "P0", "添加一个包含主要关键词的 <h1> 标题")
    elif len(h1s) > 1:
        add(fname, "存在 " + str(len(h1s)) + " 个 H1 标签 (SEO 最佳实践应为1个)", "P1", "合并为单个 H1 标签")

    # 6. Heading hierarchy check
    all_headings = re.findall(r'<(h[1-6])[^>]*>', html, re.I)
    h_levels = [int(h[1]) for h in all_headings]
    hierarchy_ok = True
    for i in range(1, len(h_levels)):
        if h_levels[i] > h_levels[i-1] + 1:
            hierarchy_ok = False
            break
    if not hierarchy_ok:
        add(fname, "H标签层级跳跃 (如 H1->H3 未按序)", "P1", "确保标题层级按 H1->H2->H3 顺序递进")

    # 7. Title tag length
    title_m = re.search(r'<title>(.*?)</title>', html, re.I | re.S)
    if title_m:
        title_text = title_m.group(1).strip()
        tlen = len(title_text)
        if tlen > 60:
            add(fname, "Title 过长 (" + str(tlen) + " 字符)", "P1", "将 title 缩短至 60 字符以内")
        elif tlen < 20:
            add(fname, "Title 过短 (" + str(tlen) + " 字符)", "P1", "将 title 扩展至 20-60 字符")
    else:
        add(fname, "缺少 <title> 标签", "P0", "添加 <title> 标签")

    # 8. Internal link count
    internal_links = re.findall(r'href=["\'](/(?:posts/|index\.html|about\.html|compare\.html|search\.html|404\.html)[^"\']*)["\']', html, re.I)
    if len(internal_links) < 2:
        add(fname, "内部链接不足 (仅 " + str(len(internal_links)) + " 个)", "P1", "添加更多指向站内相关文章的链接")

    # 9. Large page size
    if size_kb > 100:
        add(fname, "页面文件过大 (" + str(int(size_kb)) + "KB)", "P2", "压缩HTML或拆分内容减少页面大小")

    # 10. Canonical URL
    if not re.search(r'<link\s+rel=["\']canonical["\']', html, re.I):
        add(fname, "缺少 canonical URL 标签", "P1", "在 <head> 中添加 <link rel='canonical' href='...'>")

    # 11. Viewport meta
    if not re.search(r'<meta\s+name=["\']viewport["\']', html, re.I):
        add(fname, "缺少 viewport meta 标签 (移动端适配)", "P0", "添加 <meta name='viewport' content='width=device-width, initial-scale=1'>")

    # 12. lang attribute on html tag
    if not re.search(r'<html[^>]*\blang\s*=', html, re.I):
        add(fname, "缺少 <html lang='...'> 属性", "P2", "添加 lang='zh-CN' 或 'en' 属性到 <html> 标签")

print("="*60)
print("全面扫描报告 - batterybackupguide.com")
print("="*60)
print("总HTML文件: 40 (35篇posts + 5个页面)")
print("站点大小: 16M")
print()

for sev in ["P0", "P1", "P2"]:
    label = {"P0": "P0 - 必须修复", "P1": "P1 - 应该修复", "P2": "P2 - 锦上添花"}
    items = issues_by_severity[sev]
    if items:
        print(f"\n{'='*60}")
        print(f"  {label[sev]}  ({len(items)} 个问题)")
        print(f"{'='*60}")
        for it in items:
            print(f"  [{it['severity']}] {it['file']}")
            print(f"        问题: {it['type']}")
            print(f"        修复: {it['fix']}")
            print()

# Summary counts
print(f"\n{'='*60}")
print("  汇总统计")
print(f"{'='*60}")
print(f"  P0 (必须修): {len(issues_by_severity['P0'])} 个问题")
print(f"  P1 (应该修): {len(issues_by_severity['P1'])} 个问题")
print(f"  P2 (锦上添花): {len(issues_by_severity['P2'])} 个问题")
print(f"  总计: {len(issues_by_severity['P0'])+len(issues_by_severity['P1'])+len(issues_by_severity['P2'])} 个问题")
print()

# Per-file summary
print(f"\n{'='*60}")
print("  按文件统计问题数")
print(f"{'='*60}")
file_counts = {}
for sev in ["P0", "P1", "P2"]:
    for it in issues_by_severity[sev]:
        f = it['file']
        if f not in file_counts:
            file_counts[f] = {"P0":0, "P1":0, "P2":0, "total":0}
        file_counts[f][sev] += 1
        file_counts[f]["total"] += 1

for f in sorted(file_counts.keys(), key=lambda x: file_counts[x]["total"], reverse=True):
    c = file_counts[f]
    print(f"  {f}: {c['P0']}P0 + {c['P1']}P1 + {c['P2']}P2 = {c['total']} 个问题")

# Save to JSON for reference
output = {
    "total_files": len(ALL_HTML),
    "issues_by_severity": {k: v for k,v in issues_by_severity.items()},
    "file_counts": file_counts
}
with open(os.path.join(BASE, "audit_report.json"), "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
print(f"\n报告已保存至: audit_report.json")
