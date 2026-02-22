#!/usr/bin/env python3
print("Starting simple test...")

try:
    from modules.payment import payment_router

    print("✅ Payment router imported")

    from fastapi import FastAPI

    app = FastAPI()
    app.include_router(payment_router)
    print("✅ FastAPI app created")

    print("✅ Routes:")
    for route in app.routes:
        print(f"  {route.methods} {route.path}")

    print("🎉 All imports working!")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback

    traceback.print_exc()
