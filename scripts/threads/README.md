# 日檢手帖 Threads 每日自動發文系統

每日固定發布 **5 則專欄貼文 ＋ 2 則同串自動解答回覆**，每則貼文結尾固定署名：

```text
日檢手帖 - 日檢 JLPT 自學網站 👉 jlpt.chiaoban.com
```

---

## 📅 每日時刻表（台北時間 UTC+8）

| 時間 | 專欄開頭 | 內容與接地來源 |
|---|---|---|
| **08:00** | `📖 每日五單字｜日檢手帖陪你背單字` | 從 `src/data/vocabulary/n1..n5.json` 同分類挑 5 個不重複單字，附逐字振假名與例句 |
| **12:30** | `✏️ 今日一題｜日檢手帖陪你練手感` | N4／N5 基礎單選題（15:30 自動於同串底下回覆 `【解答公布】`） |
| **15:30** | `🔍 每日文法｜日檢手帖陪你拆句型` | 從 `src/data/grammar/n1..n4.json` 528 個文法點拆解接續、語意、真例句與考試陷阱 |
| **18:30** | `🍂 今日一句｜日檢手帖陪你學道地日文` | 依 `src/data/threads/calendar.json` 隔日輪替「當月季節道地招呼句」與「日本經典格言／慣用句」 |
| **21:00** | `🌙 睡前一題｜日檢手帖陪你衝高分` | N1～N3 進階陷阱題（23:57 自動於同串底下回覆 `【解答公布】`） |

---

## 🛠️ 本機指令（零外部套件依賴，直接用 `python3`）

```bash
# 1. 乾跑預覽今天全部 5 則貼文 ＋ 2 則解答回覆（不會發到 Threads）
python3 scripts/threads/publish.py --slot all --dry-run

# 2. 產生一週 35 則貼文佇列與 Markdown 審稿預覽檔
python3 scripts/threads/generate_week.py --start 2026-09-21 --days 7
```

產生的週佇列與預覽檔位於 `content/threads-queue/YYYY-Www.json` 與 `YYYY-Www.md`。你隨時可以直接編輯 `.json` 裡的文字，發送器會優先使用你改過的版本。

---

## 🔑 啟用正式自動發文（GitHub Secrets 設定）

在未設定 Secrets 前，GitHub Actions 會自動以 `--dry-run` 乾跑模式執行，不會報錯也不會實際發文。
準備好正式發文時，到 GitHub repo 的 **Settings → Secrets and variables → Actions** 新增：

| Secret 名稱 | 必填 | 說明 |
|---|---|---|
| `THREADS_USER_ID` | ✅ 必填 | 你的 Threads 帳號 User ID（可由 `GET https://graph.threads.net/v1.0/me?access_token=...` 查得） |
| `THREADS_ACCESS_TOKEN` | ✅ 必填 | 60 天長期 Access Token（需勾選 `threads_basic`、`threads_content_publish`、`threads_manage_insights` 權限；每週 workflow 會自動呼叫 `refresh_access_token` 續期） |
| `GEMINI_API_KEY` | 選填 | Google AI Studio API Key。設定後，每週生成器會額外啟動「三道驗證關卡」全新出題；未設定時自動使用 repo 內人工驗證過的 1,584 題題庫與 528 個文法點 |
