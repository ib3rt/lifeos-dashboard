#!/bin/bash
# 🛡️ Life OS Master Backup Script
# As ordered by the General

echo "🛡️ INITIATING MASTER BACKUP..."
echo "================================"
echo ""

BACKUP_DIR="$HOME/.openclaw/backups/$(date +%Y-%m-%d_%H-%M-%S)"
mkdir -p "$BACKUP_DIR"

echo "📁 Backup location: $BACKUP_DIR"
echo ""

# 1. Backup workspace
echo "1️⃣ Backing up workspace..."
tar -czf "$BACKUP_DIR/workspace.tar.gz" -C "$HOME/.openclaw" workspace/ 2>/dev/null
echo "   ✅ Workspace archived"

# 2. Backup config
echo "2️⃣ Backing up configurations..."
cp "$HOME/.openclaw/openclaw.json" "$BACKUP_DIR/" 2>/dev/null
cp -r "$HOME/.openclaw/agents" "$BACKUP_DIR/" 2>/dev/null
echo "   ✅ Configs saved"

# 3. Backup agent deliverables
echo "3️⃣ Backing up agent tasks..."
tar -czf "$BACKUP_DIR/agent-tasks.tar.gz" -C "$HOME/.openclaw/workspace" agent-tasks/ 2>/dev/null
echo "   ✅ Agent tasks archived"

# 4. Backup missions
echo "4️⃣ Backing up missions..."
tar -czf "$BACKUP_DIR/missions.tar.gz" -C "$HOME/.openclaw/workspace" missions/ 2>/dev/null
echo "   ✅ Missions archived"

# 5. Backup memory
echo "5️⃣ Backing up memory..."
tar -czf "$BACKUP_DIR/memory.tar.gz" -C "$HOME/.openclaw/workspace" memory/ 2>/dev/null
cp "$HOME/.openclaw/workspace/MEMORY.md" "$BACKUP_DIR/" 2>/dev/null
cp "$HOME/.openclaw/workspace/USER.md" "$BACKUP_DIR/" 2>/dev/null
echo "   ✅ Memory archived"

# 6. Backup SOPs and docs
echo "6️⃣ Backing up SOPs..."
tar -czf "$BACKUP_DIR/sops.tar.gz" -C "$HOME/.openclaw/workspace" SOPs/ docs/ 2>/dev/null
echo "   ✅ SOPs archived"

# 7. Create backup manifest
cat > "$BACKUP_DIR/MANIFEST.txt" << EOF
🛡️ LIFE OS MASTER BACKUP
========================

Date: $(date)
System: $(uname -a)
User: $(whoami)

CONTENTS:
- workspace.tar.gz     (Full workspace code)
- openclaw.json        (System configuration)
- agents/              (Agent configurations)
- agent-tasks.tar.gz   (All agent deliverables)
- missions.tar.gz      (Mission files)
- memory.tar.gz        (Memory logs)
- MEMORY.md            (Long-term memory)
- USER.md              (User profile)
- sops.tar.gz          (Standard Operating Procedures)

RESTORE INSTRUCTIONS:
1. Extract workspace.tar.gz to ~/.openclaw/workspace/
2. Copy configs to ~/.openclaw/
3. Restore any additional files as needed

BACKUP SIZE: $(du -sh "$BACKUP_DIR" | cut -f1)
EOF

echo ""
echo "================================"
echo "✅ MASTER BACKUP COMPLETE!"
echo "================================"
echo ""
echo "📁 Location: $BACKUP_DIR"
echo "📊 Size: $(du -sh "$BACKUP_DIR" | cut -f1)"
echo ""
echo "🔄 Creating symlink to latest..."
ln -sfn "$BACKUP_DIR" "$HOME/.openclaw/backups/latest"
echo "   ✅ Latest backup: ~/.openclaw/backups/latest"
echo ""
echo "🛡️ BACKUP MANIFEST:"
cat "$BACKUP_DIR/MANIFEST.txt" | head -20
