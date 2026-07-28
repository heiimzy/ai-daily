#!/usr/bin/env python3
import json
import re
from email.utils import formatdate
import time

# ===== 1. Update posts.json =====
with open('/home/admin/.hermes/projects/ai-daily/posts.json', 'r') as f:
    posts = json.load(f)

new_post = {
    "id": "415",
    "date": "2026-07-27",
    "zh": {
        "title": "⚡ 7月27日国际政治实时动态：沙特拦截伊朗支持武装无人机袭击石油设施、胡塞武装红海再起波澜、伊朗革命卫队霍尔木兹海峡拦截6艘商船、特朗普警告谈判失败将恢复强有力军事行动",
        "summary": "⚡ 7月27日国际政治实时动态：沙特阿拉伯防空部队拦截多架从伊拉克发射的伊朗支持武装无人机目标直指东部省份和利雅得石油设施；胡塞武装同步声称袭击沙特原油运输走廊；伊朗革命卫队在霍尔木兹海峡鸣枪拦截6艘商船；特朗普接受Axios专访称美伊正进行非常深入的谈判警告若失败将恢复非常强力的军事行动；内塔尼亚胡因安全威胁秘密从军事基地启程赴华盛顿。",
        "tags": ["国际政治", "沙特", "伊朗", "胡塞武装", "霍尔木兹海峡", "美伊战争", "特朗普", "内塔尼亚胡"],
        "file": "posts/415-saudi-drone-attacks-houthi-oil-iran-guards-hormuz-trump-netanyahu-july-27-2026.zh.html"
    },
    "en": {
        "title": "⚡ July 27 World Politics Update: Saudi Intercepts Iran-Backed Drones Targeting Oil Facilities, Houthis Strike Saudi Oil Corridor, IRGC Turns Back 6 Ships in Hormuz, Trump Warns of Very Strong Military Action if Talks Fail",
        "summary": "⚡ July 27 world politics live update: Saudi air defenses intercept multiple Iran-backed militia drones targeting oil facilities in Eastern Province and Riyadh; Houthis separately claim drone strikes on Saudi crude oil transport corridor; Iran Revolutionary Guard fires warning shots to turn back 6 vessels in Strait of Hormuz; President Trump tells Axios US and Iran are in very deep talks but warns of very strong military action if diplomacy fails; Netanyahu departs secretly from military base amid Iranian security threat.",
        "tags": ["World Politics", "Saudi Arabia", "Iran", "Houthis", "Strait of Hormuz", "US-Iran War", "Trump", "Netanyahu"],
        "file": "posts/415-saudi-drone-attacks-houthi-oil-iran-guards-hormuz-trump-netanyahu-july-27-2026.en.html"
    }
}

posts.insert(0, new_post)

with open('/home/admin/.hermes/projects/ai-daily/posts.json', 'w') as f:
    json.dump(posts, f, ensure_ascii=False, indent=2)

print("posts.json updated successfully")

# ===== 2. Update rss.xml =====
now = time.gmtime()
last_build = formatdate(timeval=time.mktime(now), localtime=False, usegmt=True)

rss_item = """    <item>
      <title>⚡ 7月27日国际政治实时动态：沙特拦截伊朗支持武装无人机袭击石油设施、胡塞武装红海再起波澜、伊朗革命卫队霍尔木兹海峡拦截6艘商船、特朗普警告谈判失败将恢复强有力军事行动</title>
      <link>https://ai-daily.cc.cd/posts/415-saudi-drone-attacks-houthi-oil-iran-guards-hormuz-trump-netanyahu-july-27-2026.zh.html</link>
      <description>⚡ 7月27日国际政治实时动态：沙特阿拉伯防空部队拦截多架从伊拉克发射的伊朗支持武装无人机目标直指东部省份和利雅得石油设施；胡塞武装同步声称袭击沙特原油运输走廊；伊朗革命卫队在霍尔木兹海峡鸣枪拦截6艘商船；特朗普接受Axios专访称美伊正进行非常深入的谈判警告若失败将恢复非常强力的军事行动；内塔尼亚胡因安全威胁秘密从军事基地启程赴华盛顿。</description>
      <pubDate>""" + last_build + """</pubDate>
      <guid>https://ai-daily.cc.cd/posts/415-saudi-drone-attacks-houthi-oil-iran-guards-hormuz-trump-netanyahu-july-27-2026.zh.html</guid>
    </item>"""

with open('/home/admin/.hermes/projects/ai-daily/rss.xml', 'r') as f:
    rss_content = f.read()

# Update lastBuildDate
rss_content = re.sub(
    r'<lastBuildDate>[^<]+</lastBuildDate>',
    '<lastBuildDate>' + last_build + '</lastBuildDate>',
    rss_content
)

# Insert new item before the first <item>
rss_content = rss_content.replace(
    '    <item>\n',
    rss_item + '\n\n    <item>\n',
    1
)

with open('/home/admin/.hermes/projects/ai-daily/rss.xml', 'w') as f:
    f.write(rss_content)

print("rss.xml updated successfully - lastBuildDate:", last_build)

# ===== 3. Update sitemap.xml =====
sitemap_urls = """  <url>
    <loc>https://ai-daily.cc.cd/posts/415-saudi-drone-attacks-houthi-oil-iran-guards-hormuz-trump-netanyahu-july-27-2026.zh.html</loc>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://ai-daily.cc.cd/posts/415-saudi-drone-attacks-houthi-oil-iran-guards-hormuz-trump-netanyahu-july-27-2026.en.html</loc>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>"""

with open('/home/admin/.hermes/projects/ai-daily/sitemap.xml', 'r') as f:
    sitemap_content = f.read()

sitemap_content = sitemap_content.replace('</urlset>', sitemap_urls + '\n</urlset>')

with open('/home/admin/.hermes/projects/ai-daily/sitemap.xml', 'w') as f:
    f.write(sitemap_content)

print("sitemap.xml updated successfully")
print("\nAll files updated!")
