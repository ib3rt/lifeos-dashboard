#!/bin/bash
# Quick article generator using Knowledge Curator

echo "🦞 Article Generator"
echo "===================="
echo ""
echo "Usage: ./generate-article.sh \"Your Article Topic\""
echo "       ./generate-article.sh \"Topic\" tutorial"
echo "       ./generate-article.sh \"Topic\" 5"
echo ""
echo "Examples:"
echo '  ./generate-article.sh "AI Automation"'
echo '  ./generate-article.sh "API Integration" technical-guide'
echo ""

# Default to asking for topic if none provided
if [ -z "$1" ]; then
    read -p "Enter article topic: " topic
    if [ -z "$topic" ]; then
        echo "Error: Topic required"
        exit 1
    fi
    cd /home/ubuntu/.openclaw/workspace/agents/super-swarm/research/knowledge-synth
    python3 knowledge-curator.py generate "$topic"
else
    cd /home/ubuntu/.openclaw/workspace/agents/super-swarm/research/knowledge-synth
    python3 knowledge-curator.py "$@"
fi
