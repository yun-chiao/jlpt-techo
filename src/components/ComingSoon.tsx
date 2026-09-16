import { Link } from 'react-router-dom';
import type { Level, Section } from '../data/types';
import { LEVEL_LABELS, SECTION_LABELS } from '../data/meta';
import { useDocumentTitle } from '../hooks/useDocumentTitle';
import { RetroCard } from './RetroCard';
import { TapeLabel } from './TapeLabel';
import { LevelBadge } from './LevelBadge';

interface ComingSoonProps {
  section: Section;
  level: Level;
}

export function ComingSoon({ section, level }: ComingSoonProps) {
  const title = `${LEVEL_LABELS[level]} ${SECTION_LABELS[section]}`;
  useDocumentTitle(`敬請期待｜${title}`);

  return (
    <div className="mx-auto flex max-w-2xl flex-col items-center gap-8 py-8 text-center">
      <RetroCard shadow="lg" className="relative w-full px-5 py-10 md:px-6 md:py-14">
        <TapeLabel className="absolute -top-3 left-1/2 -translate-x-1/2">COMING SOON</TapeLabel>

        {/* 純 CSS 插畫感區塊：級別色幾何貼紙 */}
        <div aria-hidden="true" className="mx-auto mb-8 flex items-end justify-center gap-3">
          <span className="h-10 w-10 rotate-6 rounded-lg border-2 border-paper-sumi bg-level-tint" />
          <span className="h-16 w-16 -rotate-3 rounded-full border-2 border-paper-sumi bg-level" />
          <span className="h-12 w-12 rotate-12 rounded-lg border-2 border-paper-sumi bg-paper-butter" />
        </div>

        <h1 className="font-display text-3xl font-black md:text-5xl">敬請期待</h1>
        <p className="mt-4 flex items-center justify-center gap-2 text-base md:text-lg">
          <LevelBadge level={level} />
          <span>
            {SECTION_LABELS[section]} 現正製作中
          </span>
        </p>
        <p className="mt-2 font-mono text-sm text-paper-sumi/60">under construction ...</p>

        <Link to="/" className="btn-retro mt-10">
          回到首頁
        </Link>
      </RetroCard>
    </div>
  );
}
