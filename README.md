# 日檢手帖 NIKKEN TECHO

> 像翻雜誌一樣，把日檢讀完。

JLPT（日本語能力試驗）N1～N5 自學網站。視覺風格為「日雜感」（FUDGE / CLUEL 靈感的復古摩登撞色）。
純靜態網站，資料驅動：新增 JSON ＋ 在註冊表填一行，即可開通新的級別或分類。

## 啟動與建置

```bash
npm install          # 安裝依賴
npm run dev          # 開發伺服器（http://localhost:5173）
npm run build        # 型別檢查 + 產出 dist/（可部署到 GitHub Pages / Netlify / Vercel）
npm run preview      # 預覽 build 結果
npm run lint         # ESLint
npm run typecheck    # tsc --noEmit
npm run validate:data  # 驗證 src/data/**/*.json 格式
```

技術棧：Vite・React 18・TypeScript（strict）・React Router v6・Tailwind CSS v3・zod（資料驗證）。

## 專案結構

```
src/
  data/
    registry.ts        ← 內容註冊表（唯一需要手動維護的地方）
    types.ts           ← 教材資料的 TypeScript 型別
    meta.ts            ← 級別/分類清單、站名等常數
    validate.ts        ← zod runtime 驗證（dev 模式載入時自動檢查）
    grammar/n5.json    ← N5 課程教材（16 課，文法＋隨堂練習）
    vocabulary/n5.json ← N5 單字總表（獨立於課程，含主題分類）
    quiz/              ← 預留
    blog/
      index.ts         ← 部落格資料層（自動掃描 posts/）
      posts/*.md       ← 部落格文章（一篇一個 Markdown 檔）
  hooks/
    useLessonSet.ts    ← 頁面唯一的取資料入口
    useDocumentTitle.ts
  components/          ← NavBar / Footer / Layout / RetroCard / LevelBadge /
                          LevelDot / TapeLabel / Breadcrumb / ComingSoon /
                          LessonCard / GrammarPointCard / StatusStates
  pages/               ← HomePage / GrammarLevelPage / GrammarLessonPage /
                          VocabularyLevelPage / QuizLevelPage / NotFoundPage
scripts/
  validate-data.mjs    ← npm run validate:data 用的 Node 腳本
```

路由：`/`、`/grammar/:level`、`/grammar/:level/:lessonNumber`（＝文法點 1）、`/grammar/:level/:lessonNumber/:pointNumber`、`/vocabulary/:level`、`/quiz/:level`、`/blog`、`/blog/:slug`、`*`（404）。

文法單課頁為**分步導覽**：一頁一個文法點，下方接該文法點的隨堂練習，
「下一個文法點 →」走到課末會變成「前往第 X 課 →」；側欄目錄可直接跳轉。
`:level` 合法值為 `n1`～`n5` 小寫；不合法顯示 404。未開通的分類×級別顯示「敬請期待」。

## 如何新增內容

一切由 [src/data/registry.ts](src/data/registry.ts) 決定，**不需要改任何元件程式碼**。

### 例一：開通 N4 文法

1. 把 `n4.json`（格式見下方）放到 `src/data/grammar/`。
2. 在 `registry.ts` 的 `grammar.n4` 填入 loader：

```ts
grammar: {
  // ...
  n4: () => import('./grammar/n4.json').then((m) => m.default as unknown as LessonSet),
},
```

3. 執行 `npm run validate:data` 確認格式正確。完成——導覽列、首頁卡片、文法頁全部自動開通。

### 例二：開通其他級別的單字

單字區使用「單字總表」格式（非課程制）：頂層為 VocabEntry 陣列，
每筆為 `VocabularyItem` 加上 `category`（主題分類，自由文字，頁面依它分組）：

```ts
export interface VocabEntry extends VocabularyItem {
  category: string; // 例：「動詞」「食物・飲料」「時間・日期」
}
```

把 `n4.json`（VocabEntry 陣列）放到 `src/data/vocabulary/`，在 `registry.ts` 的
`vocabulary.n4` 填入 loader，執行 `npm run validate:data` 即可。

### 例三：開通練習題

`quiz` 區使用課程教材格式，指向含 `quizzes` 欄位的課程 JSON 即可：

```ts
quiz: {
  // ...
  n5: () => import('./grammar/n5.json').then((m) => m.default as unknown as LessonSet),
},
```

### 例四：新增一篇部落格文章

在 `src/data/blog/posts/` 丟一個 `.md` 檔即可，**檔名（去掉 .md）就是網址 slug**，
例如 `ha-vs-ga.md` → `/blog/ha-vs-ga`。文章會自動出現在列表（依 date 新→舊排序），不需改任何程式碼。

檔案開頭需要 frontmatter：

```markdown
---
title: 「は」與「が」到底差在哪？
date: 2026-09-20
category: 文法小知識
excerpt: 一句話講清楚初學者最常卡關的兩個助詞。
---

## 正文從這裡開始

支援 **粗體**、`行內程式碼`、[連結](https://example.com)、
「- 」開頭的清單、「1. 」有序清單、「> 」引用區塊（奶油黃便籤樣式）、「---」分隔線。
```

`category` 為自由文字（例：公告、文法小知識、學習筆記、文章分享），會顯示成標籤。

## 資料 JSON 格式

頂層為 Lesson 陣列。型別定義（同 [src/data/types.ts](src/data/types.ts)）：

```ts
export interface VocabularyItem {
  kanji: string;
  kana: string;
  romaji: string;
  part_of_speech: string;
  meaning: string;
  example_ja: string;
  example_zh: string;
}

export interface GrammarExample {
  ja: string;
  zh: string;
}

export interface GrammarPoint {
  point_title: string;
  formula: string;      // [名詞A] 之類的中括號片語會自動以級別色高亮
  explanation: string;
  alert: string;
  examples: GrammarExample[];
  quizzes?: Quiz[];     // 選填：這個文法點的隨堂練習（建議 3 題）；沒有時單課頁不顯示練習區塊
}

export interface Quiz {
  question_id: number;
  type: 'multiple_choice';
  question_text: string;
  options: string[];
  correct_answer: string;
  explanation: string;
}

export interface Lesson {
  lesson_number: number;
  lesson_title: string;
  vocabulary: VocabularyItem[];
  grammar_points: GrammarPoint[];
  quizzes: Quiz[];
}

export type LessonSet = Lesson[];
```

一課的最小範例：

```json
[
  {
    "lesson_number": 1,
    "lesson_title": "發音基礎與基本打招呼",
    "vocabulary": [
      {
        "kanji": "私",
        "kana": "わたし",
        "romaji": "watashi",
        "part_of_speech": "代名詞",
        "meaning": "我",
        "example_ja": "私は学生です。",
        "example_zh": "我是學生。"
      }
    ],
    "grammar_points": [
      {
        "point_title": "「AはBです」肯定判斷句",
        "formula": "[名詞A] は [名詞B] です",
        "explanation": "表示「A 是 B」的基本判斷句。",
        "alert": "「は」作助詞時唸 wa，不唸 ha。",
        "examples": [{ "ja": "私は学生です。", "zh": "我是學生。" }]
      }
    ],
    "quizzes": [
      {
        "question_id": 1,
        "type": "multiple_choice",
        "question_text": "わたし（　）学生です。",
        "options": ["が", "は", "の", "を"],
        "correct_answer": "は",
        "explanation": "主題用助詞「は」。"
      }
    ]
  }
]
```

三個分類可共用同一份 JSON（文法頁只讀 `grammar_points`、單字頁只讀 `vocabulary`、練習題頁只讀 `quizzes`），也可各自指向不同檔案；註冊表決定一切。

## 設計 tokens

- 基底色：米白洋紙 `#FAF7F2`／厚卡白 `#FFFFFF`／焙茶墨黑 `#2B2523`／奶油便籤黃 `#FFE5A3`／燕麥灰 `#EFEAE1`
- 級別色：N1 `#E63956`・N2 `#FF6B35`・N3 `#7CB518`・N4 `#0096C7`・N5 `#8338EC`（各含 tint）
- 級別主題化：Layout 依路由在 `<html>` 設 `data-level`，元件只用 `var(--level)` / `var(--level-tint)`
- 復古硬陰影（0 模糊）：`2/3/5px` 實心位移，無漸層、無玻璃擬態、無模糊
