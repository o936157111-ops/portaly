import json
import requests
from bs4 import BeautifulSoup

# 定義要自動抓取的媒體清單與設定（已完全移除 ustv 非凡新聞）
MEDIA_CONFIG = {
    "economic": {"name": "經濟日報", "url": "https://money.udn.com/money/index"},
    "commercial": {"name": "工商時報", "url": "https://ctee.com.tw/"},
    "united": {"name": "聯合報", "url": "https://udn.com/news/index"},
    "freedom": {"name": "自由時報", "url": "https://news.ltn.com.tw/"},
    "china": {"name": "中國時報", "url": "https://www.chinatimes.com/"},
    # "ustv": 已經在此處移除，不會再被抓取與輸出
    "ettoday": {"name": "ETtoday新聞雲", "url": "https://www.ettoday.net/"},
    "tvbs": {"name": "TVBS新聞網", "url": "https://news.tvbs.com.tw/"},
    "cti": {"name": "中天新聞網", "url": "https://ctinews.com/"},
    "digitimes": {"name": "數位時代", "url": "https://www.bnext.com.tw/"},
    "manager": {"name": "經理人", "url": "https://www.managertoday.com.tw/"},
    "futureweb": {"name": "未來商務", "url": "https://www.futurecity.express.urbreaking.com/"},
    "hbr": {"name": "哈佛商業評論", "url": "https://www.hbrtaiwan.com/"},
    "cw": {"name": "天下雜誌", "url": "https://www.cw.com.tw/"},
    "bwnet": {"name": "商業周刊", "url": "https://www.businessweekly.com.tw/"},
    "twreporter": {"name": "報導者", "url": "https://www.twreporter.org/"}
}

def fetch_news_data():
    news_database = {}
    
    for media_id, info in MEDIA_CONFIG.items():
        print(f"正在處理：{info['name']}...")
        
        # 這裡放置您的抓取與解析邏輯 (BeautifulSoup / API 等)
        # 產出符合前端結構的字典資料
        news_database[media_id] = {
            "name": info["name"],
            "headline": f"【每日焦點】{info['name']} 即時頭條新聞主旨內容",
            "analysis": f"這是自動化排程針對 {info['name']} 當日新聞所進行的結構化深度分析與觀點提煉。",
            "diffSummary": "各主流媒體在該議題的報導上，受眾定位與側重點各有不同。",
            "tableData": [
                {"type": "產業與財經觀點", "angle": "著重於市場鏈結、趨勢與實質影響。"},
                {"type": "社會與大眾觀點", "angle": "聚焦於大眾有感層面與後續追蹤。"}
            ],
            "exclusive": "市場共振度：高",
            "summaryText": f"這是來自 {info['name']} 的詳細報導摘要與重點引文說明..."
        }

    # 輸出為前端所讀取的 news.json
    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(news_database, f, ensure_ascii=False, indent=4)
    
    print("成功更新 news.json，且已排除非凡新聞！")

if __name__ == "__main__":
    fetch_news_data()
