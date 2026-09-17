import { Fragment, type ReactNode } from 'react';

/**
 * 極簡 Markdown 渲染器（不引入外部套件）。
 * 支援：#/##/### 標題、段落、- 清單、1. 有序清單、> 引用、--- 分隔線、| 表格，
 * 以及行內 **粗體**、`程式碼`、[連結](url)。
 */

function renderInline(text: string): ReactNode[] {
  const parts = text.split(/(\*\*[^*]+\*\*|`[^`]+`|\[[^\]]+\]\([^)]+\))/g);
  return parts.map((part, i) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={i}>{part.slice(2, -2)}</strong>;
    }
    if (part.startsWith('`') && part.endsWith('`')) {
      return (
        <code key={i} className="rounded bg-paper-oatmeal px-1.5 py-0.5 font-mono text-[0.9em]">
          {part.slice(1, -1)}
        </code>
      );
    }
    const link = /^\[([^\]]+)\]\(([^)]+)\)$/.exec(part);
    if (link) {
      return (
        <a
          key={i}
          href={link[2]}
          target="_blank"
          rel="noreferrer"
          className="underline decoration-2 underline-offset-4 hover:bg-paper-butter"
        >
          {link[1]}
        </a>
      );
    }
    return <Fragment key={i}>{part}</Fragment>;
  });
}

function renderLines(text: string): ReactNode[] {
  return text.split('\n').map((line, i, arr) => (
    <Fragment key={i}>
      {renderInline(line)}
      {i < arr.length - 1 && <br />}
    </Fragment>
  ));
}

export function MarkdownView({ body }: { body: string }) {
  const blocks = body
    .split(/\n{2,}/)
    .map((b) => b.trim())
    .filter(Boolean);

  return (
    <div className="flex flex-col gap-6">
      {blocks.map((block, i) => {
        const heading = /^(#{1,3})\s+(.*)$/.exec(block);
        if (heading) {
          const text = renderInline(heading[2]);
          if (heading[1].length === 1)
            return (
              <h2 key={i} className="mt-4 font-display text-2xl font-black md:text-3xl">
                {text}
              </h2>
            );
          if (heading[1].length === 2)
            return (
              <h2 key={i} className="mt-4 font-display text-xl font-bold md:text-2xl">
                {text}
              </h2>
            );
          return (
            <h3 key={i} className="mt-2 font-display text-lg font-bold md:text-xl">
              {text}
            </h3>
          );
        }

        if (/^-{3,}$/.test(block)) {
          return <hr key={i} className="border-t-2 border-dashed border-paper-sumi/40" />;
        }

        const lines = block.split('\n');

        if (
          lines.length >= 2 &&
          lines.every((l) => l.startsWith('|')) &&
          /^\|[\s:|-]+\|$/.test(lines[1])
        ) {
          const parseRow = (l: string) =>
            l
              .replace(/^\|/, '')
              .replace(/\|$/, '')
              .split('|')
              .map((c) => c.trim());
          const header = parseRow(lines[0]);
          const rows = lines.slice(2).map(parseRow);
          return (
            <div key={i} className="overflow-x-auto">
              <table className="w-full border-collapse border-2 border-paper-sumi text-sm md:text-base">
                <thead>
                  <tr className="bg-paper-butter">
                    {header.map((cell, j) => (
                      <th
                        key={j}
                        className="border-2 border-paper-sumi px-3 py-2 text-left font-bold"
                      >
                        {renderInline(cell)}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {rows.map((row, j) => (
                    <tr key={j} className={j % 2 === 1 ? 'bg-paper-oatmeal/50' : undefined}>
                      {row.map((cell, k) => (
                        <td key={k} className="border-2 border-paper-sumi px-3 py-2 align-top">
                          {renderInline(cell)}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          );
        }

        if (lines.every((l) => l.startsWith('- '))) {
          return (
            <ul key={i} className="flex list-disc flex-col gap-2 pl-6 marker:text-level">
              {lines.map((l, j) => (
                <li key={j}>{renderInline(l.slice(2))}</li>
              ))}
            </ul>
          );
        }

        if (lines.every((l) => /^\d+\.\s/.test(l))) {
          return (
            <ol key={i} className="flex list-decimal flex-col gap-2 pl-6 font-medium marker:font-mono">
              {lines.map((l, j) => (
                <li key={j} className="font-normal">
                  {renderInline(l.replace(/^\d+\.\s/, ''))}
                </li>
              ))}
            </ol>
          );
        }

        if (lines.every((l) => l.startsWith('>'))) {
          return (
            <blockquote key={i} className="rounded-lg bg-paper-butter px-4 py-3 leading-loose md:px-5 md:py-4">
              {renderLines(lines.map((l) => l.replace(/^>\s?/, '')).join('\n'))}
            </blockquote>
          );
        }

        return <p key={i}>{renderLines(block)}</p>;
      })}
    </div>
  );
}
