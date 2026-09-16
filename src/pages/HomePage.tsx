import { Link } from 'react-router-dom';
import { BLOG_LABEL, LEVELS, LEVEL_LABELS, SECTIONS, SECTION_LABELS, SITE_NAME, SITE_NAME_EN, SITE_TAGLINE } from '../data/meta';
import { isAvailable } from '../data/registry';
import { useDocumentTitle } from '../hooks/useDocumentTitle';
import { LevelBadge } from '../components/LevelBadge';
import { TapeLabel } from '../components/TapeLabel';

export function HomePage() {
  useDocumentTitle();

  return (
    <div className="flex flex-col gap-10 md:gap-16">
      {/* Hero */}
      <section className="flex flex-col items-start gap-8 py-4 md:flex-row md:items-center md:justify-between md:py-14">
        <div className="max-w-xl">
          <p className="font-mono text-xs tracking-widest text-paper-sumi/60 md:text-sm">{SITE_NAME_EN} — JLPT STUDY MAGAZINE</p>
          <h1 className="mt-3 font-display text-4xl font-black leading-tight md:text-6xl">{SITE_NAME}</h1>
          <p className="mt-4 text-base md:mt-6 md:text-lg">{SITE_TAGLINE}</p>
          <div className="mt-6 flex flex-wrap gap-4 md:mt-8">
            <Link
              to="/grammar/n5"
              className="btn-retro !border-3 md:text-lg"
              style={{ backgroundColor: 'var(--jlpt-n5-tint)' }}
            >
              從 N5 開始
            </Link>
            <Link to="/grammar/n5" className="btn-retro md:text-lg">
              看看文法
            </Link>
          </div>
        </div>

        {/* 五級色幾何貼紙裝飾（純 CSS） */}
        <div aria-hidden="true" className="relative mx-auto h-40 w-40 shrink-0 md:mx-0 md:h-64 md:w-64">
          <div className="absolute left-0 top-0 h-64 w-64 origin-top-left scale-[0.625] md:scale-100">
            <span className="absolute left-2 top-2 h-20 w-20 rotate-6 rounded-xl border-2 border-paper-sumi shadow-retro-sm" style={{ backgroundColor: 'var(--jlpt-n1)' }} />
            <span className="absolute right-4 top-8 h-16 w-16 -rotate-12 rounded-full border-2 border-paper-sumi shadow-retro-sm" style={{ backgroundColor: 'var(--jlpt-n2)' }} />
            <span className="absolute bottom-16 left-10 h-14 w-24 -rotate-3 rounded-lg border-2 border-paper-sumi shadow-retro-sm" style={{ backgroundColor: 'var(--jlpt-n3)' }} />
            <span className="absolute bottom-4 right-8 h-20 w-20 rotate-12 rounded-xl border-2 border-paper-sumi shadow-retro-sm" style={{ backgroundColor: 'var(--jlpt-n4)' }} />
            <span className="absolute bottom-10 left-1/2 h-16 w-16 -translate-x-1/2 rotate-45 border-2 border-paper-sumi shadow-retro-sm" style={{ backgroundColor: 'var(--jlpt-n5)' }} />
            <TapeLabel className="absolute -top-2 left-1/2 -translate-x-1/2">N1 – N5</TapeLabel>
          </div>
        </div>
      </section>

      {/* 入口卡片矩陣 */}
      {SECTIONS.map((section) => (
        <section key={section} aria-labelledby={`section-${section}`}>
          <h2 id={`section-${section}`} className="mb-4 font-display text-2xl font-black md:mb-6 md:text-3xl">
            {SECTION_LABELS[section]}
          </h2>
          <div className="grid grid-cols-2 gap-4 sm:grid-cols-2 md:grid-cols-3 md:gap-6 lg:grid-cols-5">
            {LEVELS.map((level) => {
              const available = isAvailable(section, level);
              return (
                <Link
                  key={level}
                  to={`/${section}/${level}`}
                  className="card-lift relative block rounded-xl border-2 border-paper-sumi bg-paper-card p-4 shadow-retro"
                >
                  <LevelBadge level={level} />
                  <p className="mt-3 font-display text-base font-bold md:mt-4 md:text-xl">
                    {LEVEL_LABELS[level]} {SECTION_LABELS[section]}
                  </p>
                  <p className="mt-1 font-mono text-[10px] text-paper-sumi/60 md:text-xs">
                    {available ? '開始學習 →' : 'in preparation'}
                  </p>
                  {!available && (
                    <>
                      <span aria-hidden="true" className="absolute inset-0 rounded-[10px] bg-paper-canvas/60" />
                      <span className="absolute right-3 top-3 -rotate-12 rounded border-2 border-paper-sumi/70 px-1.5 py-0.5 font-mono text-[10px] font-medium uppercase text-paper-sumi/70">
                        Coming Soon
                      </span>
                    </>
                  )}
                </Link>
              );
            })}
          </div>
        </section>
      ))}

      {/* 部落格入口 */}
      <section aria-labelledby="section-blog">
        <h2 id="section-blog" className="mb-4 font-display text-2xl font-black md:mb-6 md:text-3xl">
          {BLOG_LABEL}
        </h2>
        <Link
          to="/blog"
          className="card-lift relative block rounded-xl border-2 border-paper-sumi bg-paper-butter p-5 shadow-retro md:p-8"
        >
          <p className="font-mono text-xs tracking-widest text-paper-sumi/60">BLOG / JOURNAL</p>
          <p className="mt-2 font-display text-lg font-bold md:text-2xl">更新公告・文法小知識・學習筆記</p>
          <p className="mt-2 font-mono text-xs text-paper-sumi/60">去翻翻 →</p>
        </Link>
      </section>
    </div>
  );
}
