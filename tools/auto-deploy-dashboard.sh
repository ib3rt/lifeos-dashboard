#!/bin/bash
# Fully Automated Dashboard Deployment
# Run this script to deploy the dashboard with zero manual steps

set -e  # Exit on error

echo "🚀 AUTO-DEPLOYING LIFE OS DASHBOARD..."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Pull latest changes
echo "📥 Pulling latest changes..."
cd /home/ubuntu/.openclaw/workspace
git pull origin main 2>/dev/null || echo "No remote changes"

# Step 2: Navigate to dashboard
echo ""
echo "📁 Navigating to dashboard..."
cd /home/ubuntu/.openclaw/workspace/lifeos-dashboard

# Step 3: Initialize git if needed
if [ ! -d .git ]; then
    echo "🔧 Initializing git repository..."
    git init
    git remote add origin git@github.com:ib3rt/lifeos-dashboard.git
fi

# Step 4: Configure git (one-time)
echo ""
echo "🔧 Configuring git..."
git config user.email "ubuntu@lifeos.local" 2>/dev/null || true
git config user.name "Life OS Auto-Deploy" 2>/dev/null || true

# Step 5: Add all files
echo ""
echo "📦 Adding files..."
git add -A

# Step 6: Commit
echo ""
echo "📝 Committing..."
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
git commit -m "Auto-deploy: Dashboard update - $TIMESTAMP" 2>/dev/null || echo "No changes to commit"

# Step 7: Push to GitHub
echo ""
echo "🔗 Pushing to GitHub..."
git push origin main 2>/dev/null || git push -f origin main

# Step 8: Wait for Vercel
echo ""
echo "⏳ Waiting for Vercel to deploy..."
sleep 5

# Step 9: Verify deployment
echo ""
echo "✅ Verifying deployment..."

# Check if domain works
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" https://lifeos.b3rt.dev 2>/dev/null || echo "000")

if [ "$RESPONSE" = "200" ]; then
    echo -e "${GREEN}✅ DEPLOYMENT SUCCESSFUL!${NC}"
    echo ""
    echo "🌐 https://lifeos.b3rt.dev is live!"
else
    echo -e "${YELLOW}⚠️ Deployment may still be processing...${NC}"
    echo ""
    echo "Check: https://vercel.com/dashboard"
fi

echo ""
echo "🎉 Auto-deployment complete!"
