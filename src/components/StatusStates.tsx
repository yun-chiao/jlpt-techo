import { Link } from 'react-router-dom';
import { RetroCard } from './RetroCard';

export function LoadingState() {
  return (
    <div className="flex justify-center py-24" role="status" aria-live="polite">
      <p className="font-mono text-paper-sumi/60">loading ...</p>
    </div>
  );
}

export function ErrorState() {
  return (
    <div className="mx-auto max-w-xl py-12">
      <RetroCard shadow="md" className="px-6 py-10 text-center">
        <h1 className="font-display text-2xl font-bold">教材載入失敗</h1>
        <p className="mt-3 text-paper-sumi/70">請重新整理頁面再試一次。</p>
        <Link to="/" className="btn-retro mt-8">
          回到首頁
        </Link>
      </RetroCard>
    </div>
  );
}
