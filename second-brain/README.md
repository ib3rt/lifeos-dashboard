# 🧠 Second Brain

A personal knowledge management system that combines the best of Obsidian's linked thinking with Linear's polished UI. Built with Next.js 14, TypeScript, and Tailwind CSS.

![Second Brain Screenshot](https://via.placeholder.com/800x400/1f2937/3b82f6?text=Second+Brain+App)

## ✨ Features

- **📚 Document Management**: Organize content into Journal, Concepts, Projects, and Reference
- **🔗 Wiki-Style Links**: Use `[[Document Name]]` to create bidirectional links
- **🏷️ Tags**: Categorize and filter content with tags
- **🔍 Full-Text Search**: Quick document search with keyboard shortcut (⌘K)
- **🌙 Dark Mode**: Easy on the eyes for long sessions
- **📱 Responsive**: Works on desktop, tablet, and mobile
- **⚡ Fast**: Static site generation for instant page loads

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd second-brain

# Install dependencies
npm install

# Run development server
npm run dev

# Open http://localhost:3000
```

## 📝 Creating Content

All documents are Markdown files stored in the `content/` directory:

```
content/
├── journal/       # Daily thoughts and reflections
├── concepts/      # Ideas and knowledge
├── projects/      # Project documentation
└── reference/     # Reference materials
```

### Document Format

```markdown
---
title: "Your Document Title"
date: "2026-02-03"
tags: ["tag1", "tag2"]
category: "concepts"
description: "Brief description"
---

# Your Content

Write in **Markdown** with support for:

- Headers, lists, and formatting
- Code blocks with syntax highlighting
- [[Wiki-style links]] to other documents
- Tables and task lists
```

### Wiki Links

Create connections between documents:

```markdown
See [[Getting Started]] for more info.
Use [[Another Page|custom display text]].
```

## 🛠️ Development

### Build for Production

```bash
npm run build
```

This generates a static site in the `dist/` folder.

### Project Structure

```
second-brain/
├── app/                    # Next.js App Router
│   ├── docs/[slug]/        # Document pages
│   ├── journal/            # Journal view
│   ├── tags/               # Tag browser
│   └── page.tsx            # Dashboard
├── components/
│   ├── documents/          # Document components
│   └── layout/             # Layout components
├── content/                # Markdown content
├── lib/
│   ├── documents.ts        # Document loading utilities
│   └── markdown.ts         # Markdown processing
├── types/                  # TypeScript types
└── public/                 # Static assets
```

### Key Technologies

- **Next.js 14**: App Router, Server Components, Static Generation
- **TypeScript**: Type safety throughout
- **Tailwind CSS**: Utility-first styling
- **gray-matter**: YAML frontmatter parsing
- **unified/remark/rehype**: Markdown processing pipeline
- **highlight.js**: Syntax highlighting

## 🚀 Deployment

### Vercel (Recommended)

1. Push to GitHub
2. Import in Vercel
3. Deploy automatically

### Static Export

The app is configured for static export:

```javascript
// next.config.ts
const config = {
  output: 'export',
  distDir: 'dist',
};
```

## 🎨 Customization

### Styling

- Global styles: `app/globals.css`
- Tailwind config: Modify classes directly in components
- Colors: Uses CSS variables for theming

### Adding Categories

1. Create folder in `content/`
2. Update `DocumentFrontmatter['category']` type
3. Add icon to `categoryIcons` in DocumentList

## 📝 License

MIT License - feel free to use this for your own Second Brain!

## 🙏 Credits

- Inspired by [Obsidian](https://obsidian.md/) for knowledge linking
- UI patterns from [Linear](https://linear.app/) for clean design
- Built with [Next.js](https://nextjs.org/) and [Tailwind CSS](https://tailwindcss.com/)
