import { Fragment } from 'react';
import type { GrammarPoint } from '../data/types';
import { RetroCard } from './RetroCard';

interface GrammarPointCardProps {
  point: GrammarPoint;
  index: number;
  anchorId: string;
}

/** 把公式中的 [名詞A] 等中括號片語以級別 tint 高亮。 */
function FormulaText({ formula }: { formula: string }) {
  const parts = formula.split(/(\[[^\]]*\])/g);
  return (
    <>
      {parts.map((part, i) =>
        part.startsWith('[') && part.endsWith(']') ? (
          <span key={i} className="rounded bg-level-tint px-1 py-0.5 font-medium">
            {part}
          </span>
        ) : (
          <Fragment key={i}>{part}</Fragment>
        ),
      )}
    </>
  );
}

export function GrammarPointCard({ point, index, anchorId }: GrammarPointCardProps) {
  return (
    <RetroCard shadow="md" className="p-4 md:p-7">
      <article id={anchorId} aria-labelledby={`${anchorId}-title`}>
        {/* 標題＋級色編號圓章 */}
        <h2 id={`${anchorId}-title`} className="flex items-start gap-2 font-display text-lg font-bold leading-snug md:gap-3 md:text-2xl">
          <span
            aria-hidden="true"
            className="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full border-2 border-level bg-level-tint font-mono text-sm md:h-8 md:w-8 md:text-base"
          >
            {index + 1}
          </span>
          {point.point_title}
        </h2>

        {/* 句型公式 */}
        <p className="mt-4 rounded-lg border-2 border-dashed border-paper-sumi/50 bg-paper-oatmeal px-3 py-2.5 font-mono text-sm leading-loose md:mt-6 md:px-4 md:py-3 md:text-base">
          <FormulaText formula={point.formula} />
        </p>

        {/* 說明 */}
        <p className="mt-4 text-sm md:mt-6 md:text-base">{point.explanation}</p>

        {/* 注意（奶油便籤 + 膠帶） */}
        {point.alert && (
          <div className="relative mt-6 rounded-lg bg-paper-butter px-3 py-2.5 before:absolute before:-left-2 before:-top-2 before:h-4 before:w-12 before:-rotate-12 before:bg-paper-butter before:opacity-70 before:content-[''] md:mt-8 md:px-4 md:py-3">
            <p className="text-sm font-medium md:text-base">⚠ 注意：{point.alert}</p>
          </div>
        )}

        {/* 例句 */}
        {point.examples.length > 0 && (
          <ul className="mt-6 flex flex-col gap-4 md:mt-8 md:gap-5">
            {point.examples.map((ex, i) => (
              <li key={i} className="border-l-4 border-level pl-3 md:pl-4">
                <p lang="ja" className="text-lg font-medium leading-relaxed md:text-xl">
                  {ex.ja}
                </p>
                <p className="mt-1 text-xs text-paper-sumi/70 md:text-sm">{ex.zh}</p>
              </li>
            ))}
          </ul>
        )}
      </article>
    </RetroCard>
  );
}
