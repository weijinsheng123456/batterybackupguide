# Battery Backup Guide 🪫🔋

[![GitHub Pages](https://img.shields.io/github/deployments/weijinsheng123456/batterybackupguide/github-pages?label=Pages&logo=github)](https://batterybackupguide.com)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/weijinsheng123456/batterybackupguide)](https://github.com/weijinsheng123456/batterybackupguide/commits/main)
[![Repo Size](https://img.shields.io/github/repo-size/weijinsheng123456/batterybackupguide)](https://github.com/weijinsheng123456/batterybackupguide)

**Honest, research-backed reviews of portable power stations and home battery backup solutions.**

A static affiliate site built with plain HTML/CSS — no frameworks, no bloat. Content generated via automated pipeline and deployed to GitHub Pages.

## Features

- 🏠 **33+ in-depth articles** — Buying guides, comparisons, survival guides
- 🔬 **Data-driven** — Real specs (Wh, Watts, cycle life, solar input, temperature range)
- 🎯 **Honest reviews** — No fake "We tested" claims, transparent affiliate links
- 📱 **Mobile-first** — Clean responsive design, works on any device
- ⚡ **Blazing fast** — Pure static HTML, zero JS dependencies, instant load

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Static Site** | Pure HTML + CSS (no frameworks) |
| **Content Pipeline** | Python (pipeline.py + deep_content.py) |
| **Deployment** | GitHub Pages + auto-deploy via cron + CI |
| **Images** | WebP with lazy loading, product thumbnails |
| **SEO** | IndexNow, sitemap.xml, semantic HTML5 |

## Content Pipeline

Articles are generated through an automated pipeline and deployed Tuesdays and Fridays:

```
content-plan.json → pipeline.py → HTML + sitemap → Git push → GitHub Pages
```

Each article goes through:
1. Topic selection from content plan
2. Content generation with real product data (deep_content.py)
3. Image injection (product thumbnails)
4. Amazon affiliate CTA injection
5. SEO optimization (OG images, heading IDs, internal links)

## Affiliate Disclosure

This site uses Amazon Affiliate links (tag: `batteryback08-20`). We may earn a small commission on qualifying purchases at no extra cost to you. All reviews are based on research and analysis, not sponsored content.

## Project Structure

```
batterybackupguide/
├── posts/                # Article HTML files
├── assets/
│   └── images/           # Product images (WebP)
├── content-plan.json     # Article roadmap
├── sitemap.xml           # Auto-generated
├── style.css             # Site styles
├── .github/workflows/    # CI/CD (auto-deploy on push)
└── auto_deploy.sh        # Deployment script
```

## License

MIT © 2026 Battery Backup Guide
