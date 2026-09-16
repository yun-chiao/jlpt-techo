import { useState } from 'react';
import type { Quiz } from '../data/types';
import { RetroCard } from './RetroCard';

interface QuizCardProps {
  quiz: Quiz;
  index: number;
}

/** 互動選擇題卡：作答後即顯示正解與解說。 */
export function QuizCard({ quiz, index }: QuizCardProps) {
  const [selected, setSelected] = useState<string | null>(null);
  const answered = selected !== null;
  const correct = selected === quiz.correct_answer;

  return (
    <RetroCard shadow="sm" className="p-4 md:p-5">
      <p lang="ja" className="text-lg font-medium leading-relaxed">
        <span className="mr-2 font-mono text-sm text-paper-sumi/50">Q{index + 1}.</span>
        {quiz.question_text}
      </p>
      <div className="mt-3 grid grid-cols-2 gap-2 sm:grid-cols-4 md:mt-4 md:gap-3">
        {quiz.options.map((option) => {
          const isCorrectOption = option === quiz.correct_answer;
          const isSelected = option === selected;
          let stateClass = 'bg-paper-card';
          if (answered && isCorrectOption) stateClass = 'bg-level-tint !border-level';
          else if (answered && isSelected) stateClass = 'bg-paper-oatmeal';
          return (
            <button
              key={option}
              type="button"
              lang="ja"
              disabled={answered}
              onClick={() => setSelected(option)}
              className={`btn-retro !px-3 ${stateClass} disabled:cursor-default`}
            >
              {option}
            </button>
          );
        })}
      </div>
      {answered && (
        <div aria-live="polite" className="mt-3 rounded-lg bg-paper-butter px-3 py-2.5 md:mt-4 md:px-4 md:py-3">
          <p className="text-sm font-bold md:text-base">
            {correct ? '○ 答對了！' : `✗ 答錯了，正解：${quiz.correct_answer}`}
          </p>
          <p className="mt-1 text-xs md:text-sm">{quiz.explanation}</p>
        </div>
      )}
    </RetroCard>
  );
}
