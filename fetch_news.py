import feedparser
import json
import re

# مصادر الأخبار المحدثة (السياسة، التقنية، وأخبار الأدوية والعلاجات)
FEEDS = {
    "politics": [
        "https://www.skynewsarabia.com/web/rss.xml", 
        "https://arabic.cnn.com/api/v1/rss/middle_east/rss.xml"
    ],
    "tech": [
        "https://aitnews.com/feed/",
        "https://www.tech-wd.com/wd/feed/"
    ],
    "medicines": [
        "https://www.webteb.com/rss/news",                       # أخبار طبية ودوائية من ويب طب
        "https://www.seha.ae/feed/",                            # أخبار العلاجات والرعاية الصحية
        "https://arabic.rt.com/rss/medicine/"                   # أحدث أبحاث الأدوية والاكتشافات الطبية
    ]
}

def calculate_read_time(text):
    clean_text = re.sub(r'<[^>]+>', '', text)
    word_count = len(clean_text.split())
    read_time = max(1, round(word_count / 150))
    return read_time

news_data = {"politics": [], "tech": [], "medicines": []}

for category, urls in FEEDS.items():
    for url in urls:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:10]:
                summary = entry.get('summary', '')
                title = entry.title.strip()
                
                news_data[category].append({
                    "title": title,
                    "link": entry.link,
                    "time": entry.get('published', 'اليوم'),
                    "summary": summary,
                    "read_time": calculate_read_time(summary + " " + title)
                })
        except Exception as e:
            print(f"فشل السحب من المصدر {url}: {e}")

with open('news.json', 'w', encoding='utf-8') as f:
    json.dump(news_data, f, ensure_ascii=False, indent=4)

print("تم تحديث محرك الأخبار وقسم الأدوية بنجاح! 💊")
