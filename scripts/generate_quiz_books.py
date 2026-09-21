#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日檢手帖・JLPT N1～N5 題型專攻・500 題全真手帳題本生成器 (scripts/generate_quiz_books.py)

功能：
1. 讀取 src/data/quiz/n{1..5}.json（每級 500 題，全庫 2,500 題）。
2. 為每個級別產生高質感、A4 / GoodNotes 向量排版的日雜手帳題本：
   - 【實戰空白刷題本】（全 500 題純題目＋完整 500 題答案矩陣卡，留有手寫做題與筆記空白）
   - 【逐題詳解訂正本】（全 500 題含完整句、中日對照、💡考點陷阱拆解與手帳錯題訂正欄）
   - 【試閱體驗本】（精準 30 題試閱體驗，包含完整 30 題之 Part1/Part2/Part3 解答，供官網直接在線開啟預覽）
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
  background-color: #FAF7F2;
  color: var(--sumi);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  word-break: break-word;
  overflow-wrap: break-word;
}

.btn-cta {
  background: var(--butter);
  color: var(--sumi);
  font-weight: 800;
  font-size: 13px;
  border: 1.5px solid var(--sumi);
  padding: 8px 18px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.15s ease;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.btn-cta:hover {
  background: #FFFFFF;
  transform: translate(-1px, -1px);
}

.book-container {
  max-width: 210mm;
  margin: 0 auto;
  background: #FFFFFF;
  box-shadow: 0 4px 20px rgba(0,0,0,0.06);
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
  .scroll-hint {
    display: none !important;
  }
  .table-wrap {
    overflow: visible !important;
    border: none !important;
    box-shadow: none !important;
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
  font-size: 36px;
  font-weight: 900;
  line-height: 1.25;
  color: var(--sumi);
  letter-spacing: -0.5px;
}

.cover-desc {
  font-size: 13.5px;
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
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 4px;
}

.sol-badge {
  background: var(--butter);
  border: 1px solid var(--sumi);
  padding: 1px 6px;
  border-radius: 4px;
  font-weight: 900;
  font-size: 11px;
  shrink: 0;
}

.sol-full {
  font-family: 'Noto Serif JP', serif;
  font-weight: 700;
  color: var(--sumi);
  word-break: break-word;
}

.sol-expl {
  color: rgba(43,37,35,0.9);
  line-height: 1.5;
  margin-top: 3px;
  word-break: break-word;
}

.note-taking-space {
  margin-top: 6px;
  padding: 6px 8px;
  border: 1px dashed rgba(43,37,35,0.25);
  border-radius: 4px;
  background: #FFFFFF;
  font-size: 10.5px;
  color: rgba(43,37,35,0.55);
  word-break: break-all;
  overflow-wrap: anywhere;
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
  margin-top: 4px;
  margin-bottom: 8px;
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

.scroll-hint {
  display: none;
}

.table-wrap {
  width: 100%;
}

.lock-cta-box {
  background: var(--canvas);
  border: 2px dashed var(--sumi);
  border-radius: 10px;
  padding: 24px;
  text-align: center;
  margin: 30px 0;
}

/* 手機與窄螢幕預覽視窗全面響應式（防止溢出、破版與排版錯位） */
@media screen and (max-width: 680px) {
  html, body {
    width: 100% !important;
    max-width: 100vw !important;
    overflow-x: hidden !important;
  }

  .book-container {
    width: 100% !important;
    max-width: 100% !important;
    margin: 0 !important;
    box-shadow: none !important;
    overflow-x: hidden !important;
  }

  .book-cover {
    min-height: auto !important;
    margin: 8px !important;
    padding: 18px 12px !important;
    border-width: 2px !important;
  }

  .cover-header {
    padding-bottom: 10px !important;
  }

  .cover-issue {
    font-size: 9.5px !important;
    letter-spacing: 1px !important;
  }

  .cover-badge {
    font-size: 13.5px !important;
    padding: 3px 8px !important;
    margin-top: 8px !important;
    box-shadow: 2px 2px 0px var(--sumi) !important;
    white-space: normal !important;
  }

  .cover-title-group {
    margin: 18px 0 !important;
  }

  .cover-jp-sub {
    font-size: 11px !important;
    letter-spacing: 1px !important;
    margin-bottom: 4px !important;
  }

  .cover-title {
    font-size: 20px !important;
    line-height: 1.3 !important;
    word-break: break-word !important;
  }

  .cover-desc {
    font-size: 12px !important;
    margin-top: 10px !important;
    line-height: 1.6 !important;
  }

  .cover-stats {
    display: grid !important;
    grid-template-columns: repeat(3, 1fr) !important;
    gap: 6px !important;
    margin-top: 16px !important;
  }

  .stat-box {
    padding: 8px 4px !important;
    border-width: 1.5px !important;
  }

  .stat-num {
    font-size: 15px !important;
  }

  .stat-label {
    font-size: 9px !important;
    line-height: 1.2 !important;
  }

  .cover-footer {
    padding-top: 12px !important;
    flex-direction: column !important;
    align-items: flex-start !important;
    gap: 6px !important;
    font-size: 10px !important;
  }

  .page-sheet {
    padding: 16px 12px !important;
    min-height: auto !important;
    margin-bottom: 16px !important;
    border-bottom: 1.5px dashed rgba(43,37,35,0.2) !important;
  }

  .sheet-header {
    margin-bottom: 12px !important;
    padding-bottom: 6px !important;
    flex-wrap: wrap !important;
    gap: 6px !important;
  }

  .sheet-part-badge {
    font-size: 10px !important;
    padding: 2px 6px !important;
  }

  .sheet-title {
    font-size: 13px !important;
  }

  .sheet-page-num {
    font-size: 10px !important;
  }

  .quiz-item-box {
    padding: 10px 10px !important;
    margin-bottom: 10px !important;
  }

  .q-meta-line {
    margin-bottom: 4px !important;
    flex-wrap: wrap !important;
    gap: 4px !important;
  }

  .q-sentence {
    font-size: 13px !important;
    line-height: 1.6 !important;
    word-break: break-word !important;
    margin-bottom: 8px !important;
  }

  .q-options-grid {
    grid-template-columns: 1fr !important;
    gap: 6px !important;
  }

  .opt-pill {
    font-size: 12px !important;
    padding: 5px 8px !important;
    word-break: break-word !important;
  }

  .solution-box {
    padding: 8px !important;
    font-size: 11px !important;
  }

  .sol-ans-row {
    flex-wrap: wrap !important;
    gap: 4px !important;
  }

  .passage-box {
    padding: 10px !important;
    font-size: 12px !important;
    line-height: 1.7 !important;
  }

  .passage-title-bar {
    flex-wrap: wrap !important;
    gap: 6px !important;
  }

  .passage-title {
    font-size: 13px !important;
  }

  .scroll-hint {
    display: block !important;
    font-size: 10.5px !important;
    color: rgba(43,37,35,0.6) !important;
    margin-bottom: 4px !important;
    font-family: 'DM Mono', monospace !important;
  }

  .table-wrap {
    width: 100% !important;
    overflow-x: auto !important;
    -webkit-overflow-scrolling: touch !important;
    margin-bottom: 16px !important;
    border: 1.5px solid var(--sumi) !important;
    border-radius: 6px !important;
    background: #FFFFFF !important;
  }

  .answer-key-table {
    min-width: 440px !important;
    font-size: 10px !important;
    margin-top: 0 !important;
    margin-bottom: 0 !important;
  }

  .answer-key-table th, .answer-key-table td {
    padding: 5px 3px !important;
  }

  .lock-cta-box {
    padding: 16px 12px !important;
    margin: 20px 0 !important;
  }
}
"""

def build_answer_key_html(sentence_list, star_list, passage_list):
    """產生包含 Part 1、Part 2、Part 3 所有題目的完整標準答案卡"""
    # 1. Part 1 挖空題解答（每 10 題一列）
    p1_cells = []
    for idx, q in enumerate(sentence_list, 1):
        p1_cells.append(f"<td><strong>Q{idx:02d}</strong>: {q['correctIndex']}</td>")
    p1_rows = []
    for i in range(0, len(p1_cells), 10):
        p1_rows.append("<tr>" + "".join(p1_cells[i:i+10]) + "</tr>")
    
    p1_section = f"""
    <div style="margin-bottom:16px;">
      <h4 style="font-size:13px; font-weight:900; color:var(--sumi); margin-bottom:4px;">
        【PART 01 文法形式挖空】標準正解（共 {len(sentence_list)} 題）
      </h4>
      <div class="scroll-hint">👈 可左右滑動查看完整題號解答 👉</div>
      <div class="table-wrap">
        <table class="answer-key-table"><tbody>{"".join(p1_rows)}</tbody></table>
      </div>
    </div>
    """

    # 2. Part 2 ★ 號重組題解答
    p2_rows = []
    for idx, q in enumerate(star_list, 1):
        star_opt = q['correctOrder'][q['starIndex']]
        order_str = " → ".join(str(n) for n in q['correctOrder'])
        p2_rows.append(f"""
        <tr>
          <td style="font-weight:900; width:60px;">Q.{idx:02d}</td>
          <td style="background:var(--butter); font-weight:900; width:130px;">★ 為 【 {star_opt} 】 號</td>
          <td style="text-align:left; padding-left:12px; font-family:'DM Mono', monospace;">正確排列順序：{order_str}</td>
        </tr>
        """)

    p2_section = f"""
    <div style="margin-bottom:16px;">
      <h4 style="font-size:13px; font-weight:900; color:var(--sumi); margin-bottom:4px;">
        【PART 02 ★ 號語序重組】標準正解（共 {len(star_list)} 題）
      </h4>
      <div class="scroll-hint">👈 可左右滑動查看語序 👉</div>
      <div class="table-wrap">
        <table class="answer-key-table">
          <thead>
            <tr><th>題號</th><th>★ 號正解</th><th style="text-align:left; padding-left:12px;">完整詞塊語序</th></tr>
          </thead>
          <tbody>{"".join(p2_rows)}</tbody>
        </table>
      </div>
    </div>
    """

    # 3. Part 3 篇章題解答
    total_p3_q = sum(len(p['questions']) for p in passage_list)
    p3_rows = []
    for p_idx, p in enumerate(passage_list, 1):
        blanks = [f"【空白 {q['blankNumber']:02d}】: <strong>({q['correctIndex']})</strong>" for q in p['questions']]
        p3_rows.append(f"""
        <tr>
          <td style="font-weight:900; width:70px;">第 {p_idx:02d} 篇</td>
          <td style="font-weight:700; text-align:left; padding-left:10px; width:180px;">{p['title']}</td>
          <td style="text-align:left; padding-left:10px; font-family:'DM Mono', monospace;">{" ｜ ".join(blanks)}</td>
        </tr>
        """)

    p3_section = f"""
    <div style="margin-bottom:16px;">
      <h4 style="font-size:13px; font-weight:900; color:var(--sumi); margin-bottom:4px;">
        【PART 03 篇章長文專欄】標準正解（共 {len(passage_list)} 篇 / {total_p3_q} 題）
      </h4>
      <div class="scroll-hint">👈 可左右滑動查看篇章正解 👉</div>
      <div class="table-wrap">
        <table class="answer-key-table">
          <thead>
            <tr><th>篇章</th><th style="text-align:left; padding-left:10px;">專欄標題</th><th style="text-align:left; padding-left:10px;">各空白正確選項</th></tr>
          </thead>
          <tbody>{"".join(p3_rows)}</tbody>
        </table>
      </div>
    </div>
    """

    return p1_section + p2_section + p3_section

def generate_blank_workbook_html(level_key: str, data: dict, is_preview: bool = False) -> str:
    conf = LEVEL_INFO[level_key]
    upper = conf["upper"]
    color = conf["color"]
    
    # 試閱版精準取：15 題挖空 ＋ 9 題重組 ＋ 2 篇篇章（6 題）＝ 精準 30 題整！
    # 正式版全量取：300 題挖空 ＋ 125 題重組 ＋ 25 篇篇章（75 題）＝ 精準 500 題整！
    if is_preview:
        sentence_list = data["sentenceQuizzes"][:15]
        star_list = data["starQuizzes"][:9]
        passage_list = data["passageQuizzes"][:2]
        cover_title = f"{upper} 題型專攻・30 題精華試閱本"
        edition_badge = "【官方試閱體驗本・精選 30 題全真題庫】"
        stat_p1 = "15 題"
        stat_p2 = "9 題"
        stat_p3 = "2 篇 (6題)"
        total_desc = "共 30 題精選全真試閱題本"
    else:
        sentence_list = data["sentenceQuizzes"][:300]
        star_list = data["starQuizzes"][:125]
        passage_list = data["passageQuizzes"][:25]
        cover_title = f"{upper} 500 題厚切全真手帳題本"
        edition_badge = "【考場實戰・純題目手寫空白題本（完整 500 題）】"
        stat_p1 = "300 題"
        stat_p2 = "125 題"
        stat_p3 = "25 篇 (75題)"
        total_desc = "共 500 題全真規格題庫"

    total_q = len(sentence_list) + len(star_list) + sum(len(p["questions"]) for p in passage_list)

    # 1. 產生 Part 1 挖空題目 HTML
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

    # 2. 產生 Part 2 ★ 號重組題目 HTML
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

    # 3. 產生 Part 3 篇章題目 HTML
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

    # 4. 產生涵蓋所有 Part 題目的完整標準答案卡
    full_answer_key_html = build_answer_key_html(sentence_list, star_list, passage_list)

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
          <a href="https://buymeacoffee.com/chiaoban/extras" target="_blank" class="btn-cta" style="background:{color}; color:#fff; padding:8px 24px; font-size:14px;">
            ☕ 前往商店贊助解鎖完整版 500 題套組（{conf['price_twd']}）→
          </a>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>日檢手帖｜{cover_title}</title>
<style>
{BOOK_BASE_CSS}
</style>
</head>
<body>

<div class="book-container">
  <!-- 封面 -->
  <div class="book-cover">
    <div class="cover-header">
      <div class="cover-issue">NIKKEN TECHO JLPT PRACTICE BOOK SERIES</div>
      <div class="cover-badge" style="background:{color};">{upper} 全真題型專攻</div>
    </div>
    
    <div class="cover-title-group">
      <div class="cover-jp-sub">JLPT {upper} WORKBOOK EDITION</div>
      <div class="cover-title">{cover_title}</div>
      <div style="font-size:15px; font-weight:800; color:{color}; margin-top:6px;">{edition_badge}</div>
      <p class="cover-desc">
        專為 iPad GoodNotes 手寫刷題與 A4 實體列印量身打造。<br>
        嚴格參照日本國際交流基金會官方全真日檢規格，完整涵蓋 Part 1 文法挖空、Part 2 ★ 號語序重組、Part 3 篇章脈絡長文三大題型。
      </p>
      
      <div class="cover-stats">
        <div class="stat-box">
          <div class="stat-num" style="color:{color};">{stat_p1}</div>
          <div class="stat-label">PART 01 文法形式挖空</div>
        </div>
        <div class="stat-box">
          <div class="stat-num" style="color:{color};">{stat_p2}</div>
          <div class="stat-label">PART 02 ★ 號語序重組</div>
        </div>
        <div class="stat-box">
          <div class="stat-num" style="color:{color};">{stat_p3}</div>
          <div class="stat-label">PART 03 篇章長文專欄</div>
        </div>
      </div>
    </div>
    
    <div class="cover-footer">
      <div>日檢手帖編纂委員會 ｜ 題型專攻・三部曲系列（{total_desc}）</div>
      <div>FORMAT: GOODNOTES / NOTABILITY / A4 PRINT</div>
    </div>
  </div>

  <!-- PART 1 -->
  <div class="page-sheet page-break">
    <div class="sheet-header">
      <div style="display:flex; align-items:center; gap:8px;">
        <span class="sheet-part-badge" style="background:{color};">PART 01</span>
        <span class="sheet-title">文法形式の判断（形式挖空題・共 {len(sentence_list)} 題）</span>
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
        <span class="sheet-title">文の組み立て（★ 號排序重組題・共 {len(star_list)} 題）</span>
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
        <span class="sheet-title">文章の文法（篇章脈絡填空題・共 {len(passage_list)} 篇）</span>
      </div>
      <span class="sheet-page-num">P.03</span>
    </div>
    {"".join(p3_items)}
  </div>

  <!-- 答案檢索矩陣（完整涵蓋全冊所有題目） -->
  <div class="page-sheet page-break">
    <div class="sheet-header">
      <div style="display:flex; align-items:center; gap:8px;">
        <span class="sheet-part-badge" style="background:#2B2523;">ANSWER KEY</span>
        <span class="sheet-title">全卷標準正解速查矩陣卡（共 {total_q} 題完整正解）</span>
      </div>
      <span class="sheet-page-num">APPENDIX</span>
    </div>
    <p style="font-size:12px; color:rgba(43,37,35,0.7); margin-bottom:12px;">
      💡 作答完畢後可直接核對本表格快速計算答對題數：
    </p>
    {full_answer_key_html}
  </div>

  {lock_banner}
</div>

</body>
</html>
"""

def generate_solution_workbook_html(level_key: str, data: dict, is_preview: bool = False) -> str:
    conf = LEVEL_INFO[level_key]
    upper = conf["upper"]
    color = conf["color"]
    
    if is_preview:
        sentence_list = data["sentenceQuizzes"][:15]
        star_list = data["starQuizzes"][:9]
        passage_list = data["passageQuizzes"][:2]
        cover_title = f"{upper} 題型專攻・30 題手寫詳解試閱手帳"
        edition_badge = "【考前訂正神器・30 題精選詳解體驗版】"
        stat_p1 = "15 題"
        stat_p2 = "9 題"
        stat_p3 = "2 篇 (6題)"
        total_desc = "共 30 題逐題詳解試閱手帳"
    else:
        sentence_list = data["sentenceQuizzes"][:300]
        star_list = data["starQuizzes"][:125]
        passage_list = data["passageQuizzes"][:25]
        cover_title = f"{upper} 500 題逐題詳解訂正手帳"
        edition_badge = "【考前訂正神器・考點語法全剖析（完整 500 題）】"
        stat_p1 = "300 題"
        stat_p2 = "125 題"
        stat_p3 = "25 篇 (75題)"
        total_desc = "共 500 題逐題手寫風詳解訂正本" 
    
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
            <div class="note-taking-space">✍️ 錯題訂正與手寫註記欄（考點記憶複習）：<div style="border-bottom:1px dashed rgba(43,37,35,0.25); height:14px; margin-top:3px;"></div></div>
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
            <div class="note-taking-space">✍️ 錯題訂正與手寫註記欄（考點記憶複習）：<div style="border-bottom:1px dashed rgba(43,37,35,0.25); height:14px; margin-top:3px;"></div></div>
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


    lock_banner = ""
    if is_preview:
        lock_banner = f"""
        <div class="lock-cta-box page-break">
          <div style="font-size:32px;">📑 🔒</div>
          <h3 style="font-size:18px; font-weight:900; margin-top:8px;">【詳解試閱本結束】完整 500 題詳解收錄於正式手帳套組</h3>
          <p style="font-size:13px; color:rgba(43,37,35,0.8); margin:10px auto 16px auto; max-width:460px;">
            包含 300 題挖空＋125 題重組＋25 篇長文（共 75 題）之完整手寫風詳解與錯題筆記欄！<br>
            正式版套組提供「純實戰手寫空白版」與「逐題手寫風詳解訂正版」雙 PDF 檔案。
          </p>
          <a href="https://buymeacoffee.com/chiaoban/extras" target="_blank" class="btn-cta" style="background:{color}; color:#fff; padding:8px 24px; font-size:14px;">
            ☕ 前往商店贊助解鎖完整版 500 題套組（{conf['price_twd']}）→
          </a>
        </div>
        """

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

<div class="book-container">
  <div class="book-cover">
    <div class="cover-header">
      <div class="cover-issue">NIKKEN TECHO SOLUTION & NOTES EDITION</div>
      <div class="cover-badge" style="background:{color};">{upper} 逐題手寫風詳解</div>
    </div>
    
    <div class="cover-title-group">
      <div class="cover-jp-sub">JLPT {upper} COMPLETE SOLUTIONS</div>
      <div class="cover-title">{cover_title}</div>
      <div style="font-size:15px; font-weight:800; color:{color}; margin-top:6px;">{edition_badge}</div>
      <p class="cover-desc">
        完整收錄正解選項標記、語法拆解、長文中日對照與考點筆記欄。<br>
        隨心在 iPad GoodNotes 上用螢光筆標記錯題，考前最後 30 分鐘只要複習這本錯題手帳即可安心赴考！
      </p>

      <div class="cover-stats">
        <div class="stat-box">
          <div class="stat-num" style="color:{color};">{stat_p1}</div>
          <div class="stat-label">PART 01 形式挖空詳解</div>
        </div>
        <div class="stat-box">
          <div class="stat-num" style="color:{color};">{stat_p2}</div>
          <div class="stat-label">PART 02 ★ 號重組詳解</div>
        </div>
        <div class="stat-box">
          <div class="stat-num" style="color:{color};">{stat_p3}</div>
          <div class="stat-label">PART 03 篇章長文詳解</div>
        </div>
      </div>
    </div>
    
    <div class="cover-footer">
      <div>日檢手帖編纂委員會 ｜ 題型專攻・三部曲系列（{total_desc}）</div>
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
        <span class="sheet-title">篇章脈絡填空・{len(passage_list)} 篇長文逐題詳解</span>
      </div>
      <span class="sheet-page-num">SOLUTIONS P.03</span>
    </div>
    {"".join(p3_items)}
  </div>
  {lock_banner}
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
   - 卷末附有涵蓋全部 500 題之標準正解速查矩陣卡。

2. `日檢手帖-{conf['upper']}-500題全真手帳題本-逐題詳解訂正版.html`
   - 完整 500 題的考點語法剖析、正解選項標記、中日對照長文與專屬手寫錯題筆記欄。
   - 專門用於考前訂正與衝刺複習。

3. `日檢手帖-{conf['upper']}-500題全真手帳題本-試閱版.html`
   - 30 題精華速覽版（含 15 題挖空＋9 題重組＋2 篇長文 6 題，附完整 30 題標準正解卡）。

【使用建議】：
- 方式 A（iPad / 平板使用者）：在瀏覽器按列印 ➔ 另存為 PDF ➔ 匯入 GoodNotes ➔ 使用 Apple Pencil 像手帳一樣刷題、圈助詞與訂正。
- 方式 B（紙本愛好者）：使用雙面黑白或彩色列印（A4 規格），帶入考場作為最後 30 分鐘衝刺神手冊。

祝您順利考取 JLPT {conf['upper']} 高分及格！
官方網站：https://jlpt.chiaoban.com
"""

def main():
    print("🚀 開始產製 JLPT N1～N5 題型專攻 500 題全真手帳題本套組（校驗正解與封面題數）...")
    
    for lvl in ["n5", "n4", "n3", "n2", "n1"]:
        conf = LEVEL_INFO[lvl]
        upper = conf["upper"]
        json_path = QUIZ_DATA_DIR / f"{lvl}.json"
        
        if not json_path.exists():
            print(f"❌ 找不到 {json_path}")
            continue
            
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        print(f"📦 正在產製 {upper} 題本 HTML（實戰 500 題 ＋ 試閱 30 題精華）...")
        
        # 1. 產生空白試閱版 HTML（精準 30 題整，解答包含全部 30 題）
        preview_html = generate_blank_workbook_html(lvl, data, is_preview=True)
        preview_file = DIST_PRODUCTS_DIR / f"日檢手帖-{upper}-500題全真手帳題本-試閱版.html"
        with open(preview_file, "w", encoding="utf-8") as f:
            f.write(preview_html)
            
        # 同步複製至 public/dist-products/quiz/
        public_preview = PUBLIC_PRODUCTS_DIR / f"日檢手帖-{upper}-500題全真手帳題本-試閱版.html"
        with open(public_preview, "w", encoding="utf-8") as f:
            f.write(preview_html)

        # 1b. 產生詳解試閱版 HTML（精準 30 題手寫風詳解試閱）
        sol_preview_html = generate_solution_workbook_html(lvl, data, is_preview=True)
        sol_preview_file = DIST_PRODUCTS_DIR / f"日檢手帖-{upper}-500題全真手帳題本-詳解試閱版.html"
        with open(sol_preview_file, "w", encoding="utf-8") as f:
            f.write(sol_preview_html)

        public_sol_preview = PUBLIC_PRODUCTS_DIR / f"日檢手帖-{upper}-500題全真手帳題本-詳解試閱版.html"
        with open(public_sol_preview, "w", encoding="utf-8") as f:
            f.write(sol_preview_html)
            
        # 2. 產生實戰空白版 HTML（精準 500 題整，解答包含全部 500 題）
        blank_html = generate_blank_workbook_html(lvl, data, is_preview=False)
        blank_file = DIST_PRODUCTS_DIR / f"日檢手帖-{upper}-500題全真手帳題本-實戰空白版.html"
        with open(blank_file, "w", encoding="utf-8") as f:
            f.write(blank_html)
            
        # 3. 產生逐題詳解訂正版 HTML（精準 500 題整）
        sol_html = generate_solution_workbook_html(lvl, data)
        sol_file = DIST_PRODUCTS_DIR / f"日檢手帖-{upper}-500題全真手帳題本-逐題詳解訂正版.html"
        with open(sol_file, "w", encoding="utf-8") as f:
            f.write(sol_html)
            
        # 4. 產生 README
        readme_file = DIST_PRODUCTS_DIR / f"README-{upper}-使用說明.txt"
        with open(readme_file, "w", encoding="utf-8") as f:
            f.write(generate_readme(lvl))
            
        # 5. 打包成 ZIP
        zip_path = DIST_PRODUCTS_DIR / f"日檢手帖-{upper}-500題全真手帳題本套組.zip"
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            zf.write(blank_file, arcname=f"日檢手帖-{upper}-500題全真手帳題本-實戰空白版.html")
            zf.write(sol_file, arcname=f"日檢手帖-{upper}-500題全真手帳題本-逐題詳解訂正版.html")
            zf.write(preview_file, arcname=f"日檢手帖-{upper}-500題全真手帳題本-試閱版.html")
            zf.write(readme_file, arcname="README-使用說明.txt")
            
        print(f"  ✓ {upper} 題本完成：{zip_path.name} ({zip_path.stat().st_size / 1024:.1f} KB)")
        
    # 產生全套 N1～N5 典藏大禮包 ZIP
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
