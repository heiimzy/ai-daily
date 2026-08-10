#!/usr/bin/env python3
import json, re

ZH_FILE="posts/629-tech-news-openai-astra-critical-cyber-capabilities-aug-8-2026.zh.html"
EN_FILE="posts/629-tech-news-openai-astra-critical-cyber-capabilities-aug-8-2026.en.html"
ZH_URL="https://ai-daily.cc.cd/"+ZH_FILE
EN_URL="https://ai-daily.cc.cd/"+EN_FILE
zh_title="⚡ 8月8日AI要闻：OpenAI称在研模型Astra或触及「关键网络安全」能力阈值"
zh_summary="⚡ AI要闻：OpenAI官方博客披露，其尚在研发中的新模型Astra在内部初步评估中可能已触及「Preparedness框架」下的关键（Critical）网络安全能力等级——即能在无需人类干预下独立开发针对多种加固关键系统的全等级零日漏洞，或仅凭目标描述即自行设计与执行端到端网络攻击策略。OpenAI据此暂停相关内部活动、收紧安全护栏，并与政府部门及多家AI安全组织合作深入测试，同时强调Astra与先前的Hugging Face漏洞事件无关。"
pub="Sat, 08 Aug 2026 00:00:00 GMT"

# ---------- posts.json ----------
with open('posts.json', encoding='utf-8') as f:
    data = json.load(f)
assert data[0]['id'] == '628', data[0]['id']
prev_id = int(data[0]['id'])
new_id = f"{prev_id+1:03d}"  # 629
entry = {
    "id": new_id,
    "date": "2026-08-08",
    "zh": {
        "title": zh_title,
        "summary": zh_summary,
        "tags": ["AI要闻","OpenAI","Astra","人工智能","网络安全","大模型","安全保障"],
        "file": ZH_FILE,
    },
    "en": {
        "title": "⚡ Aug 8 AI News: OpenAI Says In-Development Astra Model May Hit 'Critical' Cybersecurity Capabilities",
        "summary": "AI update: OpenAI disclosed that its in-development Astra model may have reached the 'Critical' cybersecurity level under its Preparedness Framework — able to autonomously identify and develop zero-day exploits across many hardened real-world critical systems, or devise end-to-end cyberattack strategies from a target description alone. OpenAI is pausing internal work on Astra, raising security guardrails, and working with government agencies and select AI safety groups, noting Astra was not involved in the earlier Hugging Face breach.",
        "tags": ["AI News","OpenAI","Astra","AI Safety","Cybersecurity","Large Model"],
        "file": EN_FILE,
    },
}
data.insert(0, entry)
with open('posts.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("posts.json ->", len(data), "items, top id", data[0]['id'])

# ---------- rss.xml ----------
with open('rss.xml', encoding='utf-8') as f:
    rss = f.read()
rss_item = """    <item>
      <title>⚡ 8月8日AI要闻：OpenAI称在研模型Astra或触及关键网络安全能力阈值</title>
      <link>ZHURL</link>
      <description>ZHSUM</description>
      <pubDate>PUB</pubDate>
      <guid>ZHURL</guid>
    </item>
"""
rss_item = rss_item.replace("ZHURL", ZH_URL).replace("ZHSUM", zh_summary).replace("PUB", pub)
# insert before first <item>
idx = rss.find("<item>")
assert idx != -1
rss = rss[:idx] + rss_item + "\n" + rss[idx:]
# update lastBuildDate (replace existing)
rss = re.sub(r'<lastBuildDate>[^<]+</lastBuildDate>',
             '<lastBuildDate>'+pub+'</lastBuildDate>', rss, count=1)
with open('rss.xml', 'w', encoding='utf-8') as f:
    f.write(rss)
print("rss.xml updated")

# ---------- sitemap.xml ----------
with open('sitemap.xml', encoding='utf-8') as f:
    sm = f.read()
new_urls = """  <url>
    <loc>ZHURL</loc>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>ENURL</loc>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
""".replace("ZHURL", ZH_URL).replace("ENURL", EN_URL)
idx = sm.rfind("</urlset>")
sm = sm[:idx] + new_urls + "  " + "</urlset>"
with open('sitemap.xml','w',encoding='utf-8') as f:
    f.write(sm)
print("sitemap.xml updated")
print("DONE")