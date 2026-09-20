import { useMemo, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import type { FuriganaSegment, Level, VocabEntry } from '../data/types';
import { LEVEL_LABELS, isLevel } from '../data/meta';
import { useVocabSet } from '../hooks/useVocabSet';
import { useDocumentTitle } from '../hooks/useDocumentTitle';
import { ComingSoon } from '../components/ComingSoon';
import { RetroCard } from '../components/RetroCard';
import { LoadingState, ErrorState } from '../components/StatusStates';
import { NotFoundPage } from './NotFoundPage';

export function VocabularyLevelPage() {
  const { level } = useParams();
  if (!isLevel(level)) return <NotFoundPage />;
  return <VocabularyLevelContent level={level} />;
}

function VocabularyLevelContent({ level }: { level: Level }) {
  const state = useVocabSet(level);
  const levelLabel = LEVEL_LABELS[level];
  useDocumentTitle(`${levelLabel} 單字`);

  if (state.status === 'unavailable') return <ComingSoon section="vocabulary" level={level} />;
  if (state.status === 'loading') return <LoadingState />;
  if (state.status === 'error' || !state.data) return <ErrorState />;

  return <VocabBrowser levelLabel={levelLabel} entries={state.data} />;
}

/** 第一層分類：依詞性歸組，層級一致 */
const GROUP_ORDER = [
  '名詞',
  '動詞',
  'い形容詞',
  'な形容詞',
  '副詞・接續詞',
  '代名詞・指示・疑問',
  '數字・量詞',
  '寒暄・其他',
] as const;

type Group = (typeof GROUP_ORDER)[number];

function groupOf(entry: VocabEntry): Group {
  const pos = entry.part_of_speech;
  if (pos.startsWith('動詞')) return '動詞';
  if (pos === 'い形容詞') return 'い形容詞';
  if (pos === 'な形容詞') return 'な形容詞';
  if (pos === '副詞' || pos === '接續詞') return '副詞・接續詞';
  if (pos === '代名詞' || pos === '指示代名詞' || pos === '連體詞' || pos === '疑問詞')
    return '代名詞・指示・疑問';
  if (pos === '數詞' || pos === '量詞') return '數字・量詞';
  if (pos === '名詞') return '名詞';
  return '寒暄・其他';
}

function VocabBrowser({ levelLabel, entries }: { levelLabel: string; entries: VocabEntry[] }) {
  const [query, setQuery] = useState('');
  const [group, setGroup] = useState<'全部' | Group>('全部');
  const [theme, setTheme] = useState('全部');
  const [showFurigana, setShowFurigana] = useState(true);
  const [hideKana, setHideKana] = useState(false);
  const [hideMeaning, setHideMeaning] = useState(false);
  const [showRomaji, setShowRomaji] = useState(false);

  const grouped = useMemo(() => {
    const map = new Map<Group, VocabEntry[]>();
    for (const g of GROUP_ORDER) map.set(g, []);
    for (const e of entries) map.get(groupOf(e))?.push(e);
    return map;
  }, [entries]);

  // 名詞內的主題子分類（依資料中的出現順序）
  const nounThemes = useMemo(() => {
    const seen: string[] = [];
    for (const e of grouped.get('名詞') ?? []) {
      if (!seen.includes(e.category)) seen.push(e.category);
    }
    return seen;
  }, [grouped]);

  const trimmed = query.trim().toLowerCase();
  const searching = trimmed.length > 0;

  const filtered = useMemo(() => {
    let list = group === '全部' ? entries : (grouped.get(group) ?? []);
    if (group === '名詞' && theme !== '全部') list = list.filter((e) => e.category === theme);
    if (searching) {
      list = list.filter(
        (e) =>
          e.kanji.toLowerCase().includes(trimmed) ||
          e.kana.includes(trimmed) ||
          e.romaji.toLowerCase().includes(trimmed) ||
          e.meaning.toLowerCase().includes(trimmed),
      );
    }
    return list;
  }, [entries, grouped, group, theme, searching, trimmed]);

  // 「全部＋未搜尋」時以詞性收合呈現，避免一次展開六百多張卡
  const collapsedView = group === '全部' && !searching;

  const chip = (active: boolean) =>
    `rounded-lg border-2 border-paper-sumi px-2.5 py-1 font-mono text-xs transition-colors md:text-sm ${
      active ? 'bg-level text-paper-card' : 'bg-paper-card hover:bg-level-tint'
    }`;

  const toggleChip = (active: boolean) =>
    `rounded-lg border-2 border-paper-sumi px-3 py-1.5 font-display text-sm font-bold transition-colors ${
      active ? 'bg-level text-paper-card' : 'bg-paper-card hover:bg-level-tint'
    }`;

  return (
    <div>
      <header className="rounded-xl border-3 border-paper-sumi bg-level-tint px-5 py-6 shadow-retro md:px-10 md:py-10">
        <h1 className="font-display text-3xl font-black md:text-5xl">
          <span className="mr-3 inline-block rounded-lg border-2 border-paper-sumi bg-level px-2.5 py-0.5 text-paper-card md:px-3 md:py-1">
            {levelLabel}
          </span>
          單字
        </h1>
        <p className="mt-3 font-mono text-xs text-paper-sumi/70 md:mt-4 md:text-sm">
          全 {entries.length} 個單字・依詞性分類
        </p>

        <div className="mt-5 flex flex-wrap items-center justify-between gap-3 rounded-xl border-2 border-paper-sumi bg-paper-card p-3.5 shadow-retro-sm md:p-4">
          <div className="text-left">
            <span className="inline-block rounded bg-level px-2 py-0.5 font-display text-xs font-bold text-paper-card">
              數位備考套組
            </span>
            <p className="mt-1 text-xs font-bold md:text-sm">
              想要離線刷字卡？下載《{levelLabel} 逐字振假名 Anki 牌組 ＋ 考場速查講義手冊》
            </p>
          </div>
          <div className="flex flex-wrap items-center gap-2">
            <Link
              to="/products"
              className="btn-retro text-xs md:text-sm"
            >
              👀 線上試玩字卡 ＆ 預覽手冊 →
            </Link>
            <a
              href="https://buymeacoffee.com/chiaoban/shop"
              target="_blank"
              rel="noreferrer"
              className="btn-retro bg-paper-butter text-xs md:text-sm"
            >
              🛒 立即購買 {levelLabel} 套組
            </a>
          </div>
        </div>
      </header>

      {/* 控制列：搜尋＋拼音與自測模式 */}
      <RetroCard shadow="sm" className="mt-6 p-4 md:mt-8 md:p-5">
        <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
          <input
            type="search"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="搜尋漢字・假名・羅馬字・中文"
            aria-label="搜尋單字"
            className="w-full rounded-lg border-2 border-paper-sumi bg-paper-card px-3 py-2 text-sm md:max-w-xs"
          />
          <div className="flex flex-wrap gap-2" role="group" aria-label="顯示與自測模式">
            <button
              type="button"
              aria-pressed={showFurigana}
              onClick={() => setShowFurigana((v) => !v)}
              className={toggleChip(showFurigana)}
              title="切換漢字上方振假名或並列假名"
            >
              漢字標音
            </button>
            <button
              type="button"
              aria-pressed={hideKana}
              onClick={() => setHideKana((v) => !v)}
              className={toggleChip(hideKana)}
            >
              隱藏假名
            </button>
            <button
              type="button"
              aria-pressed={hideMeaning}
              onClick={() => setHideMeaning((v) => !v)}
              className={toggleChip(hideMeaning)}
            >
              隱藏中譯
            </button>
            <button
              type="button"
              aria-pressed={showRomaji}
              onClick={() => setShowRomaji((v) => !v)}
              className={toggleChip(showRomaji)}
            >
              羅馬字
            </button>
          </div>
        </div>
        {(hideKana || hideMeaning) && (
          <p className="mt-3 font-mono text-xs text-paper-sumi/60">
            自測中：點擊漢字或「？？？」可顯示答案
          </p>
        )}
      </RetroCard>

      {/* 第一層：詞性分類 chips */}
      <div className="mt-4 flex flex-wrap gap-2">
        {(['全部', ...GROUP_ORDER] as const).map((g) => (
          <button
            key={g}
            type="button"
            aria-pressed={group === g}
            onClick={() => {
              setGroup(g);
              setTheme('全部');
            }}
            className={chip(group === g)}
          >
            {g}
            {g !== '全部' && (
              <span className="ml-1 opacity-60">{grouped.get(g)?.length ?? 0}</span>
            )}
          </button>
        ))}
      </div>

      {/* 第二層：名詞內的主題篩選 */}
      {group === '名詞' && (
        <div className="mt-3 flex flex-wrap gap-2 rounded-xl border-2 border-dashed border-paper-sumi/40 bg-paper-oatmeal/50 p-3">
          <span className="self-center font-mono text-xs text-paper-sumi/60">主題：</span>
          {['全部', ...nounThemes].map((t) => (
            <button key={t} type="button" aria-pressed={theme === t} onClick={() => setTheme(t)} className={chip(theme === t)}>
              {t}
            </button>
          ))}
        </div>
      )}

      {/* 單字列表 */}
      {collapsedView ? (
        <div className="mt-6 flex flex-col gap-4">
          {GROUP_ORDER.map((g) => {
            const list = grouped.get(g) ?? [];
            if (list.length === 0) return null;
            return (
              <details key={g} className="group">
                <summary className="card-lift flex cursor-pointer list-none items-center justify-between rounded-xl border-2 border-paper-sumi bg-paper-card p-4 shadow-retro md:p-5">
                  <span className="font-display text-base font-bold md:text-xl">{g}</span>
                  <span className="font-mono text-xs text-paper-sumi/60">
                    {list.length} 個單字
                    <span aria-hidden="true" className="ml-2 inline-block transition-transform group-open:rotate-90">
                      ›
                    </span>
                  </span>
                </summary>
                {g === '名詞' ? (
                  <div className="mt-3 flex flex-col gap-5">
                    {nounThemes.map((t) => {
                      const sub = list.filter((e) => e.category === t);
                      if (sub.length === 0) return null;
                      return (
                        <section key={t} aria-label={`名詞：${t}`}>
                          <h3 className="mb-2 inline-block rounded-lg bg-level-tint px-2.5 py-0.5 font-display text-sm font-bold md:text-base">
                            {t}
                            <span className="ml-1.5 font-mono text-xs font-normal text-paper-sumi/60">{sub.length}</span>
                          </h3>
                          <VocabGrid
                            entries={sub}
                            showFurigana={showFurigana}
                            hideKana={hideKana}
                            hideMeaning={hideMeaning}
                            showRomaji={showRomaji}
                          />
                        </section>
                      );
                    })}
                  </div>
                ) : (
                  <div className="mt-3">
                    <VocabGrid
                      entries={list}
                      showFurigana={showFurigana}
                      hideKana={hideKana}
                      hideMeaning={hideMeaning}
                      showRomaji={showRomaji}
                    />
                  </div>
                )}
              </details>
            );
          })}
        </div>
      ) : (
        <>
          <p className="mt-6 font-mono text-xs text-paper-sumi/60">共 {filtered.length} 個單字</p>
          {filtered.length === 0 ? (
            <RetroCard shadow="sm" className="mt-3 p-8 text-center">
              <p>找不到符合的單字。</p>
            </RetroCard>
          ) : (
            <div className="mt-3">
              <VocabGrid
                entries={filtered}
                showFurigana={showFurigana}
                hideKana={hideKana}
                hideMeaning={hideMeaning}
                showRomaji={showRomaji}
              />
            </div>
          )}
        </>
      )}
    </div>
  );
}

interface VocabDisplayOptions {
  showFurigana: boolean;
  hideKana: boolean;
  hideMeaning: boolean;
  showRomaji: boolean;
}

function VocabGrid({
  entries,
  showFurigana,
  hideKana,
  hideMeaning,
  showRomaji,
}: { entries: VocabEntry[] } & VocabDisplayOptions) {
  return (
    <div className="grid grid-cols-1 gap-3 md:grid-cols-2 md:gap-4 lg:grid-cols-3">
      {entries.map((entry, i) => (
        <VocabCard
          key={`${entry.kanji}-${entry.kana}-${i}-${hideKana}-${hideMeaning}`}
          entry={entry}
          showFurigana={showFurigana}
          hideKana={hideKana}
          hideMeaning={hideMeaning}
          showRomaji={showRomaji}
        />
      ))}
    </div>
  );
}

function speak(text: string) {
  if (!('speechSynthesis' in window)) return;
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = 'ja-JP';
  window.speechSynthesis.speak(utterance);
}

function toHiragana(str: string): string {
  return str.replace(/[\u30a1-\u30f6]/g, (ch) =>
    String.fromCharCode(ch.charCodeAt(0) - 0x60),
  );
}

function isKanjiChar(ch: string): boolean {
  const code = ch.charCodeAt(0);
  return (
    (code >= 0x4e00 && code <= 0x9fff) ||
    ch === '々' ||
    ch === 'ヶ' ||
    ch === 'ヵ'
  );
}

function escapeRegExp(str: string): string {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/**
 * 後備切分：只切出「漢字段 vs 送假名段」，同一段連續漢字共用一個讀音。
 * 正常情況下會使用資料中由 scripts/generate_furigana.py 產生的逐字對位；
 * 這個函式只在資料缺少 furigana 欄位時作為保底。
 */
function splitFurigana(kanji: string, kana: string): FuriganaSegment[] {
  if (kanji === kana || ![...kanji].some(isKanjiChar)) {
    return [[kanji, null]];
  }

  const segments: { text: string; isKanji: boolean }[] = [];
  for (const ch of kanji) {
    const isK = isKanjiChar(ch);
    const last = segments[segments.length - 1];
    if (last && last.isKanji === isK) {
      last.text += ch;
    } else {
      segments.push({ text: ch, isKanji: isK });
    }
  }

  const pattern =
    '^' +
    segments
      .map((seg) =>
        seg.isKanji ? '(.+)' : `(${escapeRegExp(toHiragana(seg.text))})`,
      )
      .join('') +
    '$';

  const match = new RegExp(pattern).exec(toHiragana(kana));
  if (match) {
    return segments.map(
      (seg, idx) => [seg.text, seg.isKanji ? match[idx + 1] : null] as FuriganaSegment,
    );
  }

  return [[kanji, kana]];
}

function RubyWord({
  entry,
  showFurigana,
  kanaMasked,
  onReveal,
}: {
  entry: VocabEntry;
  showFurigana: boolean;
  kanaMasked: boolean;
  onReveal: () => void;
}) {
  // 優先使用資料中預先算好的逐字對位，缺少時才即時切分
  const segments = useMemo(
    () => entry.furigana ?? splitFurigana(entry.kanji, entry.kana),
    [entry.furigana, entry.kanji, entry.kana],
  );
  const hasReading = segments.some((seg) => seg[1] !== null);

  if (!showFurigana || !hasReading) {
    return (
      <span lang="ja" className="text-xl font-bold">
        {entry.kanji}
      </span>
    );
  }

  if (kanaMasked) {
    return (
      <span
        lang="ja"
        role="button"
        tabIndex={0}
        onClick={onReveal}
        onKeyDown={(e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            onReveal();
          }
        }}
        title="點擊顯示振假名"
        className="ruby-word cursor-pointer text-xl font-bold underline decoration-dashed decoration-paper-sumi/40 underline-offset-4 hover:text-level"
      >
        {entry.kanji}
      </span>
    );
  }

  return (
    <span lang="ja" className="ruby-word text-xl font-bold">
      {segments.map(([text, reading], idx) =>
        reading ? (
          <ruby key={idx}>
            {text}
            <rp>(</rp>
            <rt>{reading}</rt>
            <rp>)</rp>
          </ruby>
        ) : (
          <span key={idx} className="ruby-okurigana">
            {text}
          </span>
        ),
      )}
    </span>
  );
}

function VocabCard({
  entry,
  showFurigana,
  hideKana,
  hideMeaning,
  showRomaji,
}: { entry: VocabEntry } & VocabDisplayOptions) {
  const [kanaRevealed, setKanaRevealed] = useState(false);
  const [meaningRevealed, setMeaningRevealed] = useState(false);
  const kanaMasked = hideKana && !kanaRevealed;
  const meaningMasked = hideMeaning && !meaningRevealed;
  const sameAsKana = entry.kanji === entry.kana;

  return (
    <RetroCard shadow="sm" className="p-4">
      <div className="flex items-start justify-between gap-2">
        <p className="flex flex-wrap items-baseline gap-x-2.5 gap-y-1">
          <RubyWord
            entry={entry}
            showFurigana={showFurigana}
            kanaMasked={kanaMasked}
            onReveal={() => setKanaRevealed(true)}
          />
          {!sameAsKana &&
            (kanaMasked ? (
              <button
                type="button"
                onClick={() => setKanaRevealed(true)}
                aria-label="顯示假名"
                className="rounded bg-paper-oatmeal px-2 py-0.5 font-mono text-sm hover:bg-paper-butter"
              >
                ？？？
              </button>
            ) : (
              !showFurigana && (
                <span lang="ja" className="text-base text-paper-sumi/80">
                  {entry.kana}
                </span>
              )
            ))}
          {showRomaji && (
            <span className="font-mono text-xs text-paper-sumi/50">{entry.romaji}</span>
          )}
        </p>
        <button
          type="button"
          onClick={() => speak(entry.kana === entry.kanji ? entry.kana : entry.kanji)}
          aria-label={`播放「${entry.kanji}」的發音`}
          className="shrink-0 rounded-lg border-2 border-paper-sumi bg-paper-card px-1.5 py-0.5 text-sm hover:bg-level-tint"
        >
          🔊
        </button>
      </div>

      <p className="mt-2 text-sm">
        <span className="mr-2 rounded border border-paper-sumi/40 bg-paper-oatmeal px-1.5 py-0.5 font-mono text-xs">
          {entry.part_of_speech}
        </span>
        {meaningMasked ? (
          <button
            type="button"
            onClick={() => setMeaningRevealed(true)}
            aria-label="顯示中文意思"
            className="rounded bg-paper-oatmeal px-2 py-0.5 font-mono text-xs hover:bg-paper-butter"
          >
            ？？？
          </button>
        ) : (
          entry.meaning
        )}
      </p>

      <p lang="ja" className="mt-3 border-l-4 border-level pl-3 text-lg leading-relaxed">
        {entry.example_ja}
      </p>
      {!meaningMasked && <p className="pl-3 text-xs text-paper-sumi/70 md:text-sm">{entry.example_zh}</p>}
    </RetroCard>
  );
}
