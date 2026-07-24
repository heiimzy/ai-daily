#!/usr/bin/env python3
"""
ai-daily deploy script: uploads only changed/new files to GitHub via Contents API.
Used by the daily cron job. Run from project root.
"""
import os, re, json, base64, requests, time, sys
import functools
from pathlib import Path

# Force unbuffered output
_print = print
print = functools.partial(_print, flush=True)

def load_token():
    """Load GitHub token from various sources."""
    # Try .hermes/.env
    env_path = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("GITHUB_TOKEN="):
                    return line.strip().split("=", 1)[1]
    # Try gh hosts.yml
    hosts_path = os.path.expanduser("~/.config/gh/hosts.yml")
    if os.path.exists(hosts_path):
        with open(hosts_path) as f:
            m = re.search(r"oauth_token:\s*(.+)", f.read())
            if m:
                return m.group(1).strip()
    return os.environ.get("GITHUB_TOKEN", "")

def get_github_files(token, owner, repo, path=""):
    """Get dict of filename -> sha for files at a GitHub path."""
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    resp = requests.get(url, headers=headers, timeout=15)
    if resp.status_code == 200:
        return {item["name"]: item["sha"] for item in resp.json()}
    return {}

def get_github_file_sha(token, owner, repo, path):
    """Get SHA of a single file."""
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    resp = requests.get(url, headers=headers, timeout=15)
    if resp.status_code == 200:
        return resp.json().get("sha")
    return None

def upload_file(token, owner, repo, rel_path, content_bytes, message):
    """Upload a single file via GitHub Contents API."""
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{rel_path}"
    
    # Check if file exists
    resp = requests.get(url, headers=headers, timeout=15)
    sha = resp.json().get("sha") if resp.status_code == 200 else None
    
    body = {
        "message": message,
        "content": base64.b64encode(content_bytes).decode()
    }
    if sha:
        body["sha"] = sha  # Required for updates
    
    resp = requests.put(url, headers=headers, json=body, timeout=30)
    return resp.status_code in [200, 201], sha is None

def main():
    owner = "heiimzy"
    repo = "ai-daily"
    project_root = Path(__file__).parent.resolve()
    
    print(f"🚀 ai-daily deploy script")
    print(f"   Project root: {project_root}")
    
    # Step 1: Load token
    token = load_token()
    if not token:
        print("❌ No GitHub token found")
        sys.exit(1)
    print(f"   ✅ Token loaded")
    
    # Step 2: Determine what's new/changed
    # Compare local files vs GitHub files
    gh_posts = get_github_files(token, owner, repo, "posts")
    gh_root_files = get_github_files(token, owner, repo, "")
    
    local_posts = {f.name for f in (project_root / "posts").glob("*.html")}
    local_root = {f.name for f in project_root.glob("*") if f.is_file() and f.name in 
                  ["index.html", "en/index.html", "rss.xml", "posts.json", "sitemap.xml", "topic-database.json"]}
    
    new_posts = local_posts - set(gh_posts.keys())
    changed_posts = set()
    # Check content changes on posts that exist
    for name in local_posts & set(gh_posts.keys()):
        local_path = project_root / "posts" / name
        with open(local_path, 'rb') as f:
            local_content = f.read()
        gh_sha = gh_posts[name]
        # We can't check content without downloading, so trust the build script
        # For safety, upload all posts that exist locally (fast check = always upload)
        # Actually no - this is slow. Let's just upload new ones.
        # The build script will tell us which files changed.
    
    # Read the manifest from build output
    manifest_path = project_root / ".deploy_manifest.json"
    if manifest_path.exists():
        with open(manifest_path) as f:
            manifest = json.load(f)
        files_to_upload = manifest.get("files", [])
        commit_msg = manifest.get("message", "chore: update ai-daily")
    else:
        # Just upload new post files
        files_to_upload = [f"posts/{n}" for n in new_posts]
        # Also upload index, rss, sitemap, posts.json
        for root_file in ["index.html", "rss.xml", "posts.json", "sitemap.xml", "en/index.html"]:
            if (project_root / root_file).exists():
                files_to_upload.append(root_file)
        commit_msg = "chore: daily ai-news update"
    
    # Also always upload template.html and topic-database.json if they changed
    for meta_file in ["template.html", "article.css", "topic-database.json"]:
        if (project_root / meta_file).exists() and meta_file not in [f.rsplit("/", 1)[-1] for f in files_to_upload]:
            files_to_upload.append(meta_file)
    
    # Deduplicate
    files_to_upload = list(set(files_to_upload))
    
    if not files_to_upload:
        print("   ℹ No files to upload")
        return
    
    print(f"   📦 Uploading {len(files_to_upload)} file(s)...")
    
    successes = 0
    for rel_path in sorted(files_to_upload):
        full_path = project_root / rel_path
        if not full_path.exists():
            print(f"   ⚠ {rel_path} not found locally, skipping")
            continue
        
        with open(full_path, 'rb') as f:
            content = f.read()
        
        ok, is_new = upload_file(token, owner, repo, rel_path, content, commit_msg)
        if ok:
            status = "new" if is_new else "updated"
            successes += 1
            print(f"   ✓ {rel_path} ({status})")
        else:
            print(f"   ✗ {rel_path} FAILED")
        
        time.sleep(0.3)
    
    # Clean up manifest
    if manifest_path.exists():
        manifest_path.unlink()
    
    print(f"\n✅ Done! {successes}/{len(files_to_upload)} files uploaded")
    
    # Trigger Pages rebuild
    try:
        r = requests.post(
            f"https://api.github.com/repos/{owner}/{repo}/pages/builds",
            headers={"Authorization": f"token {token}", "Accept": "application/vnd.github+json"},
            timeout=15
        )
        if r.status_code in [200, 201]:
            print(f"   🔄 Pages rebuild triggered")
        else:
            print(f"   ⚠ Pages rebuild trigger returned {r.status_code}")
    except Exception as e:
        print(f"   ⚠ Pages rebuild trigger failed: {e}")

if __name__ == "__main__":
    main()
