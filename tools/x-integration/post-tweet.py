#!/usr/bin/env python3
"""X (Twitter) Integration - Post a Tweet using OAuth 1.0a"""

import sys
import json
import base64
import hmac
import hashlib
import time
import http.client
import urllib.parse

# Load keys
def load_keys():
    keys = {}
    with open('/home/ubuntu/.openclaw/keys/x_api.key') as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                line = line.replace('export ', '')
                if '=' in line:
                    parts = line.split('=', 1)
                    if len(parts) == 2:
                        key = parts[0].strip().replace(' ', '_').upper()
                        value = parts[1].strip()
                        keys[key] = value
    return keys

def percent_encode(s):
    return urllib.parse.quote(str(s), safe='')

def oauth_nonce():
    return base64.b64encode(str(time.time()).encode()).decode()[:32]

def post_tweet(message):
    keys = load_keys()
    
    # Use CONSUMER KEY (API Key), not Bearer Token
    consumer_key = keys.get('CONSUMER_KEY', '')
    consumer_secret = keys.get('CONSUMER_SECRET_KEY', '')
    access_token = keys.get('ACCESS_TOKEN', '')
    access_secret = keys.get('ACCESS_TOKEN_SECRET', '')
    
    # Build OAuth 1.0a parameters
    oauth_params = {
        'oauth_consumer_key': consumer_key,
        'oauth_token': access_token,
        'oauth_signature_method': 'HMAC-SHA1',
        'oauth_timestamp': str(int(time.time())),
        'oauth_nonce': oauth_nonce(),
        'oauth_version': '1.0'
    }
    
    # Create signature
    sorted_params = sorted((percent_encode(k), percent_encode(v)) for k, v in oauth_params.items())
    param_str = '&'.join([f"{k}={v}" for k, v in sorted_params])
    
    base_str = '&'.join([
        percent_encode('POST'),
        percent_encode('https://api.twitter.com/2/tweets'),
        percent_encode(param_str)
    ])
    
    key = f"{percent_encode(consumer_secret)}&{percent_encode(access_secret)}"
    signature = base64.b64encode(
        hmac.new(key.encode(), base_str.encode(), hashlib.sha1).digest()
    ).decode()
    
    oauth_params['oauth_signature'] = signature
    
    # Create Authorization header
    auth_parts = []
    for k, v in sorted(oauth_params.items()):
        if k.startswith('oauth_'):
            auth_parts.append(f'{percent_encode(k)}="{percent_encode(v)}"')
    
    auth_header = 'OAuth ' + ', '.join(auth_parts)
    
    # Make request
    conn = http.client.HTTPSConnection('api.twitter.com')
    headers = {
        'Authorization': auth_header,
        'Content-Type': 'application/json'
    }
    body = json.dumps({'text': message})
    
    try:
        conn.request('POST', '/2/tweets', body, headers)
        response = conn.getresponse()
        data = response.read().decode()
        
        if response.status == 201:
            result = json.loads(data)
            print(f"✅ SUCCESS! Tweet posted!")
            print(f"🆔 ID: {result['data']['id']}")
            print(f"🔗 https://twitter.com/i/status/{result['data']['id']}")
            return True
        else:
            print(f"❌ ERROR {response.status}: {data}")
            return False
    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")
        return False
    finally:
        conn.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: ./post-tweet.py \"Your message\"")
        sys.exit(1)
    post_tweet(sys.argv[1])
