#!/bin/bash
# Life OS Skills Installer
# Install recommended skills for maximum productivity

set -e

SKILLS=(
    # Productivity
    "notion"
    "obsidian" 
    "trello"
    "things-mac"
    "summarize"
    
    # Communication
    "slack"
    
    # Calendar
    "apple-reminders"
    
    # Research
    "github"
    "blogwatcher"
    
    # Media
    "openai-image-gen"
    "remotion-video-toolkit"
    
    # Finance
    "crypto-tracker"
    
    # Security
    "1password"
)

echo "🚀 Installing Life OS Skills..."
echo ""

for skill in "${SKILLS[@]}"; do
    echo "Installing: $skill"
    npx clawhub@latest install "$skill" --quiet 2>/dev/null || {
        echo "  ⚠️  Failed or already installed"
    }
done

echo ""
echo "✅ Skills installation complete!"
echo ""
echo "To use a skill, just ask your AI assistant."
echo "Example: 'Summarize my conversations from today'"
