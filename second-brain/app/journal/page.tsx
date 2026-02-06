import { SidebarLayout } from '@/components/layout/SidebarLayout';
import { DailyJournal } from '@/components/documents/DailyJournal';
import { getAllDocuments, getDocumentsByCategory } from '@/lib/documents';
import { Calendar, TrendingUp, Clock } from 'lucide-react';

export default function JournalPage() {
  const documents = getAllDocuments();
  const journalEntries = getDocumentsByCategory('journal');
  
  // Calculate streak (simplified)
  const streak = journalEntries.length > 0 ? Math.min(journalEntries.length, 7) : 0;
  
  return (
    <SidebarLayout documents={documents}>
      <div className="h-full overflow-y-auto">
        <div className="max-w-3xl mx-auto px-6 py-12">
          {/* Header */}
          <div className="flex items-center justify-between mb-8">
            <div>
              <div className="flex items-center gap-3 mb-2">
                <div className="p-2 bg-purple-500/10 rounded-xl">
                  <Calendar className="w-6 h-6 text-purple-400" />
                </div>
                <h1 className="text-3xl font-bold text-gray-100">Journal</h1>
              </div>
              <p className="text-gray-400">
                Daily thoughts, reflections, and learnings
              </p>
            </div>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-3 gap-4 mb-10">
            <div className="p-5 bg-gray-900 border border-gray-800 rounded-2xl">
              <div className="flex items-center gap-2 mb-2">
                <Calendar className="w-4 h-4 text-gray-500" />
                <span className="text-sm text-gray-500">Total Entries</span>
              </div>
              <div className="text-2xl font-bold text-gray-100">{journalEntries.length}</div>
            </div>
            
            <div className="p-5 bg-gray-900 border border-gray-800 rounded-2xl">
              <div className="flex items-center gap-2 mb-2">
                <TrendingUp className="w-4 h-4 text-green-500" />
                <span className="text-sm text-gray-500">Current Streak</span>
              </div>
              <div className="text-2xl font-bold text-gray-100">{streak} days</div>
            </div>
            
            <div className="p-5 bg-gray-900 border border-gray-800 rounded-2xl">
              <div className="flex items-center gap-2 mb-2">
                <Clock className="w-4 h-4 text-blue-500" />
                <span className="text-sm text-gray-500">Total Reading</span>
              </div>
              <div className="text-2xl font-bold text-gray-100">
                {journalEntries.reduce((acc, e) => acc + e.readingTime, 0)} min
              </div>
            </div>
          </div>

          {/* Journal Entries */}
          <DailyJournal entries={journalEntries} />
        </div>
      </div>
    </SidebarLayout>
  );
}
