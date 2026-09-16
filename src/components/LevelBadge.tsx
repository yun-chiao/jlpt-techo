import type { Level } from '../data/types';
import { LEVEL_LABELS } from '../data/meta';
import { LevelDot } from './LevelDot';

interface LevelBadgeProps {
  level: Level;
  className?: string;
}

/**
 * 級別標籤：tint 底 + 2px 墨黑框 + 主色圓點 + 墨黑文字。
 * （級別主色直接當文字對比不足，依規範改用墨黑文字＋主色圓點。）
 */
export function LevelBadge({ level, className = '' }: LevelBadgeProps) {
  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-lg border-2 border-paper-sumi px-2 py-0.5 font-mono text-sm font-medium text-paper-sumi ${className}`}
      style={{ backgroundColor: `var(--jlpt-${level}-tint)` }}
    >
      <LevelDot level={level} />
      {LEVEL_LABELS[level]}
    </span>
  );
}
