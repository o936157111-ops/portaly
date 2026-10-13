import os
import json
import re
import time
from datetime import datetime, timedelta, timezone
from google import genai
from google.genai.errors import ServerError

def update_news_with_retry(client, model_name, contents, max_retries=5):
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=contents
            )
            return response
        except ServerError as e:
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 10  # 遞增等待時間：10秒、20秒、30秒...
                print(f"遇到伺服器繁忙 (503)，正在進行第 {attempt + 1} 次重試，等待 {wait_time} 秒... (原因: {e})")
                time.sleep(wait_time)
            else:
                raise e

def update_news():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("找不到 GEMINI_API_KEY 環境變數，請確認 GitHub Secrets 是否設定正確。")

    client = genai.Client(api_key=api_key)

    # 強制設定為台灣時區 (UTC+8)，確保抓到的日期是台灣的「今天」
    tw_timezone = timezone(timedelta(hours=8))
    today_str = datetime.now(tw_timezone).strftime("%Y-%m-%d")

    prompt = f"""請幫我整理今天（{today_str}）最新的重要焦點新聞，總共必須涵蓋以下 8 個類別：
1. 科技新聞 (tech)
2. 娛樂新聞 (entertainment)
3. 國家大事 (national)
4. 經濟財經 (finance)
5. 社會新聞 (society)
6. 國際新聞 (international)
7. 生活與民生新聞 (life)
8. 體育新聞 (sports)

【非常重要規定】
1. 每一個類別底下都必須確實提供 4 則代表性新聞！總共會有 32 則新聞。
2. 每一則新聞除了「source」、「category」、「title」、「summary」之外，還必須包含一個「analysis」物件，裡面詳細填寫三個欄位：
   - "context": 事件的核心脈絡或背景說明。
   - "trend": 該事件所帶動的未來產業發展趨勢。
   - "enterprises": 目前市場上相關的重要企業、供應鏈或發展方向（以具體實際的市場走向描述）。

請務必只輸出標準的 JSON 格式物件（以 {{ 開頭，以 }} 結尾），不要包含任何額外的解釋文字。結構必須嚴格包含：
{{
  "date": "{today_str}",
  "categories": {{
    "tech": {{
      "name": "科技新聞",
      "articles": [
        {{ 
          "source": "專業媒體", 
          "category": "科技新聞", 
          "title": "標題1", 
          "summary": "摘要...",
          "analysis": {{
            "context": "事件核心脈絡背景...",
            "trend": "未來產業發展趨勢...",
            "enterprises": "相關企業與市場發展方向..."
          }}
        }}
      ]
    }}
  }}
}}
（註：請依上述結構，將 8 大類別、每類 4 則新聞完整產出，確保每一則新聞都有完整的 analysis 結構）"""

    print("正在呼叫 Gemini API 取得完整 8 大類別（每類 4 則）新聞與深度脈絡分析...")
    response = update_news_with_retry(
        client=client,
        model_name='gemini-1.5-flash',
        contents=prompt
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

    # 【絕對防線】強制將 JSON 內的日期欄位覆蓋為台灣時區的今天
    news_data["date"] = today_str

    # 寫入檔案
    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(news_data, f, ensure_ascii=False, indent=4)
    
    print(f"news.json 更新成功，已完整產出 8 大類別（附帶深度脈絡與趨勢分析），並強制寫入日期: {today_str}")

if __name__ == "__main__":
    update_news()
