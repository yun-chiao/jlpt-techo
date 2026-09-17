import { SITE_NAME, SITE_NAME_EN } from '../data/meta';

const BMC_URL = 'https://buymeacoffee.com/chiaoban';

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
        <p className="text-xs md:text-sm">
          覺得日檢手帖有幫助嗎？
          <a
            href={BMC_URL}
            target="_blank"
            rel="noreferrer"
            className="ml-1 underline decoration-2 underline-offset-4 hover:bg-paper-butter"
          >
            請我喝杯咖啡 ☕
          </a>
        </p>
        <p className="text-xs md:text-sm">© {new Date().getFullYear()} {SITE_NAME}. All rights reserved.</p>
      </div>
    </footer>
  );
}
