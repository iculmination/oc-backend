from fastapi import APIRouter, Request, Response, status

from app.api.dependencies import auth_service
from app.schemas.auth import AuthResponse, LoginRequest, MeResponse, RegisterRequest

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=AuthResponse)
async def register(payload: RegisterRequest, response: Response, service: auth_service):
    return await service.register(payload, response)


@router.post("/login", response_model=AuthResponse)
async def login(payload: LoginRequest, response: Response, service: auth_service):
    return await service.login(payload, response)


@router.post("/refresh", response_model=AuthResponse)
async def refresh(request: Request, response: Response, service: auth_service):
    return await service.refresh(request, response)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response, service: auth_service):
    service.clear_auth_cookies(response)


@router.get("/me", response_model=MeResponse)
async def me(request: Request, service: auth_service):
    return await service.me(request)
