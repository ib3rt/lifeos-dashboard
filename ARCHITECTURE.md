# Architecture Documentation

Technical documentation for the Life OS Docs Viewer, including architecture decisions, file structure, and customization guide.

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [File Structure](#file-structure)
4. [Core Components](#core-components)
5. [Data Flow](#data-flow)
6. [Customization Guide](#customization-guide)
7. [Extending Features](#extending-features)

---

## Overview

The Life OS Docs Viewer is a client-side Single Page Application (SPA) designed for browsing markdown documentation. It uses vanilla JavaScript with no build step, making it easy to deploy and customize.

### Key Design Principles

- **No Build Step**: Pure HTML/CSS/JavaScript for easy deployment
- **Client-Side Only**: All processing happens in the browser
- **Progressive Enhancement**: Works without JavaScript (basic functionality)
- **Accessibility First**: Full ARIA support and keyboard navigation
- **Local Storage**: Persists user preferences without a backend

---

## Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           BROWSER                                        │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    Life OS Docs Viewer                           │   │
│  │                                                                   │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐   │   │
│  │  │   Sidebar   │  │  Main Area  │  │      Components        │   │   │
│  │  │  - Tree     │  │  - Content  │  │  - Breadcrumbs         │   │   │
│  │  │  - Search   │  │  - TOC      │  │  - Recent Files        │   │   │
│  │  │  - Recent   │  │  - Print    │  │  - Theme Toggle        │   │   │
│  │  └─────────────┘  └─────────────┘  └─────────────────────────┘   │   │
│  │                                                                   │   │
│  │  ┌─────────────────────────────────────────────────────────┐   │   │
│  │  │                      State Management                    │   │   │
│  │  │  - File Tree State  - Search State  - UI State          │   │   │
│  │  └─────────────────────────────────────────────────────────┘   │   │
│  │                                                                   │   │
│  │  ┌─────────────────────────────────────────────────────────┐   │   │
│  │  │                   Local Storage                          │   │   │
│  │  │  - Theme  - Expanded Folders  - Recent Files  - History  │   │   │
│  │  └─────────────────────────────────────────────────────────┘   │   │
│  │                                                                   │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                      External Services                           │   │
│  │  - Prism.js (syntax highlighting CDN)                           │   │
│  │  - Marked.js (markdown parsing CDN)                             │   │
│  │  - Google Fonts (Inter & JetBrains Mono)                         │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Component Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         COMPONENT RELATIONSHIPS                          │
└─────────────────────────────────────────────────────────────────────────┘

                           ┌─────────────┐
                           │   App.js    │ ← Main entry point
                           └──────┬──────┘
                                  │
          ┌───────────────────────┼───────────────────────┐
          │                       │                       │
          ▼                       ▼                       ▼
   ┌─────────────┐         ┌─────────────┐         ┌─────────────┐
   │  State      │         │  DOM        │         │  Storage    │
   │  Management │◄───────►│  Elements   │◄───────►│  Manager    │
   └─────────────┘         └─────────────┘         └─────────────┘
          │                       │                       │
          │                       │                       │
          ▼                       ▼                       ▼
   ┌─────────────┐         ┌─────────────┐         ┌─────────────┐
   │  File Tree  │         │  Renderer   │         │   Search    │
   │  Navigator  │         │  (Markdown) │         │  Index      │
   └─────────────┘         └─────────────┘         └─────────────┘
          │                       │                       │
          └───────────────────────┼───────────────────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │   Accessibility │
                         │   Manager       │
                         └─────────────────┘
```

---

## File Structure

```
docs-viewer/
├── index.html              # Main HTML entry point
├── app.js                  # Application logic (20KB+)
├── styles.css              # All styling (30KB+)
├── generate-index.py       # Index generation script
├── search-index.json       # Generated search index
├── debug.html              # Debug/testing page
├── diagnostic.html         # Diagnostic tools
├── vercel.json             # Vercel deployment config
├── test-minimal.html       # Minimal test page
├── README.md               # Overview & features
├── USAGE.md                # Detailed usage guide
├── SHORTCUTS.md            # Keyboard shortcuts reference
└── ARCHITECTURE.md        # Technical architecture
```

### Key Files

#### index.html
- **Purpose**: Main entry point
- **Contains**:
  - Sidebar structure
  - Main content area
  - Hidden accessibility regions
  - CDN script imports (Marked.js, Prism.js)
  - Font preconnects

#### app.js
- **Purpose**: Core application logic
- **Size**: ~20KB
- **Sections**:
  - Configuration constants
  - Error handling system
  - State management
  - DOM element references
  - Initialization logic
  - File tree rendering
  - Document loading
  - Search functionality
  - Theme management
  - Keyboard shortcuts

#### styles.css
- **Purpose**: Complete styling
- **Size**: ~30KB
- **Sections**:
  - CSS variables (themes, colors, spacing)
  - Reset & base styles
  - Layout (sidebar, main content)
  - Component styles (tree, search, TOC)
  - Error states
  - Print styles
  - Responsive design
  - Accessibility styles

#### generate-index.py
- **Purpose**: Generate search index
- **Input**: Markdown files in parent directory
- **Output**: `search-index.json`
- **Features**:
  - Recursive directory scanning
  - Content excerpt extraction
  - File metadata extraction

---

## Core Components

### 1. State Management

```javascript
const state = {
    index: null,              // Search index data
    fileTree: [],            // Hierarchical file tree
    expandedFolders: Set,    // IDs of expanded folders
    activeFile: null,        // Currently open file
    searchQuery: '',         // Current search text
    searchResults: [],       // Search results array
    isSidebarCollapsed: false,
    theme: 'dark',
    recentFiles: [],
    searchHistory: []
};
```

### 2. Error Handling System

```javascript
const ERROR_TYPES = {
    NETWORK: 'network',
    NOT_FOUND: 'not_found',
    PARSE: 'parse',
    STORAGE: 'storage',
    RENDER: 'render',
    CORS: 'cors',
    UNKNOWN: 'unknown'
};

// Features:
// - Automatic error type detection
// - Retry functionality
// - Error reporting
// - User-friendly error messages
```

### 3. File Tree Builder

```javascript
function buildFileTree(files) {
    // Converts flat file list to hierarchical tree
    // Input: [{path: 'docs/guide.md'}, ...]
    // Output: [{name: 'docs', children: [...]}]
}
```

### 4. Markdown Renderer

```javascript
// Uses Marked.js with custom configuration
marked.use({
    gfm: true,           // GitHub Flavored Markdown
    breaks: true,        // Convert \n to <br>
    headerIds: true,      // Add IDs to headings
    mangle: false         // Don't mangle email addresses
});
```

### 5. Code Highlighting

```javascript
// Prism.js integration
const handler = getFileTypeHandler(ext);  // Get handler by extension
const html = await handler(path, content);  // Render with highlighting
```

---

## Data Flow

### Loading a Document

```
User clicks file
    │
    ▼
┌──────────────┐
│ loadDocument │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Update tree │
│  active state│
└──────┬───────┘
       │
       ▼
┌──────────────┐
│Show loading  │
│spinner       │
└──────┬───────┘
       │
       ▼
┌──────────────┐     ┌──────────────┐
│ Fetch file   │────►│ Check cache  │
└──────┬───────┘     └──────────────┘
       │
       ▼
┌──────────────┐
│ Parse and   │
│ render       │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Update DOM   │
│ with content │
└──────┬───────┘
       │
       ▼
┌──────────────┐     ┌──────────────┐
│ Update TOC   │────►│ Add to       │
│ and scroll   │     │ recent files │
│ spy          │     │              │
└──────────────┘     └──────────────┘
```

### Search Flow

```
User types in search
    │
    ▼
┌──────────────┐
│ Update state │
│ searchQuery  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Debounce (if │
│ implemented) │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Filter index │◄── Load index on init
│ by query     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Render       │
│ results      │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Highlight     │
│ matches       │
└──────────────┘
```

---

## Customization Guide

### Changing the Base Path

Edit `app.js`:

```javascript
// Line ~30
const MARKDOWN_BASE_PATH = '../';  // Change to your path
```

### Adding New File Types

Edit `getFileTypeHandler()` in `app.js`:

```javascript
// Add to FILE_TYPE_HANDLERS object
FILE_TYPE_HANDLERS.rust = async function(path, content) {
    const highlighted = Prism.highlight(
        content,
        Prism.languages.rust,
        'rust'
    );
    return `<pre class="language-rust">${highlighted}</pre>`;
};

// Add extension mapping
handlers['rs'] = FILE_TYPE_HANDLERS.rust;
```

### Custom Styling

Create a custom CSS file and include it after `styles.css`:

```html
<!-- In index.html, after styles.css link -->
<link rel="stylesheet" href="custom.css">
```

```css
/* custom.css */
:root {
    /* Override default colors */
    --accent-color: #ff6b6b;
    --bg-primary: #1a1a2e;
    --font-sans: 'Your Font', sans-serif;
}

.sidebar {
    /* Custom sidebar styling */
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
}
```

### Custom Logo

Edit `index.html`:

```html
<div class="logo" aria-hidden="true">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <!-- Your custom icon SVG -->
    </svg>
    <span>Your Title</span>
</div>
```

### Adding Custom JavaScript

Create a `custom.js` file:

```javascript
// custom.js
// Your custom functionality

// Example: Add a custom button to toolbar
function addCustomButton() {
    const footer = document.querySelector('.sidebar-footer');
    const button = document.createElement('button');
    button.innerHTML = '⚡ Custom';
    button.className = 'custom-btn';
    button.addEventListener('click', () => {
        console.log('Custom button clicked!');
    });
    footer.appendChild(button);
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', addCustomButton);
} else {
    addCustomButton();
}
```

Include it in `index.html`:

```html
<script src="custom.js"></script>
```

---

## Extending Features

### Adding a New Theme

1. Add theme CSS variables:

```css
[data-theme="custom"] {
    --bg-primary: #1e1e2e;
    --text-primary: #cdd6f4;
    --accent-color: #89b4fa;
    /* ... more variables */
}
```

2. Add toggle option in `app.js`:

```javascript
// In toggleTheme function, add 'custom' to cycle
const themes = ['light', 'dark', 'custom'];
```

### Adding Analytics

Create an analytics service:

```javascript
// analytics.js
const Analytics = {
    track: function(event, data) {
        // Example: Send to Google Analytics
        gtag('event', event, data);
        
        // Or log to console
        console.log('[Analytics]', event, data);
    }
};

// Track document views
function trackDocumentView(path) {
    Analytics.track('document_view', { path });
}
```

Call in `loadDocument()`:

```javascript
// At end of loadDocument function
trackDocumentView(path);
```

### Adding Print Styles

Edit `styles.css`:

```css
@media print {
    .sidebar,
    .breadcrumbs,
    .table-of-contents {
        display: none !important;
    }
    
    .main-content {
        margin: 0;
        padding: 0;
    }
    
    .document {
        max-width: 100%;
        padding: 20px;
    }
}
```

### Adding Custom Renderers

Create a custom renderer:

```javascript
// custom-renderer.js
marked.use({
    renderer: {
        heading(text, level) {
            // Custom heading rendering
            return `<h${level} class="custom-heading">${text}</h${level}>`;
        },
        
        link(href, title, text) {
            // Add target=_blank for external links
            const isExternal = href.startsWith('http');
            if (isExternal) {
                return `<a href="${href}" title="${title || ''}" target="_blank" rel="noopener">${text} ↗</a>`;
            }
            return marked.Renderer.prototype.link.call(this, href, title, text);
        }
    }
});
```

### Adding Internationalization (i18n)

```javascript
// i18n.js
const translations = {
    en: {
        'search.placeholder': 'Search docs...',
        'recent.files': 'Recent Files',
        'theme.toggle': 'Toggle dark mode'
    },
    es: {
        'search.placeholder': 'Buscar documentos...',
        'recent.files': 'Archivos recientes',
        'theme.toggle': 'Cambiar modo oscuro'
    }
};

function t(key) {
    const lang = document.documentElement.lang || 'en';
    return translations[lang]?.[key] || translations.en[key] || key;
}

// Use: t('search.placeholder')
```

---

## Performance Considerations

### Large Documentation Sets

For large documentation sets:

1. **Lazy Loading**: Modify `loadDocument()` to fetch on demand
2. **Virtual Scrolling**: Implement for file tree with thousands of items
3. **Web Workers**: Move search to a Web Worker

### Caching

The viewer uses browser caching:

```javascript
// Service Worker example (sw.js)
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open('docs-cache-v1').then((cache) => {
            return cache.addAll([
                '/',
                '/docs-viewer/',
                '/docs-viewer/index.html',
                '/docs-viewer/styles.css',
                '/docs-viewer/app.js'
            ]);
        })
    );
});
```

---

## Browser Compatibility

### Minimum Supported Versions

| Browser | Version | Notes |
|---------|---------|-------|
| Chrome | 90+ | Full support |
| Firefox | 88+ | Full support |
| Safari | 14+ | Full support |
| Edge | 90+ | Full support |

### Feature Detection

```javascript
// Check for required features
const supportsLocalStorage = (() => {
    try {
        localStorage.setItem('test', 'test');
        localStorage.removeItem('test');
        return true;
    } catch (e) {
        return false;
    }
})();

const supportsFetch = typeof fetch === 'function';
const supportsES6 = (() => {
    try {
        new Function('() => {}');
        return true;
    } catch (e) {
        return false;
    }
})();
```

---

## Deployment

### Vercel

The included `vercel.json` configures Vercel deployment:

```json
{
    "rewrites": [
        { "source": "/docs-viewer/(.*)", "destination": "/docs-viewer/index.html" }
    ]
}
```

### Netlify

Create `netlify.toml`:

```toml
[[redirects]]
from = "/docs-viewer/*"
to = "/docs-viewer/index.html"
status = 200
```

### Apache

Add to `.htaccess`:

```apache
RewriteEngine On
RewriteRule ^docs-viewer/(.*)$ docs-viewer/index.html [L]
```

### Nginx

Add to server config:

```nginx
location /docs-viewer/ {
    try_files $uri $uri/ /docs-viewer/index.html;
}
```

---

## Troubleshooting

### Common Issues

**1. Files not loading**
- Check CORS headers on server
- Verify `MARKDOWN_BASE_PATH` is correct
- Check browser console for errors

**2. Search not working**
- Regenerate `search-index.json`
- Verify JSON is valid
- Check file encoding (use UTF-8)

**3. Styles not applying**
- Clear browser cache
- Verify CSS file path
- Check for CSS conflicts

### Debug Mode

Enable debug logging:

```javascript
// In app.js, set at top
const DEBUG = true;

function debug(...args) {
    if (DEBUG) {
        console.log('[Docs Viewer]', ...args);
    }
}
```

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Test in multiple browsers
5. Submit pull request

---

## License

MIT License - See repository root for full license text.
