export type Level = 'n1' | 'n2' | 'n3' | 'n4' | 'n5';
export type Section = 'grammar' | 'vocabulary' | 'quiz';

/**
 * 振假名對位的一段：[文字, 讀音]。
 * 讀音為 null 代表這段不需要標音（送假名、助詞等非漢字部分）。
 * 由 scripts/generate_furigana.py 離線產生，前端只負責渲染。
 */
export type FuriganaSegment = [string, string | null];

export interface VocabularyItem {
  kanji: string;
  kana: string;
  romaji: string;
  part_of_speech: string;
  meaning: string;
  example_ja: string;
  example_zh: string;
  /** 逐字振假名對位資料；沒有漢字的單字不會有這個欄位 */
  furigana?: FuriganaSegment[];
}

export interface GrammarExample {
  ja: string;
  zh: string;
}

export interface GrammarPoint {
  point_title: string;
  formula: string;
  explanation: string;
  alert: string;
  examples: GrammarExample[];
  /** 這個文法點專屬的隨堂練習（選填；沒有時單課頁不顯示練習區塊） */
  quizzes?: Quiz[];
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

/** 一個級別的完整教材 = Lesson 陣列 */
export type LessonSet = Lesson[];

/** 單字總表的一筆：比課程單字多一個主題分類 */
export interface VocabEntry extends VocabularyItem {
  category: string;
}

/** 一個級別的完整單字總表（獨立於課程教材） */
export type VocabSet = VocabEntry[];

/** ─────────────────────────────────────────────────────────────
 * 日檢題型專攻・三部曲闖關書（JLPT Section-by-Section）資料結構
 * ──────────────────────────────────────────────────────────── */

/** 第 1 部：文法形式挖空（句子填空題） */
export interface SentenceQuizItem {
  id: string;
  question: string;
  options: string[];
  correctIndex: number; // 1-based: 1, 2, 3, 4
  explanation: string;
  targetGrammar?: string;
}

/** 第 2 部：★ 號排序重組（文の組み立て） */
export interface StarScrambleQuizItem {
  id: string;
  preText: string;
  postText: string;
  starIndex: number; // 0-based index of slot with ★ (usually 2, meaning 3rd slot)
  chunks: string[]; // 4 items (1, 2, 3, 4)
  correctOrder: number[]; // e.g. [2, 4, 1, 3] (1-based indices)
  explanation: string;
  fullSentence: string;
  translation: string;
}

/** 第 3 部：篇章脈絡填空小題 */
export interface PassageQuestionItem {
  blankNumber: number; // 1, 2, 3
  options: string[];
  correctIndex: number; // 1, 2, 3, 4
  explanation: string;
}

/** 第 3 部：篇章脈絡填空（文章整體文法） */
export interface PassageQuizItem {
  id: string;
  title: string;
  genre: string;
  passage: string;
  questions: PassageQuestionItem[];
  translation: string;
}

/** 一個級別的完整題型專攻闖關套組 */
export interface LevelQuizSet {
  level: Level;
  levelLabel: string;
  sentenceQuizzes: SentenceQuizItem[];
  starQuizzes: StarScrambleQuizItem[];
  passageQuizzes: PassageQuizItem[];
}

