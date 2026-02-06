#!/bin/bash
# Multi-Platform Publisher
# Usage: ./publish_all.sh --drafts

MODE="${1:-pending}"

case "$MODE" in
    --drafts)
        echo "Publishing all drafted content..."
        python3 tools/content/publish_drafts.py
        ;;
    --scheduled)
        echo "Publishing scheduled content for today..."
        python3 tools/content/publish_scheduled.py
        ;;
    *)
        echo "Usage: publish_all.sh [--drafts | --scheduled]"
        exit 1
        ;;
esac

echo "Publishing complete"
