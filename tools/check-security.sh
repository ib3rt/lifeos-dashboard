#!/bin/bash
# Weekly security audit
echo "[$(date '+%Y-%m-%d %H:%M')] Weekly Security Audit"
echo ""

# Check for exposed API keys in logs
echo "🔍 Checking for exposed keys in logs..."
if grep -r "api_key\|apikey\|password" ~/.openclaw/logs/ 2>/dev/null | grep -v ".log:" | head -5; then
    echo "  ⚠️ Potential exposed credentials found"
else
    echo "  ✅ No exposed credentials in logs"
fi

# Check file permissions
echo ""
echo "🔍 Checking sensitive file permissions..."
find ~/.openclaw -name "*.token" -o -name "*.key" -o -name ".env*" 2>/dev/null | while read file; do
    perms=$(stat -c "%a" "$file" 2>/dev/null)
    if [ "$perms" != "600" ] && [ "$perms" != "400" ]; then
        echo "  ⚠️ $file has permissions $perms (should be 600)"
    fi
done

# Check disk space
echo ""
echo "🔍 Checking disk space..."
df -h / | tail -1 | awk '{print "  Disk usage: "$5}'

echo ""
echo "✅ Security audit complete"
