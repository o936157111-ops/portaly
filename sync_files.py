# sync_files.py

source_file = "index.html"
target_file = "index_python.html"

try:
    # 以讀取模式開啟來源檔案，並以寫入模式開啟目標檔案 (指定 UTF-8 編碼避免亂碼)
    with open(source_file, "r", encoding="utf-8") as src:
        content = src.read()

    with open(target_file, "w", encoding="utf-8") as tgt:
        tgt.write(content)

    print(f"成功！已將 {source_file} 的內容同步到 {target_file}")

except FileNotFoundError:
    print("找不到指定的檔案，請確認檔案名稱與路徑是否正確。")