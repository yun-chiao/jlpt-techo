import { Link } from 'react-router-dom';
import { useDocumentTitle } from '../hooks/useDocumentTitle';
import { RetroCard } from '../components/RetroCard';
import { TapeLabel } from '../components/TapeLabel';

export function NotFoundPage() {
  useDocumentTitle('404 找不到頁面');

  return (
    <div className="mx-auto flex max-w-2xl flex-col items-center py-8 text-center">
      <RetroCard shadow="lg" className="relative w-full px-5 py-10 md:px-6 md:py-14">
        <TapeLabel className="absolute -top-3 left-1/2 -translate-x-1/2">PAGE NOT FOUND</TapeLabel>
        <p className="font-mono text-6xl font-medium tracking-widest md:text-7xl">404</p>
        <h1 className="mt-4 font-display text-2xl font-black md:text-3xl">這一頁被撕走了</h1>
        <p className="mt-3 text-sm text-paper-sumi/70 md:text-base">找不到你要的頁面，回到目錄重新翻閱吧。</p>
        <Link to="/" className="btn-retro mt-10">
          回到首頁
        </Link>
      </RetroCard>
    </div>
  );
}
