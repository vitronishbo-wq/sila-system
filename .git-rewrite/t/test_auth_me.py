#!/usr/bin/env python3
import requests
import json

# Login
login_resp = requests.post(
    'http://localhost:8000/api/v1/auth/login',
    json={'email': 'admin@sila.gov.ao', 'password': 'Truman1*'},
)

if login_resp.status_code == 200:
    token = login_resp.json()['access_token']
    
    # Get profile
    me_resp = requests.get(
        'http://localhost:8000/api/v1/auth/me',
        headers={'Authorization': f'Bearer {token}'}
    )
    print(f"Profile Response: {me_resp.status_code}")
    print(f"Content: {me_resp.text[:500]}")
