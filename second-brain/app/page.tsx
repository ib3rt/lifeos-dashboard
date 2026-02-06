import { SidebarLayout } from '@/components/layout/SidebarLayout';
import { DailyJournal } from '@/components/documents/DailyJournal';
import { TagCloud } from '@/components/documents/TagCloud';
import { getAllDocuments, getAllTags, getDocumentsByCategory } from '@/lib/documents';
import Link from 'next/link';
import { 
  BookOpen, 
  FolderGit2, 
  Bookmark, 
  Calendar, 
  ArrowRight,
  Sparkles,
  Zap,
  Clock
} from 'lucide-react';

export default function Home() {
  const documents = getAllDocuments();
  const tags = getAllTags();
  const journalEntries = getDocumentsByCategory('journal');
  
  const stats = {
    total: documents.length,
    journal: getDocumentsByCategory('journal').length,
    concepts: getDocumentsByCategory('concepts').length,
    projects: getDocumentsByCategory('projects').length,
    reference: getDocumentsByCategory('reference').length,
  };

  const recentDocs = documents.slice(0, 5);

  return (
    <SidebarLayout documents={documents}>
      <div className="h-full overflow-y-auto">
        <div className="max-w-5xl mx-auto px-6 py-12">
          {/* Welcome Section */}
          <div className="mb-12">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 bg-blue-500/10 rounded-xl">
                <Sparkles className="w-6 h-6 text-blue-400" />
              </div>
              <h1 className="text-3xl font-bold text-gray-100">
                Welcome back, b3rt
              </h1>
            </div>
            <p className="text-gray-400 text-lg">
              Your personal knowledge base. {stats.total} documents organized and ready.
            </p>
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-12">
            <Link href="/journal" className="group p-5 bg-gray-900 border border-gray-800 hover:border-gray-700 rounded-2xl transition-all">
              <div className="flex items-center justify-between mb-3">
                <div className="p-2 bg-purple-500/10 rounded-lg">
                  <Calendar className="w-5 h-5 text-purple-400" />
                </div>
                <ArrowRight className="w-4 h-4 text-gray-600 group-hover:text-gray-400 transition-colors" />
              </div>
              <div className="text-2xl font-bold text-gray-100">{stats.journal}</div>
              <div className="text-sm text-gray-500">Journal Entries</div>
            </Link>

            <Link href="/docs?category=concepts" className="group p-5 bg-gray-900 border border-gray-800 hover:border-gray-700 rounded-2xl transition-all">
              <div className="flex items-center justify-between mb-3">
                <div className="p-2 bg-green-500/10 rounded-lg">
                  <BookOpen className="w-5 h-5 text-green-400" />
                </div>
                <ArrowRight className="w-4 h-4 text-gray-600 group-hover:text-gray-400 transition-colors" />
              </div>
              <div className="text-2xl font-bold text-gray-100">{stats.concepts}</div>
              <div className="text-sm text-gray-500">Concepts</div>
            </Link>

            <Link href="/docs?category=projects" className="group p-5 bg-gray-900 border border-gray-800 hover:border-gray-700 rounded-2xl transition-all">
              <div className="flex items-center justify-between mb-3">
                <div className="p-2 bg-orange-500/10 rounded-lg">
                  <FolderGit2 className="w-5 h-5 text-orange-400" />
                </div>
                <ArrowRight className="w-4 h-4 text-gray-600 group-hover:text-gray-400 transition-colors" />
              </div>
              <div className="text-2xl font-bold text-gray-100">{stats.projects}</div>
              <div className="text-sm text-gray-500">Projects</div>
            </Link>

            <Link href="/docs?category=reference" className="group p-5 bg-gray-900 border border-gray-800 hover:border-gray-700 rounded-2xl transition-all">
              <div className="flex items-center justify-between mb-3">
                <div className="p-2 bg-blue-500/10 rounded-lg">
                  <Bookmark className="w-5 h-5 text-blue-400" />
                </div>
                <ArrowRight className="w-4 h-4 text-gray-600 group-hover:text-gray-400 transition-colors" />
              </div>
              <div className="text-2xl font-bold text-gray-100">{stats.reference}</div>
              <div className="text-sm text-gray-500">References</div>
            </Link>
          </div>

          <div className="grid lg:grid-cols-3 gap-8">
            {/* Journal Section */}
            <div className="lg:col-span-2">
              <div className="flex items-center gap-2 mb-6">
                <Zap className="w-5 h-5 text-yellow-400" />
                <h2 className="text-xl font-semibold text-gray-100">Daily Journal</h2>
              </div>
              <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
                <DailyJournal entries={journalEntries} />
              </div>
            </div>

            {/* Sidebar Column */}
            <div className="space-y-8">
              {/* Recent Documents */}
              <div>
                <div className="flex items-center gap-2 mb-4">
                  <Clock className="w-4 h-4 text-gray-500" />
                  <h3 className="text-sm font-semibold text-gray-300 uppercase tracking-wider">
                    Recent Documents
                  </h3>
                </div>
                <div className="space-y-2">
                  {recentDocs.map((doc) => (
                    <Link
                      key={doc.slug}
                      href={`/docs/${doc.slug}`}
                      className="block p-3 bg-gray-800/20 hover:bg-gray-800/40 border border-gray-800/50 hover:border-gray-700 rounded-xl transition-all group"
                    >
                      <div className="flex items-start justify-between">
                        <div>
                          <h4 className="text-sm font-medium text-gray-300 group-hover:text-gray-100 transition-colors">
                            {doc.frontmatter.title}
                          </h4>
                          <p className="text-xs text-gray-600 mt-1 capitalize">
                            {doc.frontmatter.category}
                          </p>
                        </div>
                      </div>
                    </Link>
                  ))}
                </div>
              </div>

              {/* Popular Tags */}
              <div>
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-sm font-semibold text-gray-300 uppercase tracking-wider">
                    Popular Tags
                  </h3>
                  <Link 
                    href="/tags" 
                    className="text-xs text-gray-500 hover:text-gray-400"
                  >
                    View all
                  </Link>
                </div>
                <TagCloud tags={tags.slice(0, 10)} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </SidebarLayout>
  );
}
