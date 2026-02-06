#!/bin/bash
# Serve Business Websites Locally
# Makes sites accessible via server IP

IP=$(curl -s ipinfo.io/ip)

echo "🌐 Starting Business Website Servers..."
echo "======================================="
echo ""

# Sparkling Solutions on port 8081
cd ~/.openclaw/workspace/workspace/brands/sparkling-solutions
nohup python3 -m http.server 8081 > /dev/null 2>&1 &
echo $! > /tmp/sparkling.pid
echo "✨ Sparkling Solutions: http://$IP:8081"

# BE Repaired on port 8082
cd ~/.openclaw/workspace/workspace/brands/be-repaired
nohup python3 -m http.server 8082 > /dev/null 2>&1 &
echo $! > /tmp/berepaired.pid
echo "🔧 BE Repaired:       http://$IP:8082"

# Personal Tech on port 8083
cd ~/.openclaw/workspace/workspace/brands/personal-tech
nohup python3 -m http.server 8083 > /dev/null 2>&1 &
echo $! > /tmp/personaltech.pid
echo "💻 Personal Tech:     http://$IP:8083"

echo ""
echo "======================================="
echo "🎉 All sites are LIVE!"
echo ""
echo "Dashboard will be updated with these URLs"
