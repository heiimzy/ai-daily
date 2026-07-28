#!/bin/bash
# curl-based deploy script for ai-daily
set -e

cd ~/.hermes/projects/ai-daily

# Get token
TOKEN=$(grep '^GITHUB_TOKEN=' ~/.hermes/.env | head -1 | cut -d= -f2)
OWNER="heiimzy"
REPO="ai-daily"

echo "🚀 Deploying ai-daily via curl..."
echo ""

# Upload a file to GitHub
upload_file() {
    local rel_path="$1"
    local content_b64="$2"
    local msg="$3"
    
    # Check if file exists
    local sha=""
    local resp=$(curl -s --connect-timeout 15 --max-time 30 \
        -H "Authorization: Bearer $TOKEN" \
        -H "Accept: application/vnd.github+json" \
        "https://api.github.com/repos/$OWNER/$REPO/contents/$rel_path")
    
    if echo "$resp" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('sha',''))" 2>/dev/null | grep -q .; then
        sha=$(echo "$resp" | python3 -c "import sys,json; print(json.load(sys.stdin)['sha'])")
    fi
    
    # Build JSON body
    body=$(python3 -c "
import json
b = {'message': '$msg', 'content': '$content_b64'}
if '$sha':
    b['sha'] = '$sha'
print(json.dumps(b))
")
    
    local result=$(curl -s -X PUT --connect-timeout 30 --max-time 60 \
        -H "Authorization: Bearer $TOKEN" \
        -H "Accept: application/vnd.github+json" \
        -H "Content-Type: application/json" \
        -d "$body" \
        "https://api.github.com/repos/$OWNER/$REPO/contents/$rel_path" 2>&1)
    
    if echo "$result" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('commit'))" 2>/dev/null | grep -q sha; then
        echo "   ✅ $rel_path"
        return 0
    else
        local err=$(echo "$result" | python3 -c "import sys,json; print(json.load(sys.stdin).get('message','unknown'))" 2>/dev/null)
        echo "   ❌ $rel_path: $err"
        return 1
    fi
}

# Upload posts/338 files
echo "Uploading new post files..."

CONTENT_ZH=$(base64 -w0 posts/338-ai-kill-switch-act-white-house-openai-rogue-july-24-2026.zh.html)
CONTENT_EN=$(base64 -w0 posts/338-ai-kill-switch-act-white-house-openai-rogue-july-24-2026.en.html)

upload_file "posts/338-ai-kill-switch-act-white-house-openai-rogue-july-24-2026.zh.html" "$CONTENT_ZH" "post 338 zh: AI Kill Switch Act"
upload_file "posts/338-ai-kill-switch-act-white-house-openai-rogue-july-24-2026.en.html" "$CONTENT_EN" "post 338 en: AI Kill Switch Act"

# Upload updated metadata files
echo "Uploading updated metadata files..."

CONTENT_JSON=$(base64 -w0 posts.json)
upload_file "posts.json" "$CONTENT_JSON" "update posts.json for article 338"

CONTENT_RSS=$(base64 -w0 rss.xml)
upload_file "rss.xml" "$CONTENT_RSS" "update rss.xml for article 338"

CONTENT_SITEMAP=$(base64 -w0 sitemap.xml)
upload_file "sitemap.xml" "$CONTENT_SITEMAP" "update sitemap.xml for article 338"

echo ""
echo "✅ All files uploaded!"
echo ""

# Try to trigger Pages rebuild
echo "Triggering Pages rebuild..."
curl -s -X POST --connect-timeout 15 --max-time 30 \
    -H "Authorization: Bearer $TOKEN" \
    -H "Accept: application/vnd.github+json" \
    "https://api.github.com/repos/$OWNER/$REPO/pages/builds" > /dev/null 2>&1
echo "   ✅ Pages rebuild triggered via API"

echo ""
echo "🎉 Deployment complete!"