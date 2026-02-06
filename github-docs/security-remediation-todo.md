# 🛡️ Security Remediation Todo List
**Source:** Sentinel Security Audit (2026-02-02)  
**Status:** Queued - awaiting user approval to implement

---

## 🔴 CRITICAL (Implement First)

### 1. Rotate Exposed API Keys
- [ ] **Brave Search API Key** (`BSAGMo1P2i...`)
  - Location: Found in plaintext in workspace files
  - Action: Generate new key at https://api.search.brave.com
  - Update: `~/.openclaw/openclaw.json` and any agent configs
  
- [ ] **Telegram Bot Token** (`8317783755:AAE...`)
  - Location: Environment variable, backup files
  - Action: Revoke via @BotFather, generate new token
  - Update: Gateway config, agent environment variables
  
- [ ] **Gateway Auth Token** (`3f1d1feb...`)
  - Location: Environment variable `OPENCLAW_GATEWAY_TOKEN`
  - Action: Generate new token via `openclaw auth generate`
  - Update: Service config, agent configs

### 2. Revoke Discord Token (Old Backup)
- [ ] **Discord Bot Token** (from old backup files)
  - Action: Revoke immediately at https://discord.com/developers/applications
  - Reason: Token exposed in backup files, potential unauthorized access

---

## 🟡 HIGH (Implement Next)

### 3. Purge Backup Files with Secrets
- [ ] Identify all backup files containing secrets
  - Search: `grep -r "secret_\|token\|api_key\|password" ~/.openclaw/workspace --include="*.bak" --include="*.old" --include="*backup*" 2>/dev/null`
- [ ] Securely delete with `shred -vfz -n 3 <file>`
- [ ] Verify no secrets in git history: `git log --all --full-history -- . | grep -i "secret\|token\|key"`

### 4. Clear Environment Variable
- [ ] **Remove** `OPENCLAW_GATEWAY_TOKEN` from shell environment
  - Check: `env | grep OPENCLAW`
  - Clear: `unset OPENCLAW_GATEWAY_TOKEN`
  - Persist: Remove from `~/.bashrc`, `~/.profile`, systemd service files

### 5. Fix File Permissions
- [ ] **Workspace directory:** `chmod 700 ~/.openclaw/workspace`
- [ ] **Config files:** `chmod 600 ~/.openclaw/openclaw.json`
- [ ] **Agent directories:** `find ~/.openclaw/workspace/agents -type f -exec chmod 600 {} \;`
- [ ] **Scripts:** `chmod 700 ~/.openclaw/workspace/tools/*.sh`

---

## 🟢 MEDIUM (Implement When Convenient)

### 6. Implement Secrets Management
- [ ] **Option A:** Mozilla SOPS + Age
  - Install: `apt install sops age`
  - Generate key: `age-keygen -o ~/.config/sops/age/keys.txt`
  - Encrypt secrets: `sops encrypt --in-place secrets.yaml`
  
- [ ] **Option B:** HashiCorp Vault (local dev mode)
  - Install Vault
  - Run: `vault server -dev`
  - Store secrets in Vault KV store
  
- [ ] **Option C:** Docker Secrets (if using Docker Swarm)
  - Migrate to Docker Swarm
  - Use `docker secret create` for sensitive data

### 7. Log Sanitization
- [ ] Review logging configuration
- [ ] Add filters to prevent secret logging
- [ ] Audit existing logs: `grep -r "token\|secret\|key" /var/log/openclaw/ 2>/dev/null | head -20`
- [ ] Rotate and purge old logs with potential secrets

### 8. Backup Strategy
- [ ] Set up encrypted backups: `restic init --repo s3:...`
- [ ] Exclude secrets from backups or encrypt them
- [ ] Test restore procedure
- [ ] Document backup locations and encryption keys

---

## 📋 Implementation Commands (Ready to Execute)

```bash
# 1. Fix permissions immediately
chmod 700 ~/.openclaw/workspace
chmod 600 ~/.openclaw/openclaw.json
find ~/.openclaw/workspace/agents -type f -name "*.md" -o -name "*.json" | xargs chmod 600

# 2. Find and shred backup files with secrets  
find ~/.openclaw -name "*.bak" -o -name "*.old" -o -name "*backup*" | while read f; do
  if grep -q "secret\|token\|api_key" "$f" 2>/dev/null; then
    echo "Shredding: $f"
    shred -vfz -n 3 "$f"
    rm -f "$f"
  fi
done

# 3. Clear environment variable
unset OPENCLAW_GATEWAY_TOKEN
sed -i '/OPENCLAW_GATEWAY_TOKEN/d' ~/.bashrc ~/.profile 2>/dev/null

# 4. Install SOPS for secrets management
curl -LO https://github.com/getsops/sops/releases/download/v3.8.1/sops_3.8.1_amd64.deb
dpkg -i sops_3.8.1_amd64.deb
age-keygen -o ~/.config/sops/age/keys.txt
```

---

## ⏳ Waiting For User Approval

**Do not execute without explicit user confirmation.**

Security remediation requires:
1. Downtime (gateway restart for token rotation)
2. API key regeneration (user must log into provider portals)
3. Potential service disruption if done incorrectly

**Next action:** Await user instruction to proceed or modify plan.

---

*Created by: 🛡️ Sentinel*  
*Queued by: Claw*  
*Awaiting implementation approval*