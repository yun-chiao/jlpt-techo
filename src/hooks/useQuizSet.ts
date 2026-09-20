import { useEffect, useState } from 'react';
import type { Level, LevelQuizSet } from '../data/types';
import { registry } from '../data/registry';

export type QuizSetStatus = 'unavailable' | 'loading' | 'ready' | 'error';

export interface QuizSetState {
  status: QuizSetStatus;
  data?: LevelQuizSet;
}

/** 題型專攻闖關書透過此 Hook 取各級別題庫資料，不得在元件內直接 import JSON。 */
export function useQuizSet(level: Level): QuizSetState {
  const loader = registry.quiz[level];
  const [state, setState] = useState<QuizSetState>(() =>
    loader ? { status: 'loading' } : { status: 'unavailable' },
  );

  useEffect(() => {
    if (!loader) {
      setState({ status: 'unavailable' });
      return;
    }
    let cancelled = false;
    setState({ status: 'loading' });
    loader()
      .then((data) => {
        if (cancelled) return;
        setState({ status: 'ready', data });
      })
      .catch((err: unknown) => {
        if (cancelled) return;
        console.error(`[useQuizSet] 載入 quiz/${level} 失敗：`, err);
        setState({ status: 'error' });
      });
    return () => {
      cancelled = true;
    };
  }, [loader, level]);

  return state;
}
