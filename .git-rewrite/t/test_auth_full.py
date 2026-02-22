#!/usr/bin/env python3
import requests
import json

# Login
login_resp = requests.post(
    'http://localhost:8000/api/v1/auth/login',
    json={'email': 'admin@sila.gov.ao', 'password': 'Truman1*'},
    headers={'Content-Type': 'application/json'}
)
print("Login Response:", login_resp.status_code)
print(json.dumps(login_resp.json(), indent=2))

# Get token
if login_resp.status_code == 200:
    token = login_resp.json()['access_token']
    print(f"\n✅ Got token: {token[:50]}...")
    
    # Get profile
    me_resp = requests.get(
        'http://localhost:8000/api/v1/auth/me',
        headers={'Authorization': f'Bearer {token}', 'Origin': 'http://localhost:5173'}
    )
    print(f"\nProfile Response: {me_resp.status_code}")
    print(json.dumps(me_resp.json(), indent=2, default=str))
