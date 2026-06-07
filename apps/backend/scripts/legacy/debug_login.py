import json
import urllib.parse
import urllib.request

try:
    routes = [
        "http://localhost:8000/api/v1/auth/login",
        "http://localhost:8000/api/v1/auth/login-v2",
        "http://localhost:8000/api/v1/autenticacao/login",
    ]

    data = {"username": "admin@sila.gov.ao", "password": "Admin123!"}
    # Test 1: Raw Form Data (Standard)
    encoded_data = urllib.parse.urlencode(data).encode("utf-8")

    # Test 2: JSON (for debug)
    json_data = json.dumps(data).encode("utf-8")

    tests = [
        {
            "url": "http://localhost:8000/api/v1/auth/login",
            "data": encoded_data,
            "ctype": "application/x-www-form-urlencoded",
        },
        {
            "url": "http://localhost:8000/api/v1/auth/login/debug-raw",
            "data": encoded_data,
            "ctype": "application/x-www-form-urlencoded",
        },
        {
            "url": "http://localhost:8000/api/v1/auth/test-form",
            "data": encoded_data,
            "ctype": "application/x-www-form-urlencoded",
        },
    ]

    for test in tests:
        url = test["url"]
        print(f"\n--- Testing URL: {url} ---")
        try:
            req = urllib.request.Request(
                url, data=test["data"], method="POST", headers={"Content-Type": test["ctype"]}
            )
            with urllib.request.urlopen(req) as response:
                print(f"Status Code: {response.status}")
                body = response.read().decode("utf-8")
                print(f"Response Body: {body}")
        except urllib.error.HTTPError as e:
            print(f"HTTP Error: {e.code}")
            print(f"Response: {e.read().decode('utf-8')}")
        except Exception as e:
            print(f"Error: {e}")

except Exception as e:
    print(f"Global Error: {e}")
