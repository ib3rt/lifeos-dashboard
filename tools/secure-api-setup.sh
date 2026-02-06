#!/bin/bash
# secure-api-setup.sh
# Run this on your local machine to securely upload API keys to AWS

# Configuration
SERVER_USER="ubuntu"
SERVER_IP="YOUR_EC2_IP_HERE"  # Replace with your EC2 IP
SSH_KEY="~/.ssh/your-key.pem"  # Replace with your SSH key path

echo "═══════════════════════════════════════════════════════════"
echo "  SECURE API KEY UPLOAD TO AWS"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "This script will securely upload API keys to the server."
echo ""
echo "Step 1: SSH into server"
echo "Step 2: Create key files"
echo "Step 3: Set permissions"
echo "Step 4: Test keys"
echo ""

# Function to upload a key
upload_key() {
    local provider=$1
    local key_value=$2
    
    echo "Uploading $provider key..."
    
    # Create remote file with key
    ssh -i "$SSH_KEY" "$SERVER_USER@$SERVER_IP" "mkdir -p ~/.openclaw/keys && echo '$key_value' > ~/.openclaw/keys/$provider.key && chmod 600 ~/.openclaw/keys/$provider.key"
    
    if [ $? -eq 0 ]; then
        echo "✅ $provider key uploaded successfully"
    else
        echo "❌ Failed to upload $provider key"
    fi
}

# Instructions for manual upload
cat << 'INSTRUCTIONS'

═══════════════════════════════════════════════════════════
  MANUAL UPLOAD (RECOMMENDED)
═══════════════════════════════════════════════════════════

If you prefer to do it manually, run these commands:

1. SSH INTO SERVER:
   
   ssh -i ~/.ssh/your-key.pem ubuntu@YOUR_EC2_IP

2. CREATE KEY DIRECTORY:
   
   mkdir -p ~/.openclaw/keys

3. CREATE ANTHROPIC KEY (Haiku for Heartbeat):
   
   nano ~/.openclaw/keys/anthropic.key
   # Paste: sk-ant-api03-...
   # Save: Ctrl+X, Y, Enter

4. CREATE DEEPSEEK KEY (Search):
   
   nano ~/.openclaw/keys/deepseek.key
   # Paste: sk-1ab79c9aa8154057abfb1ec7a1ca0832
   # Save: Ctrl+X, Y, Enter

5. CREATE GEMINI KEY (Understanding):
   
   nano ~/.openclaw/keys/gemini.key
   # Paste: AIzaSyADRonOv9JYf3TwhG2pDwDoUmTsJdDVqeU
   # Save: Ctrl+X, Y, Enter

6. SET PERMISSIONS:
   
   chmod 600 ~/.openclaw/keys/*.key

7. VERIFY:
   
   ls -la ~/.openclaw/keys/

8. MESSAGE CLAW:
   
   "Keys uploaded to server"

═══════════════════════════════════════════════════════════
  TESTING COMMANDS (After Upload)
═══════════════════════════════════════════════════════════

Test Anthropic:
  ~/.openclaw/workspace/tools/test-haiku-heartbeat.sh

Test DeepSeek:
  export DEEPSEEK_API_KEY=$(cat ~/.openclaw/keys/deepseek.key)
  curl -s https://api.deepseek.com/chat/completions \
    -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"model": "deepseek-chat", "messages": [{"role": "user", "content": "Hello"}]}'

═══════════════════════════════════════════════════════════

INSTRUCTIONS
