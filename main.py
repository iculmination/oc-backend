from fastapi import FastAPI
from app.api.endpoints.health import router as health_router
from app.api.endpoints.dev import router as dev_router
from app.api.endpoints.card import router as card_router

app = FastAPI()

app.include_router(health_router)
app.include_router(dev_router)
app.include_router(card_router)