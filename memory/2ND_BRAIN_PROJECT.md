# 2nd Brain Project

## Overview
A NextJS document management system that feels like a mix of Obsidian and Linear. This is b3rt's personal knowledge base where Claw creates documents during conversations.

## Status: 🚧 IN DEVELOPMENT

## Purpose
- Capture important concepts from daily conversations
- Maintain daily journal entries
- Build a searchable knowledge base over time
- Create a "second brain" for b3rt's Life OS

## Tech Stack
- NextJS 14+ with App Router
- TypeScript
- Tailwind CSS
- Dark mode (Obsidian-inspired)
- Linear-inspired UI animations

## Folder Structure
```
content/
├── journal/           # Daily journal entries (auto-generated)
├── concepts/          # Important concepts from conversations
├── projects/          # Project documentation
└── reference/         # Reference materials
```

## Auto-Generation Rules

### Daily Journal
- Created at end of each day
- Summarizes all conversations
- High-level overview of topics discussed
- Decisions made, actions taken

### Concept Documents
- Created when important concepts emerge
- Deep dives into ideas worth preserving
- Linked to related concepts
- Tagged for discoverability

### Triggers for Document Creation
1. New project discussed → Create project doc
2. Important decision → Create decision doc
3. Complex concept explained → Create concept doc
4. Useful tool/process discovered → Create reference doc
5. End of day → Create journal entry

## Features
- [ ] Sidebar document list with search
- [ ] Markdown rendering with syntax highlighting
- [ ] Tag-based navigation
- [ ] Backlinks support ([[like this]])
- [ ] Daily journal view
- [ ] Full-text search
- [ ] Dark mode (default)
- [ ] Smooth animations (Linear-style)

## Deployment
- Target: Vercel
- URL: TBD

## Created
2026-02-03

## Builder
Sub-agent: 2nd-brain-build
