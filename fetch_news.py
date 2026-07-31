import feedparser
import json
import re

# مصادر الأخبار المحدثة والموسعة لأخبار الجوالات والتسريبات
FEEDS = {
    "politics": [
        "https://www.skynewsarabia.com/web/rss.xml", 
        "https://arabic.cnn.com/api/v1/rss/middle_east/rss.xml"
    ],
    "tech": [
        "https://aitnews.com/feed/",
        "https://www.tech-wd.com/wd/feed/"
    ],
    "mobiles": [
        "https://aitnews.com/category/smartphones/feed/",      # أخبار الجوالات الرسمية
        "https://www.electrony.net/category/%d8%a3%d8%ae%d8%a8%d8%a7%d8%b1-%d8%a7%d9%84%d9%87%d9%88%d8%a7%d8%aa%d9%81-%d8%a7%d9%84%d9%80%d9%85%d8%ad%d9%85%d9%88%d9%84%d8%a9/feed/", # إلكتروني للتسريبات والأخبار
        "https://www.unlimit-tech.com/category/%d9%87%d9%88%d8%a7%d8%aa%d9%81-%d9%85%d8%ad%d9%85%d9%88%d9%84%d8%a9/feed/", # تقنية بلا حدود
        "https://www.sadatech.com/category/smartphones/feed/"   # صدى التقنية للمواصفات والتسريبات
    ]
}

def calculate_read_time(text):
    clean_text = re.sub(r'<[^>]+>', '', text)
    word_count = len(clean_text.split())
    read_time = max(1, round(word_count / 150))
    return read_time

news_data = {"politics": [], "tech": [], "mobiles": []}

for category, urls in FEEDS.items():
    for url in urls:
        try:
            feed = feedparser.parse(url)
            # نأخذ أول 10 أخبار من كل مصدر عشان نضمن تنوع رهيب وتغطية كاملة
            for entry in feed.entries[:10]:
                summary = entry.get('summary', '')
                
                # تنظيف وتنقية العناوين من بعض الرموز الزائدة
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

# ترتيب الأخبار بحيث ما تتكرر إذا كانت من نفس المصدر وخلطها بشكل متناسق
with open('news.json', 'w', encoding='utf-8') as f:
    json.dump(news_data, f, ensure_ascii=False, indent=4)

print("تم تحديث محرك الأخبار والتسريبات الأسطوري بنجاح! 🚀")
