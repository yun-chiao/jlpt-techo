import { useEffect, useState } from 'react';
import { Link, NavLink, useParams } from 'react-router-dom';
import type { Level, Lesson } from '../data/types';
import { LEVEL_LABELS, isLevel } from '../data/meta';
import { useLessonSet } from '../hooks/useLessonSet';
import { useDocumentTitle } from '../hooks/useDocumentTitle';
import { ComingSoon } from '../components/ComingSoon';
import { Breadcrumb } from '../components/Breadcrumb';
import { GrammarPointCard } from '../components/GrammarPointCard';
import { QuizCard } from '../components/QuizCard';
import { LoadingState, ErrorState } from '../components/StatusStates';
import { NotFoundPage } from './NotFoundPage';

export function GrammarLessonPage() {
  const { level, lessonNumber, pointNumber } = useParams();
  if (!isLevel(level) || !lessonNumber || !/^\d+$/.test(lessonNumber)) return <NotFoundPage />;
  if (pointNumber !== undefined && !/^\d+$/.test(pointNumber)) return <NotFoundPage />;
  return (
    <GrammarLessonContent
      level={level}
      lessonNumber={Number(lessonNumber)}
      pointNumber={pointNumber ? Number(pointNumber) : 1}
    />
  );
}

function GrammarLessonContent({
  level,
  lessonNumber,
  pointNumber,
}: {
  level: Level;
  lessonNumber: number;
  pointNumber: number;
}) {
  const state = useLessonSet('grammar', level);

  if (state.status === 'unavailable') return <ComingSoon section="grammar" level={level} />;
  if (state.status === 'loading') return <LoadingState />;
  if (state.status === 'error' || !state.data) return <ErrorState />;

  const lessons = [...state.data].sort((a, b) => a.lesson_number - b.lesson_number);
  const index = lessons.findIndex((l) => l.lesson_number === lessonNumber);
  if (index === -1) return <NotFoundPage />;

  const lesson = lessons[index];
  if (pointNumber < 1 || pointNumber > lesson.grammar_points.length) return <NotFoundPage />;

  return (
    <PointView
      level={level}
      lesson={lesson}
      pointIndex={pointNumber - 1}
      prevLesson={index > 0 ? lessons[index - 1] : null}
      nextLesson={index < lessons.length - 1 ? lessons[index + 1] : null}
    />
  );
}

interface PointViewProps {
  level: Level;
  lesson: Lesson;
  pointIndex: number;
  prevLesson: Lesson | null;
  nextLesson: Lesson | null;
}

function PointView({ level, lesson, pointIndex, prevLesson, nextLesson }: PointViewProps) {
  const levelLabel = LEVEL_LABELS[level];
  const [tocOpen, setTocOpen] = useState(false);
  const point = lesson.grammar_points[pointIndex];
  const total = lesson.grammar_points.length;

  useDocumentTitle(
    `第 ${lesson.lesson_number} 課 ${lesson.lesson_title}・文法點 ${pointIndex + 1}｜${levelLabel} 文法`,
  );

  // 切換文法點時回到頁面頂端
  useEffect(() => {
    window.scrollTo(0, 0);
    setTocOpen(false);
  }, [lesson.lesson_number, pointIndex]);

  const pointUrl = (l: Lesson, p: number) => `/grammar/${level}/${l.lesson_number}/${p + 1}`;

  // 上一步：同課前一個文法點 → 前一課最後一個文法點
  const prev =
    pointIndex > 0
      ? { to: pointUrl(lesson, pointIndex - 1), label: `← 文法點 ${pointIndex}` }
      : prevLesson
        ? {
            to: pointUrl(prevLesson, prevLesson.grammar_points.length - 1),
            label: `← 第 ${prevLesson.lesson_number} 課`,
          }
        : null;

  // 下一步：同課下一個文法點 → 下一課第一個文法點
  const next =
    pointIndex < total - 1
      ? { to: pointUrl(lesson, pointIndex + 1), label: `文法點 ${pointIndex + 2} →` }
      : nextLesson
        ? { to: pointUrl(nextLesson, 0), label: `前往第 ${nextLesson.lesson_number} 課 →` }
        : null;

  return (
    <div>
      <Breadcrumb
        items={[
          { label: '首頁', to: '/' },
          { label: `${levelLabel} 文法`, to: `/grammar/${level}` },
          { label: `第 ${lesson.lesson_number} 課` },
        ]}
      />

      <div className="mt-6 flex flex-wrap items-center justify-between gap-4">
        <h1 className="font-display text-xl font-black leading-snug md:text-3xl">
          <span className="mr-2 inline-block rounded-lg border-2 border-paper-sumi bg-level-tint px-2 py-0.5 align-middle font-mono text-sm font-medium md:mr-3 md:px-2.5 md:text-base">
            第 {lesson.lesson_number} 課
          </span>
          {lesson.lesson_title}
        </h1>
        {/* 進度指示 */}
        <p className="flex items-center gap-2 font-mono text-xs text-paper-sumi/70 md:text-sm">
          文法點 {pointIndex + 1}/{total}
          <span aria-hidden="true" className="flex gap-1.5">
            {lesson.grammar_points.map((_, i) => (
              <span
                key={i}
                className={`h-2.5 w-2.5 rounded-full border border-paper-sumi ${
                  i === pointIndex ? 'bg-level' : i < pointIndex ? 'bg-level-tint' : 'bg-paper-oatmeal'
                }`}
              />
            ))}
          </span>
        </p>
      </div>

      {/* 手機：可展開目錄 */}
      <div className="mt-6 lg:hidden">
        <button
          type="button"
          aria-expanded={tocOpen}
          onClick={() => setTocOpen((v) => !v)}
          className="btn-retro w-full !justify-between"
        >
          本課文法點目錄
          <span aria-hidden="true" className="font-mono">
            {tocOpen ? '−' : '＋'}
          </span>
        </button>
        {tocOpen && (
          <nav
            aria-label="本課文法點目錄"
            className="mt-2 rounded-xl border-2 border-paper-sumi bg-paper-card p-3 shadow-retro-sm"
          >
            <TocList level={level} lesson={lesson} />
          </nav>
        )}
      </div>

      <div className="mt-8 flex items-start gap-8">
        {/* 主體：文法點 + 隨堂練習 */}
        <div className="min-w-0 flex-1">
          <GrammarPointCard point={point} index={pointIndex} anchorId={`grammar-point-${pointIndex + 1}`} />

          {point.quizzes && point.quizzes.length > 0 && (
            <section aria-labelledby="practice-heading" className="mt-10">
              <h2 id="practice-heading" className="mb-4 flex items-center gap-2 font-display text-xl font-bold md:text-2xl">
                <span
                  aria-hidden="true"
                  className="inline-block rounded-lg border-2 border-paper-sumi bg-paper-butter px-2 py-0.5 font-mono text-sm md:text-base"
                >
                  ✎
                </span>
                隨堂練習
                <span className="font-mono text-xs font-normal text-paper-sumi/60 md:text-sm">
                  {point.quizzes.length} 題・即答即解
                </span>
              </h2>
              <div className="flex flex-col gap-4">
                {point.quizzes.map((quiz, i) => (
                  <QuizCard key={`${lesson.lesson_number}-${pointIndex}-${i}`} quiz={quiz} index={i} />
                ))}
              </div>
            </section>
          )}

          {/* 上一步／下一步 */}
          <nav aria-label="文法點導覽" className="mt-8 flex flex-wrap items-center justify-between gap-3 md:mt-12 md:gap-4">
            <div>{prev && <Link to={prev.to} className="btn-retro">{prev.label}</Link>}</div>
            <Link
              to={`/grammar/${level}`}
              className="text-sm underline decoration-2 underline-offset-4 hover:bg-paper-butter md:text-base"
            >
              回到 {levelLabel} 文法列表
            </Link>
            <div>
              {next && (
                <Link to={next.to} className="btn-retro bg-level-tint">
                  {next.label}
                </Link>
              )}
            </div>
          </nav>
        </div>

        {/* 桌機：固定側欄目錄 */}
        <aside className="sticky top-24 hidden w-60 shrink-0 lg:block">
          <nav
            aria-label="本課文法點目錄"
            className="rounded-xl border-2 border-paper-sumi bg-paper-card p-4 shadow-retro-sm"
          >
            <p className="mb-2 font-display font-bold">本課文法點</p>
            <TocList level={level} lesson={lesson} />
          </nav>
        </aside>
      </div>
    </div>
  );
}

function TocList({ level, lesson }: { level: Level; lesson: Lesson }) {
  return (
    <ol className="flex flex-col gap-1">
      {lesson.grammar_points.map((point, i) => (
        <li key={i}>
          <NavLink
            to={`/grammar/${level}/${lesson.lesson_number}/${i + 1}`}
            className={({ isActive }) =>
              `block rounded-lg px-2 py-1.5 text-sm hover:bg-level-tint ${
                isActive ? 'bg-level-tint font-bold' : ''
              }`
            }
          >
            <span className="mr-1.5 font-mono text-paper-sumi/50">{i + 1}.</span>
            {point.point_title}
          </NavLink>
        </li>
      ))}
    </ol>
  );
}
