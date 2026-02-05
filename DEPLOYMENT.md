# Deployment Guide

## 🚀 Quick Deploy to Vercel

### Option 1: GitHub Integration (Recommended)

1. **Create a GitHub repository** for the docs-viewer folder
2. **Push the code**:
   ```bash
   cd docs-viewer
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/docs-viewer.git
   git push -u origin main
   ```
3. **Connect to Vercel**:
   - Go to [vercel.com/new](https://vercel.com/new)
   - Import your repository
   - Vercel auto-detects: Static HTML (no build command)
   - Deploy! 🎉

### Option 2: Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy to preview
cd docs-viewer
vercel

# Deploy to production
vercel --prod
```

### Option 3: Drag & Drop

1. Go to [vercel.com/new](https://vercel.com/new)
2. Select "Upload" tab
3. Drag the entire `docs-viewer` folder
4. Deploy! 🎉

## 🌐 Alternative Platforms

### Netlify

1. Push `docs-viewer` to GitHub
2. Connect to Netlify
3. Settings:
   - Build command: (leave empty)
   - Publish directory: `docs-viewer`
   - Deploy

### Cloudflare Pages

1. Push `docs-viewer` to GitHub
2. Connect to Cloudflare Pages
3. Build settings: None (Static)
4. Deploy

### GitHub Pages

1. Push `docs-viewer` to GitHub
2. Enable GitHub Pages in repository settings
3. Deploy from `/docs` folder or root

## 📋 Post-Deployment Checklist

- [ ] Test file tree navigation
- [ ] Verify search functionality
- [ ] Test keyboard shortcuts
- [ ] Check mobile responsiveness
- [ ] Verify dark/light mode
- [ ] Test document rendering
- [ ] Check deep linking (URL hash)
- [ ] Verify recent files tracking
- [ ] Test error states
- [ ] Check accessibility

## 🔧 Configuration

### Vercel Headers (vercel.json)

```json
{
  "version": 2,
  "builds": [
    {
      "src": "*.{html,js,json,css,md}",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "headers": {
        "Cache-Control": "public, max-age=0, must-revalidate"
      }
    }
  ]
}
```

## 🔗 Shareable URLs

After deployment, users can access documents directly via:

```
https://your-project.vercel.app/#workspace/dashboard/README.md
```

The hash-based routing allows deep linking to any document.

## 📊 Expected Performance

- **First Contentful Paint**: < 500ms
- **Time to Interactive**: < 1s
- **Lighthouse Score**: 95+
- **Bundle Size**: ~50KB (gzipped)
- **Dependencies**: External (CDN)

## 🐛 Troubleshooting

**404 on documents?**
- Ensure `search-index.json` is in the root
- Check base path configuration in app.js

**Search not working?**
- Regenerate index: `python3 generate-index.py`
- Verify search-index.json is valid JSON

**Styles not loading?**
- Check CDN links in index.html
- Verify styles.css is accessible

**Dark mode persists incorrectly?**
- Check localStorage isn't blocked
- Try clearing browser cache

## 📞 Support

For issues with:
- Deployment → Check Vercel dashboard logs
- Functionality → Review diagnostic.html
- Customization → See README.md and FEATURES.md
