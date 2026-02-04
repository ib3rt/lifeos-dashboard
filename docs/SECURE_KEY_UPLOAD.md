# Secure API Key Upload Instructions

## Method 1: Direct File Upload (Recommended)

1. **SSH into your AWS instance:**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

2. **Create the key file:**
   ```bash
   nano ~/.openclaw/keys/minimax.new
   ```

3. **Paste the API key** (just the key, nothing else)

4. **Save:** Ctrl+X, then Y, then Enter

5. **Secure the file:**
   ```bash
   chmod 600 ~/.openclaw/keys/minimax.new
   ```

6. **Test it:**
   ```bash
   ~/.openclaw/workspace/tools/test-minimax-key.sh
   ```

## Method 2: SCP File Transfer

From your local machine:
```bash
scp -i your-key.pem /path/to/minimax-key.txt ubuntu@your-ec2-ip:~/.openclaw/keys/minimax.new
```

Then SSH in and:
```bash
chmod 600 ~/.openclaw/keys/minimax.new
~/.openclaw/workspace/tools/test-minimax-key.sh
```

## Method 3: Environment Variable (Temporary)

SSH into server and run:
```bash
export MINIMAX_API_KEY="your-key-here"
~/.openclaw/workspace/tools/test-minimax-key.sh
```

If it works, I'll save it permanently.

---

## After Upload

Once you've uploaded the key via any method above, message me:
> "Key uploaded to server"

I'll test it immediately and confirm if MiniMax is working!

---

**Note:** https://platform.minimax.io/ is the correct dashboard URL
