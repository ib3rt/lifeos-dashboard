import { notFound } from 'next/navigation';
import { getDocumentBySlug, getAllDocuments, getBacklinks } from '@/lib/documents';
import { SidebarLayout } from '@/components/layout/SidebarLayout';
import { DocumentViewer } from '@/components/documents/DocumentViewer';

interface DocPageProps {
  params: Promise<{
    slug: string;
  }>;
}

export async function generateStaticParams() {
  const documents = getAllDocuments();
  return documents.map((doc) => ({
    slug: doc.slug,
  }));
}

export async function generateMetadata({ params }: DocPageProps) {
  const { slug } = await params;
  const document = getDocumentBySlug(slug);
  
  if (!document) {
    return { title: 'Document Not Found' };
  }
  
  return {
    title: `${document.frontmatter.title} | Second Brain`,
    description: document.frontmatter.description,
  };
}

export default async function DocPage({ params }: DocPageProps) {
  const { slug } = await params;
  const documents = getAllDocuments();
  const document = getDocumentBySlug(slug);
  
  if (!document) {
    notFound();
  }
  
  const backlinks = getBacklinks(slug);
  
  return (
    <SidebarLayout documents={documents} currentSlug={slug}>
      <DocumentViewer doc={document} backlinks={backlinks} />
    </SidebarLayout>
  );
}
