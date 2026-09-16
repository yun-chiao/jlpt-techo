import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { loadPosts, type BlogPost } from '../data/blog';
import { BLOG_LABEL } from '../data/meta';
import { useDocumentTitle } from '../hooks/useDocumentTitle';
import { LoadingState, ErrorState } from '../components/StatusStates';
import { TapeLabel } from '../components/TapeLabel';

export function BlogListPage() {
  useDocumentTitle(BLOG_LABEL);
  const [posts, setPosts] = useState<BlogPost[] | null>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    let cancelled = false;
    loadPosts()
      .then((p) => {
        if (!cancelled) setPosts(p);
      })
      .catch(() => {
        if (!cancelled) setError(true);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  if (error) return <ErrorState />;
  if (!posts) return <LoadingState />;

  return (
    <div className="mx-auto max-w-3xl">
      <header className="relative rounded-xl border-3 border-paper-sumi bg-paper-butter px-5 py-6 shadow-retro md:px-10 md:py-10">
        <TapeLabel className="absolute -top-3 left-6">BLOG</TapeLabel>
        <h1 className="font-display text-3xl font-black md:text-5xl">{BLOG_LABEL}</h1>
        <p className="mt-3 font-mono text-xs text-paper-sumi/70 md:mt-4 md:text-sm">
          更新公告・文法小知識・學習筆記・雜談，共 {posts.length} 篇
        </p>
      </header>

      <div className="mt-6 flex flex-col gap-4 md:mt-10 md:gap-6">
        {posts.map((post) => (
          <Link
            key={post.slug}
            to={`/blog/${post.slug}`}
            className="card-lift block rounded-xl border-2 border-paper-sumi bg-paper-card p-5 shadow-retro md:p-6"
          >
            <p className="flex flex-wrap items-center gap-3 font-mono text-xs text-paper-sumi/60">
              <span className="rounded border-2 border-paper-sumi bg-paper-butter px-1.5 py-0.5 font-medium text-paper-sumi">
                {post.category}
              </span>
              <time dateTime={post.date.slice(0, 10)}>{post.date.slice(0, 10)}</time>
            </p>
            <h2 className="mt-3 font-display text-lg font-bold leading-snug md:text-2xl">{post.title}</h2>
            {post.excerpt && <p className="mt-2 text-sm text-paper-sumi/70 md:text-base">{post.excerpt}</p>}
            <p className="mt-3 font-mono text-xs text-paper-sumi/60">閱讀全文 →</p>
          </Link>
        ))}
      </div>
    </div>
  );
}
