#!/bin/bash
# X (Twitter) Automation - Life OS

source ~/.openclaw/keys/x_api.key

echo "╔═══════════════════════════════════════════════════════╗"
echo "║        🐦 X (TWITTER) AUTOMATION SYSTEM         ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

# Menu
echo "Options:"
echo "  1. Post a tweet"
echo "  2. Post with image"
echo "  3. Get user timeline"
echo "  4. Search hashtag"
echo "  5. Auto-post metrics"
echo "  6. Exit"
echo ""
read -p "Choose (1-6): " choice

case $choice in
    1)
        echo ""
        read -p "Enter your tweet: " tweet
        /home/ubuntu/.openclaw/workspace/tools/x-integration/post-tweet.sh "$tweet"
        ;;
    2)
        echo "Image posting requires additional setup"
        echo "Coming soon!"
        ;;
    3)
        echo "📜 Getting your timeline..."
        curl -s "https://api.twitter.com/2/users/me/tweets" \
          -H "Authorization: Bearer $X_API_KEY" | jq
        ;;
    4)
        echo ""
        read -p "Enter hashtag (without #): " hashtag
        echo "🔍 Searching for #$hashtag..."
        echo "Coming soon!"
        ;;
    5)
        echo "📊 Posting daily metrics..."
        DATE=$(date +"%Y-%m-%d %H:%M")
        /home/ubuntu/.openclaw/workspace/tools/x-integration/post-tweet.sh "📊 Life OS Daily Update - $DATE | All systems nominal! 🦾"
        ;;
    6)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice"
        ;;
esac
