#!/bin/bash
# Add custom domain to Vercel project

# Check if token exists
if [ -z "$VERCEL_TOKEN" ]; then
    echo "❌ VERCEL_TOKEN environment variable not set"
    echo ""
    echo "To automate, set token:"
    echo "  export VERCEL_TOKEN=your_token_here"
    echo ""
    echo "Or add manually:"
    echo "  1. Go to: https://vercel.com/dashboard"
    echo "  2. Click: lifeos-dashboard → Settings → Domains"
    echo "  3. Add: lifeos.b3rt.dev"
    exit 1
fi

# Add domain via API
curl -X POST "https://api.vercel.com/v6/domains" \
  -H "Authorization: Bearer $VERCEL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "lifeos.b3rt.dev",
    "projectId": "prj_xxxxx"
  }' 2>/dev/null

echo ""
echo "✅ Domain addition attempted via API"
