# Feature List

## Core Features

### 📁 File Tree Navigation
- Hierarchical view of all markdown files in the workspace
- Expandable/collapsible folders
- Visual indicators for folders and files
- Scroll spy for large file trees
- Smooth animations on expand/collapse

### 📄 Document Viewer
- GitHub Flavored Markdown (GFM) support
- Syntax highlighting for code blocks (Prism.js)
- Auto-generated table of contents
- Scroll spy for TOC navigation
- Internal markdown link support
- Print-friendly layout

### 🔍 Instant Search
- Real-time search as you type
- Searches file titles, paths, and content excerpts
- Highlighted search results
- Keyboard navigable results
- Search history (last 10 searches)

### 🧭 Breadcrumb Navigation
- Full path breadcrumbs
- Clickable folders for quick navigation
- Sticky header with current location

### 📚 Recent Files
- Tracks last 10 viewed files
- Persists across sessions (localStorage)
- Quick access from sidebar
- Timestamps for each access

### 🌗 Theme Toggle
- Light and dark mode
- System preference detection
- Persisted preference
- Smooth transition between themes

## User Experience

### 📱 Mobile Responsiveness
- Collapsible sidebar with hamburger menu
- Touch-friendly targets (44px minimum)
- Responsive layouts for all screen sizes
- Mobile-optimized file tree

### ⌨️ Keyboard Shortcuts
- Full keyboard navigation
- Quick search (⌘K)
- Shortcuts reference modal
- Arrow key navigation
- Accessibility support

### ✨ Animations & Transitions
- Smooth expand/collapse
- Fade-in loading states
- Theme transitions
- Hover effects

### ♿ Accessibility
- ARIA labels throughout
- Screen reader announcements
- Skip links
- Focus indicators
- Keyboard navigation

### ⚡ Performance
- Static HTML/JS (no build step)
- Lazy-loaded syntax highlighting
- Optimized localStorage usage
- Efficient DOM updates

## Technical Features

### 🔧 Configuration
- No build required
- Simple deployment (static hosting)
- Configurable base path
- Customizable CSS variables

### 💾 Data Persistence
- Theme preference
- Expanded folders
- Recent files
- Search history
- Bookmarks

### 🔗 Deep Linking
- URL hash-based routing
- Direct links to any document
- Browser history support
- Shareable URLs

### 📊 Error Handling
- Network error detection
- Fallback states
- Retry functionality
- Error reporting
- Graceful degradation

## Browser Support

| Browser | Version | Status |
|---------|---------|--------|
| Chrome | 90+ | ✅ Full Support |
| Firefox | 88+ | ✅ Full Support |
| Safari | 14+ | ✅ Full Support |
| Edge | 90+ | ✅ Full Support |
| Mobile Safari | 14+ | ✅ Full Support |
| Chrome Mobile | 90+ | ✅ Full Support |

## Supported File Types

| Extension | Viewer | Syntax Highlighting |
|-----------|--------|---------------------|
| `.md` | Markdown | ✅ Yes |
| `.txt` | Plain Text | ❌ No |
| `.json` | JSON | ✅ Yes |
| `.yml` / `.yaml` | YAML | ✅ Yes |
| `.py` | Python | ✅ Yes |
| `.js` / `.jsx` | JavaScript | ✅ Yes |
| `.ts` / `.tsx` | TypeScript | ✅ Yes |
| `.html` | HTML | ✅ Yes |
| `.css` | CSS | ✅ Yes |
| `.sh` / `.bash` | Shell | ✅ Yes |
| `.sql` | SQL | ✅ Yes |
| And more... | Various | ✅ Yes |

## Dependencies

| Library | Purpose | Size |
|---------|---------|------|
| Marked.js | Markdown rendering | ~20KB |
| Prism.js | Syntax highlighting | ~15KB |
| Inter font | UI typography | ~200KB (variable) |
| JetBrains Mono | Code typography | ~100KB (variable) |

## Security

- No server-side processing
- No user data sent externally
- localStorage only for preferences
- CORS-friendly static serving
