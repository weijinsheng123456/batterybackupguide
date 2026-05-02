#!/usr/bin/env python3
"""Battery Backup Guide — Weekly Site Health Check (no external API needed)"""
import subprocess, json, os, datetime

SITE = "https://batterybackupguide.com"
LOG = os.path.expanduser("~/.hermes/logs/batterybackup-health.json")

def run(cmd, timeout=10):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip(), r.returncode
    except subprocess.TimeoutExpired:
        return "TIMEOUT", -1

def check():
    report = {
        "date": datetime.date.today().isoformat(),
        "checks": {}
    }

    # 1. Site reachable
    out, code = run(f"curl -s -o /dev/null -w '%{{http_code}}' --max-time 10 {SITE}/")
    report["checks"]["uptime"] = {"status": "✅" if out == "200" else "❌", "http": out}
    if out != "200":
        return report  # 站挂了就不继续了

    # 2. Sitemap valid
    out, code = run(f"curl -s --max-time 10 {SITE}/sitemap.xml | head -3")
    report["checks"]["sitemap"] = {"status": "✅" if "urlset" in out else "❌"}

    # 3. Count articles on live site
    out, code = run(f"curl -s --max-time 10 {SITE}/sitemap.xml | grep -c 'posts/'")
    article_count = out.strip()
    report["checks"]["article_count"] = {"status": "✅" if article_count.isdigit() and int(article_count) >= 18 else "⚠️", "count": article_count}

    # 4. IndexNow key accessible
    out, code = run(f"curl -s -o /dev/null -w '%{{http_code}}' --max-time 10 {SITE}/8d47ff0998004e62ab14ed1ecb365c26.txt")
    report["checks"]["indexnow_key"] = {"status": "✅" if out == "200" else "❌", "http": out}

    # 5. CNAME file present
    out, code = run(f"curl -s -o /dev/null -w '%{{http_code}}' --max-time 10 {SITE}/CNAME")
    report["checks"]["cname"] = {"status": "✅" if out == "200" else "❌"}

    # 6. Affiliate links on a sample article (check tag present)
    sample = "/posts/best-home-battery-backup-2026"
    out, code = run(f"curl -s --max-time 10 {SITE}{sample} | grep -c 'batteryback08-20'")
    has_links = out.strip()
    report["checks"]["affiliate_links"] = {"status": "✅" if has_links.isdigit() and int(has_links) > 0 else "❌", "count": has_links}

    # Save
    with open(LOG, "w") as f:
        json.dump(report, f, indent=2)

    return report

def print_report(report):
    print(f"\n=== BatteryBackupGuide 健康检查 ({report['date']}) ===")
    for k, v in report["checks"].items():
        print(f"  {v['status']} {k}: {v}")

if __name__ == "__main__":
    r = check()
    print_report(r)
