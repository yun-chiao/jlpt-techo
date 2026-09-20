import { Link } from 'react-router-dom';
import { SITE_NAME, SITE_NAME_EN } from '../data/meta';

export function Footer() {
  return (
    <footer className="mt-16 border-t-2 border-paper-sumi bg-paper-card">
      <div className="mx-auto flex max-w-6xl flex-col items-center gap-2 px-4 py-6 text-center md:py-8">
        <p className="font-display text-base font-bold md:text-lg">
          {SITE_NAME} <span className="font-mono text-sm font-medium">{SITE_NAME_EN}</span>
        </p>
        <p className="text-xs md:text-sm">
          有問題、想給我鼓勵、或是合作邀約，都歡迎來信：
          <a
            href="mailto:jojo050872@gmail.com"
            className="ml-1 font-mono underline decoration-2 underline-offset-4 hover:bg-paper-butter"
          >
            jojo050872@gmail.com
          </a>
        </p>
        <div className="my-2 inline-flex flex-wrap items-center justify-center gap-2 rounded-xl border-2 border-paper-sumi bg-paper-canvas px-4 py-2.5 text-xs font-medium shadow-retro-sm md:text-sm">
          <span>📦 想要離線背單字、iPad 筆記或考場列印講義？</span>
          <Link
            to="/products"
            className="font-bold underline decoration-2 underline-offset-4 hover:bg-paper-butter"
          >
            線上試玩 Anki 字卡 ＆ 預覽 A4 考場速查手冊 ↗
          </Link>
        </div>
        <p className="text-xs text-paper-sumi/60">© {new Date().getFullYear()} {SITE_NAME}. All rights reserved.</p>
      </div>
    </footer>
  );
}
