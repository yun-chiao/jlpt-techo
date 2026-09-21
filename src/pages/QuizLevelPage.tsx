import { useState, useMemo } from 'react';
import { useParams, Link } from 'react-router-dom';
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
  const [showGraduationModal, setShowGraduationModal] = useState(false);
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

  // 作答統計（必須在所有條件 return 之前宣告，遵循 React Hook 規則）
  const answeredCount = useMemo(() => {
    let count = 0;
    allQuestions.forEach((q) => {
      if (q.type === 'sentence' && sentenceAnswers[q.id] !== undefined) count++;
      if (q.type === 'star' && (starSlots[q.id]?.length ?? 0) === 4) count++;
      if (q.type === 'passage' && passageAnswers[q.id] !== undefined) count++;
    });
    return count;
  }, [allQuestions, sentenceAnswers, starSlots, passageAnswers]);

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
    <div className="flex flex-col gap-3 sm:gap-4 md:gap-5">
      {/* 頂部整合式控制列（手機端極致精簡：級別 + 題庫標題 + Stepper 一應俱全，零空間浪費） */}
      <div className="flex flex-col gap-2.5">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="rounded-md border-1.5 border-paper-sumi bg-level px-2 py-0.5 font-mono text-xs font-black text-white shadow-retro-sm">
              {levelLabel}
            </span>
            <h1 className="font-display text-sm font-black text-paper-sumi sm:text-lg">
              題型專攻・三部曲
            </h1>
            <span className="hidden font-mono text-xs text-paper-sumi/60 sm:inline">
              ・精華特訓 {allQuestions.length} 題（已作答 {answeredCount} 題）
            </span>
          </div>

          {/* Stepper 控制群組 */}
          <div className="inline-flex h-7 items-stretch rounded-lg border-2 border-paper-sumi bg-paper-card shadow-retro-sm sm:h-8">
            {/* 左箭頭 */}
            <button
              type="button"
              disabled={safeIdx === 0}
              onClick={handlePrev}
              className="flex w-7 items-center justify-center border-r border-paper-sumi/25 text-paper-sumi/80 transition-colors hover:bg-paper-butter disabled:cursor-not-allowed disabled:opacity-20 disabled:hover:bg-transparent"
              title="上一題"
            >
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                <polyline points="15 18 9 12 15 6" />
              </svg>
            </button>

            {/* 題號與展開箭頭 */}
            <button
              type="button"
              onClick={() => setShowJumpPanel((v) => !v)}
              className="flex items-center gap-1.5 px-2.5 font-mono text-xs font-black text-paper-sumi transition-colors hover:bg-paper-butter sm:px-3"
              title="點擊展開快速跳題面板"
            >
              <span>Q.{String(safeIdx + 1).padStart(2, '0')}</span>
              <span className="text-paper-sumi/35">/</span>
              <span className="text-paper-sumi/60">{String(filteredQuestions.length).padStart(2, '0')}</span>
              <svg width="9" height="9" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" className="text-paper-sumi/60" aria-hidden="true">
                <polyline points="6 9 12 15 18 9" />
              </svg>
            </button>

            {/* 右箭頭 */}
            <button
              type="button"
              disabled={safeIdx === filteredQuestions.length - 1}
              onClick={handleNext}
              className="flex w-7 items-center justify-center border-l border-paper-sumi/25 text-paper-sumi/80 transition-colors hover:bg-paper-butter disabled:cursor-not-allowed disabled:opacity-20 disabled:hover:bg-transparent"
              title="下一題"
            >
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                <polyline points="9 18 15 12 9 6" />
              </svg>
            </button>
          </div>
        </div>

        {/* 分類篩選 Tab（日雜 Pill 風格） */}
        <div className="flex items-center gap-1.5 overflow-x-auto pb-0.5 scrollbar-none">
          <button
            type="button"
            onClick={() => handleSwitchFilter('all')}
            className={`inline-flex h-7 shrink-0 items-center rounded-full px-3 font-mono text-xs transition-all ${
              filter === 'all'
                ? 'bg-paper-sumi text-white font-black shadow-retro-sm'
                : 'bg-paper-oatmeal/80 text-paper-sumi/80 font-bold hover:bg-paper-butter'
            }`}
          >
            全部 ({allQuestions.length})
          </button>
          <button
            type="button"
            onClick={() => handleSwitchFilter('sentence')}
            className={`inline-flex h-7 shrink-0 items-center rounded-full px-3 font-mono text-xs transition-all ${
              filter === 'sentence'
                ? 'bg-paper-sumi text-white font-black shadow-retro-sm'
                : 'bg-paper-oatmeal/80 text-paper-sumi/80 font-bold hover:bg-paper-butter'
            }`}
          >
            ① 挖空 ({sentenceCount})
          </button>
          <button
            type="button"
            onClick={() => handleSwitchFilter('star')}
            className={`inline-flex h-7 shrink-0 items-center rounded-full px-3 font-mono text-xs transition-all ${
              filter === 'star'
                ? 'bg-paper-sumi text-white font-black shadow-retro-sm'
                : 'bg-paper-oatmeal/80 text-paper-sumi/80 font-bold hover:bg-paper-butter'
            }`}
          >
            ② ★重組 ({starCount})
          </button>
          <button
            type="button"
            onClick={() => handleSwitchFilter('passage')}
            className={`inline-flex h-7 shrink-0 items-center rounded-full px-3 font-mono text-xs transition-all ${
              filter === 'passage'
                ? 'bg-paper-sumi text-white font-black shadow-retro-sm'
                : 'bg-paper-oatmeal/80 text-paper-sumi/80 font-bold hover:bg-paper-butter'
            }`}
          >
            ③ 篇章 ({passageCount})
          </button>
        </div>
      </div>

      {/* 展開式快速跳題面板 */}
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

          {/* 抽屜底部：iPad / 列印版手帳題本連結 */}
          <div className="mt-3 flex flex-wrap items-center justify-between gap-2 border-t border-paper-sumi/15 pt-2 font-mono text-xs">
            <div className="flex items-center gap-2 text-paper-sumi/70">
              <span>官方免費特訓（已完成 {answeredCount} / {filteredQuestions.length} 題）</span>
              {answeredCount > 0 && (
                <button
                  type="button"
                  onClick={() => {
                    setShowJumpPanel(false);
                    setShowGraduationModal(true);
                  }}
                  className="font-bold text-[#ff6b35] underline decoration-1 underline-offset-2 hover:text-paper-sumi"
                >
                  🏆 查看成績證書
                </button>
              )}
            </div>
            <Link
              to={`/products?tab=quiz&level=${level}`}
              className="font-bold text-paper-sumi hover:text-[#ff6b35] underline decoration-paper-sumi/30 underline-offset-2"
            >
              📥 解鎖完整 500 題手帳題本（含 350 題獨家進階題）→
            </Link>
          </div>
        </div>
      )}

      {/* 日雜手帳風：PDF 題本下載隨身條（極致美感、零打擾、文青手帳質感） */}
      <div className="flex flex-wrap items-center justify-between gap-2.5 rounded-xl border border-paper-sumi/25 bg-paper-canvas px-3.5 py-2.5 shadow-retro-sm">
        <div className="flex items-center gap-2">
          <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full border border-paper-sumi bg-paper-butter font-mono text-xs font-black">
            ✎
          </span>
          <p className="font-display text-xs font-black text-paper-sumi sm:text-sm">
            想刷更多題目？<span className="hidden sm:inline">可解鎖</span>《{levelLabel} 500 題完整題本・含 350 題獨家題與手寫詳解》
          </p>
          <span className="hidden rounded bg-paper-oatmeal px-1.5 py-0.5 font-mono text-[10px] font-bold text-paper-sumi/70 md:inline">
            A4 列印 ＋ iPad 手帳
          </span>
        </div>
        <Link
          to={`/products?tab=quiz&level=${level}`}
          className="inline-flex shrink-0 items-center gap-1.5 rounded-lg border-1.5 border-paper-sumi bg-paper-butter px-3 py-1 font-mono text-xs font-black text-paper-sumi shadow-retro-sm transition-all hover:bg-paper-sumi hover:text-white active:scale-95"
        >
          <span>📥 前往解鎖 500 題</span>
          <span className="font-mono">→</span>
        </Link>
      </div>

      {/* 核心作答卡片（border-2 + shadow-retro-sm 輕盈化，拒絕厚重囚籠感） */}
      {activeQuestion && (
        <div className="rounded-2xl border-2 border-paper-sumi bg-white p-4 shadow-retro-sm sm:p-6 md:p-7">
          {/* 卡片頂部標籤 */}
          <div className="flex items-center justify-between border-b border-paper-sumi/10 pb-2.5">
            <div className="flex items-center gap-1.5 font-mono text-xs font-bold text-paper-sumi">
              <span className="text-[#ff6b35]">
                {activeQuestion.type === 'sentence' && 'PART 01'}
                {activeQuestion.type === 'star' && 'PART 02'}
                {activeQuestion.type === 'passage' && 'PART 03'}
              </span>
              <span className="text-paper-sumi/25">/</span>
              <span className="font-display text-paper-sumi/80">
                {activeQuestion.type === 'sentence' && '文法形式挖空'}
                {activeQuestion.type === 'star' && '★ 號排序重組'}
                {activeQuestion.type === 'passage' && '篇章脈絡填空'}
              </span>
            </div>

            {activeQuestion.type === 'sentence' && activeQuestion.data.targetGrammar && sentenceAnswers[activeQuestion.id] !== undefined ? (
              <span className="shrink-0 max-w-[170px] truncate font-mono text-[11px] text-paper-sumi/60 sm:max-w-none">
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
          <div className="mt-5 flex items-center justify-between border-t border-paper-sumi/10 pt-3">
            <button
              type="button"
              disabled={safeIdx === 0}
              onClick={handlePrev}
              className="rounded-lg border border-paper-sumi/25 bg-paper-card px-3 py-1.5 font-mono text-xs font-bold text-paper-sumi hover:bg-paper-butter disabled:opacity-20"
            >
              ← PREV
            </button>
            <div className="flex items-center gap-2">
              <span className="font-mono text-xs font-bold text-paper-sumi/50">
                {String(safeIdx + 1).padStart(2, '0')} / {String(filteredQuestions.length).padStart(2, '0')}
              </span>
              {safeIdx === filteredQuestions.length - 1 && (
                <button
                  type="button"
                  onClick={() => setShowGraduationModal(true)}
                  className="animate-pulse rounded-md border border-paper-sumi bg-paper-butter px-2 py-0.5 font-mono text-[11px] font-black text-paper-sumi shadow-retro-sm hover:bg-paper-sumi hover:text-white"
                >
                  🏆 通關總結
                </button>
              )}
            </div>
            {safeIdx === filteredQuestions.length - 1 ? (
              <button
                type="button"
                onClick={() => setShowGraduationModal(true)}
                className="rounded-lg border-2 border-paper-sumi bg-paper-butter px-3.5 py-1.5 font-mono text-xs font-black text-paper-sumi shadow-retro-sm hover:translate-x-[-1px] hover:translate-y-[-1px]"
              >
                🎉 查看通關證書 →
              </button>
            ) : (
              <button
                type="button"
                onClick={handleNext}
                className="rounded-lg border-2 border-paper-sumi bg-paper-butter px-3.5 py-1.5 font-mono text-xs font-black text-paper-sumi shadow-retro-sm hover:translate-x-[-1px] hover:translate-y-[-1px]"
              >
                NEXT →
              </button>
            )}
          </div>
        </div>
      )}

      {/* 🏆 通關證書與轉化彈窗 (Graduation Modal) */}
      {showGraduationModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-paper-sumi/60 p-3 backdrop-blur-sm sm:p-4 overflow-y-auto">
          <div className="relative w-full max-w-lg rounded-2xl border-3 border-paper-sumi bg-paper-canvas p-5 shadow-retro-lg sm:p-7 animate-in fade-in zoom-in-95 duration-200">
            {/* 關閉叉叉 */}
            <button
              type="button"
              onClick={() => setShowGraduationModal(false)}
              className="absolute right-3.5 top-3.5 flex h-7 w-7 items-center justify-center rounded-full border border-paper-sumi/30 bg-white font-mono text-xs font-bold text-paper-sumi hover:bg-paper-butter"
            >
              ✕
            </button>

            {/* 證書頂部標章 */}
            <div className="text-center">
              <div className="inline-flex items-center gap-1.5 rounded-full border border-paper-sumi bg-paper-butter px-3 py-0.5 font-mono text-xs font-black text-paper-sumi shadow-retro-sm">
                <span>🏆</span>
                <span>CERTIFICATE OF COMPLETION</span>
              </div>
              <h2 className="mt-2.5 font-serif text-xl font-black text-paper-sumi sm:text-2xl">
                《日檢手帖》{levelLabel} 精華特訓修了証
              </h2>
              <p className="mt-1 font-mono text-xs text-paper-sumi/60">
                JLPT {level.toUpperCase()} CORE CURRICULUM・150 QUESTIONS COMPLETED
              </p>
            </div>

            {/* 證書中央內容框 */}
            <div className="mt-4 rounded-xl border-2 border-paper-sumi bg-white p-4 shadow-retro-sm">
              <div className="flex items-center justify-between border-b border-dashed border-paper-sumi/20 pb-2.5 text-xs font-mono">
                <span className="text-paper-sumi/70">特訓科目：言語知識（文法三部曲）</span>
                <span className="rounded bg-[#FAF7F2] px-2 py-0.5 font-black text-[#ff6b35]">合格判定：S級</span>
              </div>

              {/* 戰績三欄 */}
              <div className="my-3 grid grid-cols-3 gap-2 text-center font-mono">
                <div className="rounded-lg border border-paper-sumi/15 bg-paper-canvas p-2">
                  <div className="text-[10px] text-paper-sumi/60">Part 1 挖空</div>
                  <div className="text-sm font-black text-paper-sumi sm:text-base">90 題</div>
                </div>
                <div className="rounded-lg border border-paper-sumi/15 bg-paper-canvas p-2">
                  <div className="text-[10px] text-paper-sumi/60">Part 2 重組</div>
                  <div className="text-sm font-black text-paper-sumi sm:text-base">42 題</div>
                </div>
                <div className="rounded-lg border border-paper-sumi/15 bg-paper-canvas p-2">
                  <div className="text-[10px] text-paper-sumi/60">Part 3 篇章</div>
                  <div className="text-sm font-black text-paper-sumi sm:text-base">18 題</div>
                </div>
              </div>

              <p className="font-body text-xs leading-relaxed text-paper-sumi/85">
                🎉 <strong>恭喜通關！</strong> 您已成功完成本站 150 題全真核心特訓，針對 {levelLabel} 核心文法架構與考場常考句型，已具備極高的直覺題感！
              </p>
            </div>

            {/* 商業轉化引導區塊 */}
            <div className="mt-4 rounded-xl border-2 border-dashed border-[#ff6b35] bg-[#fffaf5] p-3.5 text-xs">
              <div className="flex items-center gap-1.5 font-display font-black text-[#ff6b35]">
                <span>👑</span>
                <span>想在考場拿下文法滿分？解鎖進階 350 題獨家真題！</span>
              </div>
              <p className="mt-1.5 leading-relaxed text-paper-sumi/80">
                網頁版僅收錄 150 題精華題。正式出版的<strong>《{levelLabel} 500 題厚切全真手帳題本》</strong>多收錄了 <strong>350 題獨家進階考點</strong>，並提供：
              </p>
              <ul className="mt-2 space-y-1 font-mono text-[11px] text-paper-sumi/75">
                <li>✓ <strong>實戰純題空白手寫本</strong>（iPad GoodNotes 向量手寫 / A4 列印無干擾）</li>
                <li>✓ <strong>逐題手寫風詳解神手帳</strong>（500 題完整解析、句型拆解與錯題筆記欄）</li>
                <li>✓ <strong>卷末 Answer Key 快速答案卡</strong>（考前 30 分鐘複習利器）</li>
              </ul>
            </div>

            {/* 動作按鈕 */}
            <div className="mt-4 flex flex-col gap-2 sm:flex-row sm:items-center">
              <Link
                to={`/products?tab=quiz&level=${level}`}
                className="btn-retro flex flex-1 items-center justify-center gap-1.5 bg-paper-butter py-2.5 text-center font-display text-xs font-black text-paper-sumi shadow-retro sm:text-sm"
              >
                <span>🛒 前往解鎖完整 500 題題本套組</span>
                <span className="font-mono">→</span>
              </Link>
              <button
                type="button"
                onClick={() => setShowGraduationModal(false)}
                className="rounded-xl border border-paper-sumi/30 bg-white px-4 py-2.5 font-mono text-xs font-bold text-paper-sumi/70 hover:bg-paper-canvas sm:shrink-0"
              >
                關閉證書
              </button>
            </div>
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
        className="my-3 font-serif text-base font-bold leading-relaxed text-paper-sumi sm:my-4 sm:text-lg sm:leading-loose"
      >
        {quiz.question.split('（　　）').map((part, idx, arr) => (
          <span key={idx}>
            {part}
            {idx < arr.length - 1 && (
              <span
                className={`mx-1 inline-block min-w-[3.5rem] rounded border-b-2 px-2 py-0.5 text-center font-serif text-sm font-bold transition-all sm:text-base ${
                  hasAnswered
                    ? 'border-paper-sumi bg-paper-butter text-paper-sumi'
                    : 'border-paper-sumi/40 bg-paper-oatmeal/50 text-paper-sumi/40'
                }`}
              >
                {hasAnswered ? quiz.options[userChoice - 1] : '（　　）'}
              </span>
            )}
          </span>
        ))}
      </div>

      {/* 選項清單 */}
      <div className="grid grid-cols-1 gap-2 sm:grid-cols-2 md:gap-2.5">
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
                'bg-paper-oatmeal/70 border border-paper-sumi/30 text-paper-sumi/50 line-through';
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
              className={`flex items-center justify-between rounded-xl border-2 p-2.5 text-left font-serif text-xs font-bold shadow-retro-sm transition-all sm:p-3 sm:text-sm md:text-base ${optStyle}`}
            >
              <div className="flex items-center gap-2">
                <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full border border-current font-mono text-xs font-black">
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
        <div className="mt-3.5 rounded-xl border-2 border-paper-sumi bg-paper-canvas p-3 text-xs leading-relaxed text-paper-sumi shadow-retro-sm sm:p-3.5 sm:text-sm">
          <div className="font-display font-bold">
            {isCorrect ? (
              <span>○ 答對了！</span>
            ) : (
              <span>
                ✗ 答錯了，正解為 ({quiz.correctIndex}) {quiz.options[quiz.correctIndex - 1]}
              </span>
            )}
          </div>
          <p className="mt-1 font-body text-paper-sumi/90">
            <strong className="font-bold text-paper-sumi">💡 考點解析：</strong>
            {quiz.explanation}
          </p>
        </div>
      )}
    </div>
  );
}

/* ─────────────────────────────────────────────────────────────
 * 子元件：第 2 部 ★ 號排序重組（全真考卷自然整句流動）
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
      <p className="font-body text-xs text-paper-sumi/65">
        點選下方 4 個詞塊填入橫線，找出落在 <strong className="font-bold text-[#ff6b35]">★ 號位置</strong> 的選項：
      </p>

      {/* 題目全句自然流動框（宛如真實考卷，前置句 + 4 插槽 + 後置句渾然一體） */}
      <div className="my-3 rounded-xl border border-paper-sumi/20 bg-paper-canvas p-3.5 leading-loose sm:my-4 sm:p-5">
        <div lang="ja" className="font-serif text-base font-bold text-paper-sumi sm:text-lg sm:leading-loose">
          {quiz.preText && <span className="mr-1">{quiz.preText}</span>}

          {/* 4 個詞塊插槽，自然融入句中 inline 排版 */}
          {[0, 1, 2, 3].map((slotIdx) => {
            const placedChunkNum = slots[slotIdx];
            const isStarSlot = slotIdx === quiz.starIndex;

            if (placedChunkNum) {
              return (
                <button
                  key={slotIdx}
                  type="button"
                  onClick={() => handleRemoveSlot(slotIdx)}
                  title="點擊撤回此詞塊"
                  className={`mx-1 inline-flex items-center gap-1 rounded-md border-b-2 px-2 py-0.5 align-baseline font-serif text-xs font-black shadow-sm transition-all sm:text-sm active:scale-95 ${
                    isStarSlot
                      ? 'border-[#ff6b35] bg-[#ffe5a3] text-paper-sumi ring-2 ring-[#ff6b35]/40'
                      : 'border-paper-sumi bg-white text-paper-sumi'
                  }`}
                >
                  {isStarSlot && <span className="font-mono text-[11px] text-[#ff6b35]">★</span>}
                  <span className="font-mono text-[11px] text-paper-sumi/50">{placedChunkNum}.</span>
                  <span>{quiz.chunks[placedChunkNum - 1]}</span>
                </button>
              );
            }

            return (
              <span
                key={slotIdx}
                className={`mx-1 inline-flex h-6 min-w-[42px] items-center justify-center rounded border-b-2 px-1 align-baseline font-mono text-xs font-bold transition-all sm:min-w-[50px] ${
                  isStarSlot
                    ? 'border-[#ff6b35] bg-[#ffe5a3]/50 text-[#ff6b35]'
                    : 'border-paper-sumi/30 bg-paper-oatmeal/40 text-paper-sumi/40'
                }`}
              >
                {isStarSlot ? '★ ＿＿' : `${slotIdx + 1} ＿＿`}
              </span>
            );
          })}

          {quiz.postText && <span className="ml-1">{quiz.postText}</span>}
        </div>
      </div>

      {/* 詞塊點選區 */}
      <div className="mt-3">
        <div className="flex items-center justify-between">
          <span className="font-display text-xs font-bold text-paper-sumi/70">
            請點擊詞塊依序填入（點擊已填詞塊可撤回）：
          </span>
          {slots.length > 0 && (
            <button
              type="button"
              onClick={handleReset}
              className="flex items-center gap-1 rounded-md border border-paper-sumi/20 bg-paper-oatmeal px-2 py-0.5 font-mono text-xs font-bold text-paper-sumi/70 hover:bg-paper-butter"
            >
              <span>↺</span>
              <span>重排</span>
            </button>
          )}
        </div>

        {/* 4 個詞塊按鈕（日雜卡片風格） */}
        <div className="mt-2 grid grid-cols-2 gap-2 sm:grid-cols-4 sm:gap-2.5">
          {quiz.chunks.map((chunkText, cIdx) => {
            const chunkNum = cIdx + 1;
            const isUsed = slots.includes(chunkNum);

            return (
              <button
                key={cIdx}
                type="button"
                lang="ja"
                onClick={() => handleToggleChunk(chunkNum)}
                className={`flex items-start gap-1.5 rounded-xl border-2 p-2.5 text-left font-serif text-xs font-bold shadow-retro-sm transition-all sm:text-sm ${
                  isUsed
                    ? 'border-paper-sumi/20 bg-paper-oatmeal/60 text-paper-sumi/40 shadow-none line-through'
                    : 'border-paper-sumi bg-white hover:bg-paper-butter active:translate-y-0.5'
                }`}
                title={isUsed ? '已填入，點擊可取消' : '點擊填入橫線'}
              >
                <span className={`flex h-5 w-5 shrink-0 items-center justify-center rounded-full border border-paper-sumi font-mono text-[11px] font-black ${isUsed ? 'bg-paper-sumi/10 border-paper-sumi/40' : ''}`}>
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
        <div className="mt-3.5 rounded-xl border-2 border-paper-sumi bg-paper-canvas p-3 text-xs leading-relaxed text-paper-sumi shadow-retro-sm sm:p-4 sm:text-sm">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <div className="font-display font-bold">
              {isOrderCorrect ? (
                <span>○ 重組順序完全正確！</span>
              ) : (
                <span className="text-paper-sumi/80">
                  順序稍有出入，可點右上「↺ 重排」再試一次
                </span>
              )}
            </div>

            {/* ★ 號選項公佈徽章 */}
            <div className="rounded-lg border-2 border-paper-sumi bg-white px-2.5 py-0.5 font-body text-xs font-black shadow-retro-sm">
              落在 ★ 號位置的是：
              <span className="text-[#ff6b35]">
                【 {starPlacedNum} 號：{quiz.chunks[starPlacedNum - 1]} 】
              </span>
              {starPlacedNum === starCorrectNum ? '（正確 ✓）' : `（正解應為 ${starCorrectNum} 號）`}
            </div>
          </div>

          <div className="mt-2.5 border-t border-paper-sumi/15 pt-2">
            <p className="font-body font-medium">
              <strong className="font-bold">正確完整句：</strong>
              <span lang="ja" className="ml-1 font-serif font-bold text-paper-sumi">
                {quiz.fullSentence}
              </span>
            </p>
            <p className="mt-1 font-body text-paper-sumi/80">
              <strong className="font-bold">中文對照：</strong>
              {quiz.translation}
            </p>
            <p className="mt-1 font-body text-paper-sumi/90">
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
      <div className="flex items-start justify-between gap-2.5">
        <h3 className="min-w-0 flex-1 font-display text-sm font-black leading-snug text-paper-sumi sm:text-base md:text-lg">
          📖 {passage.title}
        </h3>
        <span className="shrink-0 whitespace-nowrap rounded border border-paper-sumi/20 bg-paper-oatmeal px-2 py-0.5 font-mono text-[10px] font-bold text-paper-sumi sm:text-[11px]">
          {passage.genre}
        </span>
      </div>

      {/* 篇章閱讀文字框 */}
      <div
        lang="ja"
        className="my-3 max-h-[200px] overflow-y-auto rounded-xl border border-paper-sumi/20 bg-paper-canvas p-3.5 font-serif text-xs leading-relaxed text-paper-sumi/90 sm:my-4 sm:p-4 sm:text-sm sm:leading-loose md:text-base"
      >
        {passage.passage.split(/(【\s*\d+\s*】)/).map((segment, sIdx) => {
          const match = segment.match(/【\s*(\d+)\s*】/);
          if (match) {
            const blankNum = parseInt(match[1], 10);
            const isCurrentBlank = blankNum === subQ.blankNumber;

            return (
              <span
                key={sIdx}
                className={`mx-0.5 inline-flex items-center justify-center rounded border px-1.5 py-0.5 align-middle font-mono text-[11px] font-black shadow-sm sm:mx-1 sm:px-2 sm:text-xs ${
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
                  'bg-paper-oatmeal/70 border border-paper-sumi/30 text-paper-sumi/50 line-through';
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
                className={`flex items-center justify-between rounded-xl border-2 p-2.5 text-left font-serif text-xs font-bold shadow-retro-sm transition-all sm:p-3 sm:text-sm md:text-base ${btnStyle}`}
              >
                <div className="flex items-center gap-2">
                  <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full border border-current font-mono text-xs font-black">
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
