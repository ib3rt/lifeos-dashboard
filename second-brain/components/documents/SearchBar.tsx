'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Search, X, Command, FileText, ArrowRight, Loader2, Keyboard } from 'lucide-react';
import { Document } from '@/types';
import { formatDate } from '@/lib/markdown';

interface SearchBarProps {
  documents: Document[];
}

export function SearchBar({ documents }: SearchBarProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const router = useRouter();
  const inputRef = useRef<HTMLInputElement>(null);
  const resultsRef = useRef<HTMLDivElement>(null);

  const filteredDocs = query.length > 0
    ? documents.filter(doc =>
        doc.frontmatter.title.toLowerCase().includes(query.toLowerCase()) ||
        doc.content.toLowerCase().includes(query.toLowerCase()) ||
        doc.frontmatter.tags?.some(tag => tag.toLowerCase().includes(query.toLowerCase()))
      ).slice(0, 8)
    : documents.slice(0, 5);

  const handleSelect = useCallback((slug: string) => {
    setIsOpen(false);
    setQuery('');
    router.push(`/docs/${slug}`);
  }, [router]);

  // Reset selected index when results change
  useEffect(() => {
    setSelectedIndex(0);
  }, [filteredDocs.length]);

  // Focus input when opened
  useEffect(() => {
    if (isOpen) {
      requestAnimationFrame(() => {
        inputRef.current?.focus();
      });
    }
  }, [isOpen]);

  // Keyboard shortcut to open search
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setIsOpen(true);
      }
      if (e.key === 'Escape') {
        setIsOpen(false);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  // Handle keyboard navigation in results
  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelectedIndex(prev => Math.min(prev + 1, filteredDocs.length - 1));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelectedIndex(prev => Math.max(prev - 1, 0));
    } else if (e.key === 'Enter' && filteredDocs.length > 0) {
      e.preventDefault();
      handleSelect(filteredDocs[selectedIndex].slug);
    }
  }, [filteredDocs, selectedIndex, handleSelect]);

  // Simulate loading state
  useEffect(() => {
    if (isOpen && query.length > 0) {
      setIsLoading(true);
      const timer = setTimeout(() => setIsLoading(false), 150);
      return () => clearTimeout(timer);
    }
    setIsLoading(false);
  }, [isOpen, query]);

  return (
    <>
      {/* Search Trigger */}
      <button
        onClick={() => setIsOpen(true)}
        className="flex items-center gap-2 px-3 py-1.5 bg-gray-800/50 hover:bg-gray-800 border border-gray-700 hover:border-gray-600 rounded-lg text-sm text-gray-400 hover:text-gray-300 transition-all min-h-[36px] md:min-h-[unset] focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:ring-offset-2 focus:ring-offset-gray-950"
        aria-label="Open search"
      >
        <Search className="w-4 h-4" aria-hidden="true" />
        <span className="hidden xs:inline">Search...</span>
        <kbd className="hidden sm:inline-flex items-center gap-1 px-1.5 py-0.5 bg-gray-700/50 rounded text-xs text-gray-500">
          <Command className="w-3 h-3" aria-hidden="true" />
          <span>K</span>
        </kbd>
      </button>

      {/* Search Modal */}
      {isOpen && (
        <div 
          className="fixed inset-0 z-50 flex items-start justify-center pt-[10vh] sm:pt-[20vh] bg-black/60 backdrop-blur-sm p-4 animate-in fade-in"
          onClick={() => setIsOpen(false)}
          role="dialog"
          aria-modal="true"
          aria-label="Search documents"
        >
          <div 
            className="w-full max-w-2xl bg-gray-900 border border-gray-800 rounded-2xl shadow-2xl overflow-hidden animate-in scale-in-95 fade-in duration-200"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Search Input */}
            <div className="flex items-center gap-3 p-4 border-b border-gray-800">
              <Search className="w-5 h-5 text-gray-500 flex-shrink-0" aria-hidden="true" />
              <input
                ref={inputRef}
                type="text"
                placeholder="Search documents, tags, content..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={handleKeyDown}
                className="flex-1 bg-transparent text-gray-200 placeholder-gray-600 outline-none text-base md:text-lg min-h-[44px]"
                aria-autocomplete="list"
                aria-controls="search-results"
              />
              {isLoading ? (
                <Loader2 className="w-5 h-5 text-gray-500 animate-spin" aria-hidden="true" />
              ) : query ? (
                <button
                  onClick={() => setQuery('')}
                  className="p-2 hover:bg-gray-800 rounded-lg text-gray-500 hover:text-gray-300 transition-colors touch-manipulation min-w-[44px] min-h-[44px] flex items-center justify-center"
                  aria-label="Clear search"
                >
                  <X className="w-4 h-4" aria-hidden="true" />
                </button>
              ) : null}
              <kbd className="hidden sm:inline-block px-2 py-1 bg-gray-800 rounded text-xs text-gray-500">
                ESC
              </kbd>
            </div>

            {/* Results */}
            <div 
              id="search-results"
              ref={resultsRef}
              className="max-h-[60vh] overflow-y-auto py-2 scrollbar-thin"
              role="listbox"
            >
              {isLoading ? (
                // Loading skeleton
                [...Array(3)].map((_, i) => (
                  <div key={i} className="px-4 py-3 animate-pulse">
                    <div className="flex items-center gap-3">
                      <div className="w-5 h-5 bg-gray-800 rounded shimmer" />
                      <div className="flex-1">
                        <div className="h-4 bg-gray-800 rounded w-1/3 mb-2 shimmer" />
                        <div className="h-3 bg-gray-800/50 rounded w-1/4 shimmer" />
                      </div>
                    </div>
                  </div>
                ))
              ) : filteredDocs.length === 0 ? (
                <div className="p-8 text-center">
                  <div className="p-3 bg-gray-800/30 rounded-full w-fit mx-auto mb-3">
                    <Search className="w-6 h-6 text-gray-600" />
                  </div>
                  <p className="text-gray-400 font-medium">No results found</p>
                  <p className="text-sm text-gray-600 mt-1">
                    Try searching for something else
                  </p>
                </div>
              ) : (
                <>
                  <div className="px-4 py-2 text-xs font-medium text-gray-600 uppercase tracking-wider flex items-center gap-2">
                    {query ? 'Search Results' : 'Recent Documents'}
                    <span className="ml-auto text-gray-700 font-normal">{filteredDocs.length}</span>
                  </div>
                  {filteredDocs.map((doc, index) => (
                    <button
                      key={doc.slug}
                      onClick={() => handleSelect(doc.slug)}
                      style={{ animationDelay: `${index * 40}ms` }}
                      className={`
                        w-full flex items-start gap-3 px-4 py-3 transition-all duration-200 group text-left touch-manipulation min-h-[52px]
                        ${index === selectedIndex 
                          ? 'bg-gray-800/70 text-gray-100' 
                          : 'hover:bg-gray-800/40 text-gray-300'
                        }
                        focus:outline-none focus:bg-gray-800/70
                        animate-in fade-in slide-in-from-bottom-2
                      `}
                      role="option"
                      aria-selected={index === selectedIndex}
                    >
                      <div className="relative">
                        <FileText className={`w-5 h-5 mt-0.5 flex-shrink-0 transition-colors ${index === selectedIndex ? 'text-blue-400' : 'text-gray-600 group-hover:text-gray-400'}`} aria-hidden="true" />
                        {index === selectedIndex && (
                          <span className="absolute -left-2 top-1/2 -translate-y-1/2 w-1 h-4 bg-blue-400 rounded-full animate-pulse" />
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 flex-wrap">
                          <span className={`font-medium transition-colors ${index === selectedIndex ? 'text-gray-100' : 'text-gray-300 group-hover:text-gray-100'}`}>
                            {doc.frontmatter.title}
                          </span>
                          <span className="text-xs text-gray-600 capitalize px-1.5 py-0.5 bg-gray-800/50 rounded transition-colors group-hover:bg-gray-800">
                            {doc.frontmatter.category}
                          </span>
                        </div>
                        <div className="flex items-center gap-2 text-sm text-gray-600 mt-1 flex-wrap">
                          <time dateTime={doc.frontmatter.date}>{formatDate(doc.frontmatter.date)}</time>
                          {doc.frontmatter.tags && doc.frontmatter.tags.length > 0 && (
                            <>
                              <span className="text-gray-700">•</span>
                              <span className="truncate max-w-[150px] xs:max-w-[200px] group-hover:text-gray-400 transition-colors">
                                {doc.frontmatter.tags.slice(0, 3).join(', ')}
                              </span>
                            </>
                          )}
                        </div>
                      </div>
                      <ArrowRight className={`w-5 h-4 transition-all flex-shrink-0 ${index === selectedIndex ? 'text-blue-400 opacity-100 translate-x-0' : 'text-gray-700 opacity-0 group-hover:opacity-100'}`} aria-hidden="true" />
                    </button>
                  ))}
                </>
              )}
            </div>

            {/* Footer */}
            <div className="flex items-center justify-between px-4 py-3 bg-gray-800/30 border-t border-gray-800 text-xs text-gray-600 flex-wrap gap-2">
              <div className="flex items-center gap-4">
                <span className="flex items-center gap-1.5">
                  <kbd className="px-1.5 py-0.5 bg-gray-800 rounded text-gray-500 font-mono">↑↓</kbd>
                  <span className="hidden xs:inline">navigate</span>
                </span>
                <span className="flex items-center gap-1.5">
                  <kbd className="px-1.5 py-0.5 bg-gray-800 rounded text-gray-500 font-mono">↵</kbd>
                  <span className="hidden xs:inline">select</span>
                </span>
              </div>
              <Link
                href="/search"
                onClick={() => setIsOpen(false)}
                className="text-gray-500 hover:text-gray-400 transition-colors touch-manipulation flex items-center gap-1"
              >
                Advanced search
                <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
              </Link>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
