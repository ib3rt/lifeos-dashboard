'use client';

import Link from 'next/link';
import { TagCount } from '@/types';
import { Hash } from 'lucide-react';

interface TagCloudProps {
  tags: TagCount[];
  selectedTag?: string;
}

export function TagCloud({ tags, selectedTag }: TagCloudProps) {
  const maxCount = Math.max(...tags.map(t => t.count), 1);
  const minCount = Math.min(...tags.map(t => t.count), 1);

  const getSizeClass = (count: number) => {
    const normalized = (count - minCount) / (maxCount - minCount || 1);
    if (normalized > 0.8) return 'text-2xl px-5 py-2.5';
    if (normalized > 0.6) return 'text-xl px-4 py-2';
    if (normalized > 0.4) return 'text-lg px-4 py-1.5';
    if (normalized > 0.2) return 'text-base px-3 py-1.5';
    return 'text-sm px-3 py-1';
  };

  return (
    <div className="flex flex-wrap gap-3">
      {tags.map(({ tag, count }) => {
        const isSelected = selectedTag === tag;
        
        return (
          <Link
            key={tag}
            href={isSelected ? '/tags' : `/tags/${encodeURIComponent(tag)}`}
            className={`
              group inline-flex items-center gap-2 rounded-full transition-all duration-200
              ${getSizeClass(count)}
              ${isSelected 
                ? 'bg-blue-500/20 text-blue-400 border border-blue-500/30' 
                : 'bg-gray-800/50 text-gray-400 border border-gray-800 hover:border-gray-700 hover:text-gray-300 hover:bg-gray-800'
              }
            `}
          >
            <Hash className={`flex-shrink-0 ${isSelected ? 'w-4 h-4' : 'w-3.5 h-3.5'}`} />
            <span className="font-medium">{tag}</span>
            <span className={`text-xs ${isSelected ? 'text-blue-500/70' : 'text-gray-600'}`}>
              {count}
            </span>
          </Link>
        );
      })}
    </div>
  );
}
