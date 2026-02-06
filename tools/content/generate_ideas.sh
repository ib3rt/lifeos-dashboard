#!/bin/bash
# Content Idea Generator
# Usage: ./generate_ideas.sh --topic "productivity" --count 10

TOPIC="${1:-}"
COUNT="${2:-10}"
OUTPUT_FILE="content/ideas_$(date +%Y%m%d).txt"

echo "Generating content ideas for: $TOPIC"
python3 tools/content/generate_ideas.py --topic "$TOPIC" --count "$COUNT" --output "$OUTPUT_FILE"

echo "Ideas saved to: $OUTPUT_FILE"
