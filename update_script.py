import os
import json
from google import genai
from google.genai import types

def generate_media_bias_analysis():
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    # 定義結構，讓每個視角都有獨立的 searchQuery 欄位
    schema = {
        "type": "OBJECT",
        "properties": {
            "events": {
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "eventId": {"type": "STRING"},
                        "eventTitle": {"type": "STRING"},
                        "coreFacts": {"type": "STRING"},
                        "perspectives": {
                            "type": "ARRAY",
                            "items": {
                                "type": "OBJECT",
                                "properties": {
                                    "groupName": {"type": "STRING"},
                                    "focus": {"type": "STRING"},
                                    "blindspot": {"type": "STRING"},
                                    "searchQuery": {"type": "STRING", "description": "專為 Google 新聞設計的精簡搜尋關鍵字，結合核心事件與該視角面向（例如：'AI應用 職場 轉型' 或 '淨零碳排 成本 衝擊'），確保在 Google 新聞搜尋時絕對找得到豐富報導"}
                                },
                                "required": ["groupName", "focus", "blindspot", "searchQuery"]
                            }
                        },
                        "neutralSummary": {"type": "STRING"}
                    },
                    "required": ["eventId", "eventTitle", "coreFacts", "perspectives", "neutralSummary"]
                }
            }
        },
        "required": ["events"]
    }

    prompt = """
    請扮演頂尖的跨領域媒體分析師與輿情解讀專家。
    請利用 Google 搜尋工具，找出今日（2026年9月）台灣社會最受矚目、最具代表性的 3 個重大焦點議題。

    針對每一個議題，請進行深入的「多維度事件解析」：
    1. 必須包含 3 種不同切入面或立場群體（例如：「產經專業視角」、「社會民意視角」、「政策推動視角」）。
    2. 【極重要】針對每一個視角，除了提供聚焦與延伸視角外，必須在 "searchQuery" 欄位提供一組專門用來在 Google 新聞搜尋的精簡關鍵字（建議 3 到 5 個字元組合，如：事件主旨＋立場關鍵字），絕對不能空白，且三個視角的關鍵字必須各有側重，不可重複，以確保使用者點擊時能精準且順利地找到對應新聞。
    """

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.7,
            response_mime_type="application/json",
            response_schema=schema,
            tools=[{"google_search": {}}],
        ),
    )
    return response.text

def main():
    try:
        json_str = generate_media_bias_analysis()
        parsed_data = json.loads(json_str)
        with open("news.json", "w", encoding="utf-8") as f:
            json.dump(parsed_data, f, ensure_ascii=False, indent=4)
        print("成功更新多維度解析資料 (news.json)！")
    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == "__main__":
    main()
