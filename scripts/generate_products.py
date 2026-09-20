#!/usr/bin/env python3
"""
日檢手帖 N1～N5 分級數位商品打包器 (scripts/generate_products.py)

功能：
1. 分別將 N5、N4、N3、N2、N1 五個級別獨立打包成高質感的數位商品套組。
2. 每個級別獨立輸出：
   - 【Anki 牌組】`日檢手帖-{LV}-單字文法手帖.apkg`（手機／電腦一鍵匯入，內建日雜撞色卡片樣式、逐字振假名、例句、文法公式與考試陷阱）
   - 【可列印講義】`日檢手帖-{LV}-考場速查講義手冊.html`（FUDGE/CLUEL 日雜復古摩登排版，支援 A4 列印或轉存 PDF，含封面、文法公式速查、陷阱提示、完整單字表與隨堂練習題）
   - 【壓縮包】`dist-products/日檢手帖-{LV}-完全備考套組.zip`（包含 .apkg + .html 講義 + 使用說明 README.txt，可直接上傳 Buy Me a Coffee Shop 開賣）

用法：
  /tmp/jpenv/bin/python3 scripts/generate_products.py
"""

from __future__ import annotations

import json
import os
import shutil
import sys
import zipfile
from pathlib import Path
from typing import Any

# 引入 genanki
sys.path.insert(0, "/tmp/jpenv/lib/python3.13/site-packages")
import genanki

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO_ROOT / "dist-products"

LEVEL_CONFIG = {
  "n5": {
    "upper": "N5",
    "color": "#8338ec",
    "color_rgb": "131, 56, 236",
    "tint": "#f2e8fd",
    "sub_title": "入門基石・生活招呼與基礎句型",
    "deck_id_vocab": 1695200005,
    "deck_id_grammar": 1695201005,
  },
  "n4": {
    "upper": "N4",
    "color": "#0096c7",
    "color_rgb": "0, 150, 199",
    "tint": "#e2f4fa",
    "sub_title": "進階基礎・日常會話與核心動詞變化",
    "deck_id_vocab": 1695200004,
    "deck_id_grammar": 1695201004,
  },
  "n3": {
    "upper": "N3",
    "color": "#7cb518",
    "color_rgb": "124, 181, 24",
    "tint": "#f2f8e6",
    "sub_title": "實用分水嶺・日常複雜情境與職場銜接",
    "deck_id_vocab": 1695200003,
    "deck_id_grammar": 1695201003,
  },
  "n2": {
    "upper": "N2",
    "color": "#ff6b35",
    "color_rgb": "255, 107, 53",
    "tint": "#fff0e8",
    "sub_title": "中高階核心・商務會話、時事與長文理解",
    "deck_id_vocab": 1695200002,
    "deck_id_grammar": 1695201002,
  },
  "n1": {
    "upper": "N1",
    "color": "#e63956",
    "color_rgb": "230, 57, 86",
    "tint": "#ffeaef",
    "sub_title": "最高殿堂・抽象邏輯、書面政經與古典文語",
    "deck_id_vocab": 1695200001,
    "deck_id_grammar": 1695201001,
  },
}

# ── Anki 卡片 CSS 樣式（日雜復古摩登撞色，與網站 100% 一致）───────────
ANKI_CARD_CSS = """
.card {
  font-family: -apple-system, BlinkMacSystemFont, "Zen Kaku Gothic New", "Noto Sans TC", "Noto Sans JP", sans-serif;
  background-color: #faf7f2;
  color: #2b2523;
  padding: 18px 12px;
  margin: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  box-sizing: border-box;
}

.techo-container {
  background: #ffffff;
  width: 100%;
  max-width: 580px;
  border: 2px solid #2b2523;
  border-radius: 14px;
  box-shadow: 4px 4px 0px #2b2523;
  padding: 24px 22px;
  box-sizing: border-box;
  text-align: left;
}

.badge-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 18px;
}

.level-badge {
  background: var(--level-color, #2b2523);
  color: #ffffff;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.08em;
  padding: 3px 9px;
  border-radius: 6px;
  border: 1.5px solid #2b2523;
}

.cat-pill {
  background: var(--level-tint, #efeae1);
  color: #2b2523;
  font-size: 11px;
  font-weight: 700;
  padding: 3px 9px;
  border-radius: 6px;
  border: 1.5px solid rgba(43, 37, 35, 0.2);
}

.site-mark {
  margin-left: auto;
  font-size: 10px;
  font-weight: 700;
  color: rgba(43, 37, 35, 0.45);
  letter-spacing: 0.05em;
}

/* 題目卡面文字 */
.front-word {
  font-family: "Shippori Mincho", "Noto Serif JP", "Songti TC", serif;
  font-size: 38px;
  font-weight: 800;
  letter-spacing: 0.04em;
  line-height: 1.25;
  color: #2b2523;
  text-align: center;
  margin: 22px 0 16px 0;
}

.prompt-tip {
  text-align: center;
  font-size: 12px;
  font-weight: 700;
  color: rgba(43, 37, 35, 0.55);
  margin-bottom: 8px;
}

/* 振假名 Ruby 標示 */
.ruby-display {
  font-family: "Shippori Mincho", "Noto Serif JP", serif;
  font-size: 34px;
  font-weight: 800;
  line-height: 2.3;
  text-align: center;
  margin: 8px 0 12px 0;
}
.ruby-display ruby {
  ruby-align: center;
  ruby-position: over;
  margin-inline: 0.08em;
  padding-inline: 0.04em;
}
.ruby-display rt {
  font-family: -apple-system, BlinkMacSystemFont, "Noto Sans JP", sans-serif;
  font-size: 0.52em;
  font-weight: 700;
  letter-spacing: 0.04em;
  border-bottom: 2px solid var(--level-tint, #efeae1);
  padding-bottom: 0.08em;
  color: rgba(43, 37, 35, 0.75);
}

.romaji-bar {
  text-align: center;
  font-size: 13px;
  font-weight: 600;
  color: rgba(43, 37, 35, 0.6);
  letter-spacing: 0.06em;
  margin-bottom: 14px;
}

.divider {
  border: none;
  border-top: 1.5px dashed rgba(43, 37, 35, 0.25);
  margin: 16px 0;
}

.meaning-block {
  background: var(--level-tint, #efeae1);
  border-left: 4px solid var(--level-color, #2b2523);
  padding: 10px 14px;
  border-radius: 0 8px 8px 0;
  font-size: 15px;
  font-weight: 700;
  color: #2b2523;
  margin-bottom: 14px;
}

.example-box {
  background: #faf7f2;
  border: 1.5px solid rgba(43, 37, 35, 0.2);
  border-radius: 8px;
  padding: 12px 14px;
  margin-top: 10px;
}

.ex-ja {
  font-size: 14px;
  font-weight: 700;
  line-height: 1.6;
  color: #2b2523;
  margin-bottom: 4px;
}

.ex-zh {
  font-size: 12.5px;
  font-weight: 500;
  color: rgba(43, 37, 35, 0.7);
  line-height: 1.5;
}

.alert-box {
  background: #fff9e6;
  border: 1.5px solid #e0a800;
  border-radius: 8px;
  padding: 10px 12px;
  font-size: 12.5px;
  line-height: 1.55;
  color: #664d03;
  margin-top: 12px;
}

.formula-box {
  background: var(--level-tint, #efeae1);
  border: 1.5px solid var(--level-color, #2b2523);
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 13.5px;
  font-weight: 700;
  color: #2b2523;
  margin-bottom: 10px;
}

.card-footer {
  margin-top: 16px;
  font-size: 10.5px;
  font-weight: 700;
  color: rgba(43, 37, 35, 0.45);
  text-align: center;
  letter-spacing: 0.05em;
}
"""


def build_ruby_html(entry: dict[str, Any], level_tint: str) -> str:
  furigana = entry.get("furigana")
  kanji = entry.get("kanji", "")
  kana = entry.get("kana", "")
  if not furigana:
    return kanji

  parts: list[str] = []
  for surface, reading in furigana:
    if reading:
      parts.append(f"<ruby>{surface}<rt style='border-bottom:2px solid {level_tint};'>{reading}</rt></ruby>")
    else:
      parts.append(f"<span class='ruby-okurigana'>{surface}</span>")
  return "".join(parts)


def create_anki_deck_package(level_key: str, vocab_list: list[dict[str, Any]], grammar_list: list[dict[str, Any]], out_apkg_path: Path) -> int:
  conf = LEVEL_CONFIG[level_key]
  lv_upper = conf["upper"]
  lv_color = conf["color"]
  lv_tint = conf["tint"]

  model_vocab_id = 1695210000 + int(level_key[1])
  model_grammar_id = 1695220000 + int(level_key[1])

  css_with_vars = ANKI_CARD_CSS + f"\n:root {{ --level-color: {lv_color}; --level-tint: {lv_tint}; }}\n"

  # 1. 單字卡模型 (Front: 漢字/假名 + 詞性 -> Back: 振假名 + 羅馬字 + 中文意思 + 例句)
  vocab_model = genanki.Model(
    model_vocab_id,
    f"日檢手帖 {lv_upper} 單字卡",
    fields=[
      {"name": "Kanji"},
      {"name": "Kana"},
      {"name": "RubyHTML"},
      {"name": "Romaji"},
      {"name": "PartOfSpeech"},
      {"name": "Meaning"},
      {"name": "ExampleJa"},
      {"name": "ExampleZh"},
      {"name": "Category"},
      {"name": "Level"},
    ],
    templates=[
      {
        "name": f"日檢手帖 {lv_upper} 單字正向卡",
        "qfmt": f"""
<div class="card">
  <div class="techo-container">
    <div class="badge-row">
      <span class="level-badge" style="background:{lv_color};">{lv_upper} 單字</span>
      <span class="cat-pill" style="background:{lv_tint};">{{{{Category}}}}</span>
      <span class="site-mark">日檢手帖 NIKKEN TECHO</span>
    </div>
    <div class="front-word">{{{{Kanji}}}}</div>
    <div class="prompt-tip">（請回想讀音、詞性與中文意思）</div>
  </div>
</div>
""",
        "afmt": f"""
<div class="card">
  <div class="techo-container">
    <div class="badge-row">
      <span class="level-badge" style="background:{lv_color};">{lv_upper} 單字</span>
      <span class="cat-pill" style="background:{lv_tint};">{{{{PartOfSpeech}}}}</span>
      <span class="site-mark">日檢手帖 NIKKEN TECHO</span>
    </div>
    <div class="ruby-display">{{{{RubyHTML}}}}</div>
    <div class="romaji-bar">/ {{{{Romaji}}}} /</div>
    <div class="meaning-block" style="background:{lv_tint}; border-left: 4px solid {lv_color};">
      {{{{Meaning}}}}
    </div>
    <div class="example-box">
      <div class="ex-ja">📌 {{{{ExampleJa}}}}</div>
      <div class="ex-zh">{{{{ExampleZh}}}}</div>
    </div>
    <div class="card-footer">日檢手帖 - 日檢 JLPT 自學網站 👉 jlpt.chiaoban.com</div>
  </div>
</div>
""",
      }
    ],
    css=css_with_vars,
  )

  # 2. 文法卡模型 (Front: 文法句型 + 填空題 -> Back: 接續公式 + 核心語感 + 考試陷阱 + 真例句)
  grammar_model = genanki.Model(
    model_grammar_id,
    f"日檢手帖 {lv_upper} 文法卡",
    fields=[
      {"name": "PointTitle"},
      {"name": "Formula"},
      {"name": "Explanation"},
      {"name": "Alert"},
      {"name": "Example1Ja"},
      {"name": "Example1Zh"},
      {"name": "Example2Ja"},
      {"name": "Example2Zh"},
      {"name": "LessonNumber"},
      {"name": "Level"},
    ],
    templates=[
      {
        "name": f"日檢手帖 {lv_upper} 文法核心卡",
        "qfmt": f"""
<div class="card">
  <div class="techo-container">
    <div class="badge-row">
      <span class="level-badge" style="background:{lv_color};">{lv_upper} 文法</span>
      <span class="cat-pill" style="background:{lv_tint};">第 {{{{LessonNumber}}}} 課</span>
      <span class="site-mark">日檢手帖 NIKKEN TECHO</span>
    </div>
    <div class="front-word" style="font-size:32px;">{{{{PointTitle}}}}</div>
    <div class="prompt-tip">（請回想接續公式、中文核心意思與常考陷阱）</div>
  </div>
</div>
""",
        "afmt": f"""
<div class="card">
  <div class="techo-container">
    <div class="badge-row">
      <span class="level-badge" style="background:{lv_color};">{lv_upper} 文法</span>
      <span class="cat-pill" style="background:{lv_tint};">第 {{{{LessonNumber}}}} 課</span>
      <span class="site-mark">日檢手帖 NIKKEN TECHO</span>
    </div>
    <div class="front-word" style="font-size:28px; margin: 10px 0 14px 0;">{{{{PointTitle}}}}</div>
    <div class="formula-box" style="background:{lv_tint}; border-color:{lv_color};">
      🔹 接續：{{{{Formula}}}}
    </div>
    <div class="meaning-block" style="background:{lv_tint}; border-left: 4px solid {lv_color};">
      💡 語意：{{{{Explanation}}}}
    </div>
    <div class="alert-box">
      ⚠️ 考試陷阱：{{{{Alert}}}}
    </div>
    <div class="example-box">
      <div class="ex-ja">✅ {{{{Example1Ja}}}}</div>
      <div class="ex-zh">{{{{Example1Zh}}}}</div>
    </div>
    <div class="card-footer">日檢手帖 - 日檢 JLPT 自學網站 👉 jlpt.chiaoban.com/grammar/{level_key}/{{{{LessonNumber}}}}</div>
  </div>
</div>
""",
      }
    ],
    css=css_with_vars,
  )

  deck = genanki.Deck(conf["deck_id_vocab"], f"日檢手帖｜{lv_upper} 完整單字與文法手帖（逐字振假名＋例句公式版）")
  card_count = 0

  # 加入單字卡
  for w in vocab_list:
    ruby_html = build_ruby_html(w, lv_tint)
    note = genanki.Note(
      model=vocab_model,
      fields=[
        w.get("kanji", ""),
        w.get("kana", ""),
        ruby_html,
        w.get("romaji", ""),
        w.get("part_of_speech", ""),
        w.get("meaning", ""),
        w.get("example_ja", ""),
        w.get("example_zh", ""),
        w.get("category", "核心詞彙"),
        lv_upper,
      ],
    )
    deck.add_note(note)
    card_count += 1

  # 加入文法卡
  for lesson in grammar_list:
    les_num = str(lesson.get("lesson_number", 1))
    for pt in lesson.get("grammar_points", []):
      ex1 = pt["examples"][0] if pt.get("examples") else {"ja": "", "zh": ""}
      ex2 = pt["examples"][1] if len(pt.get("examples", [])) > 1 else {"ja": "", "zh": ""}
      note = genanki.Note(
        model=grammar_model,
        fields=[
          pt.get("point_title", ""),
          pt.get("formula", ""),
          pt.get("explanation", ""),
          pt.get("alert", "請注意接續時態與主客觀差異。"),
          ex1.get("ja", ""),
          ex1.get("zh", ""),
          ex2.get("ja", ""),
          ex2.get("zh", ""),
          les_num,
          lv_upper,
        ],
      )
      deck.add_note(note)
      card_count += 1

  genanki.Package(deck).write_to_file(str(out_apkg_path))
  return card_count


def generate_printable_html_handbook(
  level_key: str,
  vocab_list: list[dict[str, Any]],
  grammar_list: list[dict[str, Any]],
  out_html_path: Path,
  is_sample: bool = False,
) -> None:
  """產生日雜風（FUDGE / CLUEL 復古摩登撞色）A4 可列印講義手冊。is_sample=True 時僅展示試閱樣章，保護完整版數位資產。"""
  conf = LEVEL_CONFIG[level_key]
  lv_upper = conf["upper"]
  lv_color = conf["color"]
  lv_tint = conf["tint"]
  sub_title = conf["sub_title"]

  # 統計數字
  total_vocab = len(vocab_list)
  total_grammar = sum(len(l.get("grammar_points", [])) for l in grammar_list)
  total_quizzes = sum(len(pt.get("quizzes", [])) for l in grammar_list for pt in l.get("grammar_points", []))

  # 產生成套文法卡片 HTML
  grammar_cards_html = []
  cheat_sheet_rows = []
  quiz_section_html = []

  quiz_counter = 1
  for lesson in grammar_list:
    les_num = lesson.get("lesson_number", 1)
    les_title = lesson.get("lesson_title", "")
    for pt in lesson.get("grammar_points", []):
      pt_title = pt.get("point_title", "")
      formula = pt.get("formula", "")
      expl = pt.get("explanation", "")
      alert = pt.get("alert", "")
      exs = pt.get("examples", [])
      ex1 = exs[0] if exs else {"ja": "", "zh": ""}

      cheat_sheet_rows.append(f"""
      <tr>
        <td class="td-num">{les_num}</td>
        <td class="td-title">{pt_title}</td>
        <td class="td-formula"><code>{formula}</code></td>
        <td class="td-expl">{expl[:48]}...</td>
      </tr>
      """)

      ex_html = "".join([f"<div class='ex-row'><span class='bullet'>✅</span> <strong>{e['ja']}</strong><div class='ex-trans'>（{e['zh']}）</div></div>" for e in exs[:2]])
      alert_html = f"<div class='card-alert'><strong>⚠️ 考場陷阱提示：</strong>{alert}</div>" if alert else ""

      grammar_cards_html.append(f"""
      <div class="grammar-card">
        <div class="card-head">
          <span class="pt-tag">{lv_upper} 第 {les_num} 課</span>
          <h3 class="pt-title">{pt_title}</h3>
        </div>
        <div class="card-formula"><strong>🔹 接續公式：</strong><code>{formula}</code></div>
        <p class="card-expl">{expl}</p>
        <div class="card-examples">{ex_html}</div>
        {alert_html}
      </div>
      """)

      # 隨堂練習題
      for q in pt.get("quizzes", [])[:1]:
        opts_str = "　".join([f"({chr(65+i)}) {opt}" for i, opt in enumerate(q.get("options", []))])
        quiz_section_html.append(f"""
        <div class="quiz-item">
          <div class="quiz-q"><span class="q-badge">第 {quiz_counter} 題</span> {q.get('question_text', '')}</div>
          <div class="quiz-opts">{opts_str}</div>
          <div class="quiz-ans-toggle">正解：<strong>{q.get('correct_answer')}</strong> ｜ 解析：{q.get('explanation')}</div>
        </div>
        """)
        quiz_counter += 1

  # 產生單字總表 HTML
  vocab_rows = []
  for idx, w in enumerate(vocab_list, 1):
    ruby_html = build_ruby_html(w, lv_tint)
    pos = w.get("part_of_speech", "").split("（")[0]
    meaning = w.get("meaning", "")
    vocab_rows.append(f"""
    <tr>
      <td class="td-idx">{idx}</td>
      <td class="td-word"><div class="ruby-cell">{ruby_html}</div><span class="romaji-sub">{w.get('romaji','')}</span></td>
      <td class="td-pos"><span class="pos-badge">{pos}</span></td>
      <td class="td-meaning">{meaning}</td>
      <td class="td-ex"><strong>{w.get('example_ja','')}</strong><br><span class="ex-zh">{w.get('example_zh','')}</span></td>
    </tr>
    """)

  lock_banner = """
  <div style="background:var(--level-tint); border:2px dashed var(--sumi-black); border-radius:10px; padding:24px 20px; text-align:center; margin:24px 0;">
    <div style="font-size:26px;">🔒</div>
    <div style="font-weight:900; font-size:16px; margin-top:6px; color:var(--sumi-black);">
      【試閱版結束】其餘 {remaining} 項完整教材內容，收錄於正式版套組中
    </div>
    <p style="font-size:12.5px; color:rgba(43,37,35,0.75); margin:6px auto 14px auto; max-width:480px;">
      贊助解鎖即可獲取本級別完整講義手冊（支援存為高解析 A4 PDF 與 iPad 筆記）＋ 逐字振假名 Anki 智慧字卡包！
    </p>
    <a href="https://buymeacoffee.com/chiaoban/shop" target="_blank" style="display:inline-block; background:var(--level-color); color:#ffffff; font-weight:800; text-decoration:none; padding:8px 20px; border-radius:6px; font-size:13px; border:1.5px solid var(--sumi-black); box-shadow:3px 3px 0px var(--sumi-black);">
      ☕ 立即前往商店贊助解鎖完整版講義＆Anki 牌組 →
    </a>
  </div>
  """

  if is_sample:
    cheat_sheet_rows = cheat_sheet_rows[:5]
    cheat_sheet_rows.append(f"""
    <tr>
      <td colspan="4" style="text-align:center; padding:16px; background:var(--level-tint); font-weight:800; font-size:12.5px;">
        🔒 更多 {total_grammar - 5} 個文法公式速查，收錄於正式版手冊中（全 {total_grammar} 個句型完整收錄）
      </td>
    </tr>
    """)
    grammar_cards_html = grammar_cards_html[:3]
    grammar_cards_html.append(lock_banner.format(remaining=f"{total_grammar - 3} 個深度解構卡"))
    quiz_section_html = quiz_section_html[:2]
    quiz_section_html.append(lock_banner.format(remaining=f"{total_quizzes - 2} 題實戰測驗"))
    vocab_rows = vocab_rows[:10]
    vocab_rows.append(f"""
    <tr>
      <td colspan="5" style="text-align:center; padding:16px; background:var(--level-tint); font-weight:800; font-size:12.5px;">
        🔒 更多 {total_vocab - 10} 個逐字振假名高頻單字，收錄於正式版手冊與 Anki 牌組中（全 {total_vocab} 字完整收錄）
      </td>
    </tr>
    """)

  sample_tag_html = "<span style='background:#ff4757; color:#ffffff; font-size:13px; font-weight:800; padding:3px 10px; border-radius:4px; margin-left:10px; vertical-align:middle;'>精華試閱版 SAMPLE</span>" if is_sample else ""
  doc_title_suffix = "（精華試閱版）" if is_sample else "（完整正式版）"
  screen_header_html = "<body>" if is_sample else f"""<body>
<div class="screen-header">
  <div>📖 日檢手帖 {lv_upper} 完整備考講義手冊（已設定 A4 最佳列印排版）</div>
  <button class="screen-btn" onclick="window.print()">🖨️ 立即列印或儲存為 PDF</button>
</div>
"""

  html_content = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>日檢手帖｜{lv_upper} 考前速查講義手冊（FUDGE日雜排版）</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700;900&family=Noto+Serif+JP:wght@600;800&family=Zen+Kaku+Gothic+New:wght@500;700;900&display=swap" rel="stylesheet">
<style>
:root {{
  --level-color: {lv_color};
  --level-tint: {lv_tint};
  --sumi-black: #2b2523;
  --paper-bg: #faf7f2;
}}

@page {{
  size: A4 portrait;
  margin: 14mm 12mm 14mm 12mm;
}}

* {{
  box-sizing: border-box;
}}

body {{
  margin: 0;
  padding: 0;
  background-color: var(--paper-bg);
  color: var(--sumi-black);
  font-family: 'Zen Kaku Gothic New', -apple-system, sans-serif;
  font-size: 13px;
  line-height: 1.6;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}}

/* 畫面列印提示列（列印時自動隱藏） */
.screen-header {{
  background: var(--sumi-black);
  color: #ffffff;
  padding: 12px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 13px;
  font-weight: 700;
}}
.screen-btn {{
  background: var(--level-color);
  color: #ffffff;
  border: 1.5px solid #ffffff;
  padding: 6px 16px;
  border-radius: 6px;
  font-weight: 800;
  cursor: pointer;
}}
@media print {{
  .screen-header {{ display: none !important; }}
  body {{ background: #ffffff !important; }}
  .page-break {{ page-break-after: always; break-after: page; }}
}}

.page-container {{
  max-width: 820px;
  margin: 0 auto;
  padding: 24px 20px;
}}

/* 封面封底日雜風 */
.cover-page {{
  border: 3px solid var(--sumi-black);
  padding: 40px 30px;
  background: #ffffff;
  text-align: center;
  min-height: 920px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: 6px 6px 0px var(--sumi-black);
  margin-bottom: 30px;
}}
.mag-brand {{
  font-family: 'Cinzel', serif;
  font-size: 16px;
  letter-spacing: 0.3em;
  font-weight: 900;
  color: var(--sumi-black);
  border-bottom: 2px solid var(--sumi-black);
  padding-bottom: 12px;
}}
.cover-stamp {{
  display: inline-block;
  background: var(--level-color);
  color: #ffffff;
  font-family: 'Cinzel', serif;
  font-size: 72px;
  font-weight: 900;
  padding: 10px 36px;
  border: 3px solid var(--sumi-black);
  box-shadow: 5px 5px 0px var(--sumi-black);
  margin: 30px 0 10px 0;
}}
.cover-title {{
  font-family: 'Noto Serif JP', serif;
  font-size: 28px;
  font-weight: 800;
  margin: 15px 0 5px 0;
  letter-spacing: 0.05em;
}}
.cover-sub {{
  font-size: 15px;
  font-weight: 700;
  color: rgba(43, 37, 35, 0.75);
}}
.cover-stats {{
  display: flex;
  justify-content: center;
  gap: 20px;
  margin: 40px 0;
}}
.stat-box {{
  border: 2px solid var(--sumi-black);
  padding: 12px 20px;
  background: var(--level-tint);
  border-radius: 8px;
  box-shadow: 3px 3px 0px var(--sumi-black);
}}
.stat-num {{
  font-size: 26px;
  font-weight: 900;
  color: var(--level-color);
}}
.stat-label {{
  font-size: 12px;
  font-weight: 700;
}}
.cover-footer {{
  font-size: 12px;
  font-weight: 700;
  border-top: 1.5px dashed var(--sumi-black);
  padding-top: 15px;
}}

/* 專題章節標題 */
.section-header {{
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 3px solid var(--sumi-black);
  padding-bottom: 8px;
  margin: 36px 0 20px 0;
}}
.sec-pill {{
  background: var(--level-color);
  color: #ffffff;
  font-size: 12px;
  font-weight: 900;
  padding: 4px 10px;
  border-radius: 6px;
  border: 1.5px solid var(--sumi-black);
}}
.sec-title {{
  margin: 0;
  font-size: 20px;
  font-weight: 900;
  letter-spacing: 0.04em;
}}

/* 文法卡片網格 */
.grammar-grid {{
  display: grid;
  grid-template-columns: 1fr;
  gap: 18px;
}}
.grammar-card {{
  background: #ffffff;
  border: 2px solid var(--sumi-black);
  border-radius: 10px;
  padding: 16px 18px;
  box-shadow: 3px 3px 0px var(--sumi-black);
  break-inside: avoid;
  page-break-inside: avoid;
}}
.card-head {{
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}}
.pt-tag {{
  background: var(--level-tint);
  color: var(--sumi-black);
  font-size: 11px;
  font-weight: 800;
  padding: 2px 8px;
  border-radius: 4px;
  border: 1px solid rgba(43,37,35,0.3);
}}
.pt-title {{
  margin: 0;
  font-size: 17px;
  font-weight: 900;
  color: var(--sumi-black);
}}
.card-formula {{
  background: var(--level-tint);
  border-left: 3px solid var(--level-color);
  padding: 6px 10px;
  font-size: 12px;
  margin-bottom: 8px;
  border-radius: 0 6px 6px 0;
}}
.card-formula code {{
  font-family: monospace;
  font-weight: 700;
}}
.card-expl {{
  margin: 6px 0 10px 0;
  font-size: 12.5px;
  line-height: 1.55;
}}
.card-examples {{
  background: #faf7f2;
  border: 1px solid rgba(43,37,35,0.2);
  border-radius: 6px;
  padding: 8px 12px;
  font-size: 12px;
}}
.ex-row {{
  margin-bottom: 6px;
}}
.ex-row:last-child {{
  margin-bottom: 0;
}}
.ex-trans {{
  font-size: 11.5px;
  color: rgba(43,37,35,0.7);
  margin-left: 18px;
}}
.card-alert {{
  background: #fff9e6;
  border: 1px solid #e0a800;
  border-radius: 6px;
  padding: 8px 10px;
  font-size: 11.5px;
  color: #664d03;
  margin-top: 8px;
}}

/* 速查表格與滾動包裝 */
.table-scroll-hint {{
  display: none;
  font-size: 11px;
  font-weight: 700;
  color: rgba(43,37,35,0.6);
  margin-bottom: 6px;
  text-align: right;
}}
.table-wrap {{
  width: 100%;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  margin-bottom: 24px;
  border: 2px solid var(--sumi-black);
  border-radius: 8px;
  box-shadow: 3px 3px 0px var(--sumi-black);
  background: #ffffff;
}}
.data-table {{
  width: 100%;
  min-width: 680px;
  border-collapse: collapse;
  background: #ffffff;
  border: none;
  margin-bottom: 0;
}}
.data-table th {{
  background: var(--sumi-black);
  color: #ffffff;
  font-size: 11.5px;
  font-weight: 800;
  padding: 9px 12px;
  text-align: left;
  white-space: nowrap;
}}
.data-table td {{
  border-top: 1px solid rgba(43,37,35,0.15);
  padding: 8px 12px;
  vertical-align: middle;
}}
.data-table tr:nth-child(even) {{
  background: var(--paper-bg);
}}
.td-num {{
  width: 40px;
  min-width: 40px;
  text-align: center;
  font-size: 11px;
  font-weight: 800;
  color: rgba(43,37,35,0.6);
}}
.td-title {{
  width: 130px;
  min-width: 110px;
  font-weight: 800;
  white-space: nowrap;
}}
.td-formula {{
  width: 200px;
  min-width: 180px;
  font-family: monospace;
}}
.td-expl {{
  min-width: 260px;
  line-height: 1.55;
  color: rgba(43,37,35,0.85);
}}
.td-idx {{
  width: 36px;
  min-width: 36px;
  font-size: 11px;
  font-weight: 700;
  color: rgba(43,37,35,0.5);
  text-align: center;
}}
  color: rgba(43,37,35,0.5);
}}
.ruby-cell ruby {{
  ruby-align: center;
  ruby-position: over;
  margin-inline: 0.05em;
}}
.ruby-cell rt {{
  font-size: 0.52em;
  font-weight: 700;
  border-bottom: 1.5px solid var(--level-tint);
  color: rgba(43,37,35,0.7);
}}
.romaji-sub {{
  display: block;
  font-size: 10px;
  color: rgba(43,37,35,0.5);
}}
.pos-badge {{
  background: var(--level-tint);
  font-size: 10.5px;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 4px;
  white-space: nowrap;
}}
.td-meaning {{
  font-weight: 700;
  font-size: 12px;
}}
.td-ex {{
  font-size: 11.5px;
  line-height: 1.4;
}}
.ex-zh {{
  color: rgba(43,37,35,0.65);
}}

/* 隨堂測驗題 */
.quiz-item {{
  background: #ffffff;
  border: 1.5px solid var(--sumi-black);
  border-radius: 8px;
  padding: 10px 14px;
  margin-bottom: 12px;
  break-inside: avoid;
}}
.q-badge {{
  background: var(--level-color);
  color: #ffffff;
  font-size: 10px;
  font-weight: 800;
  padding: 2px 6px;
  border-radius: 4px;
}}
.quiz-q {{
  font-size: 13px;
  font-weight: 800;
  margin-bottom: 6px;
}}
.quiz-opts {{
  font-size: 12px;
  color: rgba(43,37,35,0.85);
  margin-bottom: 6px;
}}
.quiz-ans-toggle {{
  font-size: 11.5px;
  background: var(--level-tint);
  padding: 4px 8px;
  border-radius: 4px;
  color: #2b2523;
}}

@media screen and (max-width: 680px) {{
  .page-container {{
    padding: 8px 8px;
    width: 100%;
    max-width: 100%;
    overflow-x: hidden;
  }}
  .cover-page {{
    padding: 20px 14px;
    min-height: auto;
    border-width: 2px;
    margin-bottom: 16px;
  }}
  .mag-brand {{
    font-size: 13px;
    letter-spacing: 0.2em;
    padding-bottom: 8px;
  }}
  .cover-stamp {{
    font-size: 38px;
    padding: 6px 20px;
    margin: 16px 0 8px 0;
    border-width: 2px;
  }}
  .cover-title {{
    font-size: 18px;
    margin: 10px 0 4px 0;
  }}
  .cover-sub {{
    font-size: 12px;
  }}
  .cover-stats {{
    gap: 8px;
    margin: 16px 0;
    flex-wrap: wrap;
  }}
  .stat-box {{
    padding: 6px 10px;
  }}
  .stat-num {{
    font-size: 18px;
  }}
  .stat-label {{
    font-size: 10.5px;
  }}
  .cover-footer {{
    font-size: 10px;
    padding-top: 10px;
  }}
  .section-title {{
    font-size: 16px;
  }}
  .table-scroll-hint {{
    display: block;
  }}
  .data-table th, .data-table td {{
    padding: 7px 10px;
    font-size: 11px;
  }}
  .card-box, .quiz-box {{
    padding: 10px 8px;
    margin-bottom: 10px;
  }}
  .card-point {{
    font-size: 15px;
  }}
}}
</style>
</head>
{screen_header_html}

<div class="page-container">

  <!-- 封面 -->
  <div class="cover-page page-break">
    <div class="mag-brand">NIKKEN TECHO ・ JAPANESE LANGUAGE PROFICIENCY TEST</div>
    <div>
      <div class="cover-stamp">{lv_upper}</div>
      <h1 class="cover-title">考場最後 30 分鐘文法公式＆單字速查手冊</h1>
      <p class="cover-sub">{sub_title}</p>
      <div class="cover-stats">
        <div class="stat-box">
          <div class="stat-num">{total_grammar}</div>
          <div class="stat-label">必考文法點</div>
        </div>
        <div class="stat-box">
          <div class="stat-num">{total_vocab}</div>
          <div class="stat-label">逐字振假名單字</div>
        </div>
        <div class="stat-box">
          <div class="stat-num">{total_quizzes}</div>
          <div class="stat-label">實戰練習題</div>
        </div>
      </div>
    </div>
    <div class="cover-footer">
      日檢手帖 NIKKEN TECHO ｜ 像翻雜誌一樣，把日檢讀完 ｜ jlpt.chiaoban.com
    </div>
  </div>

  <!-- 第一章：文法公式速查表 -->
  <div class="section-header">
    <span class="sec-pill">CHAPTER 01</span>
    <h2 class="sec-title">{lv_upper} 文法公式速查清單（考前必背）</h2>
  </div>
  <div class="table-scroll-hint">👈 可左右滑動查看完整公式與核心語意 👉</div>
  <div class="table-wrap">
    <table class="data-table">
      <thead>
        <tr>
          <th style="width:40px; text-align:center;">課</th>
          <th style="width:130px; white-space:nowrap;">句型</th>
          <th style="width:200px;">接續公式</th>
          <th style="min-width:260px;">核心語意</th>
        </tr>
      </thead>
      <tbody>
        {"".join(cheat_sheet_rows)}
      </tbody>
    </table>
  </div>

  <!-- 第二章：文法核心深度解構卡片 -->
  <div class="section-header page-break">
    <span class="sec-pill">CHAPTER 02</span>
    <h2 class="sec-title">{lv_upper} 文法點完全解析卡片（公式・真例句・陷阱）</h2>
  </div>
  <div class="grammar-grid">
    {"".join(grammar_cards_html)}
  </div>

  <!-- 第三章：實戰測驗題 -->
  <div class="section-header page-break">
    <span class="sec-pill">CHAPTER 03</span>
    <h2 class="sec-title">{lv_upper} 考前隨堂實戰驗證（附答案詳解）</h2>
  </div>
  <div class="quiz-list">
    {"".join(quiz_section_html)}
  </div>

  <!-- 第四章：逐字振假名單字手帖 -->
  <div class="section-header page-break">
    <span class="sec-pill">CHAPTER 04</span>
    <h2 class="sec-title">{lv_upper} 完整高頻單字手帖（逐字振假名標註）</h2>
  </div>
  <div class="table-scroll-hint">👈 可左右滑動查看完整單字標音、釋義與例句 👉</div>
  <div class="table-wrap">
    <table class="data-table">
      <thead>
        <tr>
          <th style="width:40px; text-align:center;">#</th>
          <th style="width:130px; white-space:nowrap;">單字（標音）</th>
          <th style="width:70px; text-align:center;">詞性</th>
          <th style="width:140px;">中文釋義</th>
          <th style="min-width:260px;">實用日文例句與翻譯</th>
        </tr>
      </thead>
      <tbody>
        {"".join(vocab_rows)}
      </tbody>
    </table>
  </div>

  <div style="text-align:center; padding: 30px 0; font-size:12px; font-weight:700; color:rgba(43,37,35,0.5);">
    ── 日檢手帖 NIKKEN TECHO 祝您順利合格・jlpt.chiaoban.com ──
  </div>

</div>

</body>
</html>"""

  out_html_path.write_text(html_content, encoding="utf-8")


def main() -> None:
  OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
  print("📦 開始產生 N1～N5 獨立分級數位商品套組...")

  summary_table = []

  for lv_key in ["n5", "n4", "n3", "n2", "n1"]:
    conf = LEVEL_CONFIG[lv_key]
    lv_upper = conf["upper"]

    # 讀取資料
    vocab_path = REPO_ROOT / "src" / "data" / "vocabulary" / f"{lv_key}.json"
    grammar_path = REPO_ROOT / "src" / "data" / "grammar" / f"{lv_key}.json"
    with open(vocab_path, encoding="utf-8") as f:
      vocab_data = json.load(f)
    with open(grammar_path, encoding="utf-8") as f:
      grammar_data = json.load(f)

    # 建立該級別獨立目錄
    lv_out_dir = OUTPUT_DIR / lv_key
    lv_out_dir.mkdir(parents=True, exist_ok=True)

    apkg_file = lv_out_dir / f"日檢手帖-{lv_upper}-單字文法手帖.apkg"
    html_file = lv_out_dir / f"日檢手帖-{lv_upper}-考場速查講義手冊.html"
    sample_html_file = lv_out_dir / f"日檢手帖-{lv_upper}-試閱講義手冊.html"
    readme_file = lv_out_dir / f"README-使用說明.txt"

    # 1. 產生 Anki 牌組
    card_count = create_anki_deck_package(lv_key, vocab_data, grammar_data, apkg_file)

    # 2. 產生 FUDGE 日雜風 A4 列印講義 (完整付費版，僅打包進 ZIP)
    generate_printable_html_handbook(lv_key, vocab_data, grammar_data, html_file, is_sample=False)

    # 3. 產生 FUDGE 日雜風 A4 試閱樣章 (僅展示前數篇＋解鎖遮罩，供網頁公開預覽)
    generate_printable_html_handbook(lv_key, vocab_data, grammar_data, sample_html_file, is_sample=True)

    # 3. 附上 README 說明檔
    readme_content = f"""【日檢手帖】{lv_upper} 完整備考數位套組

感謝您的支持！本套組包含兩大核心教材，助您在 JLPT {lv_upper} 取得高分：

1. 《日檢手帖-{lv_upper}-單字文法手帖.apkg》
   - 包含 {len(vocab_data)} 張高頻單字卡 ＋ {sum(len(l.get('grammar_points',[])) for l in grammar_data)} 張文法核心卡（共 {card_count} 張字卡）。
   - 【使用方式】：
     1. 請先下載免費的 Anki 軟體（電腦版至 apps.ankiweb.net 下載；手機至 App Store / Google Play 搜尋 AnkiMobile / AnkiDroid）。
     2. 雙擊直接開啟本 .apkg 檔案，或在 Anki 點擊「檔案」→「匯入」，即可自動匯入完成！
     3. 每日抽 10～20 分鐘複習，Anki 會根據間隔重複演算法自動在您快忘記時提醒您。

2. 《日檢手帖-{lv_upper}-考場速查講義手冊.html》
   - 採用日雜 FUDGE / CLUEL 風格設計之 A4 可列印手冊。
   - 【使用方式】：
     - 用任何電腦瀏覽器（Chrome, Safari, Edge）打開本檔案。
     - 點右上角「🖨️ 立即列印或儲存為 PDF」，在列印視窗中「目的地」選擇「另存為 PDF」，紙張選 A4，即可匯出精美的高解析度 PDF 講義！
     - 可存入 iPad GoodNotes 畫重點，或列印成紙本帶進考場最後 30 分鐘複習！

官方網站：日檢手帖 NIKKEN TECHO（jlpt.chiaoban.com）
祝您考試順利，高分及格！
"""
    readme_file.write_text(readme_content, encoding="utf-8")

    # 4. 打包成可直接上架的 ZIP
    zip_path = OUTPUT_DIR / f"日檢手帖-{lv_upper}-完全備考套組.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
      zf.write(apkg_file, arcname=apkg_file.name)
      zf.write(html_file, arcname=html_file.name)
      zf.write(readme_file, arcname=readme_file.name)

    size_mb = zip_path.stat().st_size / (1024 * 1024)
    summary_table.append(f"| **{lv_upper}** | {len(vocab_data)} 單字 ＋ {sum(len(l.get('grammar_points',[])) for l in grammar_data)} 文法 | {card_count} 張 | {zip_path.name} ({size_mb:.2f} MB) |")

  print("\n" + "=" * 60)
  print("🎉 N1～N5 五大獨立分級套組全部生成完成！")
  print("=" * 60)
  print("\n".join(summary_table))


if __name__ == "__main__":
  main()
