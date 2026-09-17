import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { loadPost, type BlogPost } from '../data/blog';
import { BLOG_LABEL } from '../data/meta';
import { useDocumentTitle } from '../hooks/useDocumentTitle';
import { Breadcrumb } from '../components/Breadcrumb';
import { MarkdownView } from '../components/MarkdownView';
import { LoadingState } from '../components/StatusStates';
import { NotFoundPage } from './NotFoundPage';

type State = { status: 'loading' } | { status: 'notfound' } | { status: 'ready'; post: BlogPost };

export function BlogPostPage() {
  const { slug } = useParams();
  const [state, setState] = useState<State>({ status: 'loading' });

  useEffect(() => {
    let cancelled = false;
    setState({ status: 'loading' });
    if (!slug) {
      setState({ status: 'notfound' });
      return;
    }
    loadPost(slug)
      .then((post) => {
        if (!cancelled) setState(post ? { status: 'ready', post } : { status: 'notfound' });
      })
      .catch(() => {
        if (!cancelled) setState({ status: 'notfound' });
      });
    return () => {
      cancelled = true;
    };
  }, [slug]);

  useDocumentTitle(state.status === 'ready' ? `${state.post.title}｜${BLOG_LABEL}` : BLOG_LABEL);

  // GEO/AEO：注入 BlogPosting 結構化資料，讓搜尋引擎與 AI 引擎理解並引用文章
  useEffect(() => {
    if (state.status !== 'ready') return;
    const { post } = state;
    const script = document.createElement('script');
    script.type = 'application/ld+json';
    script.text = JSON.stringify({
      '@context': 'https://schema.org',
      '@type': 'BlogPosting',
      headline: post.title,
      description: post.excerpt,
      datePublished: post.date.slice(0, 10),
      inLanguage: 'zh-Hant',
      author: { '@type': 'Organization', name: '日檢手帖' },
      publisher: { '@type': 'Organization', name: '日檢手帖' },
      mainEntityOfPage: `https://jlpt.chiaoban.com/blog/${post.slug}`,
    });
    document.head.appendChild(script);
    return () => {
      script.remove();
    };
  }, [state]);

  if (state.status === 'loading') return <LoadingState />;
  if (state.status === 'notfound') return <NotFoundPage />;

  const { post } = state;

  return (
    <div className="mx-auto max-w-3xl">
      <Breadcrumb
        items={[{ label: '首頁', to: '/' }, { label: BLOG_LABEL, to: '/blog' }, { label: post.title }]}
      />

      <article className="mt-8">
        <header>
          <p className="flex flex-wrap items-center gap-3 font-mono text-xs text-paper-sumi/60">
            <span className="rounded border-2 border-paper-sumi bg-paper-butter px-1.5 py-0.5 font-medium text-paper-sumi">
              {post.category}
            </span>
            <time dateTime={post.date.slice(0, 10)}>{post.date.slice(0, 10)}</time>
          </p>
          <h1 className="mt-4 font-display text-2xl font-black leading-snug md:text-4xl">{post.title}</h1>
        </header>

        <div className="mt-8 md:mt-10">
          <MarkdownView body={post.body} />
        </div>
      </article>

      <div className="mt-14">
        <Link to="/blog" className="btn-retro">
          ← 回到{BLOG_LABEL}
        </Link>
      </div>
    </div>
  );
}
