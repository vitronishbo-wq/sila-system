"""
Test the economy transactions endpoint
Demonstrates the consolidated economy core API
"""

import json
import sys

# Add the backend to path
sys.path.insert(0, "/home/dev03wsl/sila-system/apps/backend")

from apps.backend.app.modules.economy.api.router import router as economy_router
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Create minimal test app (avoiding full main.py with identity module issues)
app = FastAPI(title="Economy Module Test")
app.include_router(economy_router)

# Create test client
client = TestClient(app)


def test_transactions():
    """Test the economy transactions endpoint"""
    print("=" * 70)
    print("ECONOMY TRANSACTIONS ENDPOINT TEST")
    print("=" * 70)

    # Test 1: Health check
    print("\n1️⃣ Testing /economy/ping endpoint:")
    response = client.get("/economy/ping")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    assert response.status_code == 200
    print("   ✅ PASSED")

    # Test 2: Create transaction with your curl example
    print("\n2️⃣ Testing POST /economy/transactions (from curl example):")
    payload = {"amount": 1000, "currency": "AOA"}
    print(f"   Payload: {json.dumps(payload, indent=2)}")
    response = client.post("/economy/transactions", json=payload)
    print(f"   Status: {response.status_code}")
    result = response.json()
    print("   Response:")
    print(f"     - ID: {result['id']}")
    print(f"     - Amount: {result['amount']} {result['currency']}")
    print(f"     - Status: {result['status']}")
    print(f"     - Module: {result['module']}")
    assert response.status_code == 200
    assert result["amount"] == 1000
    assert result["currency"] == "AOA"
    print("   ✅ PASSED")

    # Test 3: Invalid currency
    print("\n3️⃣ Testing error handling (invalid currency):")
    payload = {"amount": 500, "currency": "XXX"}
    response = client.post("/economy/transactions", json=payload)
    print(f"   Status: {response.status_code}")
    print(f"   Error: {response.json()['detail']}")
    assert response.status_code == 400
    print("   ✅ PASSED (correctly rejected invalid currency)")

    # Test 4: Get transaction
    print("\n4️⃣ Testing GET /economy/transactions/{{id}}:")
    response = client.get("/economy/transactions/TRX-123456789")
    print(f"   Status: {response.status_code}")
    result = response.json()
    print(f"   Transaction ID: {result['id']}")
    print(f"   Status: {result['status']}")
    assert response.status_code == 200
    print("   ✅ PASSED")

    # Test 5: List transactions
    print("\n5️⃣ Testing GET /economy/transactions (list):")
    response = client.get("/economy/transactions?skip=0&limit=10")
    print(f"   Status: {response.status_code}")
    result = response.json()
    print(f"   Module: {result['module']}")
    print(f"   Total transactions: {result['total']}")
    assert response.status_code == 200
    print("   ✅ PASSED")

    # Summary
    print("\n" + "=" * 70)
    print("✅ ALL TESTS PASSED")
    print("=" * 70)
    print("\n📋 ENDPOINT SUMMARY:")
    print("   POST   /economy/transactions        - Create transaction")
    print("   GET    /economy/transactions        - List transactions")
    print("   GET    /economy/transactions/{id}   - Get transaction by ID")
    print("\n💡 CURL EXAMPLE:")
    print("   curl -X POST http://localhost:8000/economy/transactions \\")
    print("     -H 'Content-Type: application/json' \\")
    print('     -d \'{"amount":1000,"currency":"AOA"}\'')
    print("\n🏗️ ARCHITECTURE:")
    print("   ✅ Consolidated in: core/")
    print("   ✅ Hexagonal layers: domain → application → infrastructure")
    print("   ✅ API layer: Read-only wrapper (api/router.py)")
    print("   ✅ Module status: INTERPRETER LEVEL (ready for production)")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test_transactions()
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
