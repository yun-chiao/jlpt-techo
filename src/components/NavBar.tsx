import { useEffect, useRef, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import type { Section } from '../data/types';
import { BLOG_LABEL, LEVELS, LEVEL_LABELS, SECTIONS, SECTION_LABELS, SITE_NAME, SITE_NAME_EN } from '../data/meta';
import { isAvailable } from '../data/registry';
import { LevelDot } from './LevelDot';

export function NavBar() {
  const [openMenu, setOpenMenu] = useState<Section | null>(null);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [mobileSection, setMobileSection] = useState<Section | null>(null);
  const navRef = useRef<HTMLElement>(null);
  const location = useLocation();

  // 換頁時關閉所有選單
  useEffect(() => {
    setOpenMenu(null);
    setMobileOpen(false);
    setMobileSection(null);
  }, [location.pathname]);

  // 點擊外部關閉下拉
  useEffect(() => {
    const onPointerDown = (e: PointerEvent) => {
      if (navRef.current && !navRef.current.contains(e.target as Node)) {
        setOpenMenu(null);
      }
    };
    document.addEventListener('pointerdown', onPointerDown);
    return () => document.removeEventListener('pointerdown', onPointerDown);
  }, []);

  // Esc 關閉
  useEffect(() => {
    const onKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        setOpenMenu(null);
        setMobileOpen(false);
      }
    };
    document.addEventListener('keydown', onKeyDown);
    return () => document.removeEventListener('keydown', onKeyDown);
  }, []);

  return (
    <header className="sticky top-0 z-50 border-b-2 border-paper-sumi bg-paper-card">
      <nav ref={navRef} aria-label="主導覽" className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
        <Link to="/" className="flex items-baseline gap-2">
          <span className="font-display text-xl font-black tracking-wide md:text-2xl">{SITE_NAME}</span>
          <span className="hidden font-mono text-xs text-paper-sumi/60 sm:inline">{SITE_NAME_EN}</span>
        </Link>

        {/* 桌機選單 */}
        <ul className="hidden items-center gap-2 md:flex">
          {SECTIONS.map((section) => (
            <li
              key={section}
              className="relative"
              onMouseEnter={() => setOpenMenu(section)}
              onMouseLeave={() => setOpenMenu((cur) => (cur === section ? null : cur))}
            >
              <button
                type="button"
                aria-haspopup="true"
                aria-expanded={openMenu === section}
                onClick={() => setOpenMenu((cur) => (cur === section ? null : section))}
                className="rounded-lg px-4 py-2 font-display text-lg font-bold hover:bg-paper-butter"
              >
                {SECTION_LABELS[section]}
              </button>
              {openMenu === section && (
                <ul className="absolute right-0 top-full w-56 rounded-xl border-2 border-paper-sumi bg-paper-card p-2 shadow-retro">
                  {LEVELS.map((level) => {
                    const available = isAvailable(section, level);
                    return (
                      <li key={level}>
                        <Link
                          to={`/${section}/${level}`}
                          className={`flex items-center justify-between gap-2 rounded-lg px-3 py-2 hover:bg-paper-oatmeal ${
                            available ? '' : 'text-paper-sumi/50'
                          }`}
                        >
                          <span className="flex items-center gap-2 font-mono font-medium">
                            <LevelDot level={level} />
                            {LEVEL_LABELS[level]}
                          </span>
                          {!available && (
                            <span className="rounded border border-paper-oatmeal px-1.5 py-0.5 font-mono text-[10px] uppercase text-paper-sumi/50">
                              Coming Soon
                            </span>
                          )}
                        </Link>
                      </li>
                    );
                  })}
                </ul>
              )}
            </li>
          ))}
          <li>
            <Link to="/blog" className="block rounded-lg px-4 py-2 font-display text-lg font-bold hover:bg-paper-butter">
              {BLOG_LABEL}
            </Link>
          </li>
          <li>
            <Link
              to="/products"
              className="inline-flex items-center gap-1.5 rounded-lg border-2 border-paper-sumi bg-paper-butter px-3 py-1.5 font-display text-sm font-black shadow-retro-sm transition-transform hover:translate-x-[-1px] hover:translate-y-[-1px]"
            >
              <span>📦</span>
              <span>數位備考套組</span>
            </Link>
          </li>
        </ul>

        {/* 手機漢堡按鈕 */}
        <button
          type="button"
          aria-label={mobileOpen ? '關閉選單' : '開啟選單'}
          aria-expanded={mobileOpen}
          onClick={() => setMobileOpen((v) => !v)}
          className="btn-retro !px-3 !py-2 md:hidden"
        >
          <svg width="20" height="20" viewBox="0 0 20 20" aria-hidden="true">
            {mobileOpen ? (
              <path d="M4 4 L16 16 M16 4 L4 16" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" />
            ) : (
              <path d="M3 5 H17 M3 10 H17 M3 15 H17" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" />
            )}
          </svg>
        </button>
      </nav>

      {/* 手機全寬選單（手風琴） */}
      {mobileOpen && (
        <div className="border-t-2 border-paper-sumi bg-paper-card px-4 pb-4 md:hidden">
          {SECTIONS.map((section) => (
            <div key={section} className="border-b border-paper-oatmeal">
              <button
                type="button"
                aria-expanded={mobileSection === section}
                onClick={() => setMobileSection((cur) => (cur === section ? null : section))}
                className="flex w-full items-center justify-between py-3 font-display text-base font-bold"
              >
                {SECTION_LABELS[section]}
                <span aria-hidden="true" className="font-mono">
                  {mobileSection === section ? '−' : '＋'}
                </span>
              </button>
              {mobileSection === section && (
                <ul className="pb-3">
                  {LEVELS.map((level) => {
                    const available = isAvailable(section, level);
                    return (
                      <li key={level}>
                        <Link
                          to={`/${section}/${level}`}
                          className={`flex items-center justify-between rounded-lg px-3 py-2.5 hover:bg-paper-oatmeal ${
                            available ? '' : 'text-paper-sumi/50'
                          }`}
                        >
                          <span className="flex items-center gap-2 font-mono font-medium">
                            <LevelDot level={level} />
                            {LEVEL_LABELS[level]}
                          </span>
                          {!available && (
                            <span className="rounded border border-paper-oatmeal px-1.5 py-0.5 font-mono text-[10px] uppercase text-paper-sumi/50">
                              Coming Soon
                            </span>
                          )}
                        </Link>
                      </li>
                    );
                  })}
                </ul>
              )}
            </div>
          ))}
          <Link to="/blog" className="block py-3 font-display text-base font-bold hover:bg-paper-oatmeal">
            {BLOG_LABEL}
          </Link>
          <div className="pt-2">
            <Link
              to="/products"
              className="inline-flex w-full items-center justify-center gap-2 rounded-lg border-2 border-paper-sumi bg-paper-butter py-2.5 font-display text-sm font-black shadow-retro-sm"
            >
              <span>📦</span>
              <span>數位備考套組（Anki 牌組＆A4 講義）</span>
            </Link>
          </div>
        </div>
      )}
    </header>
  );
}
