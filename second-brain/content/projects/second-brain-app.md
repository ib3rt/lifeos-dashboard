---
title: "Second Brain App"
date: "2026-02-03"
tags: ["project", "nextjs", "app-development"]
category: "projects"
description: "Building a personal knowledge management system"
---

# Second Brain App

A [[NextJS]] application for managing personal knowledge - combining [[Obsidian]]'s linked thinking with [[Linear]]'s polished UI.

## Project Overview

### Goals
1. Create a fast, beautiful document management system
2. Support Markdown with frontmatter
3. Enable wiki-style linking between documents
4. Provide automatic backlink discovery
5. Build a dark, comfortable reading experience

### Timeline
- **Phase 1**: Core document viewing and navigation (1 week)
- **Phase 2**: Search and filtering (1 week)
- **Phase 3**: Advanced features (ongoing)

## Technical Architecture

### Folder Structure
```
app/                 # Next.js App Router
components/          # React components
  documents/         # Document-related components
  layout/            # Layout components
content/             # Markdown content
  journal/           # Daily entries
  concepts/          # Knowledge base
  projects/          # Project docs
  reference/         # Reference materials
lib/                 # Utilities
  documents.ts       # Document loading
  markdown.ts        # Markdown processing
types/               # TypeScript types
```

### Key Components

#### DocumentList
- Sidebar navigation with categories
- Search/filter functionality
- Expandable folders

#### DocumentViewer
- Markdown rendering with syntax highlighting
- Table of contents
- Backlinks panel
- Tag display

#### SearchBar
- Command palette-style search
- Keyboard shortcuts (⌘K)
- Real-time filtering

## Features

### Implemented
- ✅ Category-based organization
- ✅ Tag system
- ✅ Backlinks
- ✅ Reading time estimation
- ✅ Responsive design

### In Progress
- 🔄 Full-text search
- 🔄 Graph visualization

### Planned
- ⏳ Daily journal templates
- ⏳ Export functionality
- ⏳ Git integration

## Resources

- [[Getting Started with Second Brain]]
- [[Knowledge Management Principles]]
