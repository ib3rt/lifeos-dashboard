'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Brain, Menu, X, Github, Settings } from 'lucide-react';
import { useState } from 'react';
import { SearchBar } from '../documents/SearchBar';
import { Document } from '@/types';

interface HeaderProps {
  documents: Document[];
  onMenuClick?: () => void;
}

export function Header({ documents, onMenuClick }: HeaderProps) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const pathname = usePathname();

  const navItems = [
    { href: '/', label: 'Dashboard', exact: true },
    { href: '/journal', label: 'Journal' },
    { href: '/tags', label: 'Tags' },
  ];

  return (
    <header className="sticky top-0 z-40 w-full border-b border-gray-800 bg-gray-950/80 backdrop-blur-xl">
      <div className="flex h-14 items-center justify-between px-3 lg:px-6">
        {/* Left Section */}
        <div className="flex items-center gap-2">
          {/* Mobile Docs Menu Button */}
          {onMenuClick && (
            <button
              onClick={onMenuClick}
              className="lg:hidden p-2 text-gray-400 hover:text-gray-200 hover:bg-gray-800 rounded-lg touch-manipulation min-w-[44px] min-h-[44px] flex items-center justify-center"
              aria-label="Open documents menu"
            >
              <Menu className="w-5 h-5" />
            </button>
          )}

          {/* Logo */}
          <Link 
            href="/" 
            className="flex items-center gap-2 text-gray-100 hover:text-blue-400 transition-all duration-300 group"
          >
            <div className="p-1.5 bg-blue-500/10 rounded-lg group-hover:bg-blue-500/20 transition-colors duration-300">
              <Brain className="w-5 h-5 text-blue-400 group-hover:scale-110 transition-transform duration-300" />
            </div>
            <span className="font-semibold hidden sm:block group-hover:translate-x-0.5 transition-transform duration-200">Second Brain</span>
          </Link>

          {/* Desktop Nav */}
          <nav className="hidden md:flex items-center gap-1 ml-4">
            {navItems.map((item) => {
              const isActive = item.exact 
                ? pathname === item.href
                : pathname?.startsWith(item.href);
              
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`
                    px-3 py-1.5 rounded-lg text-sm transition-all duration-200
                    ${isActive 
                      ? 'bg-gray-800 text-gray-100 shadow-sm' 
                      : 'text-gray-400 hover:text-gray-200 hover:bg-gray-800/50 hover:translate-y-[-1px]'
                    }
                  `}
                >
                  {item.label}
                </Link>
              );
            })}
          </nav>
        </div>

        {/* Right Section */}
        <div className="flex items-center gap-2">
          <SearchBar documents={documents} />
          
          <a
            href="https://github.com"
            target="_blank"
            rel="noopener noreferrer"
            className="hidden sm:flex p-2 text-gray-500 hover:text-gray-300 hover:bg-gray-800/50 rounded-lg transition-colors min-w-[44px] min-h-[44px] items-center justify-center"
          >
            <Github className="w-5 h-5" />
          </a>

          <button className="hidden sm:flex p-2 text-gray-500 hover:text-gray-300 hover:bg-gray-800/50 rounded-lg transition-colors min-w-[44px] min-h-[44px] items-center justify-center">
            <Settings className="w-5 h-5" />
          </button>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 text-gray-400 hover:text-gray-200 hover:bg-gray-800 rounded-lg transition-colors min-w-[44px] min-h-[44px] flex items-center justify-center"
          >
            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden border-t border-gray-800 bg-gray-950">
          <nav className="flex flex-col p-2">
            {navItems.map((item) => {
              const isActive = item.exact 
                ? pathname === item.href
                : pathname?.startsWith(item.href);
              
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className={`
                    px-4 py-3 rounded-lg text-base transition-colors touch-manipulation min-h-[44px] flex items-center
                    ${isActive 
                      ? 'bg-gray-800 text-gray-100' 
                      : 'text-gray-400 hover:text-gray-200 hover:bg-gray-800/50'
                    }
                  `}
                >
                  {item.label}
                </Link>
              );
            })}
          </nav>
        </div>
      )}
    </header>
  );
}
