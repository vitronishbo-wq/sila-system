#!/usr/bin/env python3
"""
Start FastAPI server for manual testing
"""

import uvicorn
from fastapi import FastAPI
from modules.payment.endpoints.payment_endpoints import router as payment_router

app = FastAPI(title="SILA Payment API", version="1.0.0")
app.include_router(payment_router)

if __name__ == "__main__":
    print("🚀 Starting FastAPI server for payment endpoints testing...")
    print("📊 Available endpoints:")
    for route in app.routes:
        if hasattr(route, "methods") and hasattr(route, "path"):
            print(f"  {route.methods} {route.path}")

    print("\n🌐 Server will be available at: http://localhost:8000")
    print("📖 Swagger UI: http://localhost:8000/docs")
    print("📖 ReDoc: http://localhost:8000/redoc")

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
