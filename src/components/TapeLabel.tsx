import type { ReactNode } from 'react';

interface TapeLabelProps {
  children: ReactNode;
  className?: string;
}

/** 奶油黃「膠帶」裝飾標籤。 */
export function TapeLabel({ children, className = '' }: TapeLabelProps) {
  return (
    <span
      className={`inline-block -rotate-3 bg-paper-butter px-4 py-1 font-mono text-sm text-paper-sumi opacity-90 ${className}`}
      style={{ clipPath: 'polygon(2% 0, 98% 4%, 100% 96%, 0 100%)' }}
    >
      {children}
    </span>
  );
}
