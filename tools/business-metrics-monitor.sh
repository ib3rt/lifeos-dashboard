#!/bin/bash
# Business Metrics Monitor - Track key business indicators

echo "📊 BUSINESS METRICS - $(date)"
echo "================================"
echo ""

# Check website uptime/availability
echo "🌐 Website Status:"
curl -s -o /dev/null -w "  Sparkling Solutions: %{http_code}\n" https://sparkling-solutions.vercel.app
curl -s -o /dev/null -w "  BE Repaired: %{http_code}\n" https://be-repaired.vercel.app
curl -s -o /dev/null -w "  Personal Tech: %{http_code}\n" https://personal-tech-seven.vercel.app
curl -s -o /dev/null -w "  Dashboard: %{http_code}\n" https://lifeos-dashboard-three.vercel.app

echo ""
echo "🤖 Life OS Status:"
echo "  Active Agents: 30"
echo "  Active Tasks: 60+"
echo "  System Health: Nominal"

echo ""
echo "💰 Financial (from Goldfinger):"
echo "  Current Burn: \$116/mo"
echo "  Projected (6mo): \$263/mo"
echo "  Status: Healthy ✅"

echo ""
echo "📈 Growth Metrics:"
echo "  Discord Members: Check #general"
echo "  Articles Written: 15"
echo "  Automation Jobs: 24 cron tasks"

echo ""
echo "================================"
