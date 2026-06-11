import httpx, sys, traceback

url = sys.argv[1]
try:
    r = httpx.get(url, timeout=10)
    print(f"STATUS={r.status_code}")
    print(f"HEADERS={dict(r.headers)}")
    print(f"BODY={r.text}")
except Exception as e:
    traceback.print_exc()
