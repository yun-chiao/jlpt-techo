import type { Level, Section, LessonSet, VocabSet, LevelQuizSet } from './types';

type LessonLoader = () => Promise<LessonSet>;
type VocabLoader = () => Promise<VocabSet>;
type QuizLoader = () => Promise<LevelQuizSet>;

/**
 * 內容註冊表：唯一的內容接口。
 * 要開通某個「分類 × 級別」，把 null 換成一個動態 import loader 即可，
 * 元件程式碼完全不必更動。
 * - grammar 指向「課程教材」（Lesson 陣列，如 grammar/n5.json）
 * - vocabulary 指向「單字總表」（VocabEntry 陣列，如 vocabulary/n5.json）
 * - quiz 指向「日檢題型專攻闖關套組」（LevelQuizSet 物件，如 quiz/n5.json）
 */
interface Registry {
  grammar: Record<Level, LessonLoader | null>;
  vocabulary: Record<Level, VocabLoader | null>;
  quiz: Record<Level, QuizLoader | null>;
}

export const registry: Registry = {
  grammar: {
    n1: () => import('./grammar/n1.json').then((m) => m.default as unknown as LessonSet),
    n2: () => import('./grammar/n2.json').then((m) => m.default as unknown as LessonSet),
    n3: () => import('./grammar/n3.json').then((m) => m.default as unknown as LessonSet),
    n4: () => import('./grammar/n4.json').then((m) => m.default as unknown as LessonSet),
    n5: () => import('./grammar/n5.json').then((m) => m.default as unknown as LessonSet),
  },
  vocabulary: {
    n1: () => import('./vocabulary/n1.json').then((m) => m.default as unknown as VocabSet),
    n2: () => import('./vocabulary/n2.json').then((m) => m.default as unknown as VocabSet),
    n3: () => import('./vocabulary/n3.json').then((m) => m.default as unknown as VocabSet),
    n4: () => import('./vocabulary/n4.json').then((m) => m.default as unknown as VocabSet),
    n5: () => import('./vocabulary/n5.json').then((m) => m.default as unknown as VocabSet),
  },
  quiz: {
    n1: () => import('./quiz/n1.json').then((m) => m.default as unknown as LevelQuizSet),
    n2: () => import('./quiz/n2.json').then((m) => m.default as unknown as LevelQuizSet),
    n3: () => import('./quiz/n3.json').then((m) => m.default as unknown as LevelQuizSet),
    n4: () => import('./quiz/n4.json').then((m) => m.default as unknown as LevelQuizSet),
    n5: () => import('./quiz/n5.json').then((m) => m.default as unknown as LevelQuizSet),
  },
};

export const isAvailable = (section: Section, level: Level): boolean =>
  registry[section][level] !== null;

