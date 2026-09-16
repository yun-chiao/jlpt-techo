import type { Level, Section, LessonSet, VocabSet } from './types';

type LessonLoader = () => Promise<LessonSet>;
type VocabLoader = () => Promise<VocabSet>;

/**
 * 內容註冊表：唯一的內容接口。
 * 要開通某個「分類 × 級別」，把 null 換成一個動態 import loader 即可，
 * 元件程式碼完全不必更動。
 * - grammar / quiz 指向「課程教材」（Lesson 陣列，如 grammar/n5.json）
 * - vocabulary 指向「單字總表」（VocabEntry 陣列，如 vocabulary/n5.json，
 *   獨立於課程，收錄該級別全部單字並附主題分類）
 */
interface Registry {
  grammar: Record<Level, LessonLoader | null>;
  vocabulary: Record<Level, VocabLoader | null>;
  quiz: Record<Level, LessonLoader | null>;
}

export const registry: Registry = {
  grammar: {
    n1: null,
    n2: null,
    n3: () => import('./grammar/n3.json').then((m) => m.default as unknown as LessonSet),
    n4: () => import('./grammar/n4.json').then((m) => m.default as unknown as LessonSet),
    n5: () => import('./grammar/n5.json').then((m) => m.default as unknown as LessonSet),
  },
  vocabulary: {
    n1: null,
    n2: null,
    n3: () => import('./vocabulary/n3.json').then((m) => m.default as unknown as VocabSet),
    n4: () => import('./vocabulary/n4.json').then((m) => m.default as unknown as VocabSet),
    n5: () => import('./vocabulary/n5.json').then((m) => m.default as unknown as VocabSet),
  },
  quiz: {
    n1: null,
    n2: null,
    n3: null,
    n4: null,
    // 練習題（課程制）未來可指向含 quizzes 的課程教材：
    // n5: () => import('./grammar/n5.json').then((m) => m.default as unknown as LessonSet),
    n5: null,
  },
};

export const isAvailable = (section: Section, level: Level): boolean =>
  registry[section][level] !== null;
