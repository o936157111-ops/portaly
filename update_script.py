import os
import json
import re
from datetime import datetime, timedelta, timezone
from google import genai

def update_news():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("找不到 GEMINI_API_KEY 環境變數，請確認 GitHub Secrets 是否設定正確。")

    client = genai.Client(api_key=api_key)

    # 強制設定為台灣時區 (UTC+8)，確保抓到的日期是台灣的「今天」
    tw_timezone = timezone(timedelta(hours=8))
    today_str = datetime.now(tw_timezone).strftime("%Y-%m-%d")

    prompt = f"""請幫我整理今天（{today_str}）最新的重要科技或相關新聞摘要。
請務必只輸出標準的 JSON 格式物件（以 {{ 開頭，以 }} 結尾），不要包含任何額外的解釋文字。結構必須包含：
{{
  "date": "{today_str}",
  "category": "科技新聞摘要",
  "total_articles": 4,
  "articles": [
    {{
      "id": 1,
      "title": "標題",
      "category": "分類",
      "summary": "摘要",
      "source": "來源",
      "url": "網址"
    }}
  ]
}}"""

    response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents=prompt,
    )

    raw_text = response.text.strip()
    print("成功取得 AI 回應內容")

    match = re.search(r'\{[\s\S]*\}', raw_text)
    if not match:
        raise ValueError(f"AI 回應中找不到有效的 JSON 結構，原始內容為:\n{raw_text}")
    
    json_str = match.group(0)

    try:
        news_data = json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"解析 JSON 失敗: {e}")
        print(f"擷取到的文字為:\n{json_str}")
        raise e

    # 【絕對防線】強制將 JSON 內的日期欄位覆蓋為台灣時區的今天，避免 AI 帶入舊日期
    news_data["date"] = today_str

    # 寫入檔案
    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(news_data, f, ensure_ascii=False, indent=4)
    
    print(f"news.json 更新成功，已強制寫入日期: {today_str}")

if __name__ == "__main__":
    update_news()