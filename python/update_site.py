import os


def generate_html():
  # 定義要展示的圖片與連結資料
  pins = [
      {
          'img': 'https://picsum.photos/300/400?random=1',
          'link': 'https://github.com',
          'alt': '圖片 1',
      },
      {
          'img': 'https://picsum.photos/300/400?random=2',
          'link': 'https://google.com',
          'alt': '圖片 2',
      },
      {
          'img': 'https://picsum.photos/300/400?random=3',
          'link': 'https://python.org',
          'alt': '圖片 3',
      },
  ]

  # 組合 HTML 內容
  html_content = """


    
    
    Python 學習作業 - index_python.html
