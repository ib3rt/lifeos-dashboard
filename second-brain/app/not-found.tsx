import Link from 'next/link';
import { SidebarLayout } from '@/components/layout/SidebarLayout';
import { getAllDocuments } from '@/lib/documents';
import { FileText, Home } from 'lucide-react';

export default function NotFound() {
  const documents = getAllDocuments();

  return (
    <SidebarLayout documents={documents} showSidebar={false}>
      <div className="h-full flex items-center justify-center">
        <div className="text-center px-6">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-gray-800/50 rounded-2xl mb-6">
            <FileText className="w-10 h-10 text-gray-600" />
          </div>
          <h1 className="text-4xl font-bold text-gray-100 mb-4">Document Not Found</h1>
          <p className="text-gray-400 mb-8 max-w-md mx-auto">
            The document you're looking for doesn't exist or has been moved. 
            Try searching for it or browse the document list.
          </p>
          <Link
            href="/"
            className="inline-flex items-center gap-2 px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white rounded-xl transition-colors"
          >
            <Home className="w-4 h-4" />
            Back to Dashboard
          </Link>
        </div>
      </div>
    </SidebarLayout>
  );
}
