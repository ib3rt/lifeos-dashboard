import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';
import { Document, DocumentFrontmatter, TagCount, Backlink } from '@/types';

const contentDirectory = path.join(process.cwd(), 'content');

// Cache for documents to avoid repeated file reads
let documentCache: Document[] | null = null;
let tagsCache: TagCount[] | null = null;

// Clear cache function (useful for development)
export function clearDocumentCache() {
  documentCache = null;
  tagsCache = null;
}

export function getAllDocuments(forceRefresh = false): Document[] {
  // Return cached documents if available and not forcing refresh
  if (documentCache && !forceRefresh) {
    return documentCache;
  }
  
  const documents: Document[] = [];
  
  const categories = ['journal', 'concepts', 'projects', 'reference'];
  
  for (const category of categories) {
    const categoryPath = path.join(contentDirectory, category);
    
    if (!fs.existsSync(categoryPath)) continue;
    
    const files = fs.readdirSync(categoryPath).filter(file => file.endsWith('.md'));
    
    for (const file of files) {
      const filePath = path.join(categoryPath, file);
      const fileContents = fs.readFileSync(filePath, 'utf8');
      const { data, content } = matter(fileContents);
      
      const slug = file.replace(/\.md$/, '');
      const frontmatter = data as DocumentFrontmatter;
      
      // Calculate reading time (approx 200 words per minute)
      const wordCount = content.split(/\s+/).length;
      const readingTime = Math.ceil(wordCount / 200);
      
      // Extract backlinks from content
      const backlinkRegex = /\[\[([^\]]+)\]\]/g;
      const backlinks: string[] = [];
      let match;
      while ((match = backlinkRegex.exec(content)) !== null) {
        backlinks.push(match[1]);
      }
      
      documents.push({
        slug,
        frontmatter: {
          ...frontmatter,
          category: category as DocumentFrontmatter['category'],
        },
        content,
        backlinks,
        readingTime,
      });
    }
  }
  
  // Sort by date descending
  documents.sort((a, b) => 
    new Date(b.frontmatter.date).getTime() - new Date(a.frontmatter.date).getTime()
  );
  
  // Cache the result
  documentCache = documents;
  
  return documents;
}

export function getDocumentBySlug(slug: string, category?: string, forceRefresh = false): Document | null {
  const documents = getAllDocuments(forceRefresh);
  
  if (category) {
    return documents.find(doc => doc.slug === slug && doc.frontmatter.category === category) || null;
  }
  
  return documents.find(doc => doc.slug === slug) || null;
}

export function getDocumentsByCategory(category: string, forceRefresh = false): Document[] {
  return getAllDocuments(forceRefresh).filter(doc => doc.frontmatter.category === category);
}

export function getAllTags(forceRefresh = false): TagCount[] {
  // Return cached tags if available
  if (tagsCache && !forceRefresh) {
    return tagsCache;
  }
  
  const documents = getAllDocuments(forceRefresh);
  const tagCounts: Record<string, number> = {};
  
  for (const doc of documents) {
    for (const tag of doc.frontmatter.tags || []) {
      tagCounts[tag] = (tagCounts[tag] || 0) + 1;
    }
  }
  
  const tags = Object.entries(tagCounts)
    .map(([tag, count]) => ({ tag, count }))
    .sort((a, b) => b.count - a.count);
  
  // Cache the result
  tagsCache = tags;
  
  return tags;
}

export function getDocumentsByTag(tag: string, forceRefresh = false): Document[] {
  return getAllDocuments(forceRefresh).filter(doc => 
    doc.frontmatter.tags?.includes(tag)
  );
}

export function getBacklinks(slug: string, forceRefresh = false): Backlink[] {
  const documents = getAllDocuments(forceRefresh);
  const backlinks: Backlink[] = [];
  
  for (const doc of documents) {
    if (doc.slug !== slug && doc.backlinks.includes(slug)) {
      // Get first 150 chars as excerpt
      const excerpt = doc.content
        .replace(/#.*$/gm, '')
        .replace(/\[\[([^\]]+)\]\]/g, '$1')
        .replace(/[*_`]/g, '')
        .trim()
        .slice(0, 150) + '...';
      
      backlinks.push({
        slug: doc.slug,
        title: doc.frontmatter.title,
        excerpt,
      });
    }
  }
  
  return backlinks;
}

export function searchDocuments(query: string, forceRefresh = false): Document[] {
  const documents = getAllDocuments(forceRefresh);
  const lowerQuery = query.toLowerCase();
  
  return documents.filter(doc => 
    doc.frontmatter.title.toLowerCase().includes(lowerQuery) ||
    doc.content.toLowerCase().includes(lowerQuery) ||
    doc.frontmatter.tags?.some(tag => tag.toLowerCase().includes(lowerQuery))
  );
}

export function getRelatedDocuments(document: Document, limit: number = 5, forceRefresh = false): Document[] {
  const documents = getAllDocuments(forceRefresh);
  
  return documents
    .filter(doc => doc.slug !== document.slug)
    .map(doc => {
      let score = 0;
      
      // Same category
      if (doc.frontmatter.category === document.frontmatter.category) {
        score += 2;
      }
      
      // Shared tags
      const sharedTags = doc.frontmatter.tags?.filter(tag => 
        document.frontmatter.tags?.includes(tag)
      ) || [];
      score += sharedTags.length * 3;
      
      // Linked documents
      if (document.backlinks.includes(doc.slug)) {
        score += 5;
      }
      if (doc.backlinks.includes(document.slug)) {
        score += 5;
      }
      
      return { doc, score };
    })
    .filter(item => item.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, limit)
    .map(item => item.doc);
}
