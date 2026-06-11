from fastapi.testclient import TestClient
from apps.backend.app.main import app

client = TestClient(app)

# token Super Admin (substituir pelo válido)
headers = {"Authorization": "Bearer <SUPER_ADMIN_TOKEN>"}

for endpoint in ["/api/admin/citizens", "/api/admin/documents"]:
    print(f"Testing {endpoint}")
    response = client.get(endpoint, headers=headers)
    print("Status:", response.status_code)
    print("Body:", response.text)
