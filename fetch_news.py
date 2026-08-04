import feedparser
import json
import re

# مصادر الأخبار المعتمدة
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
        "https://arabic.cnn.com/api/v1/rss/health/rss.xml",
        "https://arabic.rt.com/rss/health/"
    ]
}

def evaluate_article_length(text):
    # تنظيف النص وعد الكلمات بدقة
    clean_text = re.sub(r'<[^>]+>', '', text)
    word_count = len(clean_text.split())
    
    # تقدير نوع وحجم المقال بناءً على عدد الكلمات
    if word_count < 30:
        return "⚡ قراءة سريعة"
    elif word_count < 60:
        return "⏱️ مقال متوسط"
    else:
        return "📖 مقال مفصل وشامل"

news_data = {"politics": [], "tech": [], "medicines": []}

for category, urls in FEEDS.items():
    for url in urls:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:12]:
                summary = entry.get('summary', '')
                title = entry.title.strip()
                full_text = summary + " " + title
                
                news_data[category].append({
                    "title": title,
                    "link": entry.link,
                    "time": entry.get('published', 'اليوم'),
                    "summary": summary,
                    "read_label": evaluate_article_length(full_text)
                })
        except Exception as e:
            print(f"خطأ في السحب: {e}")

with open('news.json', 'w', encoding='utf-8') as f:
    json.dump(news_data, f, ensure_ascii=False, indent=4)

print("تم تقييم أحجام المقالات وتحديث الأخبار بنجاح! 🚀")
