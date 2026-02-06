'use client';

import { useState, useEffect, useMemo, useRef } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Search, FileText, BookOpen, FolderGit2, Bookmark, Calendar, ChevronRight, Hash, Loader2, X, ChevronDown, Folder, Filter } from 'lucide-react';
import { Document } from '@/types';
import { formatDate } from '@/lib/markdown';

// Debounce hook
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
}

interface DocumentListProps {
  documents: Document[];
  currentSlug?: string;
}

const categoryIcons = {
  journal: Calendar,
  concepts: BookOpen,
  projects: FolderGit2,
  reference: Bookmark,
};

const categoryLabels = {
  journal: 'Journal',
  concepts: 'Concepts',
  projects: 'Projects',
  reference: 'Reference',
};

const categoryColors = {
  journal: 'text-blue-400',
  concepts: 'text-purple-400',
  projects: 'text-emerald-400',
  reference: 'text-amber-400',
};

const categoryHoverColors = {
  journal: 'hover:bg-blue-500/10',
  concepts: 'hover:bg-purple-500/10',
  projects: 'hover:bg-emerald-500/10',
  reference: 'hover:bg-amber-500/10',
};

export function DocumentList({ documents, currentSlug }: DocumentListProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  const [expandedCategories, setExpandedCategories] = useState<Record<string, boolean>>({
    journal: true,
    concepts: true,
    projects: true,
    reference: true,
  });
  const [selectedFolder, setSelectedFolder] = useState<string | null>(null);
  const [showFolderDropdown, setShowFolderDropdown] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const pathname = usePathname();

  // Debounce search query with 300ms delay
  const debouncedSearchQuery = useDebounce(searchQuery, 300);

  // Get unique folders for filter dropdown
  const folders = useMemo(() => {
    const folderSet = new Set(documents.map(doc => doc.frontmatter.category));
    return Array.from(folderSet).sort();
  }, [documents]);

  // Update searching state
  useEffect(() => {
    setIsSearching(searchQuery.length > 0 && searchQuery !== debouncedSearchQuery);
  }, [searchQuery, debouncedSearchQuery]);

  // Auto-expand category of current document
  useEffect(() => {
    if (currentSlug) {
      const currentDoc = documents.find(d => d.slug === currentSlug);
      if (currentDoc) {
        setExpandedCategories(prev => ({
          ...prev,
          [currentDoc.frontmatter.category]: true,
        }));
      }
    }
  }, [currentSlug, documents]);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setShowFolderDropdown(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Apply folder filter first
  const filteredByFolder = useMemo(() => {
    if (!selectedFolder) return documents;
    return documents.filter(doc => doc.frontmatter.category === selectedFolder);
  }, [documents, selectedFolder]);

  // Memoize filtered documents (apply search on top of folder filter)
  const filteredDocs = useMemo(() => {
    if (!debouncedSearchQuery) {
      return filteredByFolder;
    }
    const lowerQuery = debouncedSearchQuery.toLowerCase();
    return filteredByFolder.filter(doc =>
      doc.frontmatter.title.toLowerCase().includes(lowerQuery) ||
      doc.frontmatter.tags?.some(tag => tag.toLowerCase().includes(lowerQuery))
    );
  }, [filteredByFolder, debouncedSearchQuery]);

  // Memoize documents by category
  const docsByCategory = useMemo(() => {
    return filteredDocs.reduce((acc, doc) => {
      const cat = doc.frontmatter.category;
      if (!acc[cat]) acc[cat] = [];
      acc[cat].push(doc);
      return acc;
    }, {} as Record<string, Document[]>);
  }, [filteredDocs]);

  const toggleCategory = (category: string) => {
    setExpandedCategories(prev => ({
      ...prev,
      [category]: !prev[category],
    }));
  };

  const clearFolderFilter = () => {
    setSelectedFolder(null);
  };

  const getFolderLabel = (folder: string) => {
    return categoryLabels[folder as keyof typeof categoryLabels] || folder;
  };

  // Calculate total count
  const totalCount = Object.values(docsByCategory).reduce(
    (sum, cats) => sum + cats.length, 0
  );

  return (
    <div className="h-full flex flex-col">
      {/* Folder Filter */}
      <div className="p-4 border-b border-gray-800">
        <div className="relative" ref={dropdownRef}>
          <div className="flex items-center gap-2 mb-2">
            <Filter className="w-3.5 h-3.5 text-gray-500" />
            <span className="text-xs font-medium text-gray-500 uppercase tracking-wider">Filter by Folder</span>
          </div>
          <button
            onClick={() => setShowFolderDropdown(!showFolderDropdown)}
            className="w-full flex items-center justify-between gap-2 px-3 py-2.5 bg-gray-900 border border-gray-800 rounded-lg text-sm text-gray-300 hover:border-gray-700 hover:text-gray-200 transition-all min-h-[40px]"
            aria-expanded={showFolderDropdown}
            aria-haspopup="listbox"
          >
            <span className="truncate flex items-center gap-2">
              <Folder className="w-4 h-4 text-gray-500" />
              {selectedFolder ? getFolderLabel(selectedFolder) : 'All Folders'}
            </span>
            <ChevronDown className={`w-4 h-4 text-gray-500 transition-transform ${showFolderDropdown ? 'rotate-180' : ''}`} />
          </button>

          {/* Folder Dropdown */}
          {showFolderDropdown && (
            <div className="absolute z-20 w-full mt-1 bg-gray-900 border border-gray-800 rounded-lg shadow-lg overflow-hidden animate-in fade-in duration-150">
              <button
                onClick={() => {
                  setSelectedFolder(null);
                  setShowFolderDropdown(false);
                }}
                className={`w-full flex items-center gap-2 px-3 py-2.5 text-sm transition-colors min-h-[40px] ${
                  !selectedFolder ? 'bg-gray-800 text-gray-100' : 'text-gray-300 hover:bg-gray-800'
                }`}
              >
                <Folder className="w-4 h-4" />
                <span className="font-medium">All Folders</span>
                <span className="ml-auto text-xs text-gray-600">{documents.length}</span>
              </button>
              {folders.map((folder) => {
                const Icon = categoryIcons[folder as keyof typeof categoryIcons] || Folder;
                const count = documents.filter(doc => doc.frontmatter.category === folder).length;
                return (
                  <button
                    key={folder}
                    onClick={() => {
                      setSelectedFolder(folder);
                      setShowFolderDropdown(false);
                    }}
                    className={`w-full flex items-center gap-2 px-3 py-2.5 text-sm transition-colors min-h-[40px] ${
                      selectedFolder === folder ? 'bg-gray-800 text-gray-100' : 'text-gray-300 hover:bg-gray-800'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    <span className="font-medium">{getFolderLabel(folder)}</span>
                    <span className="ml-auto text-xs text-gray-600">{count}</span>
                  </button>
                );
              })}
            </div>
          )}

          {/* Active Filter Indicator */}
          {selectedFolder && (
            <div className="flex items-center gap-2 mt-2 px-2 py-1.5 bg-blue-500/10 border border-blue-500/20 rounded-lg">
              <Folder className="w-3.5 h-3.5 text-blue-400" />
              <span className="text-xs text-blue-400 font-medium">
                Filtering: {getFolderLabel(selectedFolder)}
              </span>
              <button
                onClick={clearFolderFilter}
                className="ml-auto p-1 hover:bg-blue-500/20 rounded transition-colors"
                aria-label="Clear filter"
              >
                <X className="w-3.5 h-3.5 text-blue-400" />
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Breadcrumb */}
      {selectedFolder && (
        <div className="px-4 py-2 border-b border-gray-800 bg-gray-900/30">
          <div className="flex items-center gap-2 text-xs">
            <Folder className="w-3.5 h-3.5 text-blue-400" />
            <span className="text-gray-500">Active filter:</span>
            <span className="text-blue-400 font-medium">{getFolderLabel(selectedFolder)}</span>
            <button
              onClick={clearFolderFilter}
              className="ml-auto flex items-center gap-1 text-gray-500 hover:text-gray-300 transition-colors"
            >
              <X className="w-3 h-3" />
              <span>Clear</span>
            </button>
          </div>
        </div>
      )}

      {/* Search */}
      <div className="p-4 border-b border-gray-800">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500 transition-colors" />
          <input
            type="text"
            placeholder={selectedFolder ? `Search in ${getFolderLabel(selectedFolder)}...` : "Search documents..."}
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-9 py-2.5 bg-gray-900 border border-gray-800 rounded-lg text-sm text-gray-200 placeholder-gray-600 focus:outline-none focus:border-gray-600 focus:ring-1 focus:ring-gray-600 transition-all min-h-[40px]"
            aria-label="Search documents"
          />
          {isSearching ? (
            <Loader2 className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500 animate-spin" />
          ) : searchQuery ? (
            <button
              onClick={() => setSearchQuery('')}
              className="absolute right-3 top-1/2 -translate-y-1/2 p-1 hover:bg-gray-800 rounded text-gray-500 transition-colors touch-manipulation min-w-[24px] min-h-[24px] flex items-center justify-center"
              aria-label="Clear search"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          ) : null}
        </div>
        {searchQuery && (
          <p className="text-xs text-gray-500 mt-2">
            {totalCount} document{totalCount !== 1 ? 's' : ''} found
          </p>
        )}
      </div>

      {/* Document Tree */}
      <div className="flex-1 overflow-y-auto py-2 scrollbar-thin">
        {totalCount === 0 && searchQuery ? (
          <div className="px-4 py-12 text-center">
            <div className="p-3 bg-gray-800/30 rounded-full w-fit mx-auto mb-3">
              <Search className="w-6 h-6 text-gray-600" />
            </div>
            <p className="text-sm text-gray-500 font-medium">No documents found</p>
            <p className="text-xs text-gray-600 mt-1">
              No matches for "{searchQuery}"
            </p>
            <button
              onClick={() => {
                setSearchQuery('');
                clearFolderFilter();
              }}
              className="mt-4 text-xs text-blue-400 hover:text-blue-300 transition-colors"
            >
              Clear all filters
            </button>
          </div>
        ) : totalCount === 0 && !searchQuery ? (
          <div className="px-4 py-12 text-center">
            <FileText className="w-10 h-10 text-gray-700 mx-auto mb-3" />
            <p className="text-sm text-gray-500">No documents yet</p>
            <p className="text-xs text-gray-600 mt-1">Create your first document</p>
          </div>
        ) : selectedFolder && totalCount === 0 ? (
          <div className="px-4 py-12 text-center">
            <Folder className="w-10 h-10 text-gray-700 mx-auto mb-3" />
            <p className="text-sm text-gray-500 font-medium">No documents in this folder</p>
            <button
              onClick={clearFolderFilter}
              className="mt-4 text-xs text-blue-400 hover:text-blue-300 transition-colors"
            >
              Clear filter
            </button>
          </div>
        ) : (
          Object.entries(docsByCategory).map(([category, categoryDocs]) => {
            const Icon = categoryIcons[category as keyof typeof categoryIcons] || FileText;
            const colorClass = categoryColors[category as keyof typeof categoryColors] || 'text-gray-400';
            const hoverClass = categoryHoverColors[category as keyof typeof categoryHoverColors] || '';
            const isExpanded = expandedCategories[category];

            return (
              <div key={category} className="mb-1">
                <button
                  onClick={() => toggleCategory(category)}
                  className={`w-full flex items-center gap-2 px-4 py-2.5 text-xs font-medium text-gray-500 uppercase tracking-wider hover:text-gray-400 transition-colors touch-manipulation min-h-[40px] focus:outline-none focus-visible:text-gray-400 ${hoverClass} rounded-lg -mx-2`}
                  aria-expanded={isExpanded}
                  aria-controls={`category-${category}`}
                >
                  <ChevronRight
                    className={`w-3.5 h-3.5 transition-transform duration-300 ease-out flex-shrink-0 ${isExpanded ? 'rotate-90' : ''}`}
                    aria-hidden="true"
                  />
                  <Icon className={`w-3.5 h-3.5 flex-shrink-0 transition-transform duration-200 ${isExpanded ? 'scale-110' : 'scale-100'} ${colorClass}`} aria-hidden="true" />
                  {categoryLabels[category as keyof typeof categoryLabels]}
                  <span className="ml-auto text-gray-600 font-normal transition-colors duration-200 group-hover:text-gray-400">{categoryDocs.length}</span>
                </button>

                {isExpanded && (
                  <div 
                    id={`category-${category}`} 
                    className="mt-1 overflow-hidden animate-in slide-in-from-top-2 duration-300 ease-out"
                  >
                    {categoryDocs.map((doc, index) => {
                      const isActive = pathname?.includes(doc.slug);
                      
                      return (
                        <Link
                          key={doc.slug}
                          href={`/docs/${doc.slug}`}
                          style={{ animationDelay: `${index * 30}ms` }}
                          className={`
                            group flex items-start gap-2.5 px-4 py-2.5 mx-2 rounded-lg text-sm transition-all duration-200 ease-out
                            ${isActive 
                              ? 'bg-gray-800/80 text-gray-100 shadow-sm' 
                              : 'text-gray-400 hover:bg-gray-800/50 hover:text-gray-200'
                            }
                            focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:ring-offset-2 focus:ring-offset-gray-950 rounded-lg
                            hover:translate-x-0.5
                          `}
                          aria-current={isActive ? 'page' : undefined}
                        >
                          <div className="relative">
                            <FileText className={`w-4 h-4 mt-0.5 flex-shrink-0 transition-colors ${isActive ? 'text-blue-400' : 'text-gray-600 group-hover:text-gray-500'}`} aria-hidden="true" />
                            {/* Active indicator dot */}
                            {isActive && (
                              <span className="absolute -left-1.5 top-1/2 -translate-y-1/2 w-1.5 h-1.5 bg-blue-400 rounded-full animate-pulse" />
                            )}
                          </div>
                          <div className="flex-1 min-w-0">
                            <div className="truncate font-medium transition-transform duration-200 group-hover:translate-x-0.5">{doc.frontmatter.title}</div>
                            <div className="text-xs text-gray-600 mt-0.5 flex items-center gap-2">
                              <time dateTime={doc.frontmatter.date}>
                                {formatDate(doc.frontmatter.date)}
                              </time>
                              {doc.frontmatter.tags && doc.frontmatter.tags.length > 0 && (
                                <>
                                  <span className="text-gray-700">•</span>
                                  <span className="truncate max-w-[80px] group-hover:text-gray-400 transition-colors">{doc.frontmatter.tags[0]}</span>
                                </>
                              )}
                            </div>
                          </div>
                          {/* Arrow indicator on hover */}
                          <ChevronRight className={`w-3.5 h-3.5 mt-0.5 flex-shrink-0 text-gray-700 opacity-0 group-hover:opacity-100 group-hover:translate-x-0.5 transition-all duration-200 ${isActive ? 'opacity-50' : ''}`} aria-hidden="true" />
                        </Link>
                      );
                    })}
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>

      {/* Tags Summary */}
      <div className="p-4 border-t border-gray-800">
        <Link
          href="/tags"
          className="flex items-center gap-2 text-sm text-gray-500 hover:text-gray-300 transition-colors touch-manipulation py-2 rounded-lg hover:bg-gray-800/30 -mx-2 px-2 focus:outline-none focus:ring-2 focus:ring-blue-500/50"
        >
          <Hash className="w-4 h-4 flex-shrink-0" aria-hidden="true" />
          Browse all tags
        </Link>
      </div>
    </div>
  );
}
