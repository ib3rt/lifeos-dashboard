import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkGfm from 'remark-gfm';
import remarkRehype from 'remark-rehype';
import rehypeHighlight from 'rehype-highlight';
import rehypeSlug from 'rehype-slug';
import rehypeAutolinkHeadings from 'rehype-autolink-headings';
import rehypeStringify from 'rehype-stringify';

// Cache for processed markdown
const htmlCache = new Map<string, string>();
const headingsCache = new Map<string, Array<{ level: number; text: string; id: string }>>();

export async function markdownToHtml(markdown: string): Promise<string> {
  // Check cache first
  if (htmlCache.has(markdown)) {
    return htmlCache.get(markdown)!;
  }

  const result = await unified()
    .use(remarkParse)
    .use(remarkGfm)
    .use(remarkRehype, { allowDangerousHtml: true })
    .use(rehypeSlug)
    .use(rehypeAutolinkHeadings, {
      behavior: 'wrap',
      properties: {
        className: ['anchor-link'],
      },
    })
    .use(rehypeHighlight)
    .use(rehypeStringify, { allowDangerousHtml: true })
    .process(markdown);

  const html = result.toString();
  
  // Cache the result (limit cache size to prevent memory issues)
  if (htmlCache.size > 100) {
    // Clear oldest entries when cache is full
    const firstKey = htmlCache.keys().next().value;
    if (firstKey !== undefined) {
      htmlCache.delete(firstKey);
    }
  }
  htmlCache.set(markdown, html);

  return html;
}

export function extractHeadings(content: string): Array<{ level: number; text: string; id: string }> {
  // Check cache first
  if (headingsCache.has(content)) {
    return headingsCache.get(content)!;
  }
  
  const headings: Array<{ level: number; text: string; id: string }> = [];
  const lines = content.split('\n');
  
  for (const line of lines) {
    const match = line.match(/^(#{1,6})\s+(.+)$/);
    if (match) {
      const level = match[1].length;
      const text = match[2]?.trim() || '';
      const id = text.toLowerCase().replace(/[^\w\s-]/g, '').replace(/\s+/g, '-');
      headings.push({ level, text, id });
    }
  }
  
  // Cache the result
  headingsCache.set(content, headings);
  
  return headings;
}

export function transformBacklinks(content: string): string {
  // Convert [[Link]] to [Link](/docs/link)
  return content.replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g, (match, link, alias) => {
    const displayText = alias || link;
    const slug = link.toLowerCase().replace(/\s+/g, '-');
    return `[${displayText}](/docs/${slug})`;
  });
}

export function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  }).format(date);
}

export function getRelativeTime(dateString: string): string {
  const date = new Date(dateString);
  const now = new Date();
  const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000);
  
  if (diffInSeconds < 60) return 'just now';
  if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}m ago`;
  if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}h ago`;
  if (diffInSeconds < 604800) return `${Math.floor(diffInSeconds / 86400)}d ago`;
  
  return formatDate(dateString);
}

// Clear all caches (useful for development)
export function clearMarkdownCache() {
  htmlCache.clear();
  headingsCache.clear();
}
