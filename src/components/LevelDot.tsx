import type { Level } from '../data/types';

interface LevelDotProps {
  level: Level;
  className?: string;
}

/** 8px 實心圓點，依 level 套色。 */
export function LevelDot({ level, className = '' }: LevelDotProps) {
  return (
    <span
      aria-hidden="true"
      className={`inline-block h-2 w-2 shrink-0 rounded-full ${className}`}
      style={{ backgroundColor: `var(--jlpt-${level})` }}
    />
  );
}
