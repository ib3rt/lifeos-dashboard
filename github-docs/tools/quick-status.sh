#!/bin/bash
# Life OS Quick Status
# Usage: ./quick-status.sh

echo "🦾 Life OS Quick Status"
echo "======================="
echo ""

# Agent counts
ACTIVE=$(find ~/.openclaw/workspace/agents -name "*.md" -exec grep -l "Status: ACTIVE" {} \; 2>/dev/null | wc -l)
IDLE=$(find ~/.openclaw/workspace/agents -name "*.md" -exec grep -l "Status: IDLE" {} \; 2>/dev/null | wc -l)

echo "Agents: $ACTIVE active, $IDLE idle"

# Recent reports
REPORT_COUNT=$(ls ~/.openclaw/workspace/research/*.md 2>/dev/null | wc -l)
REPORT_SIZE=$(du -sh ~/.openclaw/workspace/research/ 2>/dev/null | cut -f1)
echo "Reports: $REPORT_COUNT files ($REPORT_SIZE)"

# System health
echo ""
echo "System:"
df -h /home/ubuntu/.openclaw 2>/dev/null | tail -1 | awk '{print "  Disk: "$5 " used"}'
free -h 2>/dev/null | grep Mem | awk '{print "  Memory: "$3"/"$2}'

# Check OpenClaw
echo ""
if pgrep -f "openclaw" > /dev/null; then
    echo "  ✅ OpenClaw: Running"
else
    echo "  🔴 OpenClaw: Not running"
fi

# Recent git activity
echo ""
cd ~/.openclaw/workspace 2>/dev/null && git log --oneline -3 2>/dev/null | sed 's/^/  /'

echo ""
echo "======================="