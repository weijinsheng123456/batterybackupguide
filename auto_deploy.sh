#!/bin/bash
# Battery Backup Guide — Automatic Deploy Pipeline
# 用 法: ./auto_deploy.sh [--generate] [--push-only]
# 依 赖: 需要在 batterybackupguide 目录下运行

set -e

SITE_DIR=~/batterybackupguide
CONTENT_DIR=~/.hermes/content-toolkit/niche-site
LOG_FILE=~/.hermes/logs/batterybackup-deploy.log
PIPELINE=$SITE_DIR/pipeline.py
NOW=$(date '+%Y-%m-%d %H:%M:%S')

log() { echo "[$NOW] $1" | tee -a "$LOG_FILE"; }

cd "$SITE_DIR"

# 1️⃣ 生成文章
if [ "$1" = "--generate" ] || [ "$1" = "" ]; then
    log "🚀 Running content pipeline..."
    python3 "$PIPELINE" 2>&1 | tee -a "$LOG_FILE"
    log "✅ Pipeline done"
fi

# 2️⃣ 检查是否有变更
if git diff --quiet && git diff --cached --quiet; then
    log "ℹ️  No changes to deploy"
else
    log "📦 Committing changes..."
    git add -A
    git commit -m "auto: site update $(date '+%Y-%m-%d %H:%M')"
    log "📤 Pushing to GitHub Pages..."
    if git push origin main 2>&1; then
        log "✅ Deployed successfully"
        # 3️⃣ 部署成功后提交 IndexNow
        log "🔍 Submitting to IndexNow..."
        curl -s -X POST "https://api.indexnow.org/indexnow" \
            -H "Content-Type: application/json" \
            -d "{
                \"host\": \"batterybackupguide.com\",
                \"key\": \"8d47ff0998004e62ab14ed1ecb365c26\",
                \"keyLocation\": \"https://batterybackupguide.com/8d47ff0998004e62ab14ed1ecb365c26.txt\",
                \"urlList\": [
                    \"https://batterybackupguide.com/\",
                    \"https://batterybackupguide.com/sitemap.xml\"
                ]
            }" 2>&1 | tee -a "$LOG_FILE"
        log "✅ IndexNow submitted"
    else
        log "❌ Git push failed"
        exit 1
    fi
fi

log "✅ Auto-deploy complete"
