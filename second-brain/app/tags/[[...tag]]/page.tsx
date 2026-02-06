import Link from 'next/link';
import { SidebarLayout } from '@/components/layout/SidebarLayout';
import { TagCloud } from '@/components/documents/TagCloud';
import { getAllDocuments, getAllTags, getDocumentsByTag } from '@/lib/documents';
import { formatDate } from '@/lib/markdown';
import { FileText, Hash } from 'lucide-react';

interface TagsPageProps {
  params: Promise<{
    tag?: string;
  }>;
}

// Generate static params for all tags
export async function generateStaticParams() {
  const tags = getAllTags();
  const params: { tag?: string[] }[] = [{ tag: undefined }];
  tags.forEach((t: { tag: string; count: number }) => {
    params.push({ tag: [encodeURIComponent(t.tag)] });
  });
  return params;
}

export default async function TagsPage({ params }: TagsPageProps) {
  const { tag } = await params || {};
  const documents = getAllDocuments();
  const tags = getAllTags();
  
  const selectedTag = tag ? decodeURIComponent(tag) : undefined;
  const filteredDocs = selectedTag ? getDocumentsByTag(selectedTag) : [];

  return (
    <SidebarLayout documents={documents} showSidebar={false}>
      <div className="h-full overflow-y-auto">
        <div className="max-w-4xl mx-auto px-6 py-12">
          {/* Header */}
          <div className="mb-10">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 bg-blue-500/10 rounded-xl">
                <Hash className="w-6 h-6 text-blue-400" />
              </div>
              <h1 className="text-3xl font-bold text-gray-100">
                {selectedTag ? `Tag: ${selectedTag}` : 'All Tags'}
              </h1>
            </div>
            <p className="text-gray-400">
              {selectedTag 
                ? `${filteredDocs.length} documents tagged with "${selectedTag}"`
                : `${tags.length} tags across ${documents.length} documents`
              }
            </p>
          </div>

          {/* Tag Cloud */}
          {!selectedTag && (
            <div className="mb-12">
              <TagCloud tags={tags} />
            </div>
          )}

          {/* Documents List */}
          {selectedTag && (
            <div className="space-y-3">
              {filteredDocs.length === 0 ? (
                <div className="text-center py-12">
                  <p className="text-gray-500">No documents found with this tag</p>
                </div>
              ) : (
                filteredDocs.map((doc) => (
                  <Link
                    key={doc.slug}
                    href={`/docs/${doc.slug}`}
                    className="flex items-center gap-4 p-4 bg-gray-900 border border-gray-800 hover:border-gray-700 rounded-xl transition-all group"
                  >
                    <div className="p-2 bg-gray-800 rounded-lg">
                      <FileText className="w-5 h-5 text-gray-400" />
                    </div>
                    <div className="flex-1">
                      <h3 className="font-medium text-gray-200 group-hover:text-blue-400 transition-colors">
                        {doc.frontmatter.title}
                      </h3>
                      <p className="text-sm text-gray-500 mt-1">
                        {formatDate(doc.frontmatter.date)} • {doc.frontmatter.category}
                      </p>
                    </div>
                    <div className="flex items-center gap-2">
                      {doc.frontmatter.tags?.filter(t => t !== selectedTag).slice(0, 2).map((t) => (
                        <span key={t} className="px-2 py-1 bg-gray-800 text-gray-500 text-xs rounded-md">
                          #{t}
                        </span>
                      ))}
                    </div>
                  </Link>
                ))
              )}
            </div>
          )}
        </div>
      </div>
    </SidebarLayout>
  );
}
