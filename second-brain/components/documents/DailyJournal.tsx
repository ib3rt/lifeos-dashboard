'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Document } from '@/types';
import { formatDate, getRelativeTime } from '@/lib/markdown';
import { Calendar, ChevronLeft, ChevronRight, Clock, FileText } from 'lucide-react';

interface DailyJournalProps {
  entries: Document[];
}

export function DailyJournal({ entries }: DailyJournalProps) {
  const [currentIndex, setCurrentIndex] = useState(0);
  
  // Sort by date descending
  const sortedEntries = [...entries].sort((a, b) => 
    new Date(b.frontmatter.date).getTime() - new Date(a.frontmatter.date).getTime()
  );

  const currentEntry = sortedEntries[currentIndex];
  const hasNext = currentIndex < sortedEntries.length - 1;
  const hasPrev = currentIndex > 0;

  if (sortedEntries.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-64 text-gray-500">
        <Calendar className="w-12 h-12 mb-4 opacity-50" />
        <p>No journal entries yet</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Navigation */}
      <div className="flex items-center justify-between p-4 bg-gray-800/30 border border-gray-800 rounded-xl">
        <button
          onClick={() => setCurrentIndex(prev => prev + 1)}
          disabled={!hasNext}
          className="flex items-center gap-2 text-sm text-gray-400 hover:text-gray-200 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
        >
          <ChevronLeft className="w-4 h-4" />
          Older
        </button>
        
        <div className="text-center">
          <div className="text-sm font-medium text-gray-200">
            {formatDate(currentEntry.frontmatter.date)}
          </div>
          <div className="text-xs text-gray-500">
            {getRelativeTime(currentEntry.frontmatter.date)}
          </div>
        </div>

        <button
          onClick={() => setCurrentIndex(prev => prev - 1)}
          disabled={!hasPrev}
          className="flex items-center gap-2 text-sm text-gray-400 hover:text-gray-200 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
        >
          Newer
          <ChevronRight className="w-4 h-4" />
        </button>
      </div>

      {/* Entry Card */}
      <Link
        href={`/docs/${currentEntry.slug}`}
        className="block group p-6 bg-gray-800/20 hover:bg-gray-800/40 border border-gray-800 hover:border-gray-700 rounded-xl transition-all"
      >
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-500/10 rounded-lg">
              <FileText className="w-5 h-5 text-blue-400" />
            </div>
            <div>
              <h3 className="font-semibold text-gray-200 group-hover:text-blue-400 transition-colors">
                {currentEntry.frontmatter.title}
              </h3>
              <div className="flex items-center gap-2 text-sm text-gray-500 mt-1">
                <Clock className="w-3.5 h-3.5" />
                {currentEntry.readingTime} min read
              </div>
            </div>
          </div>
        </div>

        {currentEntry.frontmatter.description && (
          <p className="text-gray-400 line-clamp-3">
            {currentEntry.frontmatter.description}
          </p>
        )}

        {currentEntry.frontmatter.tags && currentEntry.frontmatter.tags.length > 0 && (
          <div className="flex items-center gap-2 mt-4 flex-wrap">
            {currentEntry.frontmatter.tags.map((tag) => (
              <span
                key={tag}
                className="px-2 py-1 bg-gray-800 text-gray-500 text-xs rounded-md"
              >
                #{tag}
              </span>
            ))}
          </div>
        )}
      </Link>

      {/* Entry Stats */}
      <div className="grid grid-cols-3 gap-4">
        <div className="p-4 bg-gray-800/20 border border-gray-800 rounded-xl text-center">
          <div className="text-2xl font-bold text-gray-200">{sortedEntries.length}</div>
          <div className="text-xs text-gray-500 uppercase tracking-wider mt-1">Total Entries</div>
        </div>
        <div className="p-4 bg-gray-800/20 border border-gray-800 rounded-xl text-center">
          <div className="text-2xl font-bold text-gray-200">
            {Math.round(sortedEntries.reduce((acc, e) => acc + e.readingTime, 0) / sortedEntries.length)}
          </div>
          <div className="text-xs text-gray-500 uppercase tracking-wider mt-1">Avg. Read Time</div>
        </div>
        <div className="p-4 bg-gray-800/20 border border-gray-800 rounded-xl text-center">
          <div className="text-2xl font-bold text-gray-200">
            {new Set(sortedEntries.flatMap(e => e.frontmatter.tags || [])).size}
          </div>
          <div className="text-xs text-gray-500 uppercase tracking-wider mt-1">Unique Tags</div>
        </div>
      </div>

      {/* Recent Entries List */}
      <div className="space-y-2">
        <h4 className="text-sm font-medium text-gray-500 uppercase tracking-wider">
          Recent Entries
        </h4>
        {sortedEntries.slice(0, 5).map((entry) => (
          <Link
            key={entry.slug}
            href={`/docs/${entry.slug}`}
            className="flex items-center justify-between p-3 bg-gray-800/10 hover:bg-gray-800/30 border border-gray-800/50 hover:border-gray-700 rounded-lg transition-all group"
          >
            <span className="text-sm text-gray-400 group-hover:text-gray-200 transition-colors">
              {entry.frontmatter.title}
            </span>
            <span className="text-xs text-gray-600">
              {formatDate(entry.frontmatter.date)}
            </span>
          </Link>
        ))}
      </div>
    </div>
  );
}
