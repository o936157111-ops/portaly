import os
import json
import re
import time
from datetime import datetime, timedelta, timezone
from google import genai
from google.genai.errors import ServerError

def update_news_with_retry(client, model_name, contents, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=contents
            )
            return response
        except ServerError as e:
            if attempt < max_retries - 1:
                print(f"遇到伺服器繁忙或異常，正在進行第 {attempt + 1} 次重試... (原因: {e})")
                time.sleep(5)  # 等待 5 秒後重試
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

    prompt = f"""請幫我整理今天（{today_str}）最新的重要焦點新聞，涵蓋以下 6 個類別：
1. 國家大事 (national)
2. 經濟財經 (finance)
3. 社會新聞 (society)
4. 國際新聞 (international)
5. 生活與民生新聞 (life)
6. 體育新聞 (sports)

每個類別請提供 2 則代表性新聞。請務必只輸出標準的 JSON 格式物件（以 {{ 開頭，以 }} 結尾），不要包含任何額外的解釋文字。結構必須嚴格包含：
{{
  "date": "{today_str}",
  "categories": {{
    "national": {{
      "name": "國家大事",
      "articles": [
        {{
          "source": "專業媒體",
          "category": "國家大事",
          "title": "新聞標題1",
          "summary": "摘要內容..."
        }},
        {{
          "source": "專業媒體",
          "category": "國家大事",
          "title": "新聞標題2",
          "summary": "摘要內容..."
        }}
      ]
    }},
    "finance": {{
      "name": "經濟財經",
      "articles": [
        {{
          "source": "專業媒體",
          "category": "經濟財經",
          "title": "新聞標題1",
          "summary": "摘要內容..."
        }},
        {{
          "source": "專業媒體",
          "category": "經濟財經",
          "title": "新聞標題2",
          "summary": "摘要內容..."
        }}
      ]
    }},
    "society": {{
      "name": "社會新聞",
      "articles": [
        {{
          "source": "專業媒體",
          "category": "社會新聞",
          "title": "新聞標題1",
          "summary": "摘要內容..."
        }},
        {{
          "source": "專業媒體",
          "category": "社會新聞",
          "title": "新聞標題2",
          "summary": "摘要內容..."
        }}
      ]
    }},
    "international": {{
      "name": "國際新聞",
      "articles": [
        {{
          "source": "專業媒體",
          "category": "國際新聞",
          "title": "新聞標題1",
          "summary": "摘要內容..."
        }},
        {{
          "source": "專業媒體",
          "category": "國際新聞",
          "title": "新聞標題2",
          "summary": "摘要內容..."
        }}
      ]
    }},
    "life": {{
      "name": "生活與民生新聞",
      "articles": [
        {{
          "source": "專業媒體",
          "category": "生活與民生新聞",
          "title": "新聞標題1",
          "summary": "摘要內容..."
        }},
        {{
          "source": "專業媒體",
          "category": "生活與民生新聞",
          "title": "新聞標題2",
          "summary": "摘要內容..."
        }}
      ]
    }},
    "sports": {{
      "name": "體育新聞",
      "articles": [
        {{
          "source": "專業媒體",
          "category": "體育新聞",
          "title": "新聞標題1",
          "summary": "摘要內容..."
        }},
        {{
          "source": "專業媒體",
          "category": "體育新聞",
          "title": "新聞標題2",
          "summary": "摘要內容..."
        }}
      ]
    }}
  }}
}}"""

    print("正在呼叫 Gemini API 取得最新多類別新聞...")
    response = update_news_with_retry(
        client=client,
        model_name='gemini-2.5-flash',  # 確保使用您順手且支援的模型
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
    
    print(f"news.json 更新成功，已產出 6 大類別的多則焦點新聞，並強制寫入日期: {today_str}")

if __name__ == "__main__":
    update_news()