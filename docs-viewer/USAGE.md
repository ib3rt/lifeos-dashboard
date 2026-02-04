# Usage Guide

This guide provides detailed instructions for using the Life OS Docs Viewer effectively.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Navigating Documents](#navigating-documents)
3. [Using Search](#using-search)
4. [Reading Documents](#reading-documents)
5. [Customization](#customization)
6. [Advanced Features](#advanced-features)

---

## Getting Started

### Opening the Viewer

1. Start a web server in the project directory:
   ```bash
   python3 -m http.server 8000
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:8000/docs-viewer/
   ```

3. You should see the documentation viewer with an empty file tree

### Loading Your Documentation

The viewer looks for markdown files in the parent directory. To add your documentation:

1. Create or copy markdown files (`.md`) to the parent directory
2. Run the index generator:
   ```bash
   cd docs-viewer
   python3 generate-index.py
   ```
3. Refresh the browser to see your documents

---

## Navigating Documents

### File Tree Navigation

The sidebar displays all your documentation in a hierarchical folder structure:

- **Folders**: Click to expand/collapse and reveal nested files
- **Files**: Click to open and view the document
- **Visual Feedback**: Active file is highlighted with accent color

### Keyboard Navigation in Tree

| Key | Action |
|-----|--------|
| `↑` / `↓` | Move selection up/down |
| `←` | Collapse folder or move to parent |
| `→` | Expand folder or move to first child |
| `Enter` | Open selected file |
| `Home` | Jump to first item |
| `End` | Jump to last item |

### Breadcrumbs

The breadcrumb bar at the top shows your current location:

```
Home / project / documentation / guide.md
```

- Click any folder in the breadcrumbs to navigate there
- The current file is shown without a link
- Click "Home" to return to the root

### Recent Files

The sidebar shows your 10 most recently accessed documents:

- Recently opened files appear at the top of the sidebar
- Click any file to open it immediately
- Click "Clear" to remove all recent files

---

## Using Search

### Opening Search

**Method 1:** Click in the search bar in the sidebar

**Method 2:** Press `Cmd+K` (Mac) or `Ctrl+K` (Windows/Linux)

**Method 3:** Start typing while nothing is focused

### Search Features

- **Instant Results:** Search results appear as you type
- **File Matching:** Searches filenames, paths, and content excerpts
- **Highlighting:** Matching terms are highlighted in results
- **Navigation:** Use `↑` / `↓` to navigate results, `Enter` to select
- **Clear:** Press `Esc` to clear the search

### Search Tips

1. **Partial matching**: Search finds partial matches (e.g., "config" finds "configuration.md")
2. **Path search**: Include `/` in your search to match paths (e.g., "docs/api")
3. **Quick access**: Results are clickable - click to open directly

---

## Reading Documents

### Document Viewer

When you open a markdown file, the content is rendered with:

- **Proper typography** - Clean, readable fonts (Inter for text, JetBrains Mono for code)
- **Syntax highlighting** - Code blocks with Prism.js for 50+ languages
- **Tables** - Styled tables with proper borders
- **Blockquotes** - Highlighted quoted content
- **Task lists** - Checkboxes for todo items

### Table of Contents

For each document, an automatic TOC appears on the right:

- Generated from H2 and H3 headings
- Click any link to jump to that section
- Active section is highlighted as you scroll

### Scroll Spy

The viewer automatically tracks your scroll position:

- Current section is highlighted in the TOC
- Smooth scrolling when clicking TOC links
- Works with all heading levels

### Internal Links

Markdown files can link to each other:

```markdown
[See the API Guide](api-reference.md)

[Related Section](../other-folder/section.md)
```

Clicking these links opens the linked document in the viewer.

### Code Blocks

The viewer syntax highlights:

- **Python, JavaScript, TypeScript**
- **Bash/Shell, JSON, YAML**
- **HTML, CSS, SQL**
- **And 40+ more languages**

### Printing

Press `Cmd+P` / `Ctrl+P` to print the current document:

- Clean print layout without UI elements
- Preserves syntax highlighting
- Includes TOC and all document content

---

## Customization

### Theme

Toggle between light and dark modes:

- **Button**: Click the sun/moon icon in the sidebar footer
- **Shortcut**: Press `Cmd+D` / `Ctrl+D`
- **Persistence**: Your preference is saved automatically

### Sidebar

Collapse or expand the sidebar:

- **Button**: Click the toggle button in the sidebar header
- **Persistence**: Collapsed state is saved locally

### Font Size

The viewer uses responsive typography. To customize:

1. Open browser developer tools (F12)
2. Find the CSS variables in `styles.css`
3. Adjust `--font-sans` and related variables

---

## Advanced Features

### Deep Linking

Each document has a unique URL:

```
http://localhost:8000/docs-viewer/#project/documentation/guide.md
```

- Bookmark specific documents for quick access
- Share links that open directly to a document
- Browser back/forward navigation works correctly

### Local Storage Persistence

The viewer saves your preferences locally:

| Data | Description |
|------|-------------|
| Theme preference | Light or dark mode |
| Sidebar state | Collapsed or expanded |
| Expanded folders | Which folders are open |
| Recent files | Last 10 accessed documents |
| Search history | Last 10 searches |

### Error Handling

The viewer handles errors gracefully:

- **Network errors**: Retry button with helpful messages
- **Missing files**: Clear error with "Report Issue" option
- **Storage full**: Automatic cleanup of old data

### Accessibility

The viewer is designed for accessibility:

- **Keyboard navigation**: Complete mouse-free operation
- **Screen readers**: ARIA labels and live regions
- **Focus management**: Visible focus indicators
- **Skip links**: Quick access to main content

---

## Tips and Tricks

### Quick File Switching

1. Use `Cmd+K` to focus search
2. Type part of the filename
3. Press `Enter` to open the first result

### Bookmark a Position

1. Navigate to a document
2. Press `Cmd+S` / `Ctrl+S`
3. The document is saved to your recent files

### Multiple Monitor Setup

Keep the viewer open on one monitor while working on another. Deep links ensure you always return to the right document.

### Batch Indexing

After adding many files:

```bash
# Watch for changes and auto-regenerate index
while true; do
    python3 generate-index.py
    sleep 5
done
```

---

## Need Help?

- See the [README](README.md) for quick reference
- Check the [Shortcuts Reference](SHORTCUTS.md) for keyboard shortcuts
- Review the [Architecture](ARCHITECTURE.md) for technical details
