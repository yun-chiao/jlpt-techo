#!/usr/bin/env python3
"""
日檢手帖 Buy Me a Coffee Shop 正方形商品封面圖產生器 (scripts/generate_shop_covers.py)

功能：
使用 Google Chrome Headless 將日雜風格 HTML 模板精準渲染為 1200x1200 (1:1 正方形)
超高解析度的 Buy Me a Coffee Shop 封面商品圖（PNG 格式）。

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
import tempfile
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
        "sub": "零基礎第一次考日檢的定心丸・初學必備神包",
        "price": "$7.99 USD",
        "price_twd": "約 NT$250",
        "stats_card": "712 張",
        "stats_grammar": "48 句型",
        "stats_vocab": "664 單字",
        "sample_front": "行きます",
        "sample_ruby": "<ruby>行<rt>い</rt></ruby>きます",
        "sample_meaning": "去、前往 ｜ 動詞（I類）",
        "sample_ex": "毎朝８時に地下鐵で会社へ行きます。",
    },
    "n4": {
        "upper": "N4",
        "badge_text": "JLPT N4",
        "color": "#0096c7",
        "color_tint": "#e2f4fa",
        "title": "N4 完全備考套組",
        "sub": "核心動詞變化與日常會話全攻略・告別初階門檻",
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
        "sub": "跨越日檢分水嶺・日常複雜情境與自學必備神包",
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
        "sub": "日本求職與留學黃金門檻・時事長文完全制霸",
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
        "price_twd": "省 42%・原價 $52",
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
  height: 1200px;
  background-color: #faf7f2;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Hiragino Sans", "Hiragino Kaku Gothic ProN", "Yu Gothic", "Meiryo", "Droid Sans Fallback", sans-serif;
  color: #2b2523;
  position: relative;
  overflow: hidden;
}}

/* 復古點陣背景紋理 */
.canvas-grid {{
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background-image: radial-gradient(#2b2523 0.85px, transparent 0.85px);
  background-size: 24px 24px;
  opacity: 0.08;
  pointer-events: none;
}}

.outer-border {{
  position: absolute;
  top: 24px; left: 24px; right: 24px; bottom: 24px;
  border: 4px solid #2b2523;
  border-radius: 22px;
  pointer-events: none;
  box-shadow: inset 0 0 0 3px #ffffff;
}}

.container {{
  width: 100%;
  height: 100%;
  padding: 56px 64px 48px 64px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
  z-index: 2;
}}

/* 頂部標題與品牌列 */
.top-header {{
  display: flex;
  flex-direction: column;
}}

.brand-line {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}}

.brand-left {{
  display: flex;
  align-items: center;
  gap: 12px;
}}

.brand-title {{
  font-family: 'Cinzel', Georgia, serif;
  font-size: 18px;
  font-weight: 900;
  letter-spacing: 0.28em;
  color: #2b2523;
}}

.brand-tag {{
  background: {color};
  color: #ffffff;
  font-size: 12px;
  font-weight: 900;
  padding: 4px 12px;
  border-radius: 6px;
  border: 1.5px solid #2b2523;
  box-shadow: 2.5px 2.5px 0px #2b2523;
}}

.brand-right {{
  font-family: 'Cinzel', Georgia, serif;
  font-size: 13px;
  font-weight: 800;
  letter-spacing: 0.18em;
  color: rgba(43,37,35,0.55);
}}

.headline-block {{
  margin-top: 4px;
}}

.level-stamp {{
  display: inline-block;
  background: {color};
  color: #ffffff;
  font-family: 'Cinzel', Georgia, serif;
  font-size: 26px;
  font-weight: 900;
  padding: 5px 20px;
  border-radius: 8px;
  border: 2.5px solid #2b2523;
  box-shadow: 4px 4px 0px #2b2523;
  margin-bottom: 12px;
}}

.main-title {{
  font-family: 'Noto Serif JP', 'Yu Mincho', 'Hiragino Mincho ProN', 'Droid Sans Fallback', serif;
  font-size: 52px;
  font-weight: 900;
  line-height: 1.2;
  margin: 0 0 8px 0;
  letter-spacing: 0.02em;
}}

.sub-title {{
  font-size: 20px;
  font-weight: 800;
  color: rgba(43,37,35,0.75);
  margin: 0;
}}

/* 中間 Mockup 展示區 */
.mockup-showcase {{
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  margin: 20px 0;
}}

/* 背景：A4 講義手冊 */
.handbook-mockup {{
  position: absolute;
  width: 440px;
  height: 440px;
  background: #ffffff;
  border: 3px solid #2b2523;
  border-radius: 16px;
  box-shadow: 8px 8px 0px #2b2523;
  transform: rotate(6deg) translate(150px, -60px);
  padding: 24px 26px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  z-index: 1;
}}

.hb-header {{
  font-family: 'Cinzel', Georgia, serif;
  font-size: 13px;
  letter-spacing: 0.18em;
  font-weight: 800;
  border-bottom: 2px solid #2b2523;
  padding-bottom: 10px;
  text-align: right;
}}

.hb-stamp {{
  background: {color};
  color: #ffffff;
  font-family: 'Cinzel', Georgia, serif;
  font-size: 40px;
  font-weight: 900;
  display: inline-block;
  padding: 4px 18px;
  border: 2.5px solid #2b2523;
  border-radius: 8px;
  margin: 12px 0 8px 0;
}}

.hb-title {{
  font-family: 'Noto Serif JP', 'Yu Mincho', 'Hiragino Mincho ProN', 'Droid Sans Fallback', serif;
  font-size: 20px;
  font-weight: 900;
  line-height: 1.35;
  text-align: right;
}}

.hb-list {{
  margin: 8px 0;
  font-size: 13px;
  font-weight: 800;
  color: rgba(43,37,35,0.75);
  line-height: 1.8;
  text-align: right;
}}

.hb-footer {{
  font-size: 11px;
  font-weight: 800;
  color: rgba(43,37,35,0.5);
  border-top: 1.5px dashed rgba(43,37,35,0.3);
  padding-top: 10px;
  text-align: right;
}}

/* 前景：Anki 智慧字卡 */
.anki-mockup {{
  position: absolute;
  width: 520px;
  background: #ffffff;
  border: 3.5px solid #2b2523;
  border-radius: 18px;
  box-shadow: 10px 10px 0px #2b2523;
  transform: rotate(-3deg) translate(-110px, 40px);
  padding: 24px 24px 20px 24px;
  z-index: 5;
}}

.anki-top {{
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 14px;
}}

.anki-badge {{
  background: {color};
  color: #ffffff;
  font-size: 12px;
  font-weight: 900;
  padding: 3px 10px;
  border-radius: 5px;
  border: 1.5px solid #2b2523;
}}

.anki-pill {{
  background: {tint};
  font-size: 12px;
  font-weight: 900;
  padding: 3px 10px;
  border-radius: 5px;
  border: 1.5px solid rgba(43,37,35,0.25);
}}

.anki-ruby-word {{
  font-family: 'Noto Serif JP', 'Yu Mincho', 'Hiragino Mincho ProN', 'Droid Sans Fallback', serif;
  font-size: 44px;
  font-weight: 900;
  text-align: center;
  line-height: 2.2;
  margin: 6px 0;
}}

.anki-ruby-word ruby {{
  margin-inline: 0.05em;
}}

.anki-ruby-word rt {{
  font-family: sans-serif;
  font-size: 0.5em;
  font-weight: 800;
  border-bottom: 2.5px solid {tint};
  color: rgba(43,37,35,0.75);
}}

.anki-meaning-box {{
  background: {tint};
  border-left: 5px solid {color};
  padding: 10px 16px;
  font-size: 16.5px;
  font-weight: 800;
  border-radius: 0 8px 8px 0;
  margin: 10px 0;
}}

.anki-ex-box {{
  background: #faf7f2;
  border: 1.5px solid rgba(43,37,35,0.2);
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 14px;
  line-height: 1.5;
}}

.anki-badge-footer {{
  display: flex;
  justify-content: space-between;
  margin-top: 14px;
  font-size: 12px;
  font-weight: 800;
  color: rgba(43,37,35,0.45);
}}

/* 規格三宮格 */
.specs-row {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
  margin: 14px 0;
}}

.spec-badge {{
  background: #ffffff;
  border: 2.5px solid #2b2523;
  border-radius: 12px;
  padding: 14px 16px;
  box-shadow: 4px 4px 0px #2b2523;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}}

.spec-num {{
  font-size: 30px;
  font-weight: 900;
  color: {color};
  line-height: 1.15;
  font-family: 'Cinzel', Georgia, serif;
}}

.spec-label {{
  font-size: 13.5px;
  font-weight: 800;
  color: rgba(43,37,35,0.7);
  margin-top: 4px;
}}

/* 底部價格與平台標籤 */
.bottom-bar {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-top: 2.5px dashed rgba(43,37,35,0.3);
  padding-top: 18px;
}}

.price-pill {{
  background: #ffe5a3;
  border: 2.5px solid #2b2523;
  border-radius: 10px;
  padding: 8px 18px;
  box-shadow: 4px 4px 0px #2b2523;
  display: flex;
  align-items: baseline;
  gap: 8px;
  white-space: nowrap;
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
  white-space: nowrap;
}}
</style>
</head>
<body>

<div class="canvas-grid"></div>
<div class="outer-border"></div>

<div class="container">
  <!-- 頂部欄 -->
  <div class="top-header">
    <div class="brand-line">
      <div class="brand-left">
        <span class="brand-title">NIKKEN TECHO</span>
        <span class="brand-tag">FUDGE 日雜風備考教材</span>
      </div>
      <span class="brand-right">2026 OFFICIAL EDITION</span>
    </div>

    <div class="headline-block">
      <div>
        <span class="level-stamp">{badge_text}</span>
      </div>
      <h1 class="main-title">{title}</h1>
      <p class="sub-title">{sub}</p>
    </div>
  </div>

  <!-- 中間 Mockup 展示 -->
  <div class="mockup-showcase">
    <!-- 背景：A4 手冊 -->
    <div class="handbook-mockup">
      <div class="hb-header">NIKKEN TECHO ・ A4 HANDBOOK</div>
      <div style="display: flex; flex-direction: column; align-items: flex-end; text-align: right;">
        <div class="hb-stamp">{upper}</div>
        <div class="hb-title">考場最後 30 分鐘<br>文法公式速查手冊</div>
        <div class="hb-list">
          • 120 句型表格化速查<br>
          • 實戰測驗附即答詳解<br>
          • 易混淆考場陷阱解構
        </div>
      </div>
      <div class="hb-footer">FUDGE / CLUEL 日雜復古排版 ｜ 支援 GoodNotes / A4 列印</div>
    </div>

    <!-- 前景：Anki 智慧字卡 -->
    <div class="anki-mockup">
      <div class="anki-top">
        <span class="anki-badge">{upper} 字卡</span>
        <span class="anki-pill">逐字振假名版</span>
        <span style="margin-left:auto; font-size:11px; font-weight:800; color:rgba(43,37,35,0.45);">Anki 智慧間隔記憶</span>
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
        <span>一鍵匯入手機 / 平板 / 電腦</span>
        <span>日檢手帖 jlpt.chiaoban.com</span>
      </div>
    </div>
  </div>

  <!-- 底部規格三宮格 -->
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

  <!-- 最底層價格與標籤 -->
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

</body>
</html>"""


def main():
    COVERS_DIR.mkdir(parents=True, exist_ok=True)
    print("🎨 開始使用 Google Chrome Headless 渲染 6 張高解析正方形商品封面圖 (1200x1200)...")

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
                "--window-size=1200,1200",
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

    print("\n🎉 全部 6 張正方形商品封面圖繪製完成！")


if __name__ == "__main__":
    main()
