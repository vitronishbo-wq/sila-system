from fastapi import FastAPI

from .eligibility import router as eligibility_router

app = FastAPI(title="SILA API Gateway - Educational Automation")

app.include_router(eligibility_router)


def create_app():
    return app


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("apps.api_gateway.main:app", host="127.0.0.1", port=8000, reload=False)
