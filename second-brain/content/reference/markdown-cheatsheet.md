---
title: "Markdown Cheatsheet"
date: "2026-02-03"
tags: ["reference", "markdown", "documentation"]
category: "reference"
description: "Quick reference for Markdown syntax"
---

# Markdown Cheatsheet

A quick reference guide for Markdown syntax used in Second Brain.

## Basic Syntax

### Headers
```markdown
# H1 Header
## H2 Header
### H3 Header
#### H4 Header
```

### Emphasis
```markdown
*italic* or _italic_
**bold** or __bold__
~~strikethrough~~
***bold and italic***
```

### Lists

**Unordered:**
```markdown
- Item 1
- Item 2
  - Nested item
  - Another nested
- Item 3
```

**Ordered:**
```markdown
1. First item
2. Second item
3. Third item
```

### Links
```markdown
[Link text](https://example.com)
[Link with title](https://example.com "Title")
```

### Images
```markdown
![Alt text](image.png)
![Alt text](image.png "Image title")
```

## Extended Syntax

### Code Blocks

Inline code: `const x = 1`

Fenced code blocks:
```javascript
function greet(name) {
  return `Hello, ${name}!`;
}
```

### Blockquotes
```markdown
> This is a blockquote
> It can span multiple lines
```

### Tables
```markdown
| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
| Cell 3   | Cell 4   |
```

### Task Lists
```markdown
- [x] Completed task
- [ ] Incomplete task
- [ ] Another task
```

### Horizontal Rule
```markdown
---
```

## Wiki Links

Second Brain supports Obsidian-style wiki links:

```markdown
[[Document Name]]
[[Document Name|Display Text]]
```

These automatically create bidirectional links between documents.

## Frontmatter

Every document starts with YAML frontmatter:

```yaml
---
title: "Document Title"
date: "2026-02-03"
tags: ["tag1", "tag2"]
category: "concepts"
description: "Brief description"
---
```

### Fields

| Field | Required | Description |
|-------|----------|-------------|
| title | Yes | Document title |
| date | Yes | Creation date (YYYY-MM-DD) |
| tags | No | Array of tags |
| category | Yes | journal, concepts, projects, or reference |
| description | No | Short description |

## Tips

1. Use blank lines between paragraphs
2. Indent nested list items with 2 spaces
3. Escape special characters with backslash: `\*`
4. Use reference-style links for cleaner text
