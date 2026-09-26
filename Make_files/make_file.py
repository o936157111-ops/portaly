# make_file.py
lt = chr(60)
gt = chr(62)

html_content = f"""{lt}!DOCTYPE html{gt}
{lt}html lang="zh-Hant"{gt}
{lt}head{gt}
    {lt}meta charset="UTF-8"{gt}
    {lt}meta name="viewport" content="width=device-width, initial-scale=1.0"{gt}
    {lt}title{gt}全方位熱門焦點情報站{lt}/title{gt}
    {lt}style{gt}
        :root {{
            --primary-color: #2563eb;
            --bg-color: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #1e293b;
            --text-secondary: #64748b;
            --border-color: #e2e8f0;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: sans-serif; }}
        body {{ background-color: var(--bg-color); color: var(--text-main); line-height: 1.6; padding: 16px; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        header {{ text-align: center; margin-bottom: 24px; }}
        header h1 {{ font-size: 1.5rem; color: var(--text-main); margin-bottom: 6px; }}
        header p {{ font-size: 0.9rem; color: var(--text-secondary); }}
        .category-scroll-container {{ display: flex; justify-content: center; gap: 12px; flex-wrap: wrap; margin-bottom: 16px; }}
        .category-btn {{ padding: 8px 18px; font-size: 0.9rem; font-weight: 600; border: 1px solid var(--border-color); background: #fff; color: var(--text-secondary); border-radius: 20px; cursor: pointer; }}
        .category-btn.active {{ background: var(--primary-color); color: #fff; border-color: var(--primary-color); }}
        .nav-pagination {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }}
        .nav-btn {{ background: #fff; border: 1px solid var(--border-color); padding: 8px 16px; border-radius: 8px; cursor: pointer; }}
        .nav-btn:disabled {{ opacity: 0.4; cursor: not-allowed; }}
        .page-indicator {{ font-size: 0.85rem; color: var(--text-secondary); font-weight: 600; }}
        .card {{ background: var(--card-bg); border-radius: 12px; border: 1px solid var(--border-color); padding: 24px; margin-bottom: 20px; }}
        .card-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; border-bottom: 1px solid var(--border-color); padding-bottom: 12px; }}
        .media-badge {{ background: #eff6ff; color: var(--primary-color); padding: 4px 10px; border-radius: 6px; font-size: 0.85rem; font-weight: 700; }}
        .exclusive-badge {{ font-size: 0.75rem; color: #d97706; background: #fef3c7; padding: 4px 10px; border-radius: 6px; font-weight: 600; }}
        .headline {{ font-size: 1.3rem; font-weight: 700; margin-bottom: 14px; }}
        .content-box {{ font-size: 0.95rem; background: #f8fafc; padding: 14px; border-radius: 8px; border-left: 4px solid var(--primary-color); margin-bottom: 12px; }}
        .summary-container {{ margin-top: 16px; border-top: 1px dashed var(--border-color); padding-top: 12px; }}
        .toggle-summary-btn {{ background: none; border: none; color: var(--primary-color); font-weight: 600; cursor: pointer; }}
        .summary-content {{ margin-top: 10px; font-size: 0.9rem; color: var(--text-secondary); background: #f8fafc; padding: 14px; border-radius: 8px; display: none; }}
        .summary-content.show {{ display: block; }}
        .btn-link {{ display: inline-block; background: var(--primary-color); color: #fff; padding: 10px 20px; border-radius: 8px; text-decoration: none; margin-top: 15px; }}
        .loading, .error-msg {{ text-align: center; padding: 40px; color: var(--text-secondary); }}
        .error-msg {{ color: #ef4444; }}
    {lt}/style{gt}
{lt}/head{gt}
{lt}body{gt}
{lt}div class="container"{gt}
    {lt}header{gt}
        {lt}h1{gt}🔥 全方位熱門焦點情報站{lt}/h1{gt}
        {lt}p id="headerSubtitle"{gt}多元新聞與趨勢每日自動彙整{lt}/p{gt}
    {lt}/header{gt}
    {lt}div class="category-scroll-container" id="tabContainer"{gt}{lt}/div{gt}
    {lt}div class="nav-pagination"{gt}
        {lt}button class="nav-btn" id="prevBtn" onclick="changePage(-1)"{gt}◀ 上一則{lt}/button{gt}
        {lt}span class="page-indicator" id="pageIndicator"{gt}1 / 4{lt}/span{gt}
        {lt}button class="nav-btn" id="nextBtn" onclick="changePage(1)"{gt}下一則 ▶{lt}/button{gt}
    {lt}/div{gt}
    {lt}div id="newsCardContainer"{gt}
        {lt}div class="loading"{gt}正在讀取最新情報資料...{lt}/div{gt}
    {lt}/div{gt}
{lt}/div{gt}

{lt}script{gt}
    let newsDatabase = {{ date: "", topics: [] }};
    let currentTopicIndex = 0;
    let currentIndex = 0;

    window.addEventListener('DOMContentLoaded', async () => {{
        try {{
            const response = await fetch('news.json');
            if (!response.ok) throw new Error('無法讀取 news.json');
            newsDatabase = await response.json();
            initNewsApp();
        }} catch (error) {{
            document.getElementById('newsCardContainer').innerHTML = '{lt}div class="error-msg"{gt}⚠️ 尚無解析資料或格式錯誤。{lt}/div{gt}';
        }}
    }});

    function initNewsApp() {{
        const subtitle = document.getElementById('headerSubtitle');
        if (subtitle) subtitle.textContent = `多元即時情報（更新日期：${{newsDatabase.date || '今日'}}）`;
        if (newsDatabase.topics && newsDatabase.topics.length > 0) {{
            currentTopicIndex = 0;
            currentIndex = 0;
            renderAll();
        }}
    }}

    function switchTopic(topicIndex) {{
        currentTopicIndex = topicIndex;
        currentIndex = 0; 
        renderAll();
    }}

    function changePage(direction) {{
        const currentArticles = newsDatabase.topics[currentTopicIndex].articles;
        if (!currentArticles) return;
        currentIndex += direction;
        if (currentIndex < 0) currentIndex = 0;
        if (currentIndex >= currentArticles.length) currentIndex = currentArticles.length - 1;
        renderCurrentView();
    }}

    function renderAll() {{
        renderTabs();
        renderCurrentView();
    }}

    function renderTabs() {{
        const tabContainer = document.getElementById('tabContainer');
        tabContainer.innerHTML = '';
        newsDatabase.topics.forEach((topic, index) => {{
            const btn = document.createElement('button');
            btn.className = `category-btn ${{index === currentTopicIndex ? 'active' : ''}}`;
            btn.textContent = topic.topicName;
            btn.onclick = () => switchTopic(index);
            tabContainer.appendChild(btn);
        }});
    }}

    function renderCurrentView() {{
        const currentTopic = newsDatabase.topics[currentTopicIndex];
        const articles = currentTopic.articles;
        const currentItem = articles[currentIndex];

        document.getElementById('pageIndicator').textContent = `\({{currentIndex + 1}} /\){{articles.length}}`;
        document.getElementById('prevBtn').disabled = (currentIndex === 0);
        document.getElementById('nextBtn').disabled = (currentIndex === articles.length - 1);

        const container = document.getElementById('newsCardContainer');
        const googleSearchUrl = `https://www.google.com/search?q=${{encodeURIComponent(currentItem.title)}}`;

        container.innerHTML = `
            {lt}div class="card"{gt}
                {lt}div class="card-header"{gt}
                    {lt}span class="media-badge"{gt}來源：${{currentItem.source || '專業媒體'}}{lt}/span{gt}
                    {lt}span class="exclusive-badge"{gt}分類：${{currentTopic.topicName}}{lt}/span{gt}
                {lt}/div{gt}
                {lt}h2 class="headline"{gt}${{currentItem.title || '無標題'}}{lt}/h2{gt}
                {lt}div class="section-title"{gt}💡 內容摘要{lt}/div{gt}
                {lt}div class="content-box"{gt}${{currentItem.summary || '暫無摘要'}}{lt}/div{gt}
                {lt}div class="summary-container"{gt}
                    {lt}button class="toggle-summary-btn" onclick="toggleSummary(this)"{gt}
                        {lt}span{gt}▶ 展開詳細焦點摘要與引文{lt}/span{gt}
                    {lt}/button{gt}
                    {lt}div class="summary-content"{gt}
                        {lt}strong{gt}【焦點深度解讀】{lt}/strong{gt}{lt}br{gt}
                        本則報導由 {lt}strong{gt}\({{currentItem.source}}{lt}/strong{gt} 提供，針對「\){{currentItem.title}}」進行即時追蹤。{lt}br{gt}{lt}br{gt}
                        {lt}em{gt}原始摘要內容：{lt}/em{gt}${{currentItem.summary}}
                    {lt}/div{gt}
                {lt}/div{gt}
                {lt}div class="external-link-container"{gt}
                    {lt}a href="${{googleSearchUrl}}" target="_blank" class="btn-link"{gt}🔍 Google 相關新聞搜尋 ↗{lt}/a{gt}
                {lt}/div{gt}
            {lt}/div{gt}
        `;
    }}

    function toggleSummary(btn) {{
        const content = btn.nextElementSibling;
        const isShown = content.classList.contains('show');
        if (isShown) {{
            content.classList.remove('show');
            btn.querySelector('span').textContent = '▶ 展開詳細焦點摘要與引文';
        }} else {{
            content.classList.add('show');
            btn.querySelector('span').textContent = '▼ 收合詳細焦點摘要與引文';
        }}
    }}
{lt}/script{gt}
{lt}/body{gt}
{lt}/html{gt}
"""

with open("index_news.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("成功生成 index_news.html 檔案！")
