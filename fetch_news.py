import feedparser
import json
import re

# مصادر الأخبار اللي اخترناها
FEEDS = {
    "politics": [
        "https://www.skynewsarabia.com/web/rss.xml", 
        "https://arabic.cnn.com/api/v1/rss/middle_east/rss.xml"
    ],
    "tech": [
        "https://aitnews.com/feed/"
    ],
    "ai": [
        "https://aitnews.com/category/artificial-intelligence/feed/"
    ]
}

def calculate_read_time(text):
    clean_text = re.sub(r'<[^>]+>', '', text)
    word_count = len(clean_text.split())
    read_time = max(1, round(word_count / 150))
    return read_time

news_data = {"politics": [], "tech": [], "ai": []}

for category, urls in FEEDS.items():
    for url in urls:
        feed = feedparser.parse(url)
        for entry in feed.entries[:15]:
            summary = entry.get('summary', '')
            news_data[category].append({
                "title": entry.title,
                "link": entry.link,
                "time": entry.get('published', 'اليوم'),
                "summary": summary,
                "read_time": calculate_read_time(summary + " " + entry.title)
            })

with open('news.json', 'w', encoding='utf-8') as f:
    json.dump(news_data, f, ensure_ascii=False, indent=4)

print("تم تحديث الأخبار بنجاح!")
