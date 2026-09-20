import { Link, useParams } from 'react-router-dom';
import type { Level } from '../data/types';
import { LEVEL_LABELS, isLevel } from '../data/meta';
import { useLessonSet } from '../hooks/useLessonSet';
import { useDocumentTitle } from '../hooks/useDocumentTitle';
import { ComingSoon } from '../components/ComingSoon';
import { LessonCard } from '../components/LessonCard';
import { LoadingState, ErrorState } from '../components/StatusStates';
import { NotFoundPage } from './NotFoundPage';

export function GrammarLevelPage() {
  const { level } = useParams();
  if (!isLevel(level)) return <NotFoundPage />;
  return <GrammarLevelContent level={level} />;
}

function GrammarLevelContent({ level }: { level: Level }) {
  const state = useLessonSet('grammar', level);
  const levelLabel = LEVEL_LABELS[level];
  useDocumentTitle(`${levelLabel} 文法`);

  if (state.status === 'unavailable') return <ComingSoon section="grammar" level={level} />;
  if (state.status === 'loading') return <LoadingState />;
  if (state.status === 'error' || !state.data) return <ErrorState />;

  const lessons = [...state.data].sort((a, b) => a.lesson_number - b.lesson_number);

  return (
    <div>
      {/* 級別大標色塊 */}
      <header className="rounded-xl border-3 border-paper-sumi bg-level-tint px-5 py-6 shadow-retro md:px-10 md:py-10">
        <h1 className="font-display text-3xl font-black md:text-5xl">
          <span className="mr-3 inline-block rounded-lg border-2 border-paper-sumi bg-level px-2.5 py-0.5 text-paper-card md:px-3 md:py-1">
            {levelLabel}
          </span>
          文法
        </h1>
        <p className="mt-3 font-mono text-xs text-paper-sumi/70 md:mt-4 md:text-sm">
          全 {lessons.length} 課・共 {lessons.reduce((n, l) => n + l.grammar_points.length, 0)} 個文法點
        </p>

        <div className="mt-5 flex flex-wrap items-center justify-between gap-3 rounded-xl border-2 border-paper-sumi bg-paper-card p-3.5 shadow-retro-sm md:p-4">
          <div className="text-left">
            <span className="inline-block rounded bg-level px-2 py-0.5 font-display text-xs font-bold text-paper-card">
              考場速查手冊
            </span>
            <p className="mt-1 text-xs font-bold md:text-sm">
              想要帶紙本進考場？下載《{levelLabel} 文法公式＆必考陷阱速查手冊（A4 可列印）＋ Anki 記憶卡》
            </p>
          </div>
          <div className="flex flex-wrap items-center gap-2">
            <Link
              to="/products"
              className="btn-retro text-xs md:text-sm"
            >
              👀 線上試玩字卡 ＆ 預覽手冊 →
            </Link>
            <a
              href="https://buymeacoffee.com/chiaoban/shop"
              target="_blank"
              rel="noreferrer"
              className="btn-retro bg-paper-butter text-xs md:text-sm"
            >
              🛒 立即購買 {levelLabel} 套組
            </a>
          </div>
        </div>
      </header>

      <div className="mt-6 grid grid-cols-1 gap-4 md:mt-10 md:grid-cols-2 md:gap-6 lg:grid-cols-3">
        {lessons.map((lesson) => (
          <LessonCard
            key={lesson.lesson_number}
            lesson={lesson}
            to={`/grammar/${level}/${lesson.lesson_number}`}
            countLabel={`${lesson.grammar_points.length} 個文法點`}
          />
        ))}
      </div>
    </div>
  );
}
