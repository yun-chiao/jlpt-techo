import { useParams } from 'react-router-dom';
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
