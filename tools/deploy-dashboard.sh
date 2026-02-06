#!/bin/bash
# Deploy dashboard and add domain

cd /home/ubuntu/.openclaw/workspace/lifeos-dashboard

# Push to GitHub
git add .
git commit -m "Dashboard update"
git push origin main

echo "✅ Pushed to GitHub - Vercel will auto-deploy"

echo ""
echo "📋 To add domain, visit:"
echo "   https://vercel.com/dashboard → lifeos-dashboard → Settings → Domains"
echo "   Add: lifeos.b3rt.dev"
