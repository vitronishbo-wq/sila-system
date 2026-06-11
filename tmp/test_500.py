import httpx, sys

urls = [
    ("beneficiarios", "GET", "http://localhost:8000/society/assistencia_social/assistencia-social/beneficiarios/"),
    ("beneficios", "GET", "http://localhost:8000/society/assistencia_social/assistencia-social/beneficios/"),
    ("search_health", "GET", "http://localhost:8000/educacao/marketplace/search/search/health"),
]

for name, method, url in urls:
    try:
        r = httpx.request(method, url, timeout=10)
        print(f"{name}: STATUS={r.status_code}")
        print(f"  BODY: {r.text[:500]}")
    except Exception as e:
        print(f"{name}: ERROR={e}")
