import { Link } from 'react-router-dom';
import type { Lesson } from '../data/types';

interface LessonCardProps {
  lesson: Lesson;
  to: string;
  /** 顯示在卡片底部的數量描述，例：「3 個文法點」 */
  countLabel: string;
}

export function LessonCard({ lesson, to, countLabel }: LessonCardProps) {
  return (
    <Link
      to={to}
      className="card-lift block rounded-xl border-2 border-paper-sumi bg-paper-card p-4 shadow-retro md:p-5"
    >
      <p className="inline-block rounded-lg border-2 border-paper-sumi bg-level-tint px-2 py-0.5 font-mono text-xs font-medium md:text-sm">
        第 {lesson.lesson_number} 課
      </p>
      <h3 className="mt-2 font-display text-lg font-bold leading-snug md:mt-3 md:text-xl">{lesson.lesson_title}</h3>
      <p className="mt-2 font-mono text-xs text-paper-sumi/60">{countLabel}</p>
    </Link>
  );
}
