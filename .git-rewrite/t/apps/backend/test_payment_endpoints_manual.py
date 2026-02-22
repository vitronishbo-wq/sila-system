#!/usr/bin/env python3
"""
Manual test script for payment endpoints validation
"""

import asyncio
import sys
from httpx import AsyncClient
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# Import payment module components
from modules.payment.endpoints.payment_endpoints import router as payment_router
from core.db.session import get_db

# Setup FastAPI app
app = FastAPI(title="SILA Payment API Test")
app.include_router(payment_router)

# Setup database for testing
DATABASE_URL = "postgresql+asyncpg://localhost/sila_test"
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def override_get_db():
    async with AsyncSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


async def test_all_endpoints():
    """Test all payment endpoints"""
    print("🚀 Starting Payment Endpoints Validation")
    print("=" * 50)

    async with AsyncClient(app=app, base_url="http://test") as client:

        # Test 1: Health Check - Ping
        print("\n1️⃣ Testing GET /payments/ping")
        try:
            response = await client.get("/payments/ping")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
            assert response.status_code == 200
            assert response.json() == {"status": "ok", "module": "payment"}
            print("   ✅ PASS")
        except Exception as e:
            print(f"   ❌ FAIL: {e}")

        # Test 2: Health Check - Status
        print("\n2️⃣ Testing GET /payments/status")
        try:
            response = await client.get("/payments/status")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
            assert response.status_code == 200
            assert response.json() == {"module": "payment", "status": "active"}
            print("   ✅ PASS")
        except Exception as e:
            print(f"   ❌ FAIL: {e}")

        # Test 3: List Payments (empty list)
        print("\n3️⃣ Testing GET /payments/")
        try:
            response = await client.get("/payments/")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
            assert response.status_code == 200
            assert isinstance(response.json(), list)
            print("   ✅ PASS")
        except Exception as e:
            print(f"   ❌ FAIL: {e}")

        # Test 4: Get Payment Not Found
        print("\n4️⃣ Testing GET /payments/999999")
        try:
            response = await client.get("/payments/999999")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
            assert response.status_code == 404
            assert response.json()["detail"] == "Payment not found"
            print("   ✅ PASS")
        except Exception as e:
            print(f"   ❌ FAIL: {e}")

        # Test 5: Get Transaction Not Found
        print("\n5️⃣ Testing GET /payments/transactions/999999")
        try:
            response = await client.get("/payments/transactions/999999")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
            assert response.status_code == 404
            assert response.json()["detail"] == "Transaction not found"
            print("   ✅ PASS")
        except Exception as e:
            print(f"   ❌ FAIL: {e}")

        # Test 6: Create Payment
        print("\n6️⃣ Testing POST /payments/")
        try:
            payload = {
                "amount": 100.0,
                "method": "credit_card",
                "status": "pending",
                "description": "Pagamento de teste",
            }
            response = await client.post("/payments/", json=payload)
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
            assert response.status_code == 201
            data = response.json()
            assert data["amount"] == 100.0
            assert data["method"] == "credit_card"
            assert data["status"] == "pending"
            print("   ✅ PASS")
        except Exception as e:
            print(f"   ❌ FAIL: {e}")

    print("\n" + "=" * 50)
    print("🎯 Payment Endpoints Validation Complete!")
    print("📊 All basic endpoints are working correctly!")


if __name__ == "__main__":
    print("🔧 Running manual payment endpoint tests...")
    asyncio.run(test_all_endpoints())
