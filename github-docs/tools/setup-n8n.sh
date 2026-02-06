#!/bin/bash
# n8n (Nanobanna) Setup Script
# Self-hosted workflow automation for Life OS

echo "🔄 Setting up n8n (Nanobanna)..."
echo "================================"
echo ""

# Create n8n directory
mkdir -p ~/.openclaw/n8n
cd ~/.openclaw/n8n

# Create docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  n8n:
    image: n8nio/n8n:latest
    restart: always
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=lifeos2026
      - N8N_HOST=${N8N_HOST:-localhost}
      - N8N_PORT=5678
      - N8N_PROTOCOL=http
      - NODE_ENV=production
      - WEBHOOK_URL=${WEBHOOK_URL:-http://localhost:5678/}
      - GENERIC_TIMEZONE=America/New_York
    volumes:
      - ~/.openclaw/n8n/data:/home/node/.n8n
      - /var/run/docker.sock:/var/run/docker.sock
    networks:
      - n8n-network

  # Optional: PostgreSQL for production
  postgres:
    image: postgres:15-alpine
    restart: always
    environment:
      - POSTGRES_USER=n8n
      - POSTGRES_PASSWORD=n8n_password
      - POSTGRES_DB=n8n
    volumes:
      - ~/.openclaw/n8n/postgres-data:/var/lib/postgresql/data
    networks:
      - n8n-network
    profiles:
      - production

networks:
  n8n-network:
    driver: bridge
EOF

echo "✅ docker-compose.yml created"
echo ""

# Create environment file
cat > .env << 'EOF'
# n8n Configuration
N8N_HOST=localhost
N8N_PORT=5678
N8N_PROTOCOL=http
WEBHOOK_URL=http://localhost:5678/
GENERIC_TIMEZONE=America/New_York

# Security (CHANGE THESE!)
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=lifeos2026
EOF

echo "✅ .env created"
echo ""

# Create startup script
cat > start-n8n.sh << 'EOF'
#!/bin/bash
echo "Starting n8n..."
cd "$(dirname "$0")"
docker-compose up -d
echo ""
echo "🔄 n8n starting..."
echo "⏳ Wait 30 seconds for initialization"
sleep 5
echo "   (5s...)"
sleep 5
echo "   (10s...)"
sleep 5
echo "   (15s...)"
sleep 5
echo "   (20s...)"
sleep 5
echo "   (25s...)"
sleep 5
echo ""
echo "✅ n8n ready!"
echo ""
echo "🔗 Access: http://localhost:5678"
echo "👤 Username: admin"
echo "🔑 Password: lifeos2026"
echo ""
echo "⚠️  IMPORTANT: Change default password!"
EOF

chmod +x start-n8n.sh

echo "✅ start-n8n.sh created"
echo ""

# Create workflow examples directory
mkdir -p workflows

# Example workflow: Daily Standup Reporter
cat > workflows/daily-standup.json << 'EOF'
{
  "name": "Daily Standup Reporter",
  "nodes": [
    {
      "parameters": {
        "rule": {
          "interval": [
            {
              "field": "hours",
              "hoursInterval": 24
            }
          ]
        }
      },
      "name": "Schedule Trigger",
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1,
      "position": [250, 300]
    },
    {
      "parameters": {
        "command": "cd ~/.openclaw/workspace && ./tools/daily-standup.sh"
      },
      "name": "Execute Standup",
      "type": "n8n-nodes-base.executeCommand",
      "typeVersion": 1,
      "position": [450, 300]
    },
    {
      "parameters": {
        "chatId": "6307161005",
        "text": "={{ $json.stdout }}"
      },
      "name": "Send to Telegram",
      "type": "n8n-nodes-base.telegram",
      "typeVersion": 1,
      "position": [650, 300]
    }
  ],
  "connections": {
    "Schedule Trigger": {
      "main": [[{"node": "Execute Standup", "type": "main", "index": 0}]]
    },
    "Execute Standup": {
      "main": [[{"node": "Send to Telegram", "type": "main", "index": 0}]]
    }
  }
}
EOF

echo "✅ Example workflow: daily-standup.json"
echo ""

# Example workflow: GitHub Auto-Commit
cat > workflows/github-autocommit.json << 'EOF'
{
  "name": "GitHub Auto-Commit",
  "nodes": [
    {
      "parameters": {
        "rule": {
          "interval": [
            {
              "field": "hours",
              "hoursInterval": 4
            }
          ]
        }
      },
      "name": "Every 4 Hours",
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1,
      "position": [250, 300]
    },
    {
      "parameters": {
        "commands": [
          {
            "command": "cd ~/.openclaw/workspace && git add -A && git diff --cached --quiet || git commit -m 'Auto-commit: $(date)' && git push"
          }
        ]
      },
      "name": "Git Commit",
      "type": "n8n-nodes-base.executeCommand",
      "typeVersion": 1,
      "position": [450, 300]
    }
  ],
  "connections": {
    "Every 4 Hours": {
      "main": [[{"node": "Git Commit", "type": "main", "index": 0}]]
    }
  }
}
EOF

echo "✅ Example workflow: github-autocommit.json"
echo ""

echo "================================"
echo "🎉 n8n Setup Complete!"
echo ""
echo "📁 Location: ~/.openclaw/n8n"
echo ""
echo "🚀 Start n8n:"
echo "   cd ~/.openclaw/n8n"
echo "   ./start-n8n.sh"
echo ""
echo "🔗 Access: http://localhost:5678"
echo ""
echo "📋 Pre-built Workflows:"
echo "   • Daily Standup Reporter"
echo "   • GitHub Auto-Commit"
echo ""
echo "⚠️  Security: Change password in .env file!"
echo ""
echo "🔌 Integrations ready:"
echo "   • Telegram (configure bot token)"
echo "   • GitHub (add personal token)"
echo "   • Discord (webhook URL)"
echo "   • 400+ more via n8n nodes"
