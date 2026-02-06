export interface DocumentFrontmatter {
  title: string;
  date: string;
  tags: string[];
  category: 'journal' | 'concepts' | 'projects' | 'reference';
  description?: string;
}

export interface Document {
  slug: string;
  frontmatter: DocumentFrontmatter;
  content: string;
  backlinks: string[];
  readingTime: number;
}

export interface TagCount {
  tag: string;
  count: number;
}

export interface Backlink {
  slug: string;
  title: string;
  excerpt: string;
}
