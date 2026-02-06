'use client';

import { useEffect, useState, useRef, useCallback } from 'react';
import Link from 'next/link';
import { Document as DocType, Backlink } from '@/types';
import { markdownToHtml, transformBacklinks, extractHeadings } from '@/lib/markdown';
import { formatDate } from '@/lib/markdown';
import { Clock, Calendar, Tag, ArrowUpRight, Link2, Loader2, AlertCircle, FileQuestion } from 'lucide-react';

// Loading skeleton component
function DocumentSkeleton() {
  return (
    <div className="animate-pulse">
      {/* Header skeleton */}
      <div className="mb-8 md:mb-10 space-y-4">
        <div className="flex items-center gap-2 text-sm">
          <div className="h-5 w-20 bg-gray-800 rounded-md" />
          <div className="h-4 w-4 bg-gray-800 rounded" />
          <div className="h-5 w-24 bg-gray-800 rounded-md" />
          <div className="h-4 w-4 bg-gray-800 rounded" />
          <div className="h-5 w-20 bg-gray-800 rounded-md" />
        </div>
        <div className="h-10 bg-gray-800 rounded-lg w-3/4 shimmer" />
        <div className="h-5 bg-gray-800 rounded w-1/2 shimmer" />
        <div className="h-6 w-32 bg-gray-800/50 rounded-full shimmer" />
      </div>
      {/* Content skeleton */}
      <div className="space-y-4">
        {[...Array(6)].map((_, i) => (
          <div key={i} className="space-y-2">
            <div className="h-6 bg-gray-800 rounded w-1/3 shimmer" />
            <div className="h-4 bg-gray-800/50 rounded w-full shimmer" />
            <div className="h-4 bg-gray-800/50 rounded w-5/6 shimmer" />
            <div className="h-4 bg-gray-800/50 rounded w-4/6 shimmer" />
          </div>
        ))}
      </div>
    </div>
  );
}

// Empty state component
function EmptyBacklinks() {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <div className="p-4 bg-gray-800/30 rounded-full mb-4">
        <FileQuestion className="w-8 h-8 text-gray-600" />
      </div>
      <p className="text-gray-400 font-medium">No backlinks yet</p>
      <p className="text-sm text-gray-600 mt-1 max-w-xs">
        Other documents will appear here when they link to this page
      </p>
    </div>
  );
}

// Error state component
function ErrorState({ message, onRetry }: { message: string; onRetry?: () => void }) {
  return (
    <div className="flex flex-col items-center justify-center py-16 text-center px-4">
      <div className="p-4 bg-red-500/10 rounded-full mb-4">
        <AlertCircle className="w-10 h-10 text-red-400" />
      </div>
      <h3 className="text-lg font-semibold text-gray-200 mb-2">Unable to load content</h3>
      <p className="text-gray-400 text-sm max-w-md">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="mt-6 px-4 py-2 bg-gray-800 hover:bg-gray-700 text-gray-300 rounded-lg transition-colors touch-manipulation min-h-[44px] flex items-center gap-2"
        >
          <Loader2 className="w-4 h-4" />
          Try again
        </button>
      )}
    </div>
  );
}

interface DocumentViewerProps {
  doc: DocType;
  backlinks: Backlink[];
}

export function DocumentViewer({ doc, backlinks }: DocumentViewerProps) {
  const [htmlContent, setHtmlContent] = useState('');
  const [headings, setHeadings] = useState<Array<{ level: number; text: string; id: string }>>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const contentRef = useRef<HTMLDivElement>(null);

  const processContent = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      // Transform backlinks first, then convert to HTML
      const processedContent = transformBacklinks(doc.content);
      const html = await markdownToHtml(processedContent);
      setHtmlContent(html);
      
      // Extract headings for TOC
      const extractedHeadings = extractHeadings(doc.content);
      setHeadings(extractedHeadings);
    } catch (err) {
      setError('Failed to render document content. Please try again.');
      console.error('Error processing content:', err);
    } finally {
      setIsLoading(false);
    }
  }, [doc.content]);

  useEffect(() => {
    processContent();
  }, [processContent]);

  // Smooth scroll to heading on click
  const handleHeadingClick = useCallback((e: React.MouseEvent<HTMLAnchorElement>, id: string) => {
    e.preventDefault();
    const element = (globalThis.document as Document).querySelector<HTMLElement>(`#${id}`);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
      // Update URL without triggering navigation
      globalThis.history.pushState(null, '', `#${id}`);
    }
  }, []);

  return (
    <div className="flex h-full">
      {/* Main Content */}
      <div className="flex-1 overflow-y-auto scroll-smooth">
        <article className="max-w-3xl mx-auto px-4 py-8 md:px-8 md:py-12">
          {error ? (
            <ErrorState message={error} onRetry={processContent} />
          ) : isLoading ? (
            <DocumentSkeleton />
          ) : (
            <>
              {/* Header */}
              <header className="mb-8 md:mb-10 animate-in fade-in slide-in-from-bottom-4 duration-500">
                <div className="flex items-center gap-2 text-sm text-gray-500 mb-4 flex-wrap">
                  <span className="capitalize px-2.5 py-1 bg-gray-800/60 rounded-md text-xs font-medium text-gray-300 transition-colors hover:bg-gray-800">
                    {doc.frontmatter.category}
                  </span>
                  <span className="text-gray-700" aria-hidden="true">•</span>
                  <span className="flex items-center gap-1.5">
                    <Calendar className="w-3.5 h-3.5" aria-hidden="true" />
                    <time dateTime={doc.frontmatter.date}>
                      {formatDate(doc.frontmatter.date)}
                    </time>
                  </span>
                  <span className="text-gray-700" aria-hidden="true">•</span>
                  <span className="flex items-center gap-1.5">
                    <Clock className="w-3.5 h-3.5" aria-hidden="true" />
                    {doc.readingTime} min read
                  </span>
                </div>

                <h1 className="text-2.5xl md:text-3.5xl lg:text-4.5xl font-bold text-gray-100 mb-5 leading-[1.2] tracking-tight">
                  {doc.frontmatter.title}
                </h1>

                {doc.frontmatter.description && (
                  <p className="text-lg md:text-xl text-gray-400 leading-relaxed max-w-2xl animate-in fade-in slide-in-from-bottom-2 duration-300" style={{ animationDelay: '100ms' }}>
                    {doc.frontmatter.description}
                  </p>
                )}

                {/* Tags */}
                {doc.frontmatter.tags?.length > 0 && (
                  <div className="flex items-center gap-2.5 mt-6 flex-wrap">
                    <Tag className="w-4 h-4 text-gray-500 flex-shrink-0" aria-hidden="true" />
                    {doc.frontmatter.tags.map((tag) => (
                      <Link
                        key={tag}
                        href={`/tags/${encodeURIComponent(tag)}`}
                        className="px-3 py-1.5 bg-gray-800/50 hover:bg-gray-800 text-gray-400 hover:text-gray-200 text-sm rounded-full transition-all duration-200 ease-out hover:scale-105 touch-manipulation focus:outline-none focus:ring-2 focus:ring-blue-500/50"
                        aria-label={`View tag: ${tag}`}
                      >
                        {tag}
                      </Link>
                    ))}
                  </div>
                )}
              </header>

              {/* Content */}
              <div 
                ref={contentRef}
                className="prose prose-invert prose-lg max-w-none
                  prose-headings:text-gray-100 prose-headings:font-semibold prose-headings:tracking-tight
                  prose-h1:text-2.5xl prose-h1:mt-12 prose-h1:mb-6
                  prose-h2:text-xl prose-h2:mt-10 prose-h2:mb-4 prose-h2:font-semibold
                  prose-h3:text-lg prose-h3:mt-8 prose-h3:mb-3
                  prose-p:text-gray-300 prose-p:leading-8 prose-p:mb-6 prose-p:text-[1.05rem]
                  prose-a:text-blue-400 prose-a:no-underline prose-a:transition-colors prose-a:duration-200 hover:prose-a:text-blue-300 hover:prose-a:underline-offset-4
                  prose-strong:text-gray-200 prose-strong:font-medium
                  prose-code:text-gray-300 prose-code:bg-gray-800/70 prose-code:px-1.5 prose-code:py-0.5 prose-code:rounded-md prose-code:text-sm prose-code:font-medium
                  prose-pre:bg-gray-900 prose-pre:border prose-pre:border-gray-800 prose-pre:rounded-xl prose-pre:shadow-lg
                  prose-blockquote:border-l-4 prose-blockquote:border-gray-700 prose-blockquote:bg-gray-800/20 prose-blockquote:pl-5 prose-blockquote:py-2 prose-blockquote:not-italic prose-blockquote:rounded-r-lg
                  prose-ul:text-gray-300 prose-ul:marker:text-gray-600
                  prose-ol:text-gray-300 prose-ol:marker:text-gray-600
                  prose-li:my-2
                  prose-table:text-gray-300 prose-table:border-collapse prose-table:w-full
                  prose-th:text-gray-200 prose-th:font-semibold prose-th:bg-gray-800/50 prose-th:p-4 prose-th:text-left
                  prose-td:p-4 prose-td:border-t prose-td:border-gray-800
                  prose-img:rounded-xl prose-img:shadow-lg prose-img:max-w-full prose-img:my-8
                  prose hr:border-gray-800 prose hr:my-10
                "
                dangerouslySetInnerHTML={{ __html: htmlContent }}
              />

              {/* Backlinks */}
              <section className="mt-14 pt-8 border-t border-gray-800/60 animate-in fade-in slide-in-from-bottom-4 duration-500" style={{ animationDelay: '200ms' }}>
                <h3 className="flex items-center gap-2.5 text-lg font-semibold text-gray-200 mb-5">
                  <Link2 className="w-5 h-5 text-gray-500 flex-shrink-0" aria-hidden="true" />
                  <span>Linked from</span>
                  <span className="text-gray-600 font-normal">({backlinks.length})</span>
                </h3>
                {backlinks.length > 0 ? (
                  <div className="grid gap-3">
                    {backlinks.map((backlink, index) => (
                      <Link
                        key={backlink.slug}
                        href={`/docs/${backlink.slug}`}
                        style={{ animationDelay: `${index * 50 + 100}ms` }}
                        className="group p-5 bg-gray-800/20 hover:bg-gray-800/50 border border-gray-800/60 hover:border-gray-700 rounded-xl transition-all duration-300 ease-out hover:shadow-lg hover:shadow-black/20 hover:-translate-y-0.5 touch-manipulation focus:outline-none focus:ring-2 focus:ring-blue-500/50 animate-in fade-in slide-in-from-bottom-2"
                      >
                        <div className="flex items-start justify-between gap-4">
                          <div className="flex-1 min-w-0">
                            <h4 className="font-medium text-gray-200 group-hover:text-blue-400 transition-colors duration-200">
                              {backlink.title}
                            </h4>
                            <p className="text-sm text-gray-500 mt-2 line-clamp-2 leading-relaxed group-hover:text-gray-400 transition-colors">
                              {backlink.excerpt}
                            </p>
                          </div>
                          <ArrowUpRight className="w-5 h-5 text-gray-600 group-hover:text-gray-400 flex-shrink-0 ml-2 transition-all duration-200 group-hover:translate-x-0.5 group-hover:-translate-y-0.5" />
                        </div>
                      </Link>
                    ))}
                  </div>
                ) : (
                  <EmptyBacklinks />
                )}
              </section>
            </>
          )}
        </article>
      </div>

      {/* Table of Contents - Sticky Sidebar */}
      {!isLoading && !error && headings.length > 0 && (
        <aside className="hidden xl:block w-64 border-l border-gray-800/60 flex-shrink-0">
          <div className="sticky top-0 p-6">
            <h4 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-4">
              On this page
            </h4>
            <nav className="space-y-1" aria-label="Table of contents">
              {headings.map((heading) => (
                <a
                  key={heading.id}
                  href={`#${heading.id}`}
                  onClick={(e) => handleHeadingClick(e, heading.id)}
                  className={`
                    block text-sm transition-all duration-200 py-1.5 px-2 rounded-md -mx-2
                    ${heading.level === 1 
                      ? 'text-gray-400 hover:text-gray-200 hover:bg-gray-800/50' 
                      : ''
                    }
                    ${heading.level === 2 
                      ? 'text-gray-500 hover:text-gray-300 pl-3 hover:bg-gray-800/30' 
                      : ''
                    }
                    ${heading.level >= 3 
                      ? 'text-gray-600 hover:text-gray-400 pl-6 hover:bg-gray-800/20 text-xs' 
                      : ''
                    }
                    focus:outline-none focus:ring-2 focus:ring-blue-500/50 rounded-md
                  `}
                  aria-label={`Navigate to: ${heading.text}`}
                >
                  <span className="line-clamp-1">{heading.text}</span>
                </a>
              ))}
            </nav>
          </div>
        </aside>
      )}
    </div>
  );
}
