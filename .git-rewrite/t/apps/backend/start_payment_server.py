#!/usr/bin/env python3
"""
Start FastAPI server for payment endpoints on port 8001
"""

import uvicorn
from fastapi import FastAPI
from modules.payment.endpoints.payment_endpoints import router as payment_router

app = FastAPI(title="SILA Payment API", version="1.0.0")
app.include_router(payment_router)

if __name__ == "__main__":
    print("🚀 Starting FastAPI server for payment endpoints...")
    print("📊 Available endpoints:")
    for route in app.routes:
        if hasattr(route, "methods") and hasattr(route, "path"):
            print(f"  {route.methods} {route.path}")

    print("\n🌐 Server will be available at:")
    print("   http://127.0.0.1:8001")
    print("📖 Swagger UI:")
    print("   http://127.0.0.1:8001/docs")
    print("📖 ReDoc:")
    print("   http://127.0.0.1:8001/redoc")

    uvicorn.run(app, host="127.0.0.1", port=8001, reload=True)
