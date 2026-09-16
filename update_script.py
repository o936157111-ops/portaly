prompt = """
    請扮演頂尖網路媒體總編輯與流量成長專家。
    請利用 Google 搜尋工具，針對今日（2026年9月）台灣與全球的最新動態，針對以下 15 個媒體搜尋並產生一組結構化的 JSON 內容。
    
    【核心選題與內容導向】：
    請鎖定以下五大最容易吸引消費者眼球的熱門話題：
    1. AI 科技應用（最新 AI 潮流、工具、對日常與消費者的衝擊）
    2. 政治動態與年底選舉（2026年台灣縣市長及議員選舉、政壇熱話）
    3. 健康保健（實用養生、醫療新知、日常健康防護）
    4. 旅遊休閒（熱門旅遊景點、機票優惠、在地玩樂攻略）
    5. 賺錢賺流量（理財投資、副業、賺錢流量密碼與商業趨勢）
    
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
    2. "headline": 今日該媒體的頭條焦點標題（必須融合上述五大主題之一，具備強烈吸引力與痛點共鳴）
    3. "analysis": 對該頭條內容的深度解析與大眾解讀（約 60-100 字）
    4. "diffSummary": 跨媒體視角差異的說明引言
    5. "tableData": 陣列，包含 2 到 3 個物件，每個物件有 "type"（媒體類型）與 "angle"（切入角度與盲點差異）
    6. "exclusive": 獨家與市場共振判定（例如：「非獨家（市場高度共振焦點）」或「獨家產業深度追蹤」）
    7. "summaryText": 【焦點摘要與引文】的詳細內文（約 100-150 字）
    8. "url": ⚠️【非常重要】必須透過 Google 搜尋找出該篇頭條新聞的「真實單篇報導網址」（絕對不能只填各媒體的官網首頁）。

    請確保輸出為純 JSON 格式，且內容不可包含任何未跳脫的特殊字元。
    """
```[cite: 3]

---

### 第二步：修改 `index_news_2.html` 的前端分類與按鈕
為了讓前端網頁的按鈕跟這五大新話題契合，我們需要調整上方頁籤的分類名稱。

請找到 `index_news_2.html` 中的 `<div class="category-scroll-container">` 與底部的 `categories` 物件，將其改為對應**「AI 科技、政治選舉、健康保健、旅遊休閒、賺錢流量」**的分類：

#### 1. 修改 HTML 頁籤按鈕：
```html
            <!-- 五大熱門主題頁籤列 -->
            <div class="category-scroll-container">
                <button class="category-btn active" onclick="switchCategory('ai')" id="cat-ai">🤖 AI 科技熱話</button>
                <button class="category-btn" onclick="switchCategory('politics')" id="cat-politics">🗳️ 年底選舉政治</button>
                <button class="category-btn" onclick="switchCategory('health')" id="cat-health">🍎 健康保健養生</button>
                <button class="category-btn" onclick="switchCategory('travel')" id="cat-travel">✈️ 旅遊休閒攻略</button>
                <button class="category-btn" onclick="switchCategory('wealth')" id="cat-wealth">💰 賺錢流量密碼</button>
            </div>
```[cite: 5]

#### 2. 修改 JavaScript 中的 `categories` 資料結構：
你可以把原本的媒體重新分配到這五大新分類底下（讓每個分類都有對應的媒體可以點選）：

```javascript
        const categories = {
            ai: {
                name: "AI 科技熱話",
                options: [
                    { id: "digitimes", label: "數位時代 (AI 創新)" },
                    { id: "futureweb", label: "未來商務 (科技應用)" },
                    { id: "ettoday", label: "ETtoday (生活科技)" }
                ]
            },
            politics: {
                name: "年底選舉政治",
                options: [
                    { id: "united", label: "聯合報 (政經動態)" },
                    { id: "china", label: "中國時報 (選情觀察)" },
                    { id: "cti", label: "中天新聞網 (政治焦點)" }
                ]
            },
            health: {
                name: "健康保健養生",
                options: [
                    { id: "tvbs", label: "TVBS新聞網 (健康醫療)" },
                    { id: "cw", label: "天下雜誌 (生活福祉)" }
                ]
            },
            travel: {
                name: "旅遊休閒攻略",
                options: [
                    { id: "freedom", label: "自由時報 (旅遊生活)" },
                    { id: "bwnet", label: "商業周刊 (休閒品味)" }
                ]
            },
            wealth: {
                name: "賺錢流量密碼",
                options: [
                    { id: "economic", label: "經濟日報 (投資理財)" },
                    { id: "commercial", label: "工商時報 (致富商機)" },
                    { id: "manager", label: "經理人 (職場加薪)" },
                    { id: "hbr", label: "哈佛商業評論 (高階策略)" },
                    { id: "twreporter", label: "報導者 (深度調查)" }
                ]
            }
        };
```[cite: 5]

---

### 這樣改完之後會發生什麼事？
1. **GitHub Actions 每天自動執行**時，Gemini 會上網搜尋這五大主題（AI、選舉、健康、旅遊、賺錢）當天各大媒體最新鮮、最吸睛的頭條報導[cite: 3, 4]。
2. **前端網頁（`index_news_2.html`）**的選單會直接對應這五大高流量領域，讀者一進到你的網站，就能一眼看出這是專門為他們整理的熱門焦點[cite: 5]。

你覺得這樣的主題分類設定，是不是更貼近你想要打造的高人氣吸引力網站呢？