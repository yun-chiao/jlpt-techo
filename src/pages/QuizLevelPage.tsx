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
    <div className="flex flex-col gap-4 sm:gap-5 md:gap-6">
      {/* 級別大標色塊 */}
      <header className="rounded-xl border-3 border-paper-sumi bg-level-tint px-4 py-4 shadow-retro sm:px-6 sm:py-5 md:px-8 md:py-7">
        <h1 className="font-display text-xl font-black sm:text-2xl md:text-4xl">
          <span className="mr-2 inline-block rounded-lg border-2 border-paper-sumi bg-level px-2 py-0.5 text-paper-card sm:mr-2.5 sm:px-3 sm:py-1">
            {levelLabel}
          </span>
          練習題
        </h1>
        <p className="mt-1.5 font-mono text-[11px] text-paper-sumi/70 sm:mt-2 sm:text-xs md:text-sm">
          全真日檢規格題庫・共 {allQuestions.length} 題
        </p>
      </header>

      {/* 篩選與題號導航列（針對手機優化：Filter 橫向滑動，Stepper 與按鈕絕對水平對齊） */}
      <div className="flex flex-col gap-2.5 border-b border-paper-sumi/15 pb-2.5 sm:flex-row sm:items-center sm:justify-between">
        {/* 左側分類按鈕（手機上支援水平順暢滑動，不換行擠壓） */}
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 sm:pb-0 scrollbar-none">
          <button
            type="button"
            onClick={() => handleSwitchFilter('all')}
            className={`inline-flex h-8 shrink-0 items-center rounded-lg px-3 font-mono text-xs font-bold transition-all md:px-3.5 md:text-sm ${
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
            className={`inline-flex h-8 shrink-0 items-center rounded-lg px-3 font-mono text-xs font-bold transition-all md:px-3.5 md:text-sm ${
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
            className={`inline-flex h-8 shrink-0 items-center rounded-lg px-3 font-mono text-xs font-bold transition-all md:px-3.5 md:text-sm ${
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
            className={`inline-flex h-8 shrink-0 items-center rounded-lg px-3 font-mono text-xs font-bold transition-all md:px-3.5 md:text-sm ${
              filter === 'passage'
                ? 'border-2 border-paper-sumi bg-paper-sumi text-white shadow-retro-sm font-black'
                : 'border border-paper-sumi/30 bg-paper-card text-paper-sumi/80 hover:bg-paper-butter'
            }`}
          >
            篇章 ({passageCount})
          </button>
        </div>

        {/* 右側：一體成型、尺寸緊湊、水平幾何絕對居中的 Stepper 控制群組 */}
        <div className="flex w-full items-center justify-between sm:w-auto sm:justify-end">
          <span className="font-mono text-[11px] font-bold text-paper-sumi/60 sm:hidden">
            {filter === 'all' && '全題型混合練習'}
            {filter === 'sentence' && 'PART 01 挖空專攻'}
            {filter === 'star' && 'PART 02 ★重組專攻'}
            {filter === 'passage' && 'PART 03 篇章專攻'}
          </span>
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

            {/* 題號與展開箭頭 */}
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
      </div>

      {/* 展開式快速跳題面板（手機版優化為 5 欄網格，觸控超輕鬆） */}
      {showJumpPanel && (
        <div className="rounded-xl border-2 border-paper-sumi bg-paper-card p-3.5 shadow-retro animate-in fade-in duration-150 sm:p-4">
          <div className="flex flex-wrap items-center justify-between gap-2.5 border-b border-paper-sumi/15 pb-2.5">
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

          {/* 題號方塊網格：手機 5 欄，平板 8 欄，電腦 12 欄 */}
          <div className="mt-3 max-h-[180px] overflow-y-auto pr-1">
            <div className="grid grid-cols-5 gap-1.5 sm:grid-cols-8 md:grid-cols-12">
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

      {/* 核心作答卡片（內距針對手機優化為 p-3.5 sm:p-5 md:p-7） */}
      {activeQuestion && (
        <div className="rounded-2xl border-3 border-paper-sumi bg-white p-3.5 shadow-retro sm:p-5 md:p-7">
          {/* 卡片頂部標籤 */}
          <div className="flex flex-wrap items-center justify-between gap-2 border-b border-paper-sumi/15 pb-2.5">
            <span className="rounded border border-paper-sumi/30 bg-paper-oatmeal px-2 py-0.5 font-mono text-[11px] font-bold text-paper-sumi/80 sm:text-xs">
              {activeQuestion.type === 'sentence' && 'PART 01 ・ 文法形式挖空'}
              {activeQuestion.type === 'star' && 'PART 02 ・ ★ 號排序重組'}
              {activeQuestion.type === 'passage' && 'PART 03 ・ 篇章脈絡填空'}
            </span>

            {activeQuestion.type === 'sentence' && activeQuestion.data.targetGrammar ? (
              <span className="max-w-[200px] truncate font-mono text-[11px] text-paper-sumi/60 sm:max-w-none sm:text-xs">
                考點：{activeQuestion.data.targetGrammar}
              </span>
            ) : null}
          </div>

          {/* 題目主體渲染 */}
          <div className="mt-3 sm:mt-4">
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
          <div className="mt-5 flex items-center justify-between border-t border-paper-sumi/15 pt-3">
            <button
              type="button"
              disabled={safeIdx === 0}
              onClick={handlePrev}
              className="rounded-lg border border-paper-sumi/30 bg-paper-card px-3 py-1.5 font-mono text-xs font-bold text-paper-sumi hover:bg-paper-butter disabled:opacity-30"
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
              className="rounded-lg border-2 border-paper-sumi bg-paper-butter px-3.5 py-1.5 font-mono text-xs font-black text-paper-sumi shadow-retro-sm hover:translate-x-[-1px] hover:translate-y-[-1px] disabled:opacity-30"
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
 * 子元件：第 1 部 挖空填空
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
        className="my-3.5 font-body text-base font-bold leading-relaxed text-paper-sumi sm:my-4 md:text-lg"
      >
        {quiz.question.split('（　　）').map((part, idx, arr) => (
          <span key={idx}>
            {part}
            {idx < arr.length - 1 && (
              <span className="mx-1 inline-block min-w-[50px] rounded border-b-2 border-paper-sumi bg-paper-butter/80 px-1.5 py-0.5 text-center font-mono text-xs font-black text-[#ff6b35] sm:min-w-[56px] sm:text-sm">
                {hasAnswered ? quiz.options[userChoice - 1] : '（　　）'}
              </span>
            )}
          </span>
        ))}
      </div>

      {/* 選項清單 */}
      <div className="grid grid-cols-1 gap-2 sm:grid-cols-2 md:gap-3">
        {quiz.options.map((opt, optIdx) => {
          const optNum = optIdx + 1;
          const isSelected = userChoice === optNum;
          const isRight = optNum === quiz.correctIndex;

          let optStyle =
            'bg-paper-card border-paper-sumi hover:bg-paper-butter text-paper-sumi';
          if (hasAnswered) {
            if (isRight) {
              optStyle =
                'bg-paper-butter border-2 border-paper-sumi text-paper-sumi font-black shadow-retro-sm';
            } else if (isSelected) {
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
              className={`flex items-center justify-between rounded-xl border-2 p-2.5 text-left font-body text-xs font-bold shadow-retro-sm transition-all sm:p-3 sm:text-sm md:p-3.5 md:text-base ${optStyle}`}
            >
              <div className="flex items-center gap-2">
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

      {/* 詳解 */}
      {hasAnswered && (
        <div className="mt-3.5 rounded-xl border-2 border-paper-sumi bg-paper-canvas p-3 shadow-retro-sm sm:p-3.5 md:p-4">
          <div className="font-display text-xs font-bold text-paper-sumi sm:text-sm md:text-base">
            {isCorrect ? (
              <span>○ 答對了！</span>
            ) : (
              <span>
                ✗ 答錯了，正解為 ({quiz.correctIndex}) {quiz.options[quiz.correctIndex - 1]}
              </span>
            )}
          </div>
          <p className="mt-1 font-body text-xs font-medium leading-relaxed text-paper-sumi/90 sm:mt-1.5 md:text-sm">
            <strong className="font-bold text-paper-sumi">💡 考點解析：</strong>
            {quiz.explanation}
          </p>
        </div>
      )}
    </div>
  );
}

/* ─────────────────────────────────────────────────────────────
 * 子元件：第 2 部 ★ 號排序重組（針對手機排版徹底優化！）
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
  const handleToggleChunk = (chunkNum: number) => {
    if (slots.includes(chunkNum)) {
      onChangeSlots(slots.filter((num) => num !== chunkNum));
    } else {
      if (slots.length >= 4) return;
      onChangeSlots([...slots, chunkNum]);
    }
  };

  const handleRemoveSlot = (slotIdx: number) => {
    const chunkToRemove = slots[slotIdx];
    if (chunkToRemove) {
      onChangeSlots(slots.filter((num) => num !== chunkToRemove));
    }
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

      {/* 題目句子主體：手機版採用「前置句 ➔ 4 欄均分插槽 ➔ 後置句」架構，100% 絕對不跑版！ */}
      <div className="my-3.5 rounded-xl border border-paper-sumi/20 bg-paper-canvas p-3 sm:p-4 md:p-5">
        {quiz.preText && (
          <p lang="ja" className="mb-2 font-body text-sm font-bold text-paper-sumi sm:text-base md:text-lg">
            {quiz.preText}
          </p>
        )}

        {/* 4 個插槽：採用 grid-cols-4 均分，在手機寬度下平整對稱 */}
        <div className="my-2 grid grid-cols-4 gap-1.5 sm:gap-2">
          {[0, 1, 2, 3].map((slotIdx) => {
            const placedChunkNum = slots[slotIdx];
            const isStarSlot = slotIdx === quiz.starIndex;

            return (
              <div
                key={slotIdx}
                onClick={() => placedChunkNum && handleRemoveSlot(slotIdx)}
                className={`flex min-h-[40px] flex-col items-center justify-center rounded border-b-3 px-1 py-1 text-center transition-all sm:min-h-[44px] ${
                  isStarSlot
                    ? 'border-[#ff6b35] bg-[#ffe5a3] text-[#ff6b35] shadow-sm'
                    : 'border-paper-sumi bg-white text-paper-sumi shadow-sm'
                } ${placedChunkNum ? 'cursor-pointer hover:opacity-80 active:scale-95' : 'border-dashed opacity-60'}`}
                title={placedChunkNum ? '點擊可移除此詞塊' : undefined}
              >
                {isStarSlot && (
                  <span className="text-[10px] font-black leading-none text-[#ff6b35]">★</span>
                )}
                {placedChunkNum ? (
                  <span className="break-words font-body text-[11px] font-black leading-tight sm:text-xs md:text-sm">
                    {placedChunkNum}. {quiz.chunks[placedChunkNum - 1]}
                  </span>
                ) : (
                  <span className="font-mono text-xs text-paper-sumi/40">
                    {isStarSlot ? '★ ?' : `${slotIdx + 1}`}
                  </span>
                )}
              </div>
            );
          })}
        </div>

        {quiz.postText && (
          <p lang="ja" className="mt-2 font-body text-sm font-bold text-paper-sumi sm:text-base md:text-lg">
            {quiz.postText}
          </p>
        )}
      </div>

      {/* 詞塊碎片點選區 */}
      <div className="mt-3.5 border-t border-paper-sumi/10 pt-3">
        <div className="flex items-center justify-between">
          <span className="font-display text-xs font-bold text-paper-sumi/70">
            👇 點擊詞塊依序填入（再次點擊可取消）：
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

        {/* 詞塊按鈕：字體不截斷 (break-words)，在手機上自然折行 */}
        <div className="mt-2 grid grid-cols-2 gap-2 sm:grid-cols-4 md:gap-2.5">
          {quiz.chunks.map((chunkText, cIdx) => {
            const chunkNum = cIdx + 1;
            const isUsed = slots.includes(chunkNum);

            return (
              <button
                key={cIdx}
                type="button"
                lang="ja"
                onClick={() => handleToggleChunk(chunkNum)}
                className={`flex items-start gap-1.5 rounded-xl border-2 border-paper-sumi p-2 text-left font-body text-xs font-bold shadow-retro-sm transition-all sm:p-2.5 sm:text-sm md:p-3 ${
                  isUsed
                    ? 'border-paper-sumi/30 bg-paper-oatmeal/70 text-paper-sumi/60 shadow-none'
                    : 'bg-white hover:bg-paper-butter active:translate-y-0.5'
                }`}
                title={isUsed ? '已填入，點擊可取消選取' : '點擊填入橫線'}
              >
                <span className={`flex h-5 w-5 shrink-0 items-center justify-center rounded-full border border-paper-sumi font-mono text-[11px] font-black ${isUsed ? 'bg-paper-sumi/10' : ''}`}>
                  {chunkNum}
                </span>
                <span className="break-words leading-tight">{chunkText}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* 完成驗證回饋卡 */}
      {isCompleted && (
        <div className="mt-3.5 rounded-xl border-2 border-paper-sumi bg-paper-canvas p-3.5 shadow-retro-sm animate-in fade-in duration-150 sm:p-4">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <div className="font-display text-xs font-black text-paper-sumi sm:text-sm md:text-base">
              {isOrderCorrect ? (
                <span>○ 重組順序完全正確！</span>
              ) : (
                <span className="text-paper-sumi/80">
                  順序稍有出入，可點右上「↺ 清空重排」再試一次
                </span>
              )}
            </div>

            {/* ★ 號選項公佈徽章 */}
            <div className="rounded-lg border-2 border-paper-sumi bg-white px-2.5 py-0.5 font-body text-xs font-black shadow-retro-sm sm:px-3 sm:py-1 md:text-sm">
              落在 ★ 號位置的是：
              <span className="text-[#ff6b35]">
                【 {starPlacedNum} 號：{quiz.chunks[starPlacedNum - 1]} 】
              </span>
              {starPlacedNum === starCorrectNum ? '（正確 ✓）' : `（正解應為 ${starCorrectNum} 號）`}
            </div>
          </div>

          <div className="mt-2.5 border-t border-paper-sumi/15 pt-2 sm:mt-3 sm:pt-2.5">
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
            <p className="mt-1 font-body text-xs leading-relaxed text-paper-sumi/90 sm:mt-1.5 md:text-sm">
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
 * 子元件：第 3 部 篇章脈絡填空
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
        <h3 className="font-display text-sm font-black text-paper-sumi sm:text-base md:text-lg">
          📖 {passage.title}
        </h3>
        <span className="rounded border border-paper-sumi/20 bg-paper-oatmeal px-2 py-0.5 font-mono text-[10px] font-bold text-paper-sumi sm:text-[11px]">
          {passage.genre}
        </span>
      </div>

      {/* 篇章閱讀文字框 */}
      <div
        lang="ja"
        className="my-3 max-h-[220px] overflow-y-auto rounded-xl border border-paper-sumi/20 bg-paper-canvas p-3 font-body text-xs font-normal leading-relaxed text-paper-sumi/90 sm:my-4 sm:p-4 sm:text-sm md:text-base md:leading-loose"
      >
        {passage.passage.split(/(【\s*\d+\s*】)/).map((segment, sIdx) => {
          const match = segment.match(/【\s*(\d+)\s*】/);
          if (match) {
            const blankNum = parseInt(match[1], 10);
            const isCurrentBlank = blankNum === subQ.blankNumber;

            return (
              <span
                key={sIdx}
                className={`mx-0.5 inline-flex items-center justify-center rounded border px-1.5 py-0.5 align-middle font-body text-[11px] font-black shadow-sm sm:mx-1 sm:px-2 sm:text-xs ${
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
      <div className="mb-2.5">
        <button
          type="button"
          onClick={() => setShowTranslation((v) => !v)}
          className="font-mono text-xs font-bold text-paper-sumi/60 hover:text-[#ff6b35]"
        >
          {showTranslation ? '▲ 收合中文翻譯' : '▼ 展開中日對照全文翻譯'}
        </button>
        {showTranslation && (
          <div className="mt-2 rounded-lg border border-paper-sumi/20 bg-paper-canvas p-2.5 font-body text-xs leading-relaxed text-paper-sumi/80 sm:p-3">
            {passage.translation}
          </div>
        )}
      </div>

      {/* 本題選項 */}
      <div className="border-t border-paper-sumi/10 pt-2.5">
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
                btnStyle =
                  'bg-paper-butter border-2 border-paper-sumi text-paper-sumi font-black shadow-retro-sm';
              } else if (isSelected) {
                btnStyle =
                  'bg-paper-oatmeal border border-paper-sumi/40 text-paper-sumi/60 line-through';
              } else {
                btnStyle = 'bg-paper-card border-paper-sumi/20 opacity-40 shadow-none';
              }
            }

            return (
              <button
                key={optIdx}
                type="button"
                lang="ja"
                disabled={hasAnswered}
                onClick={() => onSelect(optNum)}
                className={`flex items-center justify-between rounded-xl border-2 p-2.5 text-left font-body text-xs font-bold shadow-retro-sm transition-all sm:text-sm md:p-3 ${btnStyle}`}
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
          <div className="mt-3 rounded-lg border-2 border-paper-sumi bg-paper-canvas p-2.5 font-body text-xs leading-relaxed text-paper-sumi shadow-retro-sm sm:p-3 md:text-sm">
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
