#!/usr/bin/env python3
"""
日檢手帖 Buy Me a Coffee Shop 封面圖產生器 (scripts/generate_shop_covers.py)

功能：
使用 Google Chrome Headless 將日雜風格 HTML 模板精準渲染為 1200x675 (16:9)
超高解析度的 Buy Me a Coffee Shop / Gumroad 封面商品圖（PNG 格式）。

輸出檔案（位於 dist-products/covers/）：
  1. cover_n5.png  (N5 完全備考套組)
  2. cover_n4.png  (N4 完全備考套組)
  3. cover_n3.png  (N3 完全備考套組)
  4. cover_n2.png  (N2 完全備考套組)
  5. cover_n1.png  (N1 完全備考套組)
  6. cover_all.png (N1～N5 終身全套典藏包)
"""

import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
COVERS_DIR = REPO_ROOT / "dist-products" / "covers"

PRODUCTS_INFO = {
  "n5": {
    "upper": "N5",
    "badge_text": "JLPT N5",
    "color": "#8338ec",
    "color_tint": "#f2e8fd",
    "title": "N5 完全備考套組",
    "sub": "零基礎第一次考日檢的定心丸",
    "price": "$7.99 USD",
    "price_twd": "約 NT$250",
    "stats_card": "712 張",
    "stats_grammar": "48 句型",
    "stats_vocab": "664 單字",
    "sample_front": "行きます",
    "sample_ruby": "<ruby>行<rt>い</rt></ruby>きます",
    "sample_meaning": "去、前往 ｜ 動詞（I類）",
    "sample_ex": "毎朝８時に地下鉄で会社へ行きます。",
  },
  "n4": {
    "upper": "N4",
    "badge_text": "JLPT N4",
    "color": "#0096c7",
    "color_tint": "#e2f4fa",
    "title": "N4 完全備考套組",
    "sub": "核心動詞變化與日常會話全攻略",
    "price": "$8.99 USD",
    "price_twd": "約 NT$280",
    "stats_card": "721 張",
    "stats_grammar": "120 句型",
    "stats_vocab": "601 單字",
    "sample_front": "壊れます",
    "sample_ruby": "<ruby>壊<rt>こわ</rt></ruby>れます",
    "sample_meaning": "壞掉、故障 ｜ 自動詞",
    "sample_ex": "洗濯機が壊れてしまいました。",
  },
  "n3": {
    "upper": "N3",
    "badge_text": "JLPT N3",
    "color": "#7cb518",
    "color_tint": "#f2f8e6",
    "title": "N3 完全備考套組",
    "sub": "跨越日檢分水嶺・自學必備神包",
    "price": "$9.99 USD",
    "price_twd": "約 NT$310",
    "stats_card": "720 張",
    "stats_grammar": "120 句型",
    "stats_vocab": "600 單字",
    "sample_front": "受け付けます",
    "sample_ruby": "<ruby>受<rt>う</rt></ruby>け<ruby>付<rt>つ</rt></ruby>けます",
    "sample_meaning": "受理、接待 ｜ 動詞（II類）",
    "sample_ex": "ホテルのフロントで申し込みを受け付けます。",
  },
  "n2": {
    "upper": "N2",
    "badge_text": "JLPT N2",
    "color": "#ff6b35",
    "color_tint": "#fff0e8",
    "title": "N2 完全備考套組",
    "sub": "日本求職與留學門檻・時事長文完全制霸",
    "price": "$12.99 USD",
    "price_twd": "約 NT$400",
    "stats_card": "720 張",
    "stats_grammar": "120 句型",
    "stats_vocab": "600 單字",
    "sample_front": "身をもって",
    "sample_ruby": "<ruby>身<rt>み</rt></ruby>をもって",
    "sample_meaning": "親身、以身作則地 ｜ 常用慣用語",
    "sample_ex": "健康の大切さを、身をもって知った。",
  },
  "n1": {
    "upper": "N1",
    "badge_text": "JLPT N1",
    "color": "#e63956",
    "color_tint": "#ffeaef",
    "title": "N1 完全備考套組",
    "sub": "最高殿堂・抽象邏輯與古典文語滿分攻克",
    "price": "$12.99 USD",
    "price_twd": "約 NT$400",
    "stats_card": "720 張",
    "stats_grammar": "120 句型",
    "stats_vocab": "600 單字",
    "sample_front": "待機児童",
    "sample_ruby": "<ruby>待<rt>たい</rt></ruby><ruby>機<rt>き</rt></ruby><ruby>児<rt>じ</rt></ruby><ruby>童<rt>どう</rt></ruby>",
    "sample_meaning": "候補入托兒童 ｜ 社會・政治",
    "sample_ex": "待機児童の解消を目指して保育施設を増設した。",
  },
  "all": {
    "upper": "ALL",
    "badge_text": "N1～N5 終身全套",
    "color": "#2b2523",
    "color_tint": "#ffe5a3",
    "title": "N1～N5 終身全套典藏包",
    "sub": "一次買齊 5 個級別・五年份完整自學教材",
    "price": "$29.99 USD",
    "price_twd": "省42%・原價$52",
    "stats_card": "3,593 張",
    "stats_grammar": "528 句型",
    "stats_vocab": "3,065 單字",
    "sample_front": "日檢手帖 N1〜N5",
    "sample_ruby": "全級別<ruby>完全<rt>かんぜん</rt></ruby><ruby>収録<rt>しゅうろく</rt></ruby>",
    "sample_meaning": "逐字振假名 Anki 牌組 ＋ 5 冊 A4 考場速查手冊",
    "sample_ex": "從五十音初學一路陪伴直通 N1 最高殿堂！",
  },
}


def render_html_template(item: dict[str, str]) -> str:
  upper = item["upper"]
  color = item["color"]
  tint = item["color_tint"]
  badge_text = item["badge_text"]
  title = item["title"]
  sub = item["sub"]
  price = item["price"]
  price_twd = item["price_twd"]
  stats_card = item["stats_card"]
  stats_grammar = item["stats_grammar"]
  stats_vocab = item["stats_vocab"]
  sample_front = item["sample_front"]
  sample_ruby = item["sample_ruby"]
  sample_meaning = item["sample_meaning"]
  sample_ex = item["sample_ex"]

  return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<style>
* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  padding: 0;
  width: 1200px;
  height: 675px;
  background-color: #faf7f2;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Hiragino Sans", "Hiragino Kaku Gothic ProN", "Yu Gothic", "Meiryo", "Droid Sans Fallback", sans-serif;
  color: #2b2523;
  display: flex;
  position: relative;
  overflow: hidden;
}}

/* 復古點陣背景紋理 */
.canvas-grid {{
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background-image: radial-gradient(#2b2523 0.75px, transparent 0.75px);
  background-size: 20px 20px;
  opacity: 0.08;
  pointer-events: none;
}}

.outer-border {{
  position: absolute;
  top: 16px; left: 16px; right: 16px; bottom: 16px;
  border: 3.5px solid #2b2523;
  border-radius: 18px;
  pointer-events: none;
  box-shadow: inset 0 0 0 2px #ffffff;
}}

.content-row {{
  width: 100%;
  height: 100%;
  display: flex;
  padding: 44px 50px;
  z-index: 2;
}}

/* 左側：文案與特點 */
.left-col {{
  flex: 1.15;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding-right: 36px;
}}

.brand-line {{
  display: flex;
  align-items: center;
  gap: 12px;
}}
.brand-title {{
  font-family: 'Cinzel', serif;
  font-size: 15px;
  font-weight: 900;
  letter-spacing: 0.25em;
  color: #2b2523;
}}
.brand-tag {{
  background: {color};
  color: #ffffff;
  font-size: 11px;
  font-weight: 900;
  padding: 3px 9px;
  border-radius: 6px;
  border: 1.5px solid #2b2523;
  box-shadow: 2px 2px 0px #2b2523;
}}

.headline-block {{
  margin: 10px 0;
}}
.level-stamp {{
  display: inline-block;
  background: {color};
  color: #ffffff;
  font-family: 'Cinzel', serif;
  font-size: 24px;
  font-weight: 900;
  padding: 4px 16px;
  border-radius: 8px;
  border: 2px solid #2b2523;
  box-shadow: 3px 3px 0px #2b2523;
  margin-bottom: 12px;
}}
.main-title {{
  font-family: 'Noto Serif JP', serif;
  font-size: 42px;
  font-weight: 900;
  line-height: 1.2;
  margin: 0 0 8px 0;
  letter-spacing: 0.02em;
}}
.sub-title {{
  font-size: 17px;
  font-weight: 800;
  color: rgba(43,37,35,0.8);
  margin: 0;
}}

/* 規格膠囊標籤 */
.specs-row {{
  display: flex;
  gap: 10px;
  margin: 14px 0;
}}
.spec-badge {{
  background: #ffffff;
  border: 2px solid #2b2523;
  border-radius: 8px;
  padding: 8px 14px;
  box-shadow: 3px 3px 0px #2b2523;
  display: flex;
  flex-direction: column;
  align-items: center;
}}
.spec-num {{
  font-size: 18px;
  font-weight: 900;
  color: {color};
  line-height: 1.1;
}}
.spec-label {{
  font-size: 10.5px;
  font-weight: 800;
  color: rgba(43,37,35,0.65);
}}

/* 底部價格與平台標籤 */
.bottom-bar {{
  display: flex;
  align-items: center;
  gap: 14px;
  border-top: 2px dashed rgba(43,37,35,0.3);
  padding-top: 14px;
  white-space: nowrap;
}}
.price-pill {{
  background: #ffe5a3;
  border: 2px solid #2b2523;
  border-radius: 8px;
  padding: 6px 12px;
  box-shadow: 3px 3px 0px #2b2523;
  display: flex;
  align-items: baseline;
  gap: 6px;
  white-space: nowrap;
  flex-shrink: 0;
}}
.price-val {{
  font-family: 'Cinzel', Georgia, serif;
  font-size: 22px;
  font-weight: 900;
  color: #2b2523;
  white-space: nowrap;
}}
.price-note {{
  font-size: 11.5px;
  font-weight: 800;
  color: rgba(43,37,35,0.7);
  white-space: nowrap;
}}
.device-tags {{
  font-size: 11.5px;
  font-weight: 800;
  color: rgba(43,37,35,0.7);
  display: flex;
  gap: 8px;
  white-space: nowrap;
  flex-shrink: 0;
}}

/* 右側：實體 Anki 字卡 ＋ A4 手冊 Mockup */
.right-col {{
  flex: 1.05;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}}

/* A4 講義背景傾斜卡 */
.handbook-mockup {{
  position: absolute;
  width: 280px;
  height: 380px;
  background: #ffffff;
  border: 2.5px solid #2b2523;
  border-radius: 12px;
  box-shadow: 6px 6px 0px #2b2523;
  transform: rotate(6deg) translate(80px, -15px);
  padding: 24px 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  text-align: center;
}}
.hb-header {{
  font-family: 'Cinzel', serif;
  font-size: 11px;
  letter-spacing: 0.15em;
  font-weight: 800;
  border-bottom: 1.5px solid #2b2523;
  padding-bottom: 8px;
}}
.hb-stamp {{
  background: {color};
  color: #ffffff;
  font-family: 'Cinzel', serif;
  font-size: 40px;
  font-weight: 900;
  display: inline-block;
  padding: 4px 18px;
  border: 2px solid #2b2523;
  border-radius: 8px;
  margin: 20px 0 10px 0;
}}
.hb-title {{
  font-family: 'Noto Serif JP', serif;
  font-size: 16px;
  font-weight: 900;
  line-height: 1.35;
}}
.hb-footer {{
  font-size: 9.5px;
  font-weight: 700;
  color: rgba(43,37,35,0.5);
  border-top: 1px dashed rgba(43,37,35,0.3);
  padding-top: 8px;
}}

/* 前景 Anki 字卡 Mockup */
.anki-mockup {{
  position: absolute;
  width: 380px;
  background: #ffffff;
  border: 2.5px solid #2b2523;
  border-radius: 14px;
  box-shadow: 6px 6px 0px #2b2523;
  transform: rotate(-3deg) translate(-30px, 15px);
  padding: 22px 22px 18px 22px;
  z-index: 5;
}}
.anki-top {{
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 14px;
}}
.anki-badge {{
  background: {color};
  color: #ffffff;
  font-size: 10px;
  font-weight: 800;
  padding: 2px 7px;
  border-radius: 4px;
  border: 1px solid #2b2523;
}}
.anki-pill {{
  background: {tint};
  font-size: 10px;
  font-weight: 800;
  padding: 2px 7px;
  border-radius: 4px;
  border: 1px solid rgba(43,37,35,0.2);
}}
.anki-ruby-word {{
  font-family: 'Shippori Mincho', 'Noto Serif JP', serif;
  font-size: 32px;
  font-weight: 900;
  text-align: center;
  line-height: 2.2;
}}
.anki-ruby-word ruby {{
  margin-inline: 0.05em;
}}
.anki-ruby-word rt {{
  font-family: sans-serif;
  font-size: 0.52em;
  font-weight: 800;
  border-bottom: 2px solid {tint};
  color: rgba(43,37,35,0.75);
}}
.anki-meaning-box {{
  background: {tint};
  border-left: 4px solid {color};
  padding: 8px 12px;
  font-size: 13.5px;
  font-weight: 800;
  border-radius: 0 6px 6px 0;
  margin: 8px 0;
}}
.anki-ex-box {{
  background: #faf7f2;
  border: 1px solid rgba(43,37,35,0.2);
  border-radius: 6px;
  padding: 8px 10px;
  font-size: 11.5px;
  font-weight: 700;
  color: rgba(43,37,35,0.85);
}}
.anki-badge-footer {{
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
  font-size: 9.5px;
  font-weight: 800;
  color: rgba(43,37,35,0.45);
}}
</style>
</head>
<body>

<div class="canvas-grid"></div>
<div class="outer-border"></div>

<div class="content-row">
  <!-- 左欄 -->
  <div class="left-col">
    <div class="brand-line">
      <span class="brand-title">NIKKEN TECHO</span>
      <span class="brand-tag">FUDGE 日雜風備考教材</span>
    </div>

    <div class="headline-block">
      <div class="level-stamp">{badge_text}</div>
      <h1 class="main-title">{title}</h1>
      <p class="sub-title">{sub}</p>
    </div>

    <div class="specs-row">
      <div class="spec-badge">
        <span class="spec-num">{stats_card}</span>
        <span class="spec-label">Anki 智慧字卡</span>
      </div>
      <div class="spec-badge">
        <span class="spec-num">{stats_grammar}</span>
        <span class="spec-label">核心文法公式</span>
      </div>
      <div class="spec-badge">
        <span class="spec-num">{stats_vocab}</span>
        <span class="spec-label">逐字振假名</span>
      </div>
    </div>

    <div class="bottom-bar">
      <div class="price-pill">
        <span class="price-val">{price}</span>
        <span class="price-note">({price_twd})</span>
      </div>
      <div class="device-tags">
        <span>📱 iPad GoodNotes</span>
        <span>⚡ Anki 間隔記憶</span>
        <span>🖨️ A4 可列印</span>
      </div>
    </div>
  </div>

  <!-- 右欄：實體 Mockup -->
  <div class="right-col">
    <!-- 背景：A4 手冊 -->
    <div class="handbook-mockup">
      <div class="hb-header">NIKKEN TECHO ・ A4 HANDBOOK</div>
      <div>
        <div class="hb-stamp">{upper}</div>
        <div class="hb-title">考場最後 30 分鐘<br>文法公式速查手冊</div>
      </div>
      <div class="hb-footer">FUDGE / CLUEL 日雜復古排版 ｜ 附實戰測驗題</div>
    </div>

    <!-- 前景：Anki 智慧字卡 -->
    <div class="anki-mockup">
      <div class="anki-top">
        <span class="anki-badge">{upper} 卡片</span>
        <span class="anki-pill">逐字振假名版</span>
        <span style="margin-left:auto; font-size:9.5px; font-weight:800; color:rgba(43,37,35,0.4);">Anki 智慧間隔複習</span>
      </div>
      <div class="anki-ruby-word">
        {sample_ruby}
      </div>
      <div class="anki-meaning-box">
        💡 {sample_meaning}
      </div>
      <div class="anki-ex-box">
        📌 {sample_ex}
      </div>
      <div class="anki-badge-footer">
        <span>一鍵匯入手機 / 電腦</span>
        <span>日檢手帖 jlpt.chiaoban.com</span>
      </div>
    </div>
  </div>
</div>

</body>
</html>"""


def main():
    import tempfile
    COVERS_DIR.mkdir(parents=True, exist_ok=True)
    print("🎨 開始使用 Google Chrome Headless 渲染 6 張高解析商品封面圖 (1200x675)...")

    for key, info in PRODUCTS_INFO.items():
        html_content = render_html_template(info)
        tmp_html = Path(f"/tmp/cover_{key}.html")
        tmp_html.write_text(html_content, encoding="utf-8")

        out_png = COVERS_DIR / f"cover_{key}.png"

        with tempfile.TemporaryDirectory() as user_data_dir:
            cmd = [
                "google-chrome",
                "--headless=new",
                "--disable-gpu",
                "--no-sandbox",
                "--hide-scrollbars",
                f"--user-data-dir={user_data_dir}",
                "--window-size=1200,675",
                f"--screenshot={out_png}",
                f"file://{tmp_html}",
            ]
            subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=20,
            )
        print(f"  ✅ 已生成：{out_png.relative_to(REPO_ROOT)} ({out_png.stat().st_size / 1024:.1f} KB)")

    print("🎉 全部 6 張商品封面圖繪製完成！")


if __name__ == "__main__":
  main()
