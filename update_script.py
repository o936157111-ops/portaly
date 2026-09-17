import os
import json
from google import genai

def update_news():
    # 檢查 API Key 是否存在
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("找不到 GEMINI_API_KEY 環境變數，請確認 GitHub Secrets 是否設定正確。")

    # 初始化 Google GenAI Client
    client = genai.Client(api_key=api_key)

    # 提示詞，請依您的需求調整
    prompt = "請幫我整理今天最新的重要科技或相關新聞摘要，並以 JSON 格式輸出（包含標題與連結或內文摘要）。"

    # 呼叫 Gemini 模型（使用 gemini-3.6-flash）
    response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents=prompt,
    )

    news_content = response.text
    print("成功取得 AI 回應內容")

    # 儲存為 news.json
    data = {
        "updated_at": os.popen("date -u +'%Y-%m-%d %H:%M:%S'").read().strip(),
        "content": news_content
    }

    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print("news.json 更新成功")

if __name__ == "__main__":
    update_news()
