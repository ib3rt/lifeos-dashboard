# 🖱️ X (Twitter) Manual Posting with Mouse Macros

**Solution for X API credit depletion!**

## Workflow

1. **Open Mouse Macro Recorder**
   ```bash
   cd /home/ubuntu/.openclaw/workspace/mouse-macro-recorder
   python main.py
   ```

2. **Record a Tweet Macro**
   - Click **Record**
   - Open Twitter in browser
   - Navigate to tweet box
   - Type your message
   - Click Post
   - Click **Stop**

3. **Save the Macro**
   - Click **Save**
   - Name: `x-post-tweet`
   - Location: `~/macros/`

4. **Replay for Future Posts**
   - Click **Load** → Select `x-post-tweet.json`
   - Click **Play**
   - Watch it post!

## Tips

- **Test first:** Record a short macro to try
- **Position matters:** Keep browser in same spot
- **Timing:** Macros replay at recorded speed
- **Adjust delays:** Use configurable delay before playback

## Macro Files Location

Save your X macros here:
```
~/macros/
├── x-post-tweet.json
├── x-post-link.json
├── x-post-image.json
└── etc.
```

## Quick Replay Command

```bash
cd /home/ubuntu/.openclaw/workspace/mouse-macro-recorder
python main.py --load ~/macros/x-post-tweet.json --play
```

## Benefits

✅ No API credits needed!
✅ Full browser functionality
✅ Images, links, everything works
✅ 100% manual control with automation speed

## For Kimi 2.5 Content

Generate content with Kimi 2.5, then macro-post it!

```bash
# Have Kimi generate tweet
kimi "Write a tweet about Life OS" > tweet.txt

# Read and post via macro
cat tweet.txt
# (Then use macro to manually post)
```

---

**Built by Life OS** 🦾
