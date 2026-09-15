import os
import json
from google import genai
from google.genai import types

def generate_news_data():
    # 初始化 Gemini Client (使用最新 google-genai SDK)
    # 請確保已在環境變數中設定 GEMINI_API_KEY，或在此直接帶入金鑰
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    # 定義提示詞，明確要求包含 url 欄位
    prompt = """
    請扮演專業的總體經濟學家、資深財經媒體總編輯與商管策略顧問。
    請針對今日（2026年9月）台灣與全球的最新財經、科技、政經與社會動態，產生一組結構化的 JSON 內容。
    
    JSON 的根物件必須包含以下 16 個媒體的 key（英文 ID）：
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
    5. "tableData": 陣列，包含 2 到 3 個物件，每個物件有 "type"（媒體類型）與 "angle"（切入角度與盲點差異）
    6. "exclusive": 獨家與市場共振判定（例如：「非獨家（市場高度共振焦點）」或「獨家產業深度追蹤」）
    7. "summaryText": 【焦點摘要與引文】的詳細內文（約 100-150 字）
    8. "url": 該頭條新聞或該媒體官網的代表性超連結網址（例如 https://money.udn.com 等有效網址）

    注意：請確保輸出為純 JSON 格式（不要包覆在 markdown 的 ```json 以外，或確保內容能被 json.loads 解析），且內容不可包含任何未跳脫的特殊字元。
    """

    print("正在呼叫 Gemini 生成最新新聞分析與原網站網址...")

    response = client.models.generate_content(
        model='gemini-2.5-flash',  # 建議使用高速且高效的模型
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.7,
            response_mime_type="application/json", # 強制輸出純 JSON
        ),
    )

    return response.text

def main():
    try:
        # 1. 取得 Gemini 生成的 JSON 字串
        json_str = generate_news_data()

        # 2. 驗證是否為正確的 JSON 格式
        parsed_data = json.loads(json_str)

        # 3. 寫入本地的 news.json 檔案
        output_filename = "news.json"
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(parsed_data, f, ensure_ascii=False, indent=4)

        print(f"成功更新！新聞資料與原網站網址已順利寫入 {output_filename}")

    except json.JSONDecodeError as e:
        print(f"解析 Gemini 回傳的 JSON 失敗: {e}")
        print("原始回傳內容：")
        print(json_str)
    except Exception as e:
        print(f"更新過程中發生錯誤: {e}")

if __name__ == "__main__":
    main()
