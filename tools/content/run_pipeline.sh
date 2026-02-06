#!/bin/bash
# Content Pipeline Orchestrator
# Usage: ./run_pipeline.sh --status

ACTION="${1:-status}"

case "$ACTION" in
    --status)
        python3 tools/content/pipeline_status.py
        ;;
    --start)
        python3 tools/content/new_content.py
        ;;
    --next)
        python3 tools/content/promote.py --stage next
        ;;
    --all)
        python3 tools/content/run_full_pipeline.py
        ;;
    *)
        echo "Usage: run_pipeline.sh [--status | --start | --next | --all]"
        exit 1
        ;;
esac
