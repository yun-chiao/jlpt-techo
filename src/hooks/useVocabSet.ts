import { useEffect, useState } from 'react';
import type { Level, VocabSet } from '../data/types';
import { registry } from '../data/registry';
import { validateVocabSet } from '../data/validate';

export type VocabSetStatus = 'unavailable' | 'loading' | 'ready' | 'error';

export interface VocabSetState {
  status: VocabSetStatus;
  data?: VocabSet;
}

/** 單字頁透過此 Hook 取單字總表，不得在元件內直接 import JSON。 */
export function useVocabSet(level: Level): VocabSetState {
  const loader = registry.vocabulary[level];
  const [state, setState] = useState<VocabSetState>(() =>
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
          validateVocabSet(data, `vocabulary/${level}`);
        }
        setState({ status: 'ready', data });
      })
      .catch((err: unknown) => {
        if (cancelled) return;
        console.error(`[useVocabSet] 載入 vocabulary/${level} 失敗：`, err);
        setState({ status: 'error' });
      });
    return () => {
      cancelled = true;
    };
  }, [loader, level]);

  return state;
}
