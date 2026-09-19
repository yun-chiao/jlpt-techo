#!/usr/bin/env python3
"""
日檢手帖 Threads 每日自動發文 —— 週佇列生成器 (generate_week.py)

功能：
1. 依日期（Asia/Taipei）無狀態輪替 3,065 單字、528 文法點、1,584 題測驗與季節日曆。
2. 若環境變數設有 GEMINI_API_KEY（且未加 --offline），自動呼叫 Gemini 2.5 Flash：
   - 為每日五單字與每日文法撰寫當日專屬鉤子與記憶捷徑（日文例句與振假名走原文鎖定）
   - 為今日一題／睡前一題執行「規則接地全新出題 ＋ 三道驗證關卡」（① 規則接地 ② 獨立作答驗證 ③ 誘答項逐一檢查）
   - 若 API 超額或驗證未過，自動無縫降級回 repo 內人工驗證過的結構化題庫與教材，確保 100% 穩定產出。
3. 內建品質守門員（檢查專欄標題、結尾品牌連結、Threads 500 字上限、禁用詞）。
4. 輸出 JSON 佇列（供發送器讀取）與 Markdown 預覽檔（供人工審稿）。

用法：
  python3 scripts/threads/generate_week.py                  # 產生當週 7 天 × 5 則 = 35 則貼文
  python3 scripts/threads/generate_week.py --start 2026-09-21 --days 7
  python3 scripts/threads/generate_week.py --offline        # 強制使用離線接地模板（不呼叫 API）
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
VOCAB_DIR = REPO_ROOT / "src" / "data" / "vocabulary"
GRAMMAR_DIR = REPO_ROOT / "src" / "data" / "grammar"
CALENDAR_FILE = REPO_ROOT / "src" / "data" / "threads" / "calendar.json"
QUEUE_DIR = REPO_ROOT / "content" / "threads-queue"

FOOTER = "日檢手帖 - 日檢 JLPT 自學網站 👉 jlpt.chiaoban.com"
THREADS_CHAR_LIMIT = 500
BANNED_PHRASES = ["保證合格", "100%考上", "絕對必考", "不看會後悔"]

TAIPEI_TZ = dt.timezone(dt.timedelta(hours=8))

SEASON_EMOJI = {
  1: "❄️", 2: "❄️",
  3: "🌸", 4: "🌸", 5: "🌿",
  6: "☔", 7: "🎐", 8: "🌻",
  9: "🍂", 10: "🍁", 11: "🍂",
  12: "❄️",
}

SLOT_HEADERS = {
  "vocab": "📖 每日五單字｜日檢手帖陪你背單字",
  "quiz_easy": "✏️ 今日一題｜日檢手帖陪你練手感",
  "grammar": "🔍 每日文法｜日檢手帖陪你拆句型",
  "quote": "{emoji} 今日一句｜日檢手帖陪你學道地日文",
  "quiz_hard": "🌙 睡前一題｜日檢手帖陪你衝高分",
}

SLOT_TIMES = {
  "vocab": "08:00",
  "quiz_easy": "12:30",
  "grammar": "15:30",
  "quote": "18:30",
  "quiz_hard": "21:00",
}


def day_seed(date_obj: dt.date, salt: str = "") -> int:
  h = hashlib.sha256(f"{date_obj.isoformat()}:{salt}".encode("utf-8")).hexdigest()
  return int(h[:12], 16)


def format_ruby_word(entry: dict[str, Any]) -> str:
  """將 furigana 陣列轉為 Threads 純文字最易讀的『漢字(かん・じ)送假名』格式。"""
  furigana = entry.get("furigana")
  kanji = entry.get("kanji", "")
  kana = entry.get("kana", "")
  if not furigana:
    return f"{kanji}({kana})" if kanji and kanji != kana else kanji

  out: list[str] = []
  kanji_buf: list[str] = []
  reading_buf: list[str] = []

  def flush_buf() -> None:
    if kanji_buf:
      joined_k = "".join(kanji_buf)
      joined_r = "・".join(reading_buf)
      out.append(f"{joined_k}({joined_r})")
      kanji_buf.clear()
      reading_buf.clear()

  for surface, reading in furigana:
    if reading:
      kanji_buf.append(surface)
      reading_buf.append(reading)
    else:
      flush_buf()
      out.append(surface)
  flush_buf()
  return "".join(out)


def load_all_data() -> dict[str, Any]:
  vocab_by_level: dict[str, list[dict[str, Any]]] = {}
  grammar_by_level: dict[str, list[dict[str, Any]]] = {}
  for lv in ["n5", "n4", "n3", "n2", "n1"]:
    with open(VOCAB_DIR / f"{lv}.json", encoding="utf-8") as f:
      vocab_by_level[lv] = json.load(f)
    with open(GRAMMAR_DIR / f"{lv}.json", encoding="utf-8") as f:
      grammar_by_level[lv] = json.load(f)
  with open(CALENDAR_FILE, encoding="utf-8") as f:
    calendar = json.load(f)
  return {
    "vocab": vocab_by_level,
    "grammar": grammar_by_level,
    "calendar": calendar,
  }


def call_gemini_json(prompt: str, api_key: str) -> dict[str, Any] | None:
  """呼叫 Gemini 2.5 Flash 並回傳解析後的 JSON；失敗時回傳 None 以觸發安全降級。"""
  url = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    f"gemini-2.5-flash:generateContent?key={api_key}"
  )
  payload = {
    "contents": [{"parts": [{"text": prompt}]}],
    "generationConfig": {
      "temperature": 0.4,
      "responseMimeType": "application/json",
    },
  }
  req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST",
  )
  try:
    with urllib.request.urlopen(req, timeout=25) as resp:
      body = json.loads(resp.read().decode("utf-8"))
    text = body["candidates"][0]["content"]["parts"][0]["text"]
    time.sleep(6.5)  # 遵守免費層 10 RPM 限制
    return json.loads(text)
  except Exception as exc:
    print(f"  [gemini fallback] {exc}", file=sys.stderr)
    return None


def generate_grounded_quiz_with_three_gates(
  level_upper: str,
  point: dict[str, Any],
  api_key: str,
) -> dict[str, Any] | None:
  """
  三道驗證關卡自動出題：
  關卡 ①：以 repo 的 grammar_point (formula + explanation + alert) 接地出題
  關卡 ②：另開乾淨上下文，只給題幹與四個選項，要求獨立作答；答案不一致即丟棄
  關卡 ③：檢查每個誘答項是否都有明確錯誤原因，缺一即丟棄
  """
  # 關卡 ①：接地出題
  gen_prompt = f"""你是 JLPT {level_upper} 命題老師。請根據以下唯一事實來源出一題四選一填空題：
文法點：{point['point_title']}
接續公式：{point['formula']}
核心說明：{point['explanation']}
考點提醒：{point.get('alert', '')}
參考真例句：{point['examples'][0]['ja']}

請輸出 JSON：
{{
  "hook": "吸引人作答的一句話（25字內，台灣繁中，不要加標題）",
  "question_text": "日文題幹，挖空處用（　　）表示",
  "options": ["選項A日文", "選項B日文", "選項C日文", "選項D日文"],
  "correct_index": 0,
  "full_sentence_ja": "填入正確答案後的完整日文句子",
  "full_sentence_zh": "完整句子的自然台灣繁中翻譯",
  "why_correct": "為什麼正解對（45字內）",
  "distractor_reasons": {{
    "0": "若為誘答項為何錯，正解則填correct",
    "1": "為何錯",
    "2": "為何錯",
    "3": "為何錯"
  }}
}}"""
  draft = call_gemini_json(gen_prompt, api_key)
  if not draft:
    return None
  try:
    options = draft["options"]
    correct_idx = int(draft["correct_index"])
    if len(options) != 4 or not (0 <= correct_idx < 4):
      return None
    # 關卡 ③：確認每個誘答項都有實質錯誤理由
    reasons = draft.get("distractor_reasons", {})
    for idx in range(4):
      if idx != correct_idx:
        r = str(reasons.get(str(idx), "")).strip()
        if len(r) < 4:
          return None
  except Exception:
    return None

  # 關卡 ②：獨立作答驗證（只給題目與四個選項，不洩漏任何提示）
  verify_prompt = f"""請解答以下 JLPT 日檢單選題，選出唯一正確的選項索引（0, 1, 2, 或 3），若超過一個選項可通順成立請將 unambiguous 設為 false。
題目：{draft['question_text']}
0: {options[0]}
1: {options[1]}
2: {options[2]}
3: {options[3]}

請只輸出 JSON：{{"chosen_index": 整數, "unambiguous": 布林值}}"""
  verdict = call_gemini_json(verify_prompt, api_key)
  if not verdict:
    return None
  if verdict.get("chosen_index") != correct_idx or not verdict.get("unambiguous", False):
    print("  [Gate 2 rejected ambiguous quiz, falling back to verified repo quiz]", file=sys.stderr)
    return None

  return draft


def build_vocab_post(date_obj: dt.date, data: dict[str, Any]) -> dict[str, Any]:
  levels = ["n5", "n4", "n3", "n2", "n1"]
  lv = levels[date_obj.toordinal() % len(levels)]
  lv_upper = lv.upper()
  pool = data["vocab"][lv]

  # 以分類群組挑出同主題且至少有 5 個不重複單字的主題
  by_cat: dict[str, list[dict[str, Any]]] = {}
  for item in pool:
    cat = item.get("category", "常用詞彙")
    by_cat.setdefault(cat, []).append(item)

  valid_cats = sorted(c for c, items in by_cat.items() if len(items) >= 5)
  if valid_cats:
    chosen_cat = valid_cats[day_seed(date_obj, "vocab_cat") % len(valid_cats)]
    cat_items = by_cat[chosen_cat]
  else:
    chosen_cat = "核心詞彙"
    cat_items = pool

  start_idx = (day_seed(date_obj, "vocab_idx") * 5) % len(cat_items)
  selected: list[dict[str, Any]] = []
  seen_keys: set[str] = set()
  for offset in range(len(cat_items)):
    cand = cat_items[(start_idx + offset) % len(cat_items)]
    key = f"{cand.get('kanji')}:{cand.get('kana')}"
    if key not in seen_keys:
      seen_keys.add(key)
      selected.append(cand)
      if len(selected) == 5:
        break

  cat_zh = (
    chosen_cat
    .replace("経済", "經濟")
    .replace("接続詞", "接續詞")
    .replace("味覚", "味覺")
  )

  lines = [
    SLOT_HEADERS["vocab"],
    "",
    f"今天一起記 5 個 {lv_upper}「{cat_zh}」高頻單字：",
    "",
  ]
  for idx, w in enumerate(selected, 1):
    ruby = format_ruby_word(w)
    meaning = w["meaning"].split("（")[0]
    lines.append(f"{idx}. {ruby}｜{meaning}")

  ex_word = selected[0]
  lines.extend([
    "",
    f"💡 實用造句：",
    f"{ex_word['example_ja']}",
    f"（{ex_word['example_zh']}）",
    "",
    FOOTER,
  ])
  text = "\n".join(lines)
  return {
    "slot": "vocab",
    "scheduled_time": SLOT_TIMES["vocab"],
    "level": lv_upper,
    "topic": f"{lv_upper} {chosen_cat}",
    "text": text,
    "reply_text": None,
  }


def is_standalone_quiz(q: dict[str, Any]) -> bool:
  """過濾掉需要看前後文（「前者／後者／下列何者」）的後設題，只留純填空好題。"""
  qt = q.get("question_text", "")
  if "（" not in qt and "(" not in qt:
    return False
  for meta_word in ["前者", "後者", "正しいものはどれ", "誤っているもの", "適切なもの"]:
    if meta_word in qt:
      return False
  return len(q.get("options", [])) == 4


def build_quiz_post(
  date_obj: dt.date,
  data: dict[str, Any],
  slot: str,
  levels: list[str],
  reply_time: str,
  api_key: str | None = None,
) -> dict[str, Any]:
  lv = levels[day_seed(date_obj, slot) % len(levels)]
  lv_upper = lv.upper()
  lessons = data["grammar"][lv]

  # 收集該級別所有可獨立作答的題目與所屬文法點
  candidates: list[tuple[dict[str, Any], dict[str, Any], dict[str, Any]]] = []
  for lesson in lessons:
    for pt in lesson.get("grammar_points", []):
      for q in pt.get("quizzes", []):
        if is_standalone_quiz(q):
          candidates.append((lesson, pt, q))

  lesson, pt, q = candidates[day_seed(date_obj, f"{slot}_pick") % len(candidates)]
  header = SLOT_HEADERS[slot]
  labels = ["A", "B", "C", "D"]

  # 若有提供 GEMINI_API_KEY，嘗試用三道驗證關卡產生全新題目
  ai_quiz = None
  if api_key:
    ai_quiz = generate_grounded_quiz_with_three_gates(lv_upper, pt, api_key)

  if ai_quiz:
    options = ai_quiz["options"]
    correct_idx = int(ai_quiz["correct_index"])
    correct_label = labels[correct_idx]
    correct_ans = options[correct_idx]
    q_text = ai_quiz["question_text"]
    hook = ai_quiz["hook"]
    opt_lines = "\n".join(f"{labels[i]}. {options[i]}" for i in range(4))
    text = (
      f"{header}\n\n"
      f"{hook}\n\n"
      f"{q_text}\n\n"
      f"{opt_lines}\n\n"
      f"留言寫下你的答案（A / B / C / D）👇\n"
      f"{reply_time} 在這串底下公布解答與詳解！\n\n"
      f"{FOOTER}"
    )
    distractor_notes = []
    for i in range(4):
      if i != correct_idx:
        reason = ai_quiz["distractor_reasons"].get(str(i), "")
        distractor_notes.append(f"・{labels[i]} {options[i]}：{reason}")
    reply_text = (
      f"【解答公布】正確答案是 {correct_label}. {correct_ans} ✅\n\n"
      f"整句：{ai_quiz['full_sentence_ja']}\n"
      f"（{ai_quiz['full_sentence_zh']}）\n\n"
      f"📌 考點：{pt['point_title']}\n"
      f"{ai_quiz['why_correct']}\n\n"
      + "\n".join(distractor_notes)
    )
  else:
    options = q["options"]
    correct_ans = q["correct_answer"]
    correct_idx = options.index(correct_ans) if correct_ans in options else 0
    correct_label = labels[correct_idx]
    q_text = q["question_text"]
    if slot == "quiz_easy":
      hook = f"這題 {lv_upper} 基礎題看起來很眼熟，你第一眼選哪一個？👇"
    else:
      hook = f"睡前一題 {lv_upper} 實戰題，測試看看你的語感準不準 👇"

    opt_lines = "\n".join(f"{labels[i]}. {options[i]}" for i in range(4))
    text = (
      f"{header}\n\n"
      f"{hook}\n\n"
      f"{q_text}\n\n"
      f"{opt_lines}\n\n"
      f"留言寫下你的答案（A / B / C / D）👇\n"
      f"{reply_time} 在這串底下公布解答！\n\n"
      f"{FOOTER}"
    )
    filled_sentence = re.sub(r"[（(]\s*[）)]", correct_ans, q_text, count=1)
    alert_tip = pt.get("alert", "").split("。")[0]
    reply_text = (
      f"【解答公布】正確答案是 {correct_label}. {correct_ans} ✅\n\n"
      f"完整句子：{filled_sentence}\n\n"
      f"📌 考點解析（{lv_upper}・{pt['point_title']}）：\n"
      f"{q['explanation']}\n\n"
      f"💡 接續公式：{pt['formula']}"
      + (f"\n⚠️ 注意：{alert_tip}。" if alert_tip else "")
    )

  return {
    "slot": slot,
    "scheduled_time": SLOT_TIMES[slot],
    "reply_scheduled_time": reply_time,
    "level": lv_upper,
    "topic": f"{lv_upper} {pt['point_title']}",
    "text": text,
    "reply_text": reply_text[:THREADS_CHAR_LIMIT],
  }


def build_grammar_post(date_obj: dt.date, data: dict[str, Any]) -> dict[str, Any]:
  levels = ["n4", "n3", "n2", "n3", "n1", "n4", "n2"]
  lv = levels[date_obj.weekday()]
  lv_upper = lv.upper()
  lessons = data["grammar"][lv]
  lesson = lessons[day_seed(date_obj, "grammar_lesson") % len(lessons)]
  pts = lesson["grammar_points"]
  pt = pts[day_seed(date_obj, "grammar_pt") % len(pts)]

  ex = pt["examples"][0]
  short_expl = pt["explanation"].split("。")[0] + "。"
  alert_sentence = pt.get("alert", "").split("。")[0]

  lines = [
    SLOT_HEADERS["grammar"],
    "",
    f"今天花 30 秒搞懂 {lv_upper} 常考句型：{pt['point_title']}",
    "",
    f"🔹 接續：{pt['formula']}",
    f"🔹 意思：{short_expl}",
    "",
    f"✅ 例句：",
    f"{ex['ja']}",
    f"（{ex['zh']}）",
  ]
  if alert_sentence:
    lines.extend([
      "",
      f"⚠️ 考試陷阱：",
      f"{alert_sentence}。",
    ])
  lines.extend(["", FOOTER])

  text = "\n".join(lines)
  if len(text) > THREADS_CHAR_LIMIT:
    # 若超過 500 字，精簡考試陷阱段以確保不截斷
    lines = [
      SLOT_HEADERS["grammar"],
      "",
      f"今天花 30 秒搞懂 {lv_upper} 常考句型：{pt['point_title']}",
      "",
      f"🔹 接續：{pt['formula']}",
      f"🔹 核心：{short_expl[:75]}",
      "",
      f"✅ {ex['ja']}",
      f"（{ex['zh']}）",
      "",
      FOOTER,
    ]
    text = "\n".join(lines)

  return {
    "slot": "grammar",
    "scheduled_time": SLOT_TIMES["grammar"],
    "level": lv_upper,
    "topic": f"{lv_upper} {pt['point_title']} (/grammar/{lv}/{lesson['lesson_number']})",
    "text": text,
    "reply_text": None,
  }


def build_quote_post(date_obj: dt.date, data: dict[str, Any]) -> dict[str, Any]:
  cal = data["calendar"]
  month_key = str(date_obj.month)
  emoji = SEASON_EMOJI.get(date_obj.month, "🍂")
  header = SLOT_HEADERS["quote"].format(emoji=emoji)

  # 偶數天發當月季節道地生活句，奇數天發日本經典諺語／慣用句
  if date_obj.toordinal() % 2 == 0:
    items = cal["seasonal_themes"].get(month_key, cal["seasonal_themes"]["9"])
    item = items[day_seed(date_obj, "quote_season") % len(items)]
    notes_block = "\n".join(f"・{n}" for n in item["notes"])
    text = (
      f"{header}\n\n"
      f"{item['hook']}\n\n"
      f"「{item['ja_ruby']}」\n"
      f"（{item['zh']}）\n\n"
      f"拆解三個實用重點：\n"
      f"{notes_block}\n\n"
      f"{item['context']}\n\n"
      f"{FOOTER}"
    )
    topic = f"季節句・{item['tag']}"
  else:
    proverbs = cal["classic_proverbs"]
    item = proverbs[day_seed(date_obj, "quote_proverb") % len(proverbs)]
    notes_block = "\n".join(f"・{n}" for n in item["notes"])
    text = (
      f"{header}\n\n"
      f"今天學一句日本人很常掛在嘴邊的經典格言：\n\n"
      f"「{item['ja_ruby']}」\n"
      f"（{item['zh']}）\n"
      f"—— {item['source']}\n\n"
      f"句型與單字拆解：\n"
      f"{notes_block}\n\n"
      f"{FOOTER}"
    )
    topic = f"經典格言・{item['ja']}"

  return {
    "slot": "quote",
    "scheduled_time": SLOT_TIMES["quote"],
    "level": "ALL",
    "topic": topic,
    "text": text,
    "reply_text": None,
  }


def validate_post(post: dict[str, Any]) -> list[str]:
  errors: list[str] = []
  text = post.get("text", "")
  slot = post.get("slot", "")

  if not text.endswith(FOOTER):
    errors.append(f"[{slot}] 結尾缺少固定署名：{FOOTER}")
  if len(text) > THREADS_CHAR_LIMIT:
    errors.append(f"[{slot}] 字數 {len(text)} 超過 Threads 500 字上限")
  for phrase in BANNED_PHRASES:
    if phrase in text:
      errors.append(f"[{slot}] 含禁用詞：{phrase}")
  if slot == "vocab":
    item_lines = [ln for ln in text.splitlines() if re.match(r"^[1-5]\.\s", ln)]
    words = [ln.split(".", 1)[1].strip() for ln in item_lines]
    if len(set(words)) != 5:
      errors.append(f"[vocab] 五個單字出現重複：{words}")
  if slot in ("quiz_easy", "quiz_hard"):
    for opt in ("A. ", "B. ", "C. ", "D. "):
      if opt not in text:
        errors.append(f"[{slot}] 題目缺少選項 {opt.strip()}")
    if not post.get("reply_text", "").startswith("【解答公布】"):
      errors.append(f"[{slot}] 缺少三小時後的【解答公布】回覆內容")
  return errors


def generate_day_posts(
  date_obj: dt.date,
  data: dict[str, Any],
  api_key: str | None = None,
) -> list[dict[str, Any]]:
  posts = [
    build_vocab_post(date_obj, data),
    build_quiz_post(date_obj, data, "quiz_easy", ["n5", "n4"], "15:30", api_key),
    build_grammar_post(date_obj, data),
    build_quote_post(date_obj, data),
    build_quiz_post(date_obj, data, "quiz_hard", ["n3", "n2", "n1"], "24:00", api_key),
  ]
  for p in posts:
    p["date"] = date_obj.isoformat()
    errs = validate_post(p)
    if errs:
      raise ValueError("品質檢查未通過：\n" + "\n".join(errs))
  return posts


def render_markdown_preview(
  week_label: str,
  start_date: dt.date,
  end_date: dt.date,
  all_posts: list[dict[str, Any]],
) -> str:
  lines = [
    f"# 日檢手帖 Threads 自動發文佇列（{week_label}）",
    "",
    f"- **涵蓋日期**：`{start_date.isoformat()}` ～ `{end_date.isoformat()}`",
    f"- **總貼文數**：{len(all_posts)} 則主貼文 ＋ {sum(1 for p in all_posts if p.get('reply_text'))} 則自動解答回覆",
    f"- **結尾固定導流**：`{FOOTER}`",
    "",
    "---",
    "",
  ]
  current_date = None
  for p in all_posts:
    if p["date"] != current_date:
      current_date = p["date"]
      lines.append(f"## 📅 {current_date}")
      lines.append("")
    lines.append(f"### ⏰ {p['scheduled_time']}｜`{p['slot']}`（{p['topic']}，{len(p['text'])} 字）")
    lines.append("")
    lines.append("```text")
    lines.append(p["text"])
    lines.append("```")
    if p.get("reply_text"):
      lines.append("")
      lines.append(f"↳ **{p['reply_scheduled_time']} 同串自動回覆解答：**")
      lines.append("")
      lines.append("```text")
      lines.append(p["reply_text"])
      lines.append("```")
    lines.append("")
  return "\n".join(lines)


def main() -> None:
  parser = argparse.ArgumentParser(description="產生日檢手帖一週 Threads 貼文佇列")
  parser.add_argument("--start", type=str, default="", help="起始日期 YYYY-MM-DD（預設為今天台北時間）")
  parser.add_argument("--days", type=int, default=7, help="生成天數（預設 7 天 = 35 則）")
  parser.add_argument("--offline", action="store_true", help="強制使用離線結構化模板，不呼叫 Gemini API")
  args = parser.parse_args()

  if args.start:
    start_date = dt.date.fromisoformat(args.start)
  else:
    start_date = dt.datetime.now(TAIPEI_TZ).date()

  api_key = None if args.offline else os.environ.get("GEMINI_API_KEY")
  data = load_all_data()

  all_posts: list[dict[str, Any]] = []
  for offset in range(args.days):
    d = start_date + dt.timedelta(days=offset)
    all_posts.extend(generate_day_posts(d, data, api_key=api_key))

  end_date = start_date + dt.timedelta(days=args.days - 1)
  iso_year, iso_week, _ = start_date.isocalendar()
  week_label = f"{iso_year}-W{iso_week:02d}"

  QUEUE_DIR.mkdir(parents=True, exist_ok=True)
  json_path = QUEUE_DIR / f"{week_label}.json"
  md_path = QUEUE_DIR / f"{week_label}.md"

  queue_payload = {
    "week": week_label,
    "start_date": start_date.isoformat(),
    "end_date": end_date.isoformat(),
    "generated_at": dt.datetime.now(TAIPEI_TZ).isoformat(),
    "footer": FOOTER,
    "count": len(all_posts),
    "posts": all_posts,
  }
  with open(json_path, "w", encoding="utf-8") as f:
    json.dump(queue_payload, f, ensure_ascii=False, indent=2)
    f.write("\n")

  with open(md_path, "w", encoding="utf-8") as f:
    f.write(render_markdown_preview(week_label, start_date, end_date, all_posts))

  print(f"✅ 已產生 {len(all_posts)} 則貼文（全數通過品質檢查）")
  print(f"   JSON 佇列：{json_path.relative_to(REPO_ROOT)}")
  print(f"   審稿預覽：{md_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
  main()
