from fastapi import FastAPI
from app.api.routes.auth import router as auth_router
from app.api.routes.user import router as user_router
app = FastAPI(title="OpenPayStack",version="0.1.0")

app.include_router(auth_router)
app.include_router(user_router)
@app.get("/")

def health():
    return {
        "status" : "healthy",
        "service" : "OpenPayStack"
    }