import { useState, useMemo } from 'react';
import { useParams } from 'react-router-dom';
import type {
  Level,
  SentenceQuizItem,
  StarScrambleQuizItem,
  PassageQuizItem,
  PassageQuestionItem,
} from '../data/types';
import { LEVEL_LABELS, isLevel } from '../data/meta';
import { useQuizSet } from '../hooks/useQuizSet';
import { useDocumentTitle } from '../hooks/useDocumentTitle';
import { ComingSoon } from '../components/ComingSoon';
import { LoadingState, ErrorState } from '../components/StatusStates';
import { NotFoundPage } from './NotFoundPage';

type FilterType = 'all' | 'sentence' | 'star' | 'passage';

type UnifiedQuestion =
  | {
      type: 'sentence';
      id: string;
      data: SentenceQuizItem;
      indexInCategory: number;
      totalInCategory: number;
    }
  | {
      type: 'star';
      id: string;
      data: StarScrambleQuizItem;
      indexInCategory: number;
      totalInCategory: number;
    }
  | {
      type: 'passage';
      id: string;
      data: { passage: PassageQuizItem; subQ: PassageQuestionItem };
      indexInCategory: number;
      totalInCategory: number;
    };

export function QuizLevelPage() {
  const { level } = useParams();
  if (!isLevel(level)) return <NotFoundPage />;
  return <QuizLevelContent level={level} />;
}

function QuizLevelContent({ level }: { level: Level }) {
  const state = useQuizSet(level);
  const levelLabel = LEVEL_LABELS[level];
  const [filter, setFilter] = useState<FilterType>('all');
  const [currentIdx, setCurrentIdx] = useState(0);
  const [showJumpPanel, setShowJumpPanel] = useState(false);
  const [jumpInput, setJumpInput] = useState('');

  // 答題紀錄
  const [sentenceAnswers, setSentenceAnswers] = useState<Record<string, number>>({});
  const [starSlots, setStarSlots] = useState<Record<string, number[]>>({});
  const [passageAnswers, setPassageAnswers] = useState<Record<string, number>>({});

  useDocumentTitle(`${levelLabel} 練習題`);

  // 將所有題型整合成一體化的題目清單
  const allQuestions = useMemo<UnifiedQuestion[]>(() => {
    if (!state.data) return [];
    const set = state.data;
    const list: UnifiedQuestion[] = [];

    // 1. 文法形式挖空
    set.sentenceQuizzes.forEach((q, idx) => {
      list.push({
        type: 'sentence',
        id: q.id,
        data: q,
        indexInCategory: idx + 1,
        totalInCategory: set.sentenceQuizzes.length,
      });
    });

    // 2. ★ 號排序重組
    set.starQuizzes.forEach((q, idx) => {
      list.push({
        type: 'star',
        id: q.id,
        data: q,
        indexInCategory: idx + 1,
        totalInCategory: set.starQuizzes.length,
      });
    });

    // 3. 篇章脈絡填空小題
    set.passageQuizzes.forEach((passage) => {
      passage.questions.forEach((subQ) => {
        list.push({
          type: 'passage',
          id: `${passage.id}-${subQ.blankNumber}`,
          data: { passage, subQ },
          indexInCategory: subQ.blankNumber,
          totalInCategory: passage.questions.length,
        });
      });
    });

    return list;
  }, [state.data]);

  // 依據篩選器篩選題目
  const filteredQuestions = useMemo(() => {
    if (filter === 'all') return allQuestions;
    return allQuestions.filter((q) => q.type === filter);
  }, [allQuestions, filter]);

  if (state.status === 'unavailable') return <ComingSoon section="quiz" level={level} />;
  if (state.status === 'loading') return <LoadingState />;
  if (state.status === 'error' || !state.data) return <ErrorState />;

  const safeIdx = Math.min(currentIdx, Math.max(0, filteredQuestions.length - 1));
  const activeQuestion = filteredQuestions[safeIdx];

  const handleSwitchFilter = (newFilter: FilterType) => {
    setFilter(newFilter);
    setCurrentIdx(0);
    setShowJumpPanel(false);
  };

  const handlePrev = () => {
    setCurrentIdx((i) => Math.max(0, i - 1));
  };

  const handleNext = () => {
    setCurrentIdx((i) => Math.min(filteredQuestions.length - 1, i + 1));
  };

  const handleDirectJump = (e: React.FormEvent) => {
    e.preventDefault();
    const num = parseInt(jumpInput.trim(), 10);
    if (!isNaN(num) && num >= 1 && num <= filteredQuestions.length) {
      setCurrentIdx(num - 1);
      setShowJumpPanel(false);
      setJumpInput('');
    }
  };

  const sentenceCount = state.data.sentenceQuizzes.length;
  const starCount = state.data.starQuizzes.length;
  const passageCount = state.data.passageQuizzes.reduce((n, p) => n + p.questions.length, 0);

  return (
    <div className="flex flex-col gap-5 md:gap-6">
      {/* 級別大標色塊 */}
      <header className="rounded-xl border-3 border-paper-sumi bg-level-tint px-5 py-5 shadow-retro md:px-8 md:py-7">
        <h1 className="font-display text-2xl font-black md:text-4xl">
          <span className="mr-2.5 inline-block rounded-lg border-2 border-paper-sumi bg-level px-2.5 py-0.5 text-paper-card md:px-3 md:py-1">
            {levelLabel}
          </span>
          練習題
        </h1>
        <p className="mt-2 font-mono text-xs text-paper-sumi/70 md:text-sm">
          全真日檢規格題庫・共 {allQuestions.length} 題
        </p>
      </header>

      {/* 篩選與題號導航列（框框外面・同一水平線・像素級對齊） */}
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-paper-sumi/15 pb-2.5">
        {/* 左側分類按鈕 */}
        <div className="flex flex-wrap items-center gap-1.5">
          <button
            type="button"
            onClick={() => handleSwitchFilter('all')}
            className={`inline-flex h-8 items-center rounded-lg px-3 font-mono text-xs font-bold transition-all md:px-3.5 md:text-sm ${
              filter === 'all'
                ? 'border-2 border-paper-sumi bg-paper-sumi text-white shadow-retro-sm font-black'
                : 'border border-paper-sumi/30 bg-paper-card text-paper-sumi/80 hover:bg-paper-butter'
            }`}
          >
            全部 ({allQuestions.length})
          </button>
          <button
            type="button"
            onClick={() => handleSwitchFilter('sentence')}
            className={`inline-flex h-8 items-center rounded-lg px-3 font-mono text-xs font-bold transition-all md:px-3.5 md:text-sm ${
              filter === 'sentence'
                ? 'border-2 border-paper-sumi bg-paper-sumi text-white shadow-retro-sm font-black'
                : 'border border-paper-sumi/30 bg-paper-card text-paper-sumi/80 hover:bg-paper-butter'
            }`}
          >
            挖空 ({sentenceCount})
          </button>
          <button
            type="button"
            onClick={() => handleSwitchFilter('star')}
            className={`inline-flex h-8 items-center rounded-lg px-3 font-mono text-xs font-bold transition-all md:px-3.5 md:text-sm ${
              filter === 'star'
                ? 'border-2 border-paper-sumi bg-paper-sumi text-white shadow-retro-sm font-black'
                : 'border border-paper-sumi/30 bg-paper-card text-paper-sumi/80 hover:bg-paper-butter'
            }`}
          >
            ★重組 ({starCount})
          </button>
          <button
            type="button"
            onClick={() => handleSwitchFilter('passage')}
            className={`inline-flex h-8 items-center rounded-lg px-3 font-mono text-xs font-bold transition-all md:px-3.5 md:text-sm ${
              filter === 'passage'
                ? 'border-2 border-paper-sumi bg-paper-sumi text-white shadow-retro-sm font-black'
                : 'border border-paper-sumi/30 bg-paper-card text-paper-sumi/80 hover:bg-paper-butter'
            }`}
          >
            篇章 ({passageCount})
          </button>
        </div>

        {/* 右側：一體成型、尺寸緊湊、水平幾何絕對居中的 Stepper 控制群組 */}
        <div className="inline-flex h-8 items-stretch rounded-lg border-2 border-paper-sumi bg-paper-card shadow-retro-sm">
          {/* 左箭頭（小巧 SVG，垂直 100% 幾何居中） */}
          <button
            type="button"
            disabled={safeIdx === 0}
            onClick={handlePrev}
            className="flex w-7 items-center justify-center border-r border-paper-sumi/25 text-paper-sumi/80 transition-colors hover:bg-paper-butter disabled:cursor-not-allowed disabled:opacity-30 disabled:hover:bg-transparent"
            title="上一題"
          >
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
              <polyline points="15 18 9 12 15 6" />
            </svg>
          </button>

          {/* 題號與展開箭頭（高度、字重與垂直中線絕對齊平） */}
          <button
            type="button"
            onClick={() => setShowJumpPanel((v) => !v)}
            className="flex items-center gap-1.5 px-3 font-mono text-xs font-black text-paper-sumi transition-colors hover:bg-paper-butter"
            title="點擊展開快速跳題面板"
          >
            <span>Q.{String(safeIdx + 1).padStart(2, '0')}</span>
            <span className="text-paper-sumi/35">/</span>
            <span className="text-paper-sumi/60">{String(filteredQuestions.length).padStart(2, '0')}</span>
            <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" className="text-paper-sumi/60" aria-hidden="true">
              <polyline points="6 9 12 15 18 9" />
            </svg>
          </button>

          {/* 右箭頭（小巧 SVG，垂直 100% 幾何居中） */}
          <button
            type="button"
            disabled={safeIdx === filteredQuestions.length - 1}
            onClick={handleNext}
            className="flex w-7 items-center justify-center border-l border-paper-sumi/25 text-paper-sumi/80 transition-colors hover:bg-paper-butter disabled:cursor-not-allowed disabled:opacity-30 disabled:hover:bg-transparent"
            title="下一題"
          >
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
              <polyline points="9 18 15 12 9 6" />
            </svg>
          </button>
        </div>
      </div>

      {/* 展開式快速跳題面板（位於框框外部） */}
      {showJumpPanel && (
        <div className="rounded-xl border-2 border-paper-sumi bg-paper-card p-4 shadow-retro animate-in fade-in duration-150">
          <div className="flex flex-wrap items-center justify-between gap-3 border-b border-paper-sumi/15 pb-2.5">
            <span className="font-display text-xs font-bold text-paper-sumi">
              快速跳題（共 {filteredQuestions.length} 題）
            </span>

            {/* 輸入題號直接前往 */}
            <form onSubmit={handleDirectJump} className="flex items-center gap-1.5">
              <span className="font-mono text-xs text-paper-sumi/60">跳至第</span>
              <input
                type="number"
                min="1"
                max={filteredQuestions.length}
                value={jumpInput}
                onChange={(e) => setJumpInput(e.target.value)}
                placeholder={String(safeIdx + 1)}
                className="h-7 w-14 rounded border border-paper-sumi px-1.5 text-center font-mono text-xs font-bold focus:outline-none focus:ring-1 focus:ring-paper-sumi"
              />
              <span className="font-mono text-xs text-paper-sumi/60">題</span>
              <button
                type="submit"
                className="rounded border border-paper-sumi bg-paper-butter px-2.5 py-0.5 font-mono text-xs font-bold text-paper-sumi hover:bg-paper-sumi hover:text-white"
              >
                前往
              </button>
            </form>
          </div>

          {/* 題號方塊網格 */}
          <div className="mt-3 max-h-[160px] overflow-y-auto pr-1">
            <div className="grid grid-cols-8 gap-1.5 sm:grid-cols-10 md:grid-cols-12">
              {filteredQuestions.map((q, idx) => {
                const isCur = idx === safeIdx;
                let isDone = false;
                if (q.type === 'sentence') isDone = sentenceAnswers[q.id] !== undefined;
                if (q.type === 'star') isDone = (starSlots[q.id]?.length ?? 0) === 4;
                if (q.type === 'passage') isDone = passageAnswers[q.id] !== undefined;

                return (
                  <button
                    key={q.id}
                    type="button"
                    onClick={() => {
                      setCurrentIdx(idx);
                      setShowJumpPanel(false);
                    }}
                    className={`flex h-7 items-center justify-center rounded border font-mono text-xs transition-all ${
                      isCur
                        ? 'border-2 border-paper-sumi bg-paper-sumi font-black text-white shadow-retro-sm'
                        : isDone
                          ? 'border-paper-sumi/40 bg-paper-oatmeal text-paper-sumi/90 font-bold'
                          : 'border-paper-sumi/20 bg-paper-canvas text-paper-sumi/60 hover:bg-paper-butter'
                    }`}
                  >
                    {String(idx + 1).padStart(2, '0')}
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* 核心作答卡片 */}
      {activeQuestion && (
        <div className="rounded-2xl border-3 border-paper-sumi bg-white p-4 shadow-retro md:p-7">
          {/* 卡片頂部標籤 */}
          <div className="flex items-center justify-between border-b border-paper-sumi/15 pb-3">
            <span className="rounded border border-paper-sumi/30 bg-paper-oatmeal px-2.5 py-0.5 font-mono text-xs font-bold text-paper-sumi/80">
              {activeQuestion.type === 'sentence' && 'PART 01 ・ 文法形式挖空'}
              {activeQuestion.type === 'star' && 'PART 02 ・ ★ 號排序重組'}
              {activeQuestion.type === 'passage' && 'PART 03 ・ 篇章脈絡填空'}
            </span>

            <span className="font-mono text-xs text-paper-sumi/50">
              {activeQuestion.type === 'sentence' && activeQuestion.data.targetGrammar
                ? `考點：${activeQuestion.data.targetGrammar}`
                : `題號：${safeIdx + 1} / ${filteredQuestions.length}`}
            </span>
          </div>

          {/* 題目主體渲染 */}
          <div className="mt-4">
            {activeQuestion.type === 'sentence' && (
              <SentenceQuestionCard
                quiz={activeQuestion.data}
                userChoice={sentenceAnswers[activeQuestion.id]}
                onSelect={(choice) =>
                  setSentenceAnswers((prev) => ({ ...prev, [activeQuestion.id]: choice }))
                }
              />
            )}

            {activeQuestion.type === 'star' && (
              <StarQuestionCard
                quiz={activeQuestion.data}
                slots={starSlots[activeQuestion.id] ?? []}
                onChangeSlots={(newSlots) =>
                  setStarSlots((prev) => ({ ...prev, [activeQuestion.id]: newSlots }))
                }
              />
            )}

            {activeQuestion.type === 'passage' && (
              <PassageQuestionCard
                passage={activeQuestion.data.passage}
                subQ={activeQuestion.data.subQ}
                userChoice={passageAnswers[activeQuestion.id]}
                onSelect={(choice) =>
                  setPassageAnswers((prev) => ({ ...prev, [activeQuestion.id]: choice }))
                }
              />
            )}
          </div>

          {/* 卡片底部翻頁按鈕 */}
          <div className="mt-6 flex items-center justify-between border-t border-paper-sumi/15 pt-3.5">
            <button
              type="button"
              disabled={safeIdx === 0}
              onClick={handlePrev}
              className="rounded-lg border border-paper-sumi/30 bg-paper-card px-3.5 py-1.5 font-mono text-xs font-bold text-paper-sumi hover:bg-paper-butter disabled:opacity-30"
            >
              ← PREV
            </button>
            <span className="font-mono text-xs font-bold text-paper-sumi/50">
              {String(safeIdx + 1).padStart(2, '0')} / {String(filteredQuestions.length).padStart(2, '0')}
            </span>
            <button
              type="button"
              disabled={safeIdx === filteredQuestions.length - 1}
              onClick={handleNext}
              className="rounded-lg border-2 border-paper-sumi bg-paper-butter px-4 py-1.5 font-mono text-xs font-black text-paper-sumi shadow-retro-sm hover:translate-x-[-1px] hover:translate-y-[-1px] disabled:opacity-30"
            >
              NEXT →
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

/* ─────────────────────────────────────────────────────────────
 * 子元件：第 1 部 挖空填空（零刺眼綠色，素雅日系質感）
 * ──────────────────────────────────────────────────────────── */
function SentenceQuestionCard({
  quiz,
  userChoice,
  onSelect,
}: {
  quiz: SentenceQuizItem;
  userChoice?: number;
  onSelect: (choice: number) => void;
}) {
  const hasAnswered = userChoice !== undefined;
  const isCorrect = userChoice === quiz.correctIndex;

  return (
    <div>
      {/* 句子文字 */}
      <div
        lang="ja"
        className="my-4 font-body text-base font-bold leading-relaxed text-paper-sumi md:text-lg"
      >
        {quiz.question.split('（　　）').map((part, idx, arr) => (
          <span key={idx}>
            {part}
            {idx < arr.length - 1 && (
              <span className="mx-1 inline-block min-w-[56px] rounded border-b-2 border-paper-sumi bg-paper-butter/80 px-2 py-0.5 text-center font-mono text-xs font-black text-[#ff6b35] md:text-sm">
                {hasAnswered ? quiz.options[userChoice - 1] : '（　　）'}
              </span>
            )}
          </span>
        ))}
      </div>

      {/* 選項四宮格：正解以奶油黃優雅高亮，不用刺眼綠色 */}
      <div className="grid grid-cols-1 gap-2.5 sm:grid-cols-2 md:gap-3">
        {quiz.options.map((opt, optIdx) => {
          const optNum = optIdx + 1;
          const isSelected = userChoice === optNum;
          const isRight = optNum === quiz.correctIndex;

          let optStyle =
            'bg-paper-card border-paper-sumi hover:bg-paper-butter text-paper-sumi';
          if (hasAnswered) {
            if (isRight) {
              // 正解：經典奶油黃 ＋ 粗黑外框
              optStyle =
                'bg-paper-butter border-2 border-paper-sumi text-paper-sumi font-black shadow-retro-sm';
            } else if (isSelected) {
              // 選錯：柔和刪除線
              optStyle =
                'bg-paper-oatmeal border border-paper-sumi/40 text-paper-sumi/60 line-through';
            } else {
              optStyle = 'bg-paper-card border-paper-sumi/20 opacity-40 shadow-none';
            }
          }

          return (
            <button
              key={optIdx}
              type="button"
              lang="ja"
              disabled={hasAnswered}
              onClick={() => onSelect(optNum)}
              className={`flex items-center justify-between rounded-xl border-2 p-3 text-left font-body text-sm font-bold shadow-retro-sm transition-all md:p-3.5 md:text-base ${optStyle}`}
            >
              <div className="flex items-center gap-2.5">
                <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full border-1.5 border-current font-mono text-xs font-black">
                  {optNum}
                </span>
                <span className="leading-snug">{opt}</span>
              </div>
              {hasAnswered && isRight && (
                <span className="font-mono text-xs font-black text-paper-sumi">✓ 正解</span>
              )}
            </button>
          );
        })}
      </div>

      {/* 詳解：素雅紙質底色 */}
      {hasAnswered && (
        <div className="mt-4 rounded-xl border-2 border-paper-sumi bg-paper-canvas p-3.5 shadow-retro-sm md:p-4">
          <div className="font-display text-sm font-bold text-paper-sumi md:text-base">
            {isCorrect ? (
              <span>○ 答對了！</span>
            ) : (
              <span>
                ✗ 答錯了，正解為 ({quiz.correctIndex}) {quiz.options[quiz.correctIndex - 1]}
              </span>
            )}
          </div>
          <p className="mt-1.5 font-body text-xs font-medium leading-relaxed text-paper-sumi/90 md:text-sm">
            <strong className="font-bold text-paper-sumi">💡 考點解析：</strong>
            {quiz.explanation}
          </p>
        </div>
      )}
    </div>
  );
}

/* ─────────────────────────────────────────────────────────────
 * 子元件：第 2 部 ★ 號排序重組（零刺眼綠色，素雅日系質感）
 * ──────────────────────────────────────────────────────────── */
function StarQuestionCard({
  quiz,
  slots,
  onChangeSlots,
}: {
  quiz: StarScrambleQuizItem;
  slots: number[];
  onChangeSlots: (newSlots: number[]) => void;
}) {
  const handleAddChunk = (chunkNum: number) => {
    if (slots.length >= 4 || slots.includes(chunkNum)) return;
    onChangeSlots([...slots, chunkNum]);
  };

  const handleReset = () => {
    onChangeSlots([]);
  };

  const isCompleted = slots.length === 4;
  const isOrderCorrect =
    isCompleted && slots.every((val, idx) => val === quiz.correctOrder[idx]);

  const starPlacedNum = slots[quiz.starIndex];
  const starCorrectNum = quiz.correctOrder[quiz.starIndex];

  return (
    <div>
      <p className="text-xs text-paper-sumi/70">
        點選下方 4 個詞塊填入橫線，找出落在 <strong>★ 號位置</strong> 的選項：
      </p>

      {/* 題目句子主體 */}
      <div className="my-4 rounded-xl border border-paper-sumi/20 bg-paper-canvas p-4 md:p-5">
        <p
          lang="ja"
          className="font-body text-base font-bold leading-loose text-paper-sumi md:text-lg"
        >
          <span>{quiz.preText}</span>

          {/* 4 個連續插槽 */}
          {[0, 1, 2, 3].map((slotIdx) => {
            const placedChunkNum = slots[slotIdx];
            const isStarSlot = slotIdx === quiz.starIndex;

            return (
              <span
                key={slotIdx}
                className={`mx-1 inline-flex min-h-[32px] min-w-[62px] items-center justify-center rounded border-b-2.5 px-2 py-0.5 align-middle font-body text-xs font-black transition-all md:min-w-[76px] md:text-sm ${
                  isStarSlot
                    ? 'border-[#ff6b35] bg-[#ffe5a3] text-[#ff6b35] shadow-sm'
                    : 'border-paper-sumi bg-white text-paper-sumi shadow-sm'
                } ${placedChunkNum ? '' : 'border-dashed opacity-60'}`}
              >
                {isStarSlot && <span className="mr-0.5 text-[11px]">★</span>}
                {placedChunkNum ? (
                  <span>
                    {placedChunkNum}. {quiz.chunks[placedChunkNum - 1]}
                  </span>
                ) : (
                  <span className="font-mono text-xs text-paper-sumi/40">
                    {isStarSlot ? '★ ?' : '?'}
                  </span>
                )}
              </span>
            );
          })}

          <span>{quiz.postText}</span>
        </p>
      </div>

      {/* 詞塊碎片點選區 */}
      <div className="mt-4 border-t border-paper-sumi/10 pt-3">
        <div className="flex items-center justify-between">
          <span className="font-display text-xs font-bold text-paper-sumi/70">
            👇 點擊詞塊依序填入：
          </span>
          {slots.length > 0 && (
            <button
              type="button"
              onClick={handleReset}
              className="flex items-center gap-1 rounded-md border border-paper-sumi/30 bg-paper-oatmeal px-2 py-0.5 font-mono text-xs font-bold text-paper-sumi/80 hover:bg-paper-butter"
            >
              <span>↺</span>
              <span>清空重排</span>
            </button>
          )}
        </div>

        <div className="mt-2.5 grid grid-cols-2 gap-2 sm:grid-cols-4 md:gap-2.5">
          {quiz.chunks.map((chunkText, cIdx) => {
            const chunkNum = cIdx + 1;
            const isUsed = slots.includes(chunkNum);

            return (
              <button
                key={cIdx}
                type="button"
                lang="ja"
                disabled={isUsed || isCompleted}
                onClick={() => handleAddChunk(chunkNum)}
                className={`flex items-center gap-2 rounded-xl border-2 border-paper-sumi p-2.5 text-left font-body text-xs font-bold shadow-retro-sm transition-all md:p-3 md:text-sm ${
                  isUsed
                    ? 'cursor-not-allowed border-paper-sumi/20 bg-paper-oatmeal/60 opacity-30 shadow-none'
                    : 'bg-white hover:bg-paper-butter active:translate-y-0.5'
                }`}
              >
                <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full border border-paper-sumi font-mono text-[11px] font-black">
                  {chunkNum}
                </span>
                <span className="truncate">{chunkText}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* 完成驗證回饋卡：素雅紙質底色 */}
      {isCompleted && (
        <div className="mt-4 rounded-xl border-2 border-paper-sumi bg-paper-canvas p-4 shadow-retro-sm animate-in fade-in duration-150">
          <div className="flex flex-wrap items-center justify-between gap-2.5">
            <div className="font-display text-sm font-black text-paper-sumi md:text-base">
              {isOrderCorrect ? (
                <span>○ 重組順序完全正確！</span>
              ) : (
                <span className="text-paper-sumi/80">
                  順序稍有出入，可點右上「↺ 清空重排」再試一次
                </span>
              )}
            </div>

            {/* ★ 號選項公佈徽章 */}
            <div className="rounded-lg border-2 border-paper-sumi bg-white px-3 py-1 font-body text-xs font-black shadow-retro-sm md:text-sm">
              落在 ★ 號位置的是：
              <span className="text-[#ff6b35]">
                【 {starPlacedNum} 號：{quiz.chunks[starPlacedNum - 1]} 】
              </span>
              {starPlacedNum === starCorrectNum ? '（正確 ✓）' : `（正解應為 ${starCorrectNum} 號）`}
            </div>
          </div>

          <div className="mt-3 border-t border-paper-sumi/15 pt-2.5">
            <p className="font-body text-xs font-medium leading-relaxed text-paper-sumi md:text-sm">
              <strong className="font-bold">正確完整句：</strong>
              <span lang="ja" className="ml-1 font-bold text-paper-sumi">
                {quiz.fullSentence}
              </span>
            </p>
            <p className="mt-1 font-body text-xs text-paper-sumi/70 md:text-sm">
              <strong className="font-bold">中文對照：</strong>
              {quiz.translation}
            </p>
            <p className="mt-1.5 font-body text-xs leading-relaxed text-paper-sumi/90 md:text-sm">
              <strong className="font-bold text-paper-sumi">💡 語法拆解：</strong>
              {quiz.explanation}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

/* ─────────────────────────────────────────────────────────────
 * 子元件：第 3 部 篇章脈絡填空（零刺眼綠色，素雅日系質感）
 * ──────────────────────────────────────────────────────────── */
function PassageQuestionCard({
  passage,
  subQ,
  userChoice,
  onSelect,
}: {
  passage: PassageQuizItem;
  subQ: PassageQuestionItem;
  userChoice?: number;
  onSelect: (choice: number) => void;
}) {
  const [showTranslation, setShowTranslation] = useState(false);
  const hasAnswered = userChoice !== undefined;
  const isCorrect = userChoice === subQ.correctIndex;

  return (
    <div>
      <div className="flex items-center justify-between">
        <h3 className="font-display text-base font-black text-paper-sumi md:text-lg">
          📖 {passage.title}
        </h3>
        <span className="rounded border border-paper-sumi/20 bg-paper-oatmeal px-2 py-0.5 font-mono text-[11px] font-bold text-paper-sumi">
          {passage.genre}
        </span>
      </div>

      {/* 篇章閱讀文字框 */}
      <div
        lang="ja"
        className="my-4 max-h-[220px] overflow-y-auto rounded-xl border border-paper-sumi/20 bg-paper-canvas p-4 font-body text-sm font-normal leading-relaxed text-paper-sumi/90 md:text-base md:leading-loose"
      >
        {passage.passage.split(/(【\s*\d+\s*】)/).map((segment, sIdx) => {
          const match = segment.match(/【\s*(\d+)\s*】/);
          if (match) {
            const blankNum = parseInt(match[1], 10);
            const isCurrentBlank = blankNum === subQ.blankNumber;

            return (
              <span
                key={sIdx}
                className={`mx-1 inline-flex items-center justify-center rounded border px-2 py-0.5 align-middle font-body text-xs font-black shadow-sm ${
                  isCurrentBlank
                    ? 'border-[#ff6b35] bg-[#ffe5a3] text-[#ff6b35] ring-2 ring-[#ff6b35]/50'
                    : hasAnswered && isCurrentBlank
                      ? 'border-paper-sumi bg-paper-butter text-paper-sumi'
                      : 'border-paper-sumi/30 bg-white text-paper-sumi/70'
                }`}
              >
                【 {String(blankNum).padStart(2, '0')} 】
              </span>
            );
          }
          return <span key={sIdx}>{segment}</span>;
        })}
      </div>

      {/* 中文翻譯收合鈕 */}
      <div className="mb-3">
        <button
          type="button"
          onClick={() => setShowTranslation((v) => !v)}
          className="font-mono text-xs font-bold text-paper-sumi/60 hover:text-[#ff6b35]"
        >
          {showTranslation ? '▲ 收合中文翻譯' : '▼ 展開中日對照全文翻譯'}
        </button>
        {showTranslation && (
          <div className="mt-2 rounded-lg border border-paper-sumi/20 bg-paper-canvas p-3 font-body text-xs leading-relaxed text-paper-sumi/80">
            {passage.translation}
          </div>
        )}
      </div>

      {/* 本題選項 */}
      <div className="border-t border-paper-sumi/10 pt-3">
        <div className="mb-2 font-display text-xs font-bold text-paper-sumi md:text-sm">
          請選擇【 空白 {String(subQ.blankNumber).padStart(2, '0')} 】應填入的最適當選項：
        </div>

        <div className="grid grid-cols-1 gap-2 sm:grid-cols-2 md:gap-2.5">
          {subQ.options.map((opt, optIdx) => {
            const optNum = optIdx + 1;
            const isSelected = userChoice === optNum;
            const isRight = optNum === subQ.correctIndex;

            let btnStyle =
              'bg-paper-card border-paper-sumi hover:bg-paper-butter text-paper-sumi';
            if (hasAnswered) {
              if (isRight) {
                // 正解：奶油黃高亮
                btnStyle =
                  'bg-paper-butter border-2 border-paper-sumi text-paper-sumi font-black shadow-retro-sm';
              } else if (isSelected) {
                btnStyle =
                  'bg-paper-oatmeal border border-paper-sumi/40 text-paper-sumi/60 line-through';
              } else {
                btnStyle = 'bg-paper-card border-paper-sumi/30 opacity-40 shadow-none';
              }
            }

            return (
              <button
                key={optIdx}
                type="button"
                lang="ja"
                disabled={hasAnswered}
                onClick={() => onSelect(optNum)}
                className={`flex items-center justify-between rounded-xl border-2 p-2.5 text-left font-body text-xs font-bold shadow-retro-sm transition-all md:p-3 md:text-sm ${btnStyle}`}
              >
                <div className="flex items-center gap-2">
                  <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full border-1.5 border-current font-mono text-[11px] font-black">
                    {optNum}
                  </span>
                  <span>{opt}</span>
                </div>
                {hasAnswered && isRight && (
                  <span className="font-mono text-xs font-black text-paper-sumi">✓ 正解</span>
                )}
              </button>
            );
          })}
        </div>

        {hasAnswered && (
          <div className="mt-3.5 rounded-lg border-2 border-paper-sumi bg-paper-canvas p-3 font-body text-xs leading-relaxed text-paper-sumi shadow-retro-sm md:text-sm">
            <div className="font-display font-bold">
              {isCorrect ? (
                <span>○ 答對了！</span>
              ) : (
                <span>
                  ✗ 答錯了，正解為 ({subQ.correctIndex}) {subQ.options[subQ.correctIndex - 1]}
                </span>
              )}
            </div>
            <p className="mt-1">
              <strong className="font-bold">💡 脈絡解析：</strong>
              {subQ.explanation}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
