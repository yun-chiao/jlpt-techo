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
