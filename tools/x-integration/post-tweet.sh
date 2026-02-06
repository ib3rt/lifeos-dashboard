#!/bin/bash
# X (Twitter) Integration - Post a Tweet (OAuth 1.0a)

# Load API keys
source ~/.openclaw/keys/x_api.key

# Check if message is provided
if [ -z "$1" ]; then
    echo "❌ Error: No message provided"
    echo ""
    echo "Usage: ./post-tweet.sh \"Your tweet message here\""
    exit 1
fi

MESSAGE="$1"

echo "🐦 Posting to X..."
echo "📝 Message: $MESSAGE"
echo ""

# Generate OAuth signature and headers
# For simplicity, we'll use a Python helper
python3 << PYTHON
import sys
import base64
import hmac
import hashlib
import time
import urllib.parse
import json

# Load keys
with open('/home/ubuntu/.openclaw/keys/x_api.key') as f:
    exec(f.read())

# OAuth 1.0a parameters
oauth = {
    'oauth_consumer_key': X_API_KEY,
    'oauth_token': X_ACCESS_TOKEN,
    'oauth_signature_method': 'HMAC-SHA1',
    'oauth_timestamp': str(int(time.time())),
    'oauth_nonce': str(int(time.time() * 1000)),
    'oauth_version': '1.0'
}

# URL encode parameters
def percent_encode(s):
    return urllib.parse.quote(str(s), safe='')

# Create signature base string
params = {**oauth, 'status': MESSAGE}
sorted_params = sorted(params.items())
param_string = '&'.join(f"{percent_encode(k)}={percent_encode(v)}" for k, v in params)
base_string = f"POST&{percent_encode('https://api.twitter.com/2/tweets')}&{percent_encode(param_string)}"

# Create signing key
signing_key = f"{percent_encode(X_API_SECRET)}&{percent_encode(X_ACCESS_TOKEN_SECRET)}"

# Generate signature
signature = base64.b64encode(
    hmac.new(
        signing_key.encode(),
        base_string.encode(),
        hashlib.sha1
    ).digest()
).decode()

oauth['oauth_signature'] = signature

# Create Authorization header
auth_header = 'OAuth ' + ', '.join(
    f'{percent_encode(k)}="{percent_encode(v)}"' for k, v in sorted(oauth.items())
)

# Make request
import urllib.request
import urllib.error

data = json.dumps({'text': MESSAGE}).encode()

req = urllib.request.Request(
    'https://api.twitter.com/2/tweets',
    data=data,
    headers={
        'Authorization': auth_header,
        'Content-Type': 'application/json'
    }
)

try:
    response = urllib.request.urlopen(req, timeout=10)
    result = json.loads(response.read().decode())
    print(f"✅ SUCCESS! Tweet posted!")
    print(f"🆔 Tweet ID: {result['data']['id']}")
    print(f"🔗 View at: https://twitter.com/i/status/{result['data']['id']}")
except urllib.error.HTTPError as e:
    error = json.loads(e.read().decode())
    print(f"❌ ERROR: {error.get('detail', 'Unknown error')}")
    print(f"Status: {e.code}")
    sys.exit(1)
PYTHON
