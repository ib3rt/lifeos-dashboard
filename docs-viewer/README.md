# Life OS Docs Viewer

A modern, feature-rich documentation viewer for browsing and navigating markdown documentation with a clean, accessible interface.

![Life OS Docs Viewer Screenshot](docs-viewer-screenshot.png)

## Features

### 📚 Document Navigation
- **Hierarchical File Tree** - Browse your documentation in a collapsible folder structure
- **Breadcrumb Navigation** - Quick navigation showing your current location
- **Recent Files** - Quickly access recently opened documents
- **Deep Linking** - Shareable URLs with direct links to specific documents

### 🔍 Search
- **Instant Search** - Quick search across all documentation
- **Smart Filtering** - Search by filename, path, or content excerpts
- **Keyboard Shortcuts** - Press `Cmd+K` / `Ctrl+K` to focus search instantly

### 🎨 Theming
- **Dark/Light Mode** - Toggle between themes with `Cmd+D` / `Ctrl+D`
- **Auto-detect Preference** - Respects your system preference by default
- **Persistent Settings** - Theme preference is saved locally

### 📖 Reading Experience
- **Table of Contents** - Auto-generated TOC for easy navigation within documents
- **Scroll Spy** - Automatically highlights the current section as you scroll
- **Syntax Highlighting** - Beautiful code blocks with Prism.js support for 20+ languages
- **Responsive Design** - Optimized for desktop and mobile devices

### ⌨️ Keyboard Accessibility
- **Full Keyboard Navigation** - Navigate the entire interface without a mouse
- **Screen Reader Support** - ARIA labels and live announcements for accessibility
- **Keyboard Shortcuts Modal** - Press `Cmd+/` / `Ctrl+/` to view all shortcuts

### 💾 Persistence
- **Recent Files History** - Automatically tracks your recently accessed documents
- **Expanded Folders** - Remembers which folders you've expanded
- **Last Position** - Remembers your last opened document

### Using Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd docs-viewer
vercel --prod
```

### Using GitHub Integration

1. Push the `docs-viewer` folder to a GitHub repository
2. Go to [vercel.com/new](https://vercel.com/new)
3. Import your repository
4. Vercel automatically detects static files - no build command needed
5. Click **Deploy**

### Using Netlify

1. Push the `docs-viewer` folder to a GitHub repository
2. Go to [app.netlify.com/start](https://app.netlify.com/start)
3. Select your repository
4. Set build command: empty
5. Set publish directory: `docs-viewer`
6. Click **Deploy site**

## Project Structure

```
docs-viewer/
├── index.html              # Main HTML structure
├── app.js                  # Application logic (1958 lines)
├── styles.css              # All styling (light/dark modes)
├── search-index.json       # Generated index of 197 markdown files
├── generate-index.py       # Script to regenerate search index
├── vercel.json             # Vercel deployment configuration
├── .vercel/                # Vercel project settings
│   └── project.json
├── README.md               # This documentation
├── FEATURES.md             # Detailed feature list
├── KEYBOARD_SHORTCUTS.md   # Keyboard shortcuts reference
├── diagnostic.html         # Browser-based diagnostic tool
└── test-*.html            # Testing files
```

## 📊 Statistics

- **Total Files Indexed**: 197 markdown files
- **Code Lines**: ~1958 (app.js) + 1000+ (styles.css)
- **Dependencies**: Marked.js, Prism.js (CDN)
- **Local Storage Keys**: 6 (theme, sidebar, expanded, recent, search, lastFile)
- **Keyboard Shortcuts**: 14+ shortcuts supported
- **Supported Languages**: 20+ for syntax highlighting

### Prerequisites
- A modern web browser (Chrome, Firefox, Safari, Edge)
- A web server (or use local file serving)

### Installation

1. **Clone or download** the docs viewer to your project
2. **Place your markdown files** in the parent directory
3. **Run the index generator** to create the search index:
   ```bash
   python3 generate-index.py
   ```
4. **Serve the directory** with any web server:
   ```bash
   # Using Python
   python3 -m http.server 8000
   
   # Using Node.js
   npx serve .
   
   # Using PHP
   php -S localhost:8000
   ```

5. **Open your browser** to `http://localhost:8000/docs-viewer/`

### Adding Your Documentation

1. Create markdown (`.md`) files in the parent directory
2. Optionally add code files (`.py`, `.js`, `.json`, etc.) for syntax highlighting
3. Run `python3 generate-index.py` to update the search index
4. Refresh the page to see your new documents

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `↑` / `↓` | Navigate file tree |
| `←` / `→` | Collapse/expand folders |
| `Enter` | Open selected file |
| `Backspace` | Go up one level |
| `Home` | Go to first item |
| `End` | Go to last item |
| `Cmd+K` / `Ctrl+K` | Focus search |
| `Cmd+/` / `Ctrl+/` | Show shortcuts |
| `Cmd+P` / `Ctrl+P` | Print document |
| `Cmd+S` / `Ctrl+S` | Save bookmark |
| `Cmd+D` / `Ctrl+D` | Toggle dark mode |
| `Esc` | Clear search / Close modal |

## Browser Support

| Browser | Version |
|---------|---------|
| Chrome | 90+ |
| Firefox | 88+ |
| Safari | 14+ |
| Edge | 90+ |

## FAQ

### Q: Can I customize the appearance?
Yes! The viewer uses CSS variables for easy theming. Edit the `:root` section in `styles.css` to customize colors, fonts, and spacing.

### Q: How do I add more file types?
The viewer supports syntax highlighting for many languages. For additional languages, add the appropriate Prism.js component script to `index.html`.

### Q: Can I use this offline?
Yes! The viewer works offline once loaded. However, initial setup requires an internet connection to fetch external dependencies (fonts, Prism.js).

### Q: How do I change the base path for documents?
Edit the `MARKDOWN_BASE_PATH` constant in `app.js` to point to your documentation directory.

### Q: Can I link between documents?
Yes! Use relative markdown links like `[Link Text](other-document.md)` to link between documents within your documentation.

### Q: How do I generate the search index?
Run `python3 generate-index.py` from the docs-viewer directory. This scans for all markdown files and creates the `search-index.json` file.

### Q: Can I add custom CSS for my documents?
Yes! Add a `<style>` block in your markdown files or create a custom stylesheet and include it in the document wrapper.

## Troubleshooting

**Files not appearing in the tree?**
- Ensure you've run `generate-index.py` to create the search index
- Check that your markdown files are in the correct directory

**Search not finding results?**
- Regenerate the search index after adding new files
- Check that the search index JSON is valid

**Dark mode not working?**
- Check that localStorage is enabled in your browser
- Try manually toggling the theme to reset the state

## License

MIT License - Feel free to use and customize for your projects.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.
