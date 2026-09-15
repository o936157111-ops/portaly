import json
import os
from google import genai

# 使用 GitHub Secrets 帶入你的 Gemini API Key
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def generate_daily_news():
    print("正在呼叫 Gemini 生成今日各媒體頭條與深度解析（包含非凡新聞）...")
    
    # 完整的提示詞，明確要求 AI 輸出包含 ustv 在內的完整 JSON
    prompt = """
    請扮演專業的全媒體與商管洞察分析師。請針對今日（2026年最新）台灣各大主流財經、實體大報、電子媒體及商管科技媒體，生成一份完整的 JSON 格式資料。
    
    必須包含以下所有的媒體 ID（Key）：
    - 傳統實體大報：economic（經濟日報）, commercial（工商時報）, united（聯合報）, freedom（自由時報）, china（中國時報）
    - 主流電子媒體：ustv（非凡新聞）, ettoday（ETtoday新聞雲）, tvbs（TVBS新聞網）, cti（中天新聞網）
    - 商管與科技媒體：digitimes（數位時代）, manager（經理人）, futureweb（未來商務）, hbr（哈佛商業評論）, cw（天下雜誌）, bwnet（商業周刊）
    - 深度獨立調查：twreporter（報導者）

    每一個媒體 ID 的物件內部，必須包含以下精確的 JSON 結構（請用繁體中文回答）：
    {
        "name": "媒體名稱",
        "headline": "今日具代表性的頭條或焦點標題",
        "analysis": "針對該頭條的深度內容解析...",
        "diffSummary": "跨媒體與商管視角差異的總結短評...",
        "tableData": [
            {"type": "對比媒體類型1", "angle": "切入角度與盲點差異1"},
            {"type": "對比媒體類型2", "angle": "切入角度與盲點差異2"}
        ],
        "exclusive": "獨家與市場共振判定標籤文字",
        "summaryText": "詳細的焦點摘要與報導引文內容..."
    }

    【重要規則】：
    1. 只能輸出合法的 JSON 格式文字，不要包在 Markdown 的 ```json 區塊裡面，也不要包含任何多餘的說明文字，確保可以直接被 json.loads 解析。
    2. 特別確認「ustv」（非凡新聞）必須具備上述所有欄位，內容需著重於盤面解盤、影音即時分析與法人資金動向。
    """
    
    try:
        # 呼叫 Gemini 模型（建議使用 gemini-2.5-flash 或 gemini-2.5-pro）
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        raw_text = response.text.strip()
        
        # 移除可能不小心包住的 markdown 標記
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.startswith("```"):
            raw_text = raw_text[3:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
        raw_text = raw_text.strip()

        # 驗證是否為正確的 JSON
        news_data = json.loads(raw_text)
        
        # 寫入至 news.json 檔案
        with open("news.json", "w", encoding="utf-8") as f:
            json.dump(news_data, f, ensure_ascii=False, indent=4)
            
        print("成功！news.json 已更新完成，且包含非凡新聞（ustv）資料。")
        
    except Exception as e:
        print(f"生成或解析新聞資料時發生錯誤：{e}")

if __name__ == "__main__":
    generate_daily_news()
