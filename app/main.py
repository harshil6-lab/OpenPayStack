from fastapi import FastAPI
from app.api.routes.auth import router as auth_router
app = FastAPI(title="OpenPayStack",version="0.1.0")

app.include_router(auth_router)

@app.get("/")

def health():
    return {
        "status" : "healthy",
        "service" : "OpenPayStack"
    }