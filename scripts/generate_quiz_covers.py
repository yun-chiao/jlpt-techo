#!/usr/bin/env python3
"""
生成《日檢手帖》【500 題手帳題本】專屬 1:1 正方形商品封面圖 (1200x1200)
專門用於 Buy Me a Coffee Shop / Extras 上架展示。

視覺設計特點（與教材字卡系列做強烈區隔）：
1. 手帳方眼紙（Graph Paper Grid）底紋，彰顯「做題手帳 / 刷題題本」質感。
2. 雙層立體 Mockup：左後方為「實戰純題空白本」，右前方為「逐題手寫風詳解訂正神手帳」。
3. 包含朱紅色正解圓圈、黃油考點筆記、Apple Pencil 手寫盲點備忘欄。
4. 三宮格題型數據印章（300 題挖空 / 125 題重組 / 75 題長文）。
5. 底部標註新定價與支援載具（iPad GoodNotes / A4 列印）。
"""

import os
import subprocess
import tempfile
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
COVERS_DIR = REPO_ROOT / "dist-products" / "covers" / "quiz"
PUBLIC_COVERS_DIR = REPO_ROOT / "public" / "covers" / "quiz"

QUIZ_COVERS_INFO = {
    "n5": {
        "upper": "N5",
        "badge_text": "JLPT N5 題本",
        "color": "#8338ec",
        "color_tint": "#f2e8fd",
        "title": "N5 500 題厚切全真手帳題本",
        "sub": "實戰空白做題本 ＋ 逐題手寫詳解訂正神手帳（含 350 題獨家進階題）",
        "price": "$6.99 USD",
        "price_twd": "約 NT$220",
        "stats_p1": "300 題",
        "stats_p2": "125 題",
        "stats_p3": "75 題 (25篇)",
        "sample_q": "毎朝８時に家を（　　）、地下鉄に乗って会社へ行きます。",
        "sample_opt1": "出て",
        "sample_opt2": "入って",
        "sample_opt3": "着いて",
        "sample_opt4": "待って",
        "corr_idx": "1",
        "corr_text": "出て",
        "explanation": "〜を出る（離開某場所）。與移動動詞搭配時，離開的出發點助詞用「を」。",
        "note": "【考點盲點】「家を出る」用「を」；「家に入る」用「に」！考前別搞混助詞！",
    },
    "n4": {
        "upper": "N4",
        "badge_text": "JLPT N4 題本",
        "color": "#0096c7",
        "color_tint": "#e2f4fa",
        "title": "N4 500 題厚切全真手帳題本",
        "sub": "實戰空白做題本 ＋ 逐題手寫詳解訂正神手帳（含 350 題獨家進階題）",
        "price": "$8.99 USD",
        "price_twd": "約 NT$280",
        "stats_p1": "300 題",
        "stats_p2": "125 題",
        "stats_p3": "75 題 (25篇)",
        "sample_q": "午後から雨が降りそうだから、傘を持って行った（　　）がいいですよ。",
        "sample_opt1": "ほう",
        "sample_opt2": "とき",
        "sample_opt3": "ため",
        "sample_opt4": "わけ",
        "corr_idx": "1",
        "corr_text": "ほう",
        "explanation": "動詞た形＋ほうがいい（最好…，給予對方的具體建議）。",
        "note": "【考點盲點】肯定建議用「た形＋ほうがいい」；否定建議用「ない形＋ほうがいい」！",
    },
    "n3": {
        "upper": "N3",
        "badge_text": "JLPT N3 題本",
        "color": "#7cb518",
        "color_tint": "#f2f8e6",
        "title": "N3 500 題厚切全真手帳題本",
        "sub": "實戰空白做題本 ＋ 逐題手寫詳解訂正神手帳（含 350 題獨家進階題）",
        "price": "$9.99 USD",
        "price_twd": "約 NT$310",
        "stats_p1": "300 題",
        "stats_p2": "125 題",
        "stats_p3": "75 題 (25篇)",
        "sample_q": "今回の企画は、経験が（　　）、やる気さえあれば誰でも参加できます。",
        "sample_opt1": "なくても",
        "sample_opt2": "なくては",
        "sample_opt3": "ないと",
        "sample_opt4": "なければ",
        "corr_idx": "1",
        "corr_text": "なくても",
        "explanation": "〜ても（即使…也）。「なくて＋も」表示讓步條件，即使沒有經驗也可以參加。",
        "note": "【考點盲點】常與「なくてはいけない（必須）」做混淆測驗；此處「さえ〜ば」搭配讓步！",
    },
    "n2": {
        "upper": "N2",
        "badge_text": "JLPT N2 題本",
        "color": "#ff6b35",
        "color_tint": "#fff0e8",
        "title": "N2 500 題厚切全真手帳題本",
        "sub": "實戰空白做題本 ＋ 逐題手寫詳解訂正神手帳（含 350 題獨家進階題）",
        "price": "$12.99 USD",
        "price_twd": "約 NT$400",
        "stats_p1": "300 題",
        "stats_p2": "125 題",
        "stats_p3": "75 題 (25篇)",
        "sample_q": "現代における情報技術の進歩は業務効率化に（　　）、生活様式をも変えた。",
        "sample_opt1": "とどまらず",
        "sample_opt2": "かぎらず",
        "sample_opt3": "およばず",
        "sample_opt4": "めぐらず",
        "corr_idx": "1",
        "corr_text": "とどまらず",
        "explanation": "〜にとどまらず（不僅局限於…而且擴及更大範圍）。前接名詞或動詞辞書形。",
        "note": "【考點盲點】強調影響範圍擴散！注意區分「〜に限らず（不限於特定對象）」。",
    },
    "n1": {
        "upper": "N1",
        "badge_text": "JLPT N1 題本",
        "color": "#e63956",
        "color_tint": "#ffeaef",
        "title": "N1 500 題厚切全真手帳題本",
        "sub": "實戰空白做題本 ＋ 逐題手寫詳解訂正神手帳（含 350 題獨家進階題）",
        "price": "$14.99 USD",
        "price_twd": "約 NT$460",
        "stats_p1": "300 題",
        "stats_p2": "125 題",
        "stats_p3": "75 題 (25篇)",
        "sample_q": "公職にある者のあの軽率な発言は、国民の信頼を損なう（　　）まじき行為だ。",
        "sample_opt1": "ある",
        "sample_opt2": "いる",
        "sample_opt3": "なる",
        "sample_opt4": "する",
        "corr_idx": "1",
        "corr_text": "ある",
        "explanation": "〜にあるまじき＋名詞（身為…絕不應有的行為）。前接立場名詞，後接負面評價名詞。",
        "note": "【考點盲點】古文禁止助動詞「まじ」之連體形；「あるまじき」為固定慣用句法！",
    },
    "all": {
        "upper": "ALL",
        "badge_text": "N1～N5 終身題本",
        "color": "#2b2523",
        "color_tint": "#ffe5a3",
        "title": "N1～N5 全真 2,500 題手帳題本終身典藏包",
        "sub": "10 冊雙版本手帳 ＋ 1,750 題獨家進階真題（含完整解答卡・現省 54%）",
        "price": "$24.99 USD",
        "price_twd": "現省 54%・原價 $54",
        "stats_p1": "1,500 題",
        "stats_p2": "625 題",
        "stats_p3": "375 題 (125篇)",
        "sample_q": "全級別 N5・N4・N3・N2・N1 完整 2,500 題全真考場厚切題海",
        "sample_opt1": "文法形式挖空",
        "sample_opt2": "★ 號語序重組",
        "sample_opt3": "篇章脈絡填空",
        "sample_opt4": "逐題手寫詳解",
        "corr_idx": "4",
        "corr_text": "2,500 題全量收錄",
        "explanation": "五大級別共 10 冊手帳題本（5 冊實戰空白做題本 ＋ 5 冊逐題手寫風詳解訂正本）。",
        "note": "【全套終身特惠】含全 2,500 題 Answer Key 答案卡！直通日檢最高殿堂！",
    },
}


def render_quiz_cover_html(item: dict[str, str]) -> str:
    upper = item["upper"]
    color = item["color"]
    tint = item["color_tint"]
    badge_text = item["badge_text"]
    title = item["title"]
    sub = item["sub"]
    price = item["price"]
    price_twd = item["price_twd"]
    stats_p1 = item["stats_p1"]
    stats_p2 = item["stats_p2"]
    stats_p3 = item["stats_p3"]
    sample_q = item["sample_q"]
    sample_opt1 = item["sample_opt1"]
    sample_opt2 = item["sample_opt2"]
    sample_opt3 = item["sample_opt3"]
    sample_opt4 = item["sample_opt4"]
    corr_idx = item["corr_idx"]
    corr_text = item["corr_text"]
    explanation = item["explanation"]
    note = item["note"]

    return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  width: 1200px;
  height: 1200px;
  background-color: #faf7f2;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Hiragino Sans", "Hiragino Kaku Gothic ProN", "Yu Gothic", "Meiryo", "Droid Sans Fallback", sans-serif;
  color: #2b2523;
  position: relative;
  overflow: hidden;
}}

/* 手帳方眼紙（Graph Paper Grid）底紋 */
.canvas-grid {{
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background-size: 24px 24px;
  background-image:
    linear-gradient(to right, rgba(43,37,35,0.065) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(43,37,35,0.065) 1px, transparent 1px);
  pointer-events: none;
}}

.outer-border {{
  position: absolute;
  top: 24px; left: 24px; right: 24px; bottom: 24px;
  border: 4.5px solid #2b2523;
  border-radius: 24px;
  pointer-events: none;
}}

.container {{
  position: relative;
  width: 100%;
  height: 100%;
  padding: 44px 50px 40px 50px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}}

/* 頂部 Header */
.brand-line {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2.5px solid #2b2523;
  padding-bottom: 12px;
}}

.brand-left {{
  display: flex;
  align-items: center;
  gap: 12px;
}}

.brand-title {{
  font-family: 'Cinzel', Georgia, serif;
  font-size: 19px;
  font-weight: 900;
  letter-spacing: 0.18em;
}}

.brand-tag {{
  background: #ffe5a3;
  border: 1.5px solid #2b2523;
  padding: 3px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 900;
  box-shadow: 2px 2px 0px #2b2523;
}}

.brand-right {{
  font-family: 'Cinzel', Georgia, serif;
  font-size: 13px;
  font-weight: 800;
  letter-spacing: 0.1em;
  opacity: 0.7;
}}

.headline-block {{
  margin-top: 18px;
}}

.level-stamp {{
  display: inline-block;
  background: {color};
  color: #ffffff;
  font-weight: 900;
  font-size: 17px;
  padding: 5px 16px;
  border-radius: 8px;
  border: 2px solid #2b2523;
  box-shadow: 3.5px 3.5px 0px #2b2523;
  letter-spacing: 0.05em;
}}

.main-title {{
  font-family: 'Noto Serif JP', "Songti TC", serif;
  font-size: 38px;
  font-weight: 900;
  margin-top: 10px;
  letter-spacing: -0.02em;
  color: #2b2523;
}}

.sub-title {{
  font-size: 15.5px;
  font-weight: 700;
  color: rgba(43,37,35,0.8);
  margin-top: 6px;
}}

/* 中間 Mockup 展示區：左右雙本手帳疊加 */
.mockup-showcase {{
  position: relative;
  height: 560px;
  margin: 10px 0 16px 0;
}}

/* 底層：考場實戰純題空白本（左後方傾斜） */
.blank-mockup {{
  position: absolute;
  top: 10px;
  left: 20px;
  width: 580px;
  height: 520px;
  background: #ffffff;
  border: 3.5px solid #2b2523;
  border-radius: 14px;
  box-shadow: 10px 14px 0px rgba(43,37,35,0.4);
  transform: rotate(-3.5deg);
  padding: 26px 28px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}}

.blank-top {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid #2b2523;
  padding-bottom: 8px;
}}

.blank-badge {{
  background: #2b2523;
  color: #ffffff;
  font-size: 12px;
  font-weight: 900;
  padding: 3px 8px;
  border-radius: 4px;
}}

.blank-title {{
  font-family: 'Noto Serif JP', serif;
  font-size: 15px;
  font-weight: 900;
}}

.blank-q-box {{
  border: 1.5px solid rgba(43,37,35,0.3);
  border-radius: 8px;
  padding: 14px;
  background: #faf7f2;
  margin-top: 14px;
}}

.blank-q-meta {{
  font-size: 11.5px;
  font-weight: 800;
  color: rgba(43,37,35,0.6);
  margin-bottom: 6px;
}}

.blank-q-sentence {{
  font-family: 'Noto Serif JP', serif;
  font-size: 16px;
  font-weight: 700;
  line-height: 1.6;
  margin-bottom: 12px;
}}

.blank-opt-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}}

.blank-opt {{
  background: #ffffff;
  border: 1.5px solid #2b2523;
  border-radius: 6px;
  padding: 6px 10px;
  font-size: 13.5px;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 8px;
}}

.blank-opt-num {{
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 1px solid #2b2523;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 900;
}}

.blank-footer {{
  border-top: 1.5px dashed rgba(43,37,35,0.25);
  padding-top: 10px;
  font-size: 12px;
  color: rgba(43,37,35,0.6);
  display: flex;
  justify-content: space-between;
  font-weight: 700;
}}

/* 表層：逐題手寫風詳解訂正神手帳（右前方浮起） */
.solution-mockup {{
  position: absolute;
  top: 30px;
  right: 15px;
  width: 620px;
  height: 520px;
  background: #ffffff;
  border: 3.5px solid #2b2523;
  border-radius: 16px;
  box-shadow: 14px 18px 0px #2b2523;
  transform: rotate(2.5deg);
  padding: 26px 30px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}}

.sol-top {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid #2b2523;
  padding-bottom: 8px;
}}

.sol-ribbon {{
  background: #ffe5a3;
  border: 1.5px solid #2b2523;
  color: #2b2523;
  font-size: 12.5px;
  font-weight: 900;
  padding: 3px 10px;
  border-radius: 6px;
  box-shadow: 2px 2px 0px #2b2523;
}}

.sol-pass-stamp {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #fff0e8;
  border: 2px solid #e63956;
  color: #e63956;
  font-weight: 900;
  font-size: 13.5px;
  padding: 2px 10px;
  border-radius: 6px;
  transform: rotate(-2deg);
}}

.sol-ans-banner {{
  background: #ffe5a3;
  border: 2px solid #2b2523;
  border-radius: 8px;
  padding: 10px 14px;
  margin-top: 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 2px 2px 0px #2b2523;
}}

.sol-ans-title {{
  font-weight: 900;
  font-size: 15px;
  color: #2b2523;
}}

.sol-ans-opt {{
  font-family: 'Noto Serif JP', serif;
  font-size: 16px;
  font-weight: 900;
  color: #2b2523;
}}

.sol-expl-box {{
  margin-top: 12px;
  background: #faf7f2;
  border-left: 4px solid {color};
  padding: 10px 14px;
  border-radius: 0 8px 8px 0;
  font-size: 13.5px;
  line-height: 1.55;
}}

.sol-notes-area {{
  margin-top: 12px;
  background: #ffffff;
  border: 2px dashed rgba(43,37,35,0.35);
  border-radius: 8px;
  padding: 12px 14px;
}}

.sol-notes-label {{
  font-size: 12px;
  font-weight: 900;
  color: #ff6b35;
  margin-bottom: 4px;
  display: flex;
  align-items: center;
  gap: 6px;
}}

.sol-notes-content {{
  font-size: 13px;
  font-weight: 700;
  color: rgba(43,37,35,0.85);
  line-height: 1.5;
  border-bottom: 1.5px dashed rgba(43,37,35,0.25);
  padding-bottom: 6px;
}}

.sol-footer-features {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 8px;
  font-size: 12px;
  font-weight: 800;
  color: rgba(43,37,35,0.65);
}}

.stats-row {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 18px;
}}

.stat-card {{
  background: #ffffff;
  border: 2.5px solid #2b2523;
  border-radius: 12px;
  padding: 10px 14px;
  box-shadow: 4px 4px 0px #2b2523;
  text-align: center;
}}

.stat-num {{
  font-family: 'Cinzel', 'DM Mono', monospace;
  font-size: 24px;
  font-weight: 900;
  color: {color};
}}

.stat-lbl {{
  font-size: 12px;
  font-weight: 800;
  color: rgba(43,37,35,0.7);
  margin-top: 2px;
}}

.bottom-bar {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 2.5px dashed rgba(43,37,35,0.3);
  padding-top: 18px;
}}

.price-pill {{
  background: #ffe5a3;
  border: 2.5px solid #2b2523;
  border-radius: 10px;
  padding: 8px 20px;
  box-shadow: 4px 4px 0px #2b2523;
  display: flex;
  align-items: baseline;
  gap: 8px;
}}

.price-val {{
  font-family: 'Cinzel', Georgia, serif;
  font-size: 28px;
  font-weight: 900;
  color: #2b2523;
}}

.price-note {{
  font-size: 14px;
  font-weight: 800;
  color: rgba(43,37,35,0.75);
}}

.device-tags {{
  font-size: 14.5px;
  font-weight: 900;
  color: rgba(43,37,35,0.75);
  display: flex;
  gap: 14px;
}}
</style>
</head>
<body>

<div class="canvas-grid"></div>
<div class="outer-border"></div>

<div class="container">
  <div class="top-header">
    <div class="brand-line">
      <div class="brand-left">
        <span class="brand-title">NIKKEN TECHO</span>
        <span class="brand-tag">500 題全真手帳題本</span>
      </div>
      <span class="brand-right">2026 PRACTICE WORKBOOK EDITION</span>
    </div>

    <div class="headline-block">
      <div>
        <span class="level-stamp">{badge_text}</span>
      </div>
      <h1 class="main-title">{title}</h1>
      <p class="sub-title">{sub}</p>
    </div>
  </div>

  <div class="mockup-showcase">
    <!-- 底層：實戰做題空白本 -->
    <div class="blank-mockup">
      <div class="blank-top">
        <span class="blank-badge">PRACTICE BOOK</span>
        <span class="blank-title">考場實戰純題空白本（A4 / GoodNotes）</span>
      </div>

      <div class="blank-q-box">
        <div class="blank-q-meta">PART 01 文法挖空 ・ 模擬考場規格</div>
        <div class="blank-q-sentence">{sample_q}</div>
        <div class="blank-opt-grid">
          <div class="blank-opt"><span class="blank-opt-num">1</span>{sample_opt1}</div>
          <div class="blank-opt"><span class="blank-opt-num">2</span>{sample_opt2}</div>
          <div class="blank-opt"><span class="blank-opt-num">3</span>{sample_opt3}</div>
          <div class="blank-opt"><span class="blank-opt-num">4</span>{sample_opt4}</div>
        </div>
      </div>

      <div class="blank-footer">
        <span>📖 無干擾純題目留白排版</span>
        <span>✎ 支援 Apple Pencil 圈詞作答</span>
      </div>
    </div>

    <!-- 表層：逐題手寫風詳解訂正神手帳 -->
    <div class="solution-mockup">
      <div class="sol-top">
        <span class="sol-ribbon">✍️ 逐題詳解訂正神手帳</span>
        <span class="sol-pass-stamp">💮 正解 ({corr_idx}) {corr_text}</span>
      </div>

      <div class="sol-ans-banner">
        <span class="sol-ans-title">💡 官方考點核心解構</span>
        <span class="sol-ans-opt">正解選項：【 {corr_text} 】</span>
      </div>

      <div class="sol-expl-box">
        <strong>語法解析：</strong>{explanation}
      </div>

      <div class="sol-notes-area">
        <div class="sol-notes-label">
          <span>✍️ 我的錯題訂正與考點盲點筆記欄（考前 30 分鐘必讀）</span>
        </div>
        <div class="sol-notes-content">
          {note}
        </div>
      </div>

      <div class="sol-footer-features">
        <span>📑 全 500 題完整解析＋錯題欄</span>
        <span>📊 附卷末 Answer Key 答案卡</span>
      </div>
    </div>
  </div>

  <div class="stats-row">
    <div class="stat-card">
      <div class="stat-num">{stats_p1}</div>
      <div class="stat-lbl">Part 1 文法形式挖空</div>
    </div>
    <div class="stat-card">
      <div class="stat-num">{stats_p2}</div>
      <div class="stat-lbl">Part 2 ★ 號語序重組</div>
    </div>
    <div class="stat-card">
      <div class="stat-num">{stats_p3}</div>
      <div class="stat-lbl">Part 3 篇章長文專欄</div>
    </div>
  </div>

  <div class="bottom-bar">
    <div class="price-pill">
      <span class="price-val">{price}</span>
      <span class="price-note">({price_twd})</span>
    </div>
    <div class="device-tags">
      <span>📝 實戰空白做題本</span>
      <span>✍️ 逐題手寫詳解手帳</span>
      <span>📱 iPad GoodNotes</span>
      <span>🖨️ A4 高清列印</span>
    </div>
  </div>
</div>

</body>
</html>"""


def main():
    COVERS_DIR.mkdir(parents=True, exist_ok=True)
    PUBLIC_COVERS_DIR.mkdir(parents=True, exist_ok=True)
    print("🎨 開始使用 Google Chrome Headless 渲染 6 張【500 題手帳題本】正方形商品封面圖 (1200x1200)...")

    for key, info in QUIZ_COVERS_INFO.items():
        html_content = render_quiz_cover_html(info)
        tmp_html = Path(f"/tmp/cover_quiz_{key}.html")
        tmp_html.write_text(html_content, encoding="utf-8")

        out_png = COVERS_DIR / f"cover_quiz_{key}.png"
        public_png = PUBLIC_COVERS_DIR / f"cover_quiz_{key}.png"

        with tempfile.TemporaryDirectory() as user_data_dir:
            cmd = [
                "google-chrome",
                "--headless=new",
                "--disable-gpu",
                "--no-sandbox",
                "--hide-scrollbars",
                f"--user-data-dir={user_data_dir}",
                "--window-size=1200,1200",
                f"--screenshot={out_png}",
                f"file://{tmp_html}",
            ]
            subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=25,
            )

        shutil.copy2(out_png, public_png)
        print(f"  ✅ 已生成：{out_png.relative_to(REPO_ROOT)} ({out_png.stat().st_size / 1024:.1f} KB)")

    print("\n🎉 全部 6 張題本專屬正方形封面圖繪製完成！")


if __name__ == "__main__":
    main()
