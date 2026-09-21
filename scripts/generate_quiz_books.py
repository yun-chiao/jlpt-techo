#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日檢手帖・JLPT N1～N5 題型專攻・500 題全真手帳題本生成器 (scripts/generate_quiz_books.py)

功能：
1. 讀取 src/data/quiz/n{1..5}.json（每級 500 題，全庫 2,500 題）。
2. 為每個級別產生高質感、A4 / GoodNotes 向量排版的日雜手帳題本：
   - 【實戰空白刷題本】（全 500 題純題目＋答案矩陣卡，留有手寫做題與筆記空白）
   - 【逐題詳解訂正本】（全 500 題含完整句、中日對照、💡考點陷阱拆解與手帳錯題訂正欄）
   - 【試閱體驗本】（精選 30 題試閱體驗，含詳解，供官網直接在線開啟預覽）
3. 打包 ZIP 套組至 dist-products/quiz/，並同步試閱 HTML 至 public/dist-products/quiz/。
"""

import json
import os
import shutil
import sys
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
QUIZ_DATA_DIR = REPO_ROOT / "src" / "data" / "quiz"
DIST_PRODUCTS_DIR = REPO_ROOT / "dist-products" / "quiz"
PUBLIC_PRODUCTS_DIR = REPO_ROOT / "public" / "dist-products" / "quiz"

DIST_PRODUCTS_DIR.mkdir(parents=True, exist_ok=True)
PUBLIC_PRODUCTS_DIR.mkdir(parents=True, exist_ok=True)

LEVEL_INFO = {
    "n1": {
        "upper": "N1",
        "name": "N1 最高殿堂",
        "sub": "抽象邏輯、書面政經與古典文語",
        "color": "#E63956",
        "tint": "#FFEAEF",
        "price_usd": "$14.99",
        "price_twd": "約 NT$460",
    },
    "n2": {
        "upper": "N2",
        "name": "N2 中高階核心",
        "sub": "日本求職留學必備・商務時事與長文理解",
        "color": "#FF6B35",
        "tint": "#FFF0E8",
        "price_usd": "$12.99",
        "price_twd": "約 NT$400",
    },
    "n3": {
        "upper": "N3",
        "name": "N3 實用分水嶺",
        "sub": "跨越日檢分水嶺・日常複雜情境與職場銜接",
        "color": "#7CB518",
        "tint": "#F2F8E6",
        "price_usd": "$9.99",
        "price_twd": "約 NT$310",
    },
    "n4": {
        "upper": "N4",
        "name": "N4 進階基礎",
        "sub": "日常會話・敬語與使役被動全面攻略",
        "color": "#0096C7",
        "tint": "#E2F4FA",
        "price_usd": "$7.99",
        "price_twd": "約 NT$250",
    },
    "n5": {
        "upper": "N5",
        "name": "N5 入門基石",
        "sub": "零基礎新手・基礎助詞動詞變化一本通",
        "color": "#8338EC",
        "tint": "#F2E8FD",
        "price_usd": "$5.99",
        "price_twd": "約 NT$190",
    },
}

BOOK_BASE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@500;700&family=Noto+Serif+JP:wght@600;700;900&family=Noto+Serif+TC:wght@600;700&family=Zen+Kaku+Gothic+New:wght@500;700;900&display=swap');

:root {
  --sumi: #2B2523;
  --canvas: #FAF7F2;
  --card: #FFFFFF;
  --butter: #FFE5A3;
  --oatmeal: #EFEAE1;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: "Zen Kaku Gothic New", "Noto Sans TC", sans-serif;
  background-color: #E5E0D8;
  color: var(--sumi);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}

.screen-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: #2B2523;
  color: #FFFFFF;
  padding: 12px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.screen-header h1 {
  font-size: 15px;
  font-weight: 900;
  display: flex;
  align-items: center;
  gap: 10px;
}

.screen-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.btn-print {
  background: var(--butter);
  color: var(--sumi);
  font-weight: 800;
  font-size: 13px;
  border: 1.5px solid var(--sumi);
  padding: 6px 14px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.15s ease;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.btn-print:hover {
  background: #FFFFFF;
  transform: translate(-1px, -1px);
}

.book-container {
  max-width: 210mm;
  margin: 30px auto;
  background: #FFFFFF;
  box-shadow: 0 10px 30px rgba(0,0,0,0.12);
}

@page {
  size: A4 portrait;
  margin: 14mm 14mm 16mm 14mm;
}

@media print {
  body {
    background: #FFFFFF;
  }
  .screen-header {
    display: none !important;
  }
  .book-container {
    max-width: 100%;
    margin: 0;
    box-shadow: none;
  }
  .page-break {
    page-break-before: always !important;
    break-before: page !important;
  }
  .no-break {
    page-break-inside: avoid !important;
    break-inside: avoid !important;
  }
}

/* 封面樣式 */
.book-cover {
  min-height: 275mm;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 24mm 20mm;
  border: 4px solid var(--sumi);
  margin: 10mm;
  background: var(--canvas);
  position: relative;
}

.cover-header {
  border-bottom: 2px solid var(--sumi);
  padding-bottom: 16px;
}

.cover-issue {
  font-family: 'DM Mono', monospace;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1.5px;
  color: rgba(43,37,35,0.7);
}

.cover-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 6px;
  border: 2px solid var(--sumi);
  color: #FFFFFF;
  font-weight: 900;
  font-size: 20px;
  font-family: 'DM Mono', monospace;
  box-shadow: 3px 3px 0px var(--sumi);
  margin-top: 12px;
}

.cover-title-group {
  margin: 40px 0;
}

.cover-jp-sub {
  font-family: 'Noto Serif JP', serif;
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 2px;
  color: rgba(43,37,35,0.8);
  margin-bottom: 8px;
}

.cover-title {
  font-family: 'Noto Serif JP', serif;
  font-size: 38px;
  font-weight: 900;
  line-height: 1.25;
  color: var(--sumi);
  letter-spacing: -0.5px;
}

.cover-desc {
  font-size: 14px;
  color: rgba(43,37,35,0.85);
  margin-top: 16px;
  line-height: 1.7;
}

.cover-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-top: 28px;
}

.stat-box {
  background: #FFFFFF;
  border: 2px solid var(--sumi);
  border-radius: 8px;
  padding: 12px;
  text-align: center;
  box-shadow: 2px 2px 0px var(--sumi);
}

.stat-num {
  font-family: 'DM Mono', monospace;
  font-size: 22px;
  font-weight: 900;
}

.stat-label {
  font-size: 11px;
  font-weight: 700;
  color: rgba(43,37,35,0.7);
  margin-top: 2px;
}

.cover-footer {
  border-top: 2px solid var(--sumi);
  padding-top: 16px;
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  font-family: 'DM Mono', monospace;
  font-size: 11px;
  color: rgba(43,37,35,0.6);
}

/* 內容頁面通用 */
.page-sheet {
  padding: 18mm 16mm;
  min-height: 280mm;
}

.sheet-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 2px solid var(--sumi);
  padding-bottom: 8px;
  margin-bottom: 20px;
}

.sheet-part-badge {
  font-family: 'DM Mono', monospace;
  font-size: 11px;
  font-weight: 900;
  background: var(--sumi);
  color: #FFFFFF;
  padding: 3px 8px;
  border-radius: 4px;
}

.sheet-title {
  font-family: 'Noto Serif JP', serif;
  font-size: 15px;
  font-weight: 900;
}

.sheet-page-num {
  font-family: 'DM Mono', monospace;
  font-size: 11px;
  color: rgba(43,37,35,0.5);
}

/* 題目卡片樣式 */
.quiz-item-box {
  border: 1.5px solid var(--sumi);
  border-radius: 8px;
  padding: 12px 14px;
  margin-bottom: 12px;
  background: #FFFFFF;
  page-break-inside: avoid;
  break-inside: avoid;
}

.q-meta-line {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 6px;
}

.q-num-tag {
  font-family: 'DM Mono', monospace;
  font-size: 11px;
  font-weight: 900;
  color: var(--sumi);
}

.q-grammar-tag {
  font-family: 'DM Mono', monospace;
  font-size: 10px;
  font-weight: 700;
  color: rgba(43,37,35,0.6);
}

.q-sentence {
  font-family: 'Noto Serif JP', serif;
  font-size: 13.5px;
  font-weight: 700;
  line-height: 1.6;
  margin-bottom: 10px;
}

.q-blank-under {
  display: inline-block;
  min-width: 48px;
  border-bottom: 2px solid var(--sumi);
  text-align: center;
  padding: 0 4px;
  font-family: 'DM Mono', monospace;
}

.q-options-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 6px 12px;
}

.opt-pill {
  font-family: 'Noto Serif JP', serif;
  font-size: 12px;
  font-weight: 600;
  padding: 4px 8px;
  border-radius: 4px;
  border: 1px solid rgba(43,37,35,0.25);
  background: var(--canvas);
  display: flex;
  align-items: center;
  gap: 6px;
}

.opt-num {
  font-family: 'DM Mono', monospace;
  font-size: 10px;
  font-weight: 900;
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--sumi);
  border-radius: 50%;
  background: #FFFFFF;
}

/* 詳解區塊樣式（訂正本專用） */
.solution-box {
  margin-top: 8px;
  padding: 8px 10px;
  background: var(--canvas);
  border-left: 3px solid var(--sumi);
  border-radius: 0 6px 6px 0;
  font-size: 11.5px;
}

.sol-ans-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.sol-badge {
  background: var(--butter);
  border: 1px solid var(--sumi);
  padding: 1px 6px;
  border-radius: 4px;
  font-weight: 900;
  font-size: 11px;
}

.sol-full {
  font-family: 'Noto Serif JP', serif;
  font-weight: 700;
  color: var(--sumi);
}

.sol-expl {
  color: rgba(43,37,35,0.9);
  line-height: 1.5;
  margin-top: 3px;
}

.note-taking-space {
  margin-top: 6px;
  padding: 6px 8px;
  border: 1px dashed rgba(43,37,35,0.25);
  border-radius: 4px;
  background: #FFFFFF;
  font-size: 10.5px;
  color: rgba(43,37,35,0.4);
}

/* 篇章閱讀題排版 */
.passage-box {
  background: var(--canvas);
  border: 1.5px solid var(--sumi);
  border-radius: 8px;
  padding: 14px;
  margin-bottom: 14px;
  font-family: 'Noto Serif JP', serif;
  font-size: 12.5px;
  line-height: 1.8;
}

.passage-title-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
  border-bottom: 1px dashed rgba(43,37,35,0.2);
  padding-bottom: 6px;
}

.passage-title {
  font-weight: 900;
  font-size: 14px;
}

.passage-genre {
  font-family: 'DM Mono', monospace;
  font-size: 10.5px;
  background: var(--oatmeal);
  padding: 2px 6px;
  border-radius: 4px;
  border: 1px solid rgba(43,37,35,0.2);
}

/* 答案卡速查矩陣 */
.answer-key-table {
  width: 100%;
  border-collapse: collapse;
  font-family: 'DM Mono', monospace;
  font-size: 11px;
  margin-top: 14px;
}

.answer-key-table th, .answer-key-table td {
  border: 1px solid var(--sumi);
  padding: 6px 4px;
  text-align: center;
}

.answer-key-table th {
  background: var(--sumi);
  color: #FFFFFF;
  font-weight: 900;
}

.answer-key-table tr:nth-child(even) td {
  background: var(--canvas);
}

.lock-cta-box {
  background: var(--canvas);
  border: 2px dashed var(--sumi);
  border-radius: 10px;
  padding: 24px;
  text-align: center;
  margin: 30px 0;
}
"""

def generate_blank_workbook_html(level_key: str, data: dict, is_preview: bool = False) -> str:
    conf = LEVEL_INFO[level_key]
    upper = conf["upper"]
    color = conf["color"]
    
    sentence_list = data["sentenceQuizzes"][:15 if is_preview else 300]
    star_list = data["starQuizzes"][:10 if is_preview else 125]
    passage_list = data["passageQuizzes"][:2 if is_preview else 25]
    
    edition_label = "【試閱體驗手帳題本（30 題精華版）】" if is_preview else "【考場實戰・純題目手寫空白題本（完整 500 題）】"

    p1_items = []
    for idx, q in enumerate(sentence_list, 1):
        q_text = q["question"].replace("（　　）", '<span class="q-blank-under">（　）</span>')
        opts = "".join([f'<div class="opt-pill"><span class="opt-num">{o_idx+1}</span>{opt}</div>' for o_idx, opt in enumerate(q["options"])])
        p1_items.append(f"""
        <div class="quiz-item-box">
          <div class="q-meta-line">
            <span class="q-num-tag">Q.{idx:02d}</span>
            <span class="q-grammar-tag">考點：{q.get('targetGrammar', '文法句型')}</span>
          </div>
          <div class="q-sentence">{q_text}</div>
          <div class="q-options-grid">{opts}</div>
        </div>
        """)

    p2_items = []
    for idx, q in enumerate(star_list, 1):
        pre = q["preText"]
        post = q["postText"]
        chunks = "".join([f'<div class="opt-pill"><span class="opt-num">{c_idx+1}</span>{c}</div>' for c_idx, c in enumerate(q["chunks"])])
        p2_items.append(f"""
        <div class="quiz-item-box">
          <div class="q-meta-line">
            <span class="q-num-tag">Q.{idx:02d}（★ 排序題）</span>
            <span class="q-grammar-tag">找出落在 ★ 號位置的選項</span>
          </div>
          <div class="q-sentence">{pre} ［ 1 ］ ［ 2 ］ ［ ★ ］ ［ 4 ］ {post}</div>
          <div class="q-options-grid">{chunks}</div>
        </div>
        """)

    p3_items = []
    for p_idx, p in enumerate(passage_list, 1):
        sub_qs = []
        for q in p["questions"]:
            opts = "".join([f'<div class="opt-pill"><span class="opt-num">{o_idx+1}</span>{opt}</div>' for o_idx, opt in enumerate(q["options"])])
            sub_qs.append(f"""
            <div style="margin-top:8px; padding-top:6px; border-top:1px solid rgba(43,37,35,0.15);">
              <div style="font-size:12px; font-weight:700; margin-bottom:4px;">【 空白 {q['blankNumber']:02d} 】應填入：</div>
              <div class="q-options-grid">{opts}</div>
            </div>
            """)
        sub_html = "".join(sub_qs)
        p3_items.append(f"""
        <div class="no-break" style="margin-bottom:20px;">
          <div class="passage-box">
            <div class="passage-title-bar">
              <span class="passage-title">📖 第 {p_idx:02d} 篇：{p['title']}</span>
              <span class="passage-genre">{p['genre']}</span>
            </div>
            <div style="white-space:pre-line;">{p['passage']}</div>
          </div>
          <div class="quiz-item-box" style="background:#FAF7F2;">
            {sub_html}
          </div>
        </div>
        """)

    ans_cells = []
    for idx, q in enumerate(sentence_list, 1):
        ans_cells.append(f"<td><strong>Q{idx}</strong>: {q['correctIndex']}</td>")
    rows = []
    for i in range(0, len(ans_cells), 10):
        rows.append("<tr>" + "".join(ans_cells[i:i+10]) + "</tr>")
    p1_key_html = "<table class='answer-key-table'><tbody>" + "".join(rows) + "</tbody></table>"

    lock_banner = ""
    if is_preview:
        lock_banner = f"""
        <div class="lock-cta-box page-break">
          <div style="font-size:32px;">📑 🔒</div>
          <h3 style="font-size:18px; font-weight:900; margin-top:8px;">【試閱本結束】完整 500 題收錄於正式手帳套組</h3>
          <p style="font-size:13px; color:rgba(43,37,35,0.8); margin:10px auto 16px auto; max-width:460px;">
            包含 300 題挖空＋125 題重組＋25 篇長文（共 75 題）！<br>
            正式版套組提供「純實戰手寫空白版」與「逐題手寫風詳解訂正版」雙 PDF 檔案，支援 iPad GoodNotes 向量手寫與 A4 高清列印。
          </p>
          <a href="https://buymeacoffee.com/chiaoban/extras" target="_blank" class="btn-print" style="background:{color}; color:#fff; padding:8px 24px; font-size:14px;">
            ☕ 前往商店贊助解鎖完整版 500 題套組（{conf['price_twd']}）→
          </a>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>日檢手帖｜{upper} 題型專攻・500題全真手帳題本（{ '試閱版' if is_preview else '實戰空白版' }）</title>
<style>
{BOOK_BASE_CSS}
</style>
</head>
<body>

<div class="screen-header">
  <h1>
    <span style="background:{color}; color:#fff; padding:2px 8px; border-radius:4px; font-family:'DM Mono';">{upper}</span>
    日檢手帖・500 題全真題型專攻手帳題本（{ '試閱版' if is_preview else '考場實戰空白版' }）
  </h1>
  <div class="screen-actions">
    <button onclick="window.print()" class="btn-print">🖨️ 列印 A4 / 轉存 PDF</button>
    <a href="/products?tab=quiz&level={level_key}" class="btn-print" style="background:#FFFFFF;">🛒 返回題庫專區</a>
  </div>
</div>

<div class="book-container">
  <!-- 封面 -->
  <div class="book-cover">
    <div class="cover-header">
      <div class="cover-issue">NIKKEN TECHO JLPT PRACTICE BOOK SERIES</div>
      <div class="cover-badge" style="background:{color};">{upper} 全真題型專攻</div>
    </div>
    
    <div class="cover-title-group">
      <div class="cover-jp-sub">JLPT {upper} 500 QUESTIONS WORKBOOK</div>
      <div class="cover-title">500 題厚切全真手帳題本</div>
      <div style="font-size:15px; font-weight:800; color:{color}; margin-top:6px;">{edition_label}</div>
      <p class="cover-desc">
        專為 iPad GoodNotes 手寫刷題與 A4 實體列印量身打造。<br>
        嚴格參照日本國際交流基金會官方全真日檢規格，完整涵蓋 Part 1 文法挖空、Part 2 ★ 號語序重組、Part 3 篇章脈絡長文三大題型。
      </p>
      
      <div class="cover-stats">
        <div class="stat-box">
          <div class="stat-num" style="color:{color};">{'15 題' if is_preview else '300 題'}</div>
          <div class="stat-label">PART 01 文法形式挖空</div>
        </div>
        <div class="stat-box">
          <div class="stat-num" style="color:{color};">{'10 題' if is_preview else '125 題'}</div>
          <div class="stat-label">PART 02 ★ 號語序重組</div>
        </div>
        <div class="stat-box">
          <div class="stat-num" style="color:{color};">{'2 篇 (5題)' if is_preview else '25 篇 (75題)'}</div>
          <div class="stat-label">PART 03 篇章長文專欄</div>
        </div>
      </div>
    </div>
    
    <div class="cover-footer">
      <div>日檢手帖編纂委員會 ｜ 題型專攻・三部曲系列</div>
      <div>FORMAT: GOODNOTES / NOTABILITY / A4 PRINT</div>
    </div>
  </div>

  <!-- PART 1 -->
  <div class="page-sheet page-break">
    <div class="sheet-header">
      <div style="display:flex; align-items:center; gap:8px;">
        <span class="sheet-part-badge" style="background:{color};">PART 01</span>
        <span class="sheet-title">文法形式の判断（形式挖空題）</span>
      </div>
      <span class="sheet-page-num">P.01</span>
    </div>
    {"".join(p1_items)}
  </div>

  <!-- PART 2 -->
  <div class="page-sheet page-break">
    <div class="sheet-header">
      <div style="display:flex; align-items:center; gap:8px;">
        <span class="sheet-part-badge" style="background:{color};">PART 02</span>
        <span class="sheet-title">文の組み立て（★ 號排序重組題）</span>
      </div>
      <span class="sheet-page-num">P.02</span>
    </div>
    {"".join(p2_items)}
  </div>

  <!-- PART 3 -->
  <div class="page-sheet page-break">
    <div class="sheet-header">
      <div style="display:flex; align-items:center; gap:8px;">
        <span class="sheet-part-badge" style="background:{color};">PART 03</span>
        <span class="sheet-title">文章の文法（篇章脈絡填空題）</span>
      </div>
      <span class="sheet-page-num">P.03</span>
    </div>
    {"".join(p3_items)}
  </div>

  <!-- 答案檢索矩陣 -->
  <div class="page-sheet page-break">
    <div class="sheet-header">
      <div style="display:flex; align-items:center; gap:8px;">
        <span class="sheet-part-badge" style="background:#2B2523;">ANSWER KEY</span>
        <span class="sheet-title">標準正解對照矩陣卡</span>
      </div>
      <span class="sheet-page-num">APPENDIX</span>
    </div>
    <p style="font-size:12px; color:rgba(43,37,35,0.7); margin-bottom:12px;">
      💡 作答完畢後可直接核對本表格快速計算答對題數：
    </p>
    {p1_key_html}
  </div>

  {lock_banner}
</div>

</body>
</html>
"""

def generate_solution_workbook_html(level_key: str, data: dict) -> str:
    conf = LEVEL_INFO[level_key]
    upper = conf["upper"]
    color = conf["color"]
    
    sentence_list = data["sentenceQuizzes"][:300]
    star_list = data["starQuizzes"][:125]
    passage_list = data["passageQuizzes"][:25]
    
    p1_items = []
    for idx, q in enumerate(sentence_list, 1):
        corr_idx = q["correctIndex"]
        corr_opt = q["options"][corr_idx - 1]
        q_text = q["question"].replace("（　　）", f'<span class="q-blank-under" style="background:var(--butter); font-weight:900;">（ {corr_opt} ）</span>')
        opts = "".join([f'<div class="opt-pill" style="{"background:var(--butter); font-weight:900; border:1.5px solid var(--sumi);" if o_idx+1 == corr_idx else ""}"><span class="opt-num">{o_idx+1}</span>{opt}{ " ✓ 正解" if o_idx+1 == corr_idx else "" }</div>' for o_idx, opt in enumerate(q["options"])])
        
        p1_items.append(f"""
        <div class="quiz-item-box">
          <div class="q-meta-line">
            <span class="q-num-tag">Q.{idx:02d}</span>
            <span class="q-grammar-tag">考點：{q.get('targetGrammar', '文法')}</span>
          </div>
          <div class="q-sentence">{q_text}</div>
          <div class="q-options-grid">{opts}</div>
          <div class="solution-box">
            <div class="sol-ans-row">
              <span class="sol-badge">正解 ({corr_idx})</span>
              <span class="sol-full">【 {corr_opt} 】</span>
            </div>
            <div class="sol-expl"><strong>💡 考點解析：</strong>{q['explanation']}</div>
            <div class="note-taking-space">✍️ 我的錯題訂正與筆記心得：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</div>
          </div>
        </div>
        """)

    p2_items = []
    for idx, q in enumerate(star_list, 1):
        star_num = q["correctOrder"][q["starIndex"]]
        star_chunk = q["chunks"][star_num - 1]
        chunks = "".join([f'<div class="opt-pill" style="{"background:var(--butter); font-weight:900; border:1.5px solid var(--sumi);" if c_idx+1 == star_num else ""}"><span class="opt-num">{c_idx+1}</span>{c}{ " ★ 正解" if c_idx+1 == star_num else "" }</div>' for c_idx, c in enumerate(q["chunks"])])
        
        p2_items.append(f"""
        <div class="quiz-item-box">
          <div class="q-meta-line">
            <span class="q-num-tag">Q.{idx:02d}</span>
            <span class="q-grammar-tag">★ 號重組題</span>
          </div>
          <div class="q-sentence" style="color:rgba(43,37,35,0.7);">{q['preText']} ＿＿ ＿＿ ★ ＿＿ {q['postText']}</div>
          <div class="q-options-grid">{chunks}</div>
          <div class="solution-box">
            <div class="sol-ans-row">
              <span class="sol-badge">正解順序</span>
              <span class="sol-full">{ " → ".join(str(n) for n in q['correctOrder']) } ｜ ★ 號位置為【 {star_num} 號：{star_chunk} 】</span>
            </div>
            <div class="sol-expl"><strong>完整句子：</strong>{q['fullSentence']}</div>
            <div class="sol-expl"><strong>中文翻譯：</strong>{q['translation']}</div>
            <div class="sol-expl"><strong>💡 語法拆解：</strong>{q['explanation']}</div>
            <div class="note-taking-space">✍️ 我的錯題訂正與筆記心得：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</div>
          </div>
        </div>
        """)

    p3_items = []
    for p_idx, p in enumerate(passage_list, 1):
        sub_qs = []
        for q in p["questions"]:
            c_idx = q["correctIndex"]
            opts = "".join([f'<div class="opt-pill" style="{"background:var(--butter); font-weight:900; border:1.5px solid var(--sumi);" if o_idx+1 == c_idx else ""}"><span class="opt-num">{o_idx+1}</span>{opt}{ " ✓" if o_idx+1 == c_idx else "" }</div>' for o_idx, opt in enumerate(q["options"])])
            sub_qs.append(f"""
            <div style="margin-top:8px; padding-top:6px; border-top:1px solid rgba(43,37,35,0.15);">
              <div style="font-size:12px; font-weight:700; margin-bottom:4px;">【 空白 {q['blankNumber']:02d} 】正解：({c_idx}) {q['options'][c_idx-1]}</div>
              <div class="q-options-grid">{opts}</div>
              <div class="sol-expl" style="font-size:11px; margin-top:4px;">💡 {q['explanation']}</div>
            </div>
            """)
        p3_items.append(f"""
        <div class="no-break" style="margin-bottom:20px;">
          <div class="passage-box">
            <div class="passage-title-bar">
              <span class="passage-title">📖 第 {p_idx:02d} 篇：{p['title']}</span>
              <span class="passage-genre">{p['genre']}</span>
            </div>
            <div style="white-space:pre-line;">{p['passage']}</div>
            <div style="margin-top:10px; padding-top:8px; border-top:1px dashed rgba(43,37,35,0.2); font-size:11.5px; color:rgba(43,37,35,0.8);">
              <strong>【全篇中文對照】：</strong>{p['translation']}
            </div>
          </div>
          <div class="quiz-item-box" style="background:#FAF7F2;">
            {"".join(sub_qs)}
          </div>
        </div>
        """)

    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>日檢手帖｜{upper} 題型專攻・500題全真手帳題本（逐題詳解訂正本）</title>
<style>
{BOOK_BASE_CSS}
</style>
</head>
<body>

<div class="screen-header">
  <h1>
    <span style="background:{color}; color:#fff; padding:2px 8px; border-radius:4px; font-family:'DM Mono';">{upper}</span>
    日檢手帖・500 題全真手帳題本（逐題手寫風詳解訂正本）
  </h1>
  <div class="screen-actions">
    <button onclick="window.print()" class="btn-print">🖨️ 列印 A4 / 轉存 PDF</button>
  </div>
</div>

<div class="book-container">
  <div class="book-cover">
    <div class="cover-header">
      <div class="cover-issue">NIKKEN TECHO SOLUTION & NOTES EDITION</div>
      <div class="cover-badge" style="background:{color};">{upper} 逐題手寫風詳解</div>
    </div>
    
    <div class="cover-title-group">
      <div class="cover-jp-sub">JLPT {upper} 500 COMPLETE SOLUTIONS</div>
      <div class="cover-title">500 題逐題詳解訂正手帳</div>
      <div style="font-size:15px; font-weight:800; color:{color}; margin-top:6px;">【考前訂正神器・考點語法全剖析】</div>
      <p class="cover-desc">
        完整收錄 500 題之正解選項標記、語法拆解、長文中日對照與考點筆記欄。<br>
        隨心在 iPad GoodNotes 上用螢光筆標記錯題，考前最後 30 分鐘只要複習這本錯題手帳即可安心赴考！
      </p>
    </div>
    
    <div class="cover-footer">
      <div>日檢手帖編纂委員會 ｜ 題型專攻・三部曲系列</div>
      <div>FORMAT: GOODNOTES / NOTABILITY / A4 PRINT</div>
    </div>
  </div>

  <!-- PART 1 詳解 -->
  <div class="page-sheet page-break">
    <div class="sheet-header">
      <div style="display:flex; align-items:center; gap:8px;">
        <span class="sheet-part-badge" style="background:{color};">PART 01</span>
        <span class="sheet-title">文法形式挖空・300 題逐題詳解</span>
      </div>
      <span class="sheet-page-num">SOLUTIONS P.01</span>
    </div>
    {"".join(p1_items)}
  </div>

  <!-- PART 2 詳解 -->
  <div class="page-sheet page-break">
    <div class="sheet-header">
      <div style="display:flex; align-items:center; gap:8px;">
        <span class="sheet-part-badge" style="background:{color};">PART 02</span>
        <span class="sheet-title">★ 號語序重組・125 題逐題詳解</span>
      </div>
      <span class="sheet-page-num">SOLUTIONS P.02</span>
    </div>
    {"".join(p2_items)}
  </div>

  <!-- PART 3 詳解 -->
  <div class="page-sheet page-break">
    <div class="sheet-header">
      <div style="display:flex; align-items:center; gap:8px;">
        <span class="sheet-part-badge" style="background:{color};">PART 03</span>
        <span class="sheet-title">篇章脈絡填空・25 篇長文逐題詳解</span>
      </div>
      <span class="sheet-page-num">SOLUTIONS P.03</span>
    </div>
    {"".join(p3_items)}
  </div>
</div>

</body>
</html>
"""

def generate_readme(level_key: str) -> str:
    conf = LEVEL_INFO[level_key]
    return f"""========================================================================
【日檢手帖 NIKKEN TECHO】JLPT {conf['upper']} 題型專攻・500 題全真手帳題本套組
========================================================================

感謝您贊助支持《日檢手帖》自學數位商品！
本套組包含為 iPad GoodNotes / Notability 手寫刷題以及 A4 實體列印量身打造的雙版本題本：

【內含檔案說明】：
1. `日檢手帖-{conf['upper']}-500題全真手帳題本-實戰空白版.html`
   - 包含 Part 1（300題）、Part 2（125題）、Part 3（25篇/75題）共 500 題純題目。
   - 雙擊即可在 Chrome、Safari 等瀏覽器開啟。
   - 點擊右上角「🖨️ 列印 A4 / 轉存 PDF」按鈕，即可匯出為高解析度 A4 PDF 匯入 iPad（GoodNotes）或列印成紙本。
   - 卷末附有標準答案速查矩陣卡。

2. `日檢手帖-{conf['upper']}-500題全真手帳題本-逐題詳解訂正版.html`
   - 完整 500 題的考點語法剖析、正解選項標記、中日對照長文與專屬手寫錯題筆記欄。
   - 專門用於考前訂正與衝刺複習。

3. `日檢手帖-{conf['upper']}-500題全真手帳題本-試閱版.html`
   - 30 題精華速覽版。

【使用建議】：
- 方式 A（iPad / 平板使用者）：在瀏覽器按列印 ➔ 另存為 PDF ➔ 匯入 GoodNotes ➔ 使用 Apple Pencil 像手帳一樣刷題、圈助詞與訂正。
- 方式 B（紙本愛好者）：使用雙面黑白或彩色列印（A4 規格），帶入考場作為最後 30 分鐘衝刺神手冊。

祝您順利考取 JLPT {conf['upper']} 高分及格！
官方網站：https://jlpt.chiaoban.com
"""

def main():
    print("🚀 開始產製 JLPT N1～N5 題型專攻 500 題全真手帳題本套組...")
    
    for lvl in ["n5", "n4", "n3", "n2", "n1"]:
        conf = LEVEL_INFO[lvl]
        upper = conf["upper"]
        json_path = QUIZ_DATA_DIR / f"{lvl}.json"
        
        if not json_path.exists():
            print(f"❌ 找不到 {json_path}")
            continue
            
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        print(f"📦 正在產製 {upper} 題本 HTML（共 500 題）...")
        
        preview_html = generate_blank_workbook_html(lvl, data, is_preview=True)
        preview_file = DIST_PRODUCTS_DIR / f"日檢手帖-{upper}-500題全真手帳題本-試閱版.html"
        with open(preview_file, "w", encoding="utf-8") as f:
            f.write(preview_html)
            
        public_preview = PUBLIC_PRODUCTS_DIR / f"日檢手帖-{upper}-500題全真手帳題本-試閱版.html"
        with open(public_preview, "w", encoding="utf-8") as f:
            f.write(preview_html)
            
        blank_html = generate_blank_workbook_html(lvl, data, is_preview=False)
        blank_file = DIST_PRODUCTS_DIR / f"日檢手帖-{upper}-500題全真手帳題本-實戰空白版.html"
        with open(blank_file, "w", encoding="utf-8") as f:
            f.write(blank_html)
            
        sol_html = generate_solution_workbook_html(lvl, data)
        sol_file = DIST_PRODUCTS_DIR / f"日檢手帖-{upper}-500題全真手帳題本-逐題詳解訂正版.html"
        with open(sol_file, "w", encoding="utf-8") as f:
            f.write(sol_html)
            
        readme_file = DIST_PRODUCTS_DIR / f"README-{upper}-使用說明.txt"
        with open(readme_file, "w", encoding="utf-8") as f:
            f.write(generate_readme(lvl))
            
        zip_path = DIST_PRODUCTS_DIR / f"日檢手帖-{upper}-500題全真手帳題本套組.zip"
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            zf.write(blank_file, arcname=f"日檢手帖-{upper}-500題全真手帳題本-實戰空白版.html")
            zf.write(sol_file, arcname=f"日檢手帖-{upper}-500題全真手帳題本-逐題詳解訂正版.html")
            zf.write(preview_file, arcname=f"日檢手帖-{upper}-500題全真手帳題本-試閱版.html")
            zf.write(readme_file, arcname="README-使用說明.txt")
            
        print(f"  ✓ {upper} 題本完成：{zip_path.name} ({zip_path.stat().st_size / 1024:.1f} KB)")
        
    all_zip = DIST_PRODUCTS_DIR / "日檢手帖-N1-N5-全真2500題手帳題本終身典藏包.zip"
    with zipfile.ZipFile(all_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for lvl in ["n5", "n4", "n3", "n2", "n1"]:
            upper = LEVEL_INFO[lvl]["upper"]
            blank_file = DIST_PRODUCTS_DIR / f"日檢手帖-{upper}-500題全真手帳題本-實戰空白版.html"
            sol_file = DIST_PRODUCTS_DIR / f"日檢手帖-{upper}-500題全真手帳題本-逐題詳解訂正版.html"
            if blank_file.exists():
                zf.write(blank_file, arcname=f"{upper}/日檢手帖-{upper}-500題全真手帳題本-實戰空白版.html")
            if sol_file.exists():
                zf.write(sol_file, arcname=f"{upper}/日檢手帖-{upper}-500題全真手帳題本-逐題詳解訂正版.html")
    print(f"🎉 全部完成！全套大禮包已產出：{all_zip.name} ({all_zip.stat().st_size / 1024:.1f} KB)")

if __name__ == "__main__":
    main()
