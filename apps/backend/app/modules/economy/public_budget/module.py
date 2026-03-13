from .api.router import router

def register(app):
    app.include_router(router)