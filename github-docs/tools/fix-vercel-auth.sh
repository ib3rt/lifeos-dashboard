#!/bin/bash
# Fix Vercel Authentication

echo "🔧 Fixing Vercel Token..."
echo "========================="
echo ""

# Method 1: Interactive login
echo "Option 1: Interactive Login (Recommended)"
echo "  Run: vercel login"
echo "  Follow browser prompts"
echo ""

# Method 2: Token-based
echo "Option 2: Use Existing Token"
echo "  1. Go to: https://vercel.com/account/tokens"
echo "  2. Create new token"
echo "  3. Run: vercel --token YOUR_TOKEN"
echo ""

# Check if token provided as argument
if [ -n "$1" ]; then
    echo "Using provided token..."
    mkdir -p ~/.vercel
    echo '{"token":"'$1'"}' > ~/.vercel/auth.json
    echo "✅ Token saved"
    echo ""
    echo "Testing..."
    vercel whoami
else
    echo "No token provided."
    echo ""
    echo "To fix NOW:"
    echo "  1. Go to https://vercel.com/account/tokens"
    echo "  2. Click 'Create Token'"
    echo "  3. Copy the token"
    echo "  4. Paste it here"
    echo ""
    echo "I'll save it and test the connection."
fi
