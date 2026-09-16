import { useParams } from 'react-router-dom';
import type { Level } from '../data/types';
import { LEVEL_LABELS, isLevel } from '../data/meta';
import { useLessonSet } from '../hooks/useLessonSet';
import { useDocumentTitle } from '../hooks/useDocumentTitle';
import { ComingSoon } from '../components/ComingSoon';
import { QuizCard } from '../components/QuizCard';
import { LoadingState, ErrorState } from '../components/StatusStates';
import { NotFoundPage } from './NotFoundPage';

export function QuizLevelPage() {
  const { level } = useParams();
  if (!isLevel(level)) return <NotFoundPage />;
  return <QuizLevelContent level={level} />;
}

function QuizLevelContent({ level }: { level: Level }) {
  const state = useLessonSet('quiz', level);
  const levelLabel = LEVEL_LABELS[level];
  useDocumentTitle(`${levelLabel} 練習題`);

  if (state.status === 'unavailable') return <ComingSoon section="quiz" level={level} />;
  if (state.status === 'loading') return <LoadingState />;
  if (state.status === 'error' || !state.data) return <ErrorState />;

  const lessons = [...state.data].sort((a, b) => a.lesson_number - b.lesson_number);

  return (
    <div>
      <header className="rounded-xl border-3 border-paper-sumi bg-level-tint px-5 py-6 shadow-retro md:px-10 md:py-10">
        <h1 className="font-display text-3xl font-black md:text-5xl">
          <span className="mr-3 inline-block rounded-lg border-2 border-paper-sumi bg-level px-2.5 py-0.5 text-paper-card md:px-3 md:py-1">
            {levelLabel}
          </span>
          練習題
        </h1>
        <p className="mt-3 font-mono text-xs text-paper-sumi/70 md:mt-4 md:text-sm">
          全 {lessons.length} 課・共 {lessons.reduce((n, l) => n + l.quizzes.length, 0)} 題
        </p>
      </header>

      <div className="mt-10 flex flex-col gap-6">
        {lessons.map((lesson) => (
          <details key={lesson.lesson_number} className="group">
            <summary className="card-lift flex cursor-pointer list-none items-center justify-between rounded-xl border-2 border-paper-sumi bg-paper-card p-4 shadow-retro md:p-5">
              <span className="font-display text-base font-bold md:text-xl">
                第 {lesson.lesson_number} 課・{lesson.lesson_title}
              </span>
              <span className="font-mono text-xs text-paper-sumi/60">
                {lesson.quizzes.length} 題
                <span aria-hidden="true" className="ml-2 inline-block transition-transform group-open:rotate-90">
                  ›
                </span>
              </span>
            </summary>
            <div className="mt-3 flex flex-col gap-4">
              {lesson.quizzes.map((quiz, i) => (
                <QuizCard key={quiz.question_id} quiz={quiz} index={i} />
              ))}
            </div>
          </details>
        ))}
      </div>
    </div>
  );
}
