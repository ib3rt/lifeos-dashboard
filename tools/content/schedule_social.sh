#!/bin/bash
# Social Media Scheduler
# Usage: ./schedule_social.sh --calendar content/calendar.md

CALENDAR_FILE="${1:-content/calendar.md}"

if [ ! -f "$CALENDAR_FILE" ]; then
    echo "Calendar file not found: $CALENDAR_FILE"
    exit 1
fi

echo "Processing social media schedule from: $CALENDAR_FILE"
python3 tools/content/schedule_social.py --calendar "$CALENDAR_FILE"

echo "Social posts scheduled successfully"
