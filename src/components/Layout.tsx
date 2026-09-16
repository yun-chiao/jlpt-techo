import { useEffect } from 'react';
import { Outlet, matchPath, useLocation } from 'react-router-dom';
import { isLevel, isSection } from '../data/meta';
import { NavBar } from './NavBar';
import { Footer } from './Footer';

/**
 * 站台外框：NavBar + Footer，並依路由自動設定 <html data-level="...">
 * 供 CSS 級別主題化（--level / --level-tint）使用。
 */
export function Layout() {
  const location = useLocation();

  useEffect(() => {
    const match = matchPath('/:section/:level/*', location.pathname) ?? matchPath('/:section/:level', location.pathname);
    const section = match?.params.section;
    const level = match?.params.level;
    if (isSection(section) && isLevel(level)) {
      document.documentElement.dataset.level = level;
    } else {
      delete document.documentElement.dataset.level;
    }
  }, [location.pathname]);

  return (
    <div className="flex min-h-screen flex-col">
      <NavBar />
      <main className="mx-auto w-full max-w-6xl flex-1 px-4 py-6 md:py-12">
        <Outlet />
      </main>
      <Footer />
    </div>
  );
}
