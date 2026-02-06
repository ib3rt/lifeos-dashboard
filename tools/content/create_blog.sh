#!/bin/bash
# Blog Content Creator
# Usage: ./create_blog.sh --title "Your Title" --keyword "target keyword"

TITLE="$1"
KEYWORD="$2"

if [ -z "$TITLE" ]; then
    echo "Usage: $0 --title 'Blog Title' [--keyword 'seo keyword']"
    exit 1
fi

echo "Creating blog post: $TITLE"
python3 tools/content/create_blog.py --title "$TITLE" --keyword "$KEYWORD"

echo "Blog draft created successfully"
