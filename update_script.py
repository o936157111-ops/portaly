import os
import json
from google import genai
from google.genai import types

def generate_media_bias_analysis():
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    # 定義嚴格的 JSON 結構規範，確保三個視角一定要有各自的 url
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
                                    "url": {"type": "STRING", "description": "該特定視角所對應的真實新聞報導網址，絕對不能空白，且三個視角的網址必須不同"}
                                },
                                "required": ["groupName", "focus", "blindspot", "url"]
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
    2. 【極重要】每一種觀點（perspective）都必須透過 Google 搜尋找出該視角對應的**真實、獨立新聞報導網址**填入 "url" 欄位中。產經視角找經濟/工商等財經報導，社會視角找大眾媒體，政策視角找政策公告或主流政經媒體。絕對不能讓三個視角的 url 互相重複或空白。
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