# 🚀 Manual Deployment Guide: Life OS Dashboard

*Since the Vercel CLI decided to be coy, here's the bulletproof manual approach!*

---

## Step 1: Create GitHub Repository

1. Go to **https://github.com/new**
2. Repository name: `lifeos-dashboard`
3. Description: "Real-time Agent Status Dashboard for the Life OS multi-agent system"
4. Set to **Public** (for easy Vercel deployment)
5. **DO NOT** initialize with README (we already have one)
6. Click **Create repository**

---

## Step 2: Push Local Files to GitHub

Run these commands in your terminal:

```bash
cd /home/ubuntu/.openclaw/workspace/lifeos-dashboard

# Add the remote (replace YOURUSERNAME with your actual GitHub username)
git remote add origin https://github.com/YOURUSERNAME/lifeos-dashboard.git

# Push to GitHub
git push -u origin main
```

**Note:** You'll be prompted to authenticate. Use:
- HTTPS: Enter your GitHub username and **Personal Access Token** (not password!)
- Or set up SSH keys for passwordless auth

---

## Step 3: Deploy to Vercel

### Option A: Web Interface (Easiest)

1. Go to **https://vercel.com/new**
2. Sign in with GitHub (if not already signed in)
3. Find and select the `lifeos-dashboard` repo
4. Configure:
   - **Framework Preset:** `Other` (static site)
   - **Build Command:** *(leave empty)*
   - **Output Directory:** *(leave empty)*
5. Click **Deploy**

### Option B: Vercel CLI (If Available)

```bash
# Install Vercel CLI if not already installed
npm i -g vercel

# Login and deploy
vercel login
vercel --prod
```

---

## Step 4: Verify Deployment

Once deployed, Vercel will provide:
- **Production URL:** `https://lifeos-dashboard-xxx.vercel.app`
- **Dashboard:** `https://vercel.com/dashboard`

---

## 📋 Files Being Deployed

| File | Purpose |
|------|---------|
| `index.html` | Main dashboard UI |
| `vercel.json` | Vercel configuration (static routing) |
| `README.md` | Documentation |
| `.gitignore` | Git ignore rules |
| `package.json` | NPM metadata |

---

## 🔧 Vercel Configuration (vercel.json)

```json
{
  "version": 2,
  "name": "lifeos-dashboard",
  "builds": [{"src": "index.html", "use": "@vercel/static"}],
  "routes": [{"src": "/(.*)", "dest": "/index.html"}]
}
```

---

## ✅ Post-Deployment Checklist

- [ ] GitHub repo created at `github.com/YOURUSERNAME/lifeos-dashboard`
- [ ] All files pushed to main branch
- [ ] Vercel project imported from GitHub
- [ ] Deployment successful (green checkmark)
- [ ] Live URL accessible in browser
- [ ] Dashboard auto-refresh working (30s interval)

---

## 🐛 Troubleshooting

**Git push rejected?**
```bash
git pull origin main --rebase
git push -u origin main
```

**Vercel build fails?**
- Ensure Framework Preset is set to `Other` (not Next.js!)
- No build command needed for static HTML

**Changes not showing?**
- Vercel auto-deploys on every git push
- Check deployment logs at `vercel.com/dashboard`

---

*Deploy on, fellow netizen! 🦾*

— **Neural Net Ned**
