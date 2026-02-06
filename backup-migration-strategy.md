# Life OS Backup & Migration Strategy

> *"Hope for the best, prepare for the worst."*

---

## 🎯 Philosophy

**Redundancy is safety.** Every component should be:
- ✅ Backed up automatically
- ✅ Documented for restore
- ✅ Portable across environments

---

## 📦 What's Need to Backup

### Core Systems (Critical)

| Component | Location | Frequency | Retention |
|-----------|----------|-----------|-----------|
| OpenClaw Config | `~/.openclaw/openclaw.json` | Daily + On Change | 30 days |
| Discord Config | `~/.openclaw/discord/config.json` | Daily + On Change | 30 days |
| Gateway Data | `~/.openclaw/gateway/` | Daily | 7 days |
| Sessions | `~/.openclaw/agents/main/sessions/` | Daily | 14 days |

### Workspace (High Priority)

| Component | Location | Frequency | Retention |
|-----------|----------|-----------|-----------|
| All Agents | `~/openclaw/workspace/agents/` | Daily + Git | Forever |
| Brands/Sites | `~/openclaw/workspace/brands/` | Daily + Git | Forever |
| Memory | `~/openclaw/workspace/memory/` | Daily | Forever |
| Automation Scripts | `~/openclaw/workspace/tools/` | Daily + Git | Forever |

### Infrastructure (Medium)

| Component | Location | Frequency | Retention |
|-----------|----------|-----------|-----------|
| Systemd Services | `/etc/systemd/system/` | On Change | 7 versions |
| Cron Jobs | `/etc/cron.d/` | On Change | 7 versions |
| SSH Config | `~/.ssh/` | On Change | 7 versions |

---

## 🔄 Backup Strategy

### Tier 1: Git (Always-On)

```bash
# All workspace is already git-backed
cd ~/openclaw/workspace
git push origin main  # Daily habit
```

**What's covered:**
- All agents (185+)
- All documentation
- All templates
- All articles
- All automation scripts

### Tier 2: Automated Nightly Backups

```bash
#!/bin/bash
# ~/openclaw/workspace/tools/backup-lifeos.sh

DATE=$(date +%Y-%m-%d_%H-%M)
BACKUP_DIR=~/backups/lifeos
mkdir -p $BACKUP_DIR

# 1. Export configs
cp ~/.openclaw/openclaw.json $BACKUP_DIR/openclaw_$DATE.json
cp ~/.openclaw/discord/config.json $BACKUP_DIR/discord_$DATE.json

# 2. Archive workspace
tar -czf $BACKUP_DIR/workspace_$DATE.tar.gz ~/openclaw/workspace

# 3. Git push everything
cd ~/openclaw/workspace && git push origin main

# 4. Clean old (keep 7 days)
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
find $BACKUP_DIR -name "*.json" -mtime +30 -delete

echo "✅ Backup complete: $DATE"
```

### Tier 3: Cloud Redundancy (Optional)

**Options:**
- 📦 **Backblaze B2** - Cheap cold storage
- ☁️ **AWS S3** - $0.023/GB/month  
- 🔐 **Encrypted Archives** - For sensitive configs

---

## 🚀 Migration Checklist

### Pre-Migration

- [ ] **Document current setup** - All services, ports, configs
- [ ] **Test backups** - Verify restores work
- [ ] **List dependencies** - API keys, tokens, credentials
- [ ] **Check DNS** - Domain pointed where?
- [ ] **Prepare target** - Fresh server/container ready

### Migration Day

#### Step 1: Freeze State
```bash
# On OLD server
cd ~/openclaw/workspace
git push origin main  # Latest
tar -czf ~/migration/workspace_final.tar.gz .
cp ~/.openclaw/*.json ~/migration/
```

#### Step 2: Transfer
```bash
# From NEW server
scp -r user@old-server:/backup/* ~/backups/
```

#### Step 3: Restore
```bash
# On NEW server
tar -xzf ~/backups/workspace_*.tar.gz -C ~/
cp ~/backups/openclaw_*.json ~/.openclaw/openclaw.json
cp ~/backups/discord_*.json ~/.openclaw/discord/config.json
```

#### Step 4: Reinstall Services
```bash
# Reinstall systemd services
sudo cp ~/openclaw/workspace/bots/discord/openclaw-discord.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable openclaw-discord
```

#### Step 5: Verify
```bash
# Test everything
openclaw status
sudo systemctl status openclaw-*
curl -s https://b3rt.dev | head -20
```

---

## ⏱️ Estimated Migration Time

| Action | Time |
|--------|------|
| Backup (workspace ~500MB) | 30 sec |
| Transfer (network dependent) | 1-5 min |
| Restore | 30 sec |
| Reinstall services | 2 min |
| Verification | 1 min |
| **Total** | **5-10 minutes** |

---

## 🛡️ Key Files to Protect

```
~/.openclaw/
├── openclaw.json          ← CRITICAL - All AI configs
├── discord/
│   └── config.json        ← CRITICAL - Bot tokens
├── gateway/
│   └── gateway.db          ← Session history
└── workspace/             ← Git-backed, mostly safe
    ├── agents/           ← 185 agents
    ├── brands/           ← All websites
    ├── memory/           ← Knowledge base
    └── tools/            ← Automation
```

---

## 🔑 Credentials Vault

**Before migration, ensure you have:**

- [ ] Discord Bot Token (reset if needed)
- [ ] Moonshot/Kimi API Key
- [ ] MiniMax API Key
- [ ] Any other AI provider keys
- [ ] Cloudflare API Token
- [ ] GitHub Personal Access Token

**Store securely:**
- Bitwarden
- 1Password
- Encrypted file (age, gpg)

---

## 📋 Quick Migration Command

```bash
# One-liner to backup everything before migration
cd ~/openclaw/workspace && \
git push origin main && \
tar -czf ~/backups/lifeos_$(date +%Y-%m-%d).tar.gz . && \
cp ~/.openclaw/openclaw.json ~/backups/ && \
cp ~/.openclaw/discord/config.json ~/backups/ && \
echo "🚀 Migration backup ready!"
```

---

## 🎯 Current Health Check

| Backup Target | Status | Last Run |
|---------------|--------|----------|
| Git (main) | ✅ Current | Now |
| Configs | ⚠️ Manual | Never |
| Full Archive | ❌ Not Set Up | - |

**Recommendation:** Set up nightly automated backup script today.

---

*Backup before you need it. Migration is easy with preparation.*
