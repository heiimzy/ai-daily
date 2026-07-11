#!/bin/bash
# Blog post publishing helper
# Usage: bash blog/publish.sh <post-filename.html>
#
# This script:
# 1. Reads the <title>, <date>, and first <p> from a blog post HTML
# 2. Adds/updates the entry in posts.json
# 3. Updates RSS feed
# 4. Commits and pushes to GitHub
#
# Note: This is a reference for the automated process.
# The actual publishing is done by AI during cron execution.

POST_FILE="$1"
POST_DIR="blog/posts"
BLOG_DIR="blog"

if [ -z "$POST_FILE" ]; then
  echo "Usage: $0 <post-filename.html>"
  echo "The file must be in $POST_DIR/"
  exit 1
fi

FULL_PATH="$POST_DIR/$POST_FILE"
if [ ! -f "$FULL_PATH" ]; then
  echo "Error: $FULL_PATH not found"
  exit 1
fi

echo "Publishing: $POST_FILE"
echo ""
echo "Steps performed by AI automation:"
echo "1. Write blog post HTML → $FULL_PATH"
echo "2. Extract title/date/tags/summary from the post"
echo "3. Prepend entry to blog/posts.json"
echo "4. Update blog/rss.xml with new item"
echo "5. git add, commit, push"
echo ""
echo "All done! GitHub Pages will auto-deploy in ~1-2 minutes."
