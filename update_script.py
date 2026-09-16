import os
import json
from google import genai
from google.genai import types

def generate_news_data():
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    prompt = """
    請扮演頂尖網路媒體總編輯與流量成長專家。
    請利用 Google 搜尋工具，針對今日（2026年9月）台灣與全球的最新動態，針對以下 15 個媒體搜尋並產生一組結構化的 JSON 內容。
    
    【核心選題方向】：
    請引導內容鎖定以下五大熱門領域：
    1. AI 科技應用（最新 AI 潮流、工具、對消費者衝擊）
    2. 政治動態與年底選舉（2026年台灣縣市長及議員選舉、政壇熱話）
    3. 健康保健（實用養生、醫療新知）
    4. 旅遊休閒（熱門旅遊景點、攻略）
    5. 賺錢流量（理財投資、副業、商業趨勢）
    
    JSON 的根物件必須包含以下 15 個媒體的 key（英文 ID）：
    - economic (經濟日報)
    - commercial (工商時報)
    - united (聯合報)
    - freedom (自由時報)
    - china (中國時報)
    - ettoday (ETtoday新聞雲)
    - tvbs (TVBS新聞網)
    - cti (中天新聞網)
    - digitimes (數位時代)
    - manager (經理人)
    - futureweb (未來商務)
    - hbr (哈佛商業評論)
    - cw (天下雜誌)
    - bwnet (商業周刊)
    - twreporter (報導者)

    每一個媒體物件必須包含以下欄位：
    1. "name": 媒體中文名稱
    2. "headline": 今日該媒體的頭條焦點標題
    3. "analysis": 對該頭條內容的深度解析（約 60-100 字）
    4. "diffSummary": 跨媒體視角差異的說明引言
    5. "tableData": 陣列，包含 2 到 3 個物件，每個物件有 "type" 與 "angle"
    6. "exclusive": 獨家與市場共振判定
    7. "summaryText": 【焦點摘要與引文】的詳細內文（約 100-150 字）
    8. "url": ⚠️ 必須透過 Google 搜尋找出該篇頭條新聞的「真實單篇報導網址」。

    請確保輸出為純 JSON 格式。
    """

    response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.7,
            response_mime_type="application/json",
            tools=[{"google_search": {}}],
        ),
    )
    return response.text

def main():
    try:
        json_str = generate_news_data()
        parsed_data = json.loads(json_str)
        with open("news.json", "w", encoding="utf-8") as f:
            json.dump(parsed_data, f, ensure_ascii=False, indent=4)
        print("成功更新 news.json！")
    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == "__main__":
    main()