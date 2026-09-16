/**
 * 部落格資料層：自動掃描 posts/ 下的所有 .md 檔。
 * 新增文章 = 丟一個 .md 檔進 src/data/blog/posts/，不需改任何程式碼。
 * 檔名（去掉 .md）即為文章網址 slug，例如 hello.md → /blog/hello。
 *
 * 每篇文章開頭需有 frontmatter：
 * ---
 * title: 文章標題
 * date: 2026-09-16
 * category: 公告
 * excerpt: 列表頁顯示的一句摘要
 * ---
 */

export interface BlogPostMeta {
  slug: string;
  title: string;
  date: string;
  category: string;
  excerpt: string;
}

export interface BlogPost extends BlogPostMeta {
  body: string;
}

const modules = import.meta.glob<string>('./posts/*.md', {
  query: '?raw',
  import: 'default',
});

function slugFromPath(path: string): string {
  const file = path.split('/').pop() ?? path;
  return file.replace(/\.md$/, '');
}

function parsePost(slug: string, raw: string): BlogPost {
  const match = /^---\r?\n([\s\S]*?)\r?\n---\r?\n?/.exec(raw);
  const meta: Record<string, string> = {};
  let body = raw;
  if (match) {
    body = raw.slice(match[0].length);
    for (const line of match[1].split(/\r?\n/)) {
      const colon = line.indexOf(':');
      if (colon > 0) {
        meta[line.slice(0, colon).trim()] = line.slice(colon + 1).trim();
      }
    }
  }
  return {
    slug,
    title: meta.title ?? slug,
    date: meta.date ?? '',
    category: meta.category ?? '未分類',
    excerpt: meta.excerpt ?? '',
    body: body.trim(),
  };
}

/** 載入全部文章（依日期新→舊排序）。 */
export async function loadPosts(): Promise<BlogPost[]> {
  const posts = await Promise.all(
    Object.entries(modules).map(async ([path, load]) => parsePost(slugFromPath(path), await load())),
  );
  return posts.sort((a, b) => b.date.localeCompare(a.date) || a.slug.localeCompare(b.slug));
}

/** 依 slug 載入單篇文章；不存在回傳 null。 */
export async function loadPost(slug: string): Promise<BlogPost | null> {
  const entry = Object.entries(modules).find(([path]) => slugFromPath(path) === slug);
  if (!entry) return null;
  return parsePost(slug, await entry[1]());
}
