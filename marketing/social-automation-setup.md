# Social Media Automation Setup

> **📈 Hype Man** - Automated posting workflow for Twitter/X

## Overview

This document describes the n8n workflow for automated social media posting to X (Twitter). The workflow accepts webhook requests with post content and optional media, validates the input, and publishes posts automatically.

## Workflow Location

- **File:** `n8n-workflows/social-media-automation.json`
- **Workflow Name:** Social Media Auto-Poster

## Architecture

```
┌─────────────┐    ┌──────────────────┐    ┌─────────────┐    ┌─────────────────┐
│   Webhook   │───▶│ Validate & Format│───▶│ Has Media?  │───▶│  Upload Media   │
│  (POST)     │    │   (Code Node)    │    │  (If Node)  │    │  (Code Node)    │
└─────────────┘    └──────────────────┘    └─────────────┘    └─────────────────┘
                                                                      │
                    ┌─────────────────┐                               │
                    │  Post to X      │◀──────────────────────────────┘
                    │  (Text Only)    │
                    └─────────────────┘
                            │
                            ▼
┌─────────────────┐    ┌─────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Log Success   │◀───│Format Success│◀───│  Merge Results  │◀───│  Post to X      │
│ (Stop & Error)  │    │ (Code Node)  │    │  (Code Node)    │    │  (w/ Media)     │
└─────────────────┘    └─────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────┐
                       │   Success   │
                       │  Response   │
                       │(Respond to  │
                       │  Webhook)   │
                       └─────────────┘
```

## Webhook Endpoint

- **Method:** `POST`
- **Path:** `/webhook/social-post`
- **Response Mode:** Using Respond to Webhook node

## Request Format

### JSON Payload

```json
{
  "text": "Your post content here (max 280 chars)",
  "mediaUrls": [
    "https://example.com/image1.jpg",
    "https://example.com/image2.png"
  ],
  "altText": "Description of media for accessibility",
  "replyTo": "optional_tweet_id_to_reply_to"
}
```

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `text` | string | Post content (max 280 characters) |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `mediaUrls` | array | URLs of images/videos to attach (max 4) |
| `altText` | string | Alt text for accessibility |
| `replyTo` | string | Tweet ID to reply to |

## Response Format

### Success Response (200 OK)

```json
{
  "status": "success",
  "message": "Post published successfully",
  "data": {
    "postId": "x_post_1706937600000",
    "platform": "X (Twitter)",
    "url": "https://twitter.com/user/status/x_post_1706937600000",
    "textPreview": "Your post content here...",
    "mediaCount": 2,
    "postedAt": "2026-02-03T12:00:00.000Z"
  }
}
```

### Error Response (500)

```json
{
  "status": "error",
  "message": "Failed to publish post",
  "error": "Text exceeds 280 characters (300 chars provided)",
  "timestamp": "2026-02-03T12:00:00.000Z"
}
```

## Validation Rules

The workflow validates incoming requests:

1. **Text is required** - Must be a non-empty string
2. **Character limit** - Maximum 280 characters for X posts
3. **Media limit** - Maximum 4 attachments allowed
4. **URL validation** - Media URLs must be valid (handled during upload)

## Error Handling

The workflow includes comprehensive error handling:

- **Validation Errors** - Returned when required fields are missing or invalid
- **Character Limit** - Enforced before posting
- **Media Upload Failures** - Captured and reported
- **Posting Errors** - X API errors are caught and returned

## X Credentials Setup

> ⚠️ **To be configured later**

To make this workflow functional, you need to:

1. Create an X Developer account at https://developer.twitter.com
2. Create a new app and generate API credentials
3. In n8n:
   - Go to **Settings** → **Credentials**
   - Add new **X (Twitter) OAuth2** credentials
   - Enter your API Key, API Secret, Access Token, and Access Token Secret
4. Replace the mock "Post to X" code nodes with the official X node:
   - Remove the code nodes named "Post to X (w/ Media)" and "Post to X (Text)"
   - Add **X (Twitter)** nodes
   - Configure with your credentials
   - Set action to "Create Tweet"

### X Node Configuration

```
Node: X (Twitter)
├── Authentication: Your X credentials
├── Resource: Tweet
├── Operation: Create
├── Text: {{ $json.text }}
├── Media IDs: {{ $json.mediaIds }} (optional)
└── Reply To: {{ $json.replyTo }} (optional)
```

## Testing the Workflow

### Using cURL

```bash
# Text-only post
curl -X POST https://your-n8n-instance.com/webhook/social-post \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello from automated workflow! 🤖"
  }'

# Post with media
curl -X POST https://your-n8n-instance.com/webhook/social-post \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Check out this automation! 🚀",
    "mediaUrls": ["https://example.com/chart.png"],
    "altText": "Marketing automation workflow diagram"
  }'
```

### Using n8n Test Webhook

1. Open the workflow in n8n
2. Click on the Webhook node
3. Click "Listen for Test Event"
4. Send a POST request to the test URL
5. View the execution results

## Security Considerations

1. **Webhook URL** - Keep the webhook URL confidential
2. **Authentication** - Consider adding API key validation to the webhook
3. **Rate Limiting** - X API has rate limits; implement retry logic if needed
4. **Content Moderation** - Consider adding a content filter before posting

## Future Enhancements

- [ ] Add support for multiple platforms (LinkedIn, Instagram, etc.)
- [ ] Implement scheduling with delayed posting
- [ ] Add content approval workflow
- [ ] Include analytics tracking
- [ ] Support for thread posting (multiple connected tweets)

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| "Text exceeds 280 characters" | Shorten your message |
| "Maximum 4 media attachments allowed" | Remove excess media URLs |
| "Failed to upload media" | Check media URLs are accessible |
| "Authentication failed" | Verify X credentials are correct and not expired |

## Support

For issues or questions about this workflow, contact the Hype Man system administrator.

---

*Last updated: 2026-02-03*
*Version: 1.0*
