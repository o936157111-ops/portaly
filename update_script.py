import os
import json
import re
from google import genai

def update_news():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("找不到 GEMINI_API_KEY 環境變數，請確認 GitHub Secrets 是否設定正確。")

    client = genai.Client(api_key=api_key)

    # 提示詞：明確要求 AI 只輸出純 JSON，不要包在 markdown 裡面
    prompt = """請幫我整理今天最新的重要科技或相關新聞摘要。
請務必直接輸出純 JSON 格式（不要包含 ```json 或其他 markdown 語法），結構必須包含：
{
  "date": "YYYY-MM-DD",
  "category": "科技新聞摘要",
  "total_articles": 數量,
  "articles": [
    {
      "id": 1,
      "title": "標題",
      "category": "分類",
      "summary": "摘要",
      "source": "來源",
      "url": "網址"
    }
  ]
}"""

    response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents=prompt,
    )

    raw_text = response.text.strip()
    print("成功取得 AI 回應內容")

    # 清理可能被帶入的 Markdown 程式碼區塊標記 (```json ... ```)
    cleaned_text = re.sub(r'^```json\s*', '', raw_text, flags=re.IGNORECASE)
    cleaned_text = re.sub(r'^```\s*', '', cleaned_text, flags=re.IGNORECASE)
    cleaned_text = re.sub(r'\s*```$', '', cleaned_text)

    try:
        # 嘗試將 AI 回應解析為標準 JSON 物件
        news_data = json.loads(cleaned_text)
    except json.JSONDecodeError as e:
        print(f"解析 AI 產生的 JSON 失敗: {e}")
        print(f"原始內容為: {raw_text}")
        raise e

    # 直接將正確的 JSON 結構寫入 news.json
    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(news_data, f, ensure_ascii=False, indent=4)
    
    print("news.json 更新成功，格式正確！")

if __name__ == "__main__":
    update_news()
