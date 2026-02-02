# 🦾 Life OS Dashboard

Real-time Agent Status Dashboard for the Life OS multi-agent system.

![Dashboard Preview](https://img.shields.io/badge/status-online-22c55e)
![Agents](https://img.shields.io/badge/agents-15-blue)
![Build](https://img.shields.io/badge/build-passing-success)

## 🚀 Quick Start

This is a static HTML dashboard - no build step required!

```bash
# Local development
npx serve .

# Or simply open index.html in your browser
```

## 📁 Structure

```
lifeos-dashboard/
├── index.html          # Main dashboard (renamed from agent-status.html)
├── vercel.json         # Vercel deployment config
├── package.json        # NPM metadata
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## 🌐 Deployment

### GitHub Pages (Alternative)
1. Push to GitHub
2. Enable GitHub Pages in repo settings
3. Set source to main branch

### Vercel (Recommended)
1. Import repo at [vercel.com](https://vercel.com)
2. Framework preset: **Other** (static)
3. Deploy!

No build command needed - it's pure HTML/CSS/JS.

## 🔄 Auto-Refresh

Dashboard auto-refreshes every 30 seconds to show latest agent status.

## 📝 License

MIT

---

*Powered by OpenClaw & Neural Net Ned*
