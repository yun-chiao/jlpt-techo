import { z } from 'zod';
import type { LessonSet, VocabSet } from './types';

const furiganaSegmentSchema = z.tuple([z.string(), z.string().nullable()]);

const vocabularyItemSchema = z.object({
  kanji: z.string(),
  kana: z.string(),
  romaji: z.string(),
  part_of_speech: z.string(),
  meaning: z.string(),
  example_ja: z.string(),
  example_zh: z.string(),
  furigana: z.array(furiganaSegmentSchema).optional(),
});

const grammarExampleSchema = z.object({
  ja: z.string(),
  zh: z.string(),
});

const quizSchema = z.object({
  question_id: z.number(),
  type: z.literal('multiple_choice'),
  question_text: z.string(),
  options: z.array(z.string()),
  correct_answer: z.string(),
  explanation: z.string(),
});

const grammarPointSchema = z.object({
  point_title: z.string(),
  formula: z.string(),
  explanation: z.string(),
  alert: z.string(),
  examples: z.array(grammarExampleSchema),
  quizzes: z.array(quizSchema).optional(),
});

const lessonSchema = z.object({
  lesson_number: z.number(),
  lesson_title: z.string(),
  vocabulary: z.array(vocabularyItemSchema),
  grammar_points: z.array(grammarPointSchema),
  quizzes: z.array(quizSchema),
});

export const lessonSetSchema = z.array(lessonSchema);

const vocabEntrySchema = vocabularyItemSchema.extend({
  category: z.string(),
});

export const vocabSetSchema = z.array(vocabEntrySchema);

/** dev 模式下驗證單字總表，錯誤時印出第幾筆、哪個欄位。 */
export function validateVocabSet(data: unknown, sourceName: string): data is VocabSet {
  const result = vocabSetSchema.safeParse(data);
  if (result.success) return true;

  for (const issue of result.error.issues) {
    const [index, ...rest] = issue.path;
    const label = typeof index === 'number' ? `第 ${index + 1} 筆（索引 ${index}）` : '頂層';
    console.error(
      `[validate:data] ${sourceName} → ${label} → 欄位 "${rest.join('.')}"：${issue.message}`,
    );
  }
  return false;
}

/**
 * dev 模式下驗證載入的 LessonSet，格式不符時在 console 印出
 * 「第幾課、哪個欄位」的清楚錯誤。回傳資料是否有效。
 */
export function validateLessonSet(data: unknown, sourceName: string): data is LessonSet {
  const result = lessonSetSchema.safeParse(data);
  if (result.success) return true;

  for (const issue of result.error.issues) {
    const [index, ...rest] = issue.path;
    const lessonLabel =
      typeof index === 'number' ? `第 ${index + 1} 個 Lesson（索引 ${index}）` : '頂層';
    console.error(
      `[validate:data] ${sourceName} → ${lessonLabel} → 欄位 "${rest.join('.')}"：${issue.message}`,
    );
  }
  return false;
}
