import { useEffect, useState } from 'react';
import type { Level, LessonSet } from '../data/types';
import { registry } from '../data/registry';
import { validateLessonSet } from '../data/validate';

export type LessonSetStatus = 'unavailable' | 'loading' | 'ready' | 'error';

export interface LessonSetState {
  status: LessonSetStatus;
  data?: LessonSet;
}

/** 課程教材（文法）用的 section；單字請用 useVocabSet，題庫請用 useQuizSet。 */
type LessonSection = 'grammar';

/**
 * 文法頁面透過此 Hook 取教材資料，不得在元件內直接 import JSON。
 */
export function useLessonSet(section: LessonSection, level: Level): LessonSetState {
  const loader = registry.grammar[level];
  const [state, setState] = useState<LessonSetState>(() =>
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
        if (import.meta.env.DEV) {
          validateLessonSet(data, `${section}/${level}`);
        }
        setState({ status: 'ready', data });
      })
      .catch((err: unknown) => {
        if (cancelled) return;
        console.error(`[useLessonSet] 載入 ${section}/${level} 失敗：`, err);
        setState({ status: 'error' });
      });
    return () => {
      cancelled = true;
    };
  }, [loader, section, level]);

  return state;
}
