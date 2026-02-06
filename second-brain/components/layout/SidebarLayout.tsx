'use client';

import { ReactNode, useState } from 'react';
import { Header } from './Header';
import { DocumentList } from '@/components/documents/DocumentList';
import { Document } from '@/types';
import { Menu, X } from 'lucide-react';

interface SidebarLayoutProps {
  children: ReactNode;
  documents: Document[];
  currentSlug?: string;
  showSidebar?: boolean;
}

export function SidebarLayout({ 
  children, 
  documents, 
  currentSlug,
  showSidebar = true 
}: SidebarLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen bg-gray-950">
      <Header 
        documents={documents} 
        onMenuClick={() => setSidebarOpen(true)}
      />
      
      <div className="flex h-[calc(100vh-3.5rem)]">
        {/* Mobile Sidebar Overlay */}
        {showSidebar && (
          <>
            {/* Overlay */}
            <div 
              className={`
                fixed inset-0 z-40 bg-black/60 backdrop-blur-sm lg:hidden
                transition-opacity duration-300
                ${sidebarOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'}
              `}
              onClick={() => setSidebarOpen(false)}
            />
            
            {/* Mobile Sidebar Drawer */}
            <aside 
              className={`
                fixed inset-y-0 left-0 z-50 w-72 bg-gray-950 border-r border-gray-800 
                transform transition-transform duration-300 ease-out lg:hidden
                ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}
              `}
            >
              <div className="flex items-center justify-between p-4 border-b border-gray-800 animate-in slide-in-from-top-2">
                <span className="font-semibold text-gray-200">Documents</span>
                <button 
                  onClick={() => setSidebarOpen(false)}
                  className="p-2 text-gray-400 hover:text-gray-200 hover:bg-gray-800 rounded-lg touch-manipulation transition-colors"
                  aria-label="Close sidebar"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
              <div className="h-[calc(100%-3.5rem)] overflow-hidden animate-in fade-in duration-300">
                <DocumentList documents={documents} currentSlug={currentSlug} />
              </div>
            </aside>
          </>
        )}

        {/* Desktop Sidebar */}
        {showSidebar && (
          <aside className="hidden lg:block w-72 border-r border-gray-800 bg-gray-950 flex-shrink-0">
            <DocumentList documents={documents} currentSlug={currentSlug} />
          </aside>
        )}

        {/* Main Content */}
        <main className="flex-1 overflow-hidden bg-gray-950 min-w-0">
          {children}
        </main>
      </div>
    </div>
  );
}
