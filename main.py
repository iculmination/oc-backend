from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints.health import router as health_router
from app.api.endpoints.dev import router as dev_router
from app.api.endpoints.card import router as card_router
from app.api.endpoints.game import router as game_router
from app.api.endpoints.auth import router as auth_router
from app.core.settings.settings import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.app.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(dev_router)
app.include_router(card_router)
app.include_router(game_router)
app.include_router(auth_router)