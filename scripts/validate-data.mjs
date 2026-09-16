// 掃描 src/data/**/*.json，用與 src/data/validate.ts 相同的 zod schema 驗證。
// 用法：npm run validate:data
import { readdir, readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { z } from 'zod';

const dataDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../src/data');

const vocabularyItemSchema = z.object({
  kanji: z.string(),
  kana: z.string(),
  romaji: z.string(),
  part_of_speech: z.string(),
  meaning: z.string(),
  example_ja: z.string(),
  example_zh: z.string(),
});

const grammarExampleSchema = z.object({ ja: z.string(), zh: z.string() });

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

const lessonSetSchema = z.array(lessonSchema);

const vocabEntrySchema = vocabularyItemSchema.extend({ category: z.string() });
const vocabSetSchema = z.array(vocabEntrySchema);

const entries = await readdir(dataDir, { recursive: true, withFileTypes: true });
const jsonFiles = entries
  .filter((e) => e.isFile() && e.name.endsWith('.json'))
  .map((e) => path.join(e.parentPath ?? e.path, e.name));

if (jsonFiles.length === 0) {
  console.log('src/data 下沒有任何 JSON 檔。');
  process.exit(0);
}

let failed = false;

for (const file of jsonFiles) {
  const rel = path.relative(dataDir, file);
  let data;
  try {
    data = JSON.parse(await readFile(file, 'utf8'));
  } catch (err) {
    console.error(`✗ ${rel}：不是合法的 JSON — ${err.message}`);
    failed = true;
    continue;
  }
  // 依形狀判斷：課程教材（有 lesson_number）或單字總表（有 category）
  const isVocabSet = Array.isArray(data) && data.length > 0 && 'category' in data[0];
  const schema = isVocabSet ? vocabSetSchema : lessonSetSchema;
  const kind = isVocabSet ? '筆單字' : '課';
  const unit = isVocabSet ? '筆' : '個 Lesson';

  const result = schema.safeParse(data);
  if (result.success) {
    console.log(`✓ ${rel}：${result.data.length} ${kind}，格式正確`);
  } else {
    failed = true;
    for (const issue of result.error.issues) {
      const [index, ...rest] = issue.path;
      const label = typeof index === 'number' ? `第 ${index + 1} ${unit}（索引 ${index}）` : '頂層';
      console.error(`✗ ${rel} → ${label} → 欄位 "${rest.join('.')}"：${issue.message}`);
    }
  }
}

process.exit(failed ? 1 : 0);
