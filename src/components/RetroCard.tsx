import type { ReactNode } from 'react';

interface RetroCardProps {
  children: ReactNode;
  shadow?: 'sm' | 'md' | 'lg';
  className?: string;
}

const shadowClass = {
  sm: 'shadow-retro-sm',
  md: 'shadow-retro',
  lg: 'shadow-retro-lg',
} as const;

/** 白底 + 2px 墨黑框 + 復古硬陰影的通用容器。 */
export function RetroCard({ children, shadow = 'md', className = '' }: RetroCardProps) {
  return (
    <div
      className={`rounded-xl border-2 border-paper-sumi bg-paper-card ${shadowClass[shadow]} ${className}`}
    >
      {children}
    </div>
  );
}
