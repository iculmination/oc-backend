from uuid import UUID

import jwt
from fastapi import HTTPException, Request, Response, status

from app.core.security import (
    ACCESS_TOKEN_COOKIE,
    REFRESH_TOKEN_COOKIE,
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.core.settings.settings import settings
from app.engine.utils.unit_of_work import UnitOfWork
from app.schemas.auth import AuthResponse, LoginRequest, MeResponse, RegisterRequest


class AuthService:
    def _set_auth_cookies(self, response: Response, access_token: str, refresh_token: str):
        secure = settings.app.auth_cookie_secure
        response.set_cookie(
            key=ACCESS_TOKEN_COOKIE,
            value=access_token,
            httponly=True,
            secure=secure,
            samesite="lax",
            max_age=settings.app.jwt_access_ttl_minutes * 60,
            path="/",
        )
        response.set_cookie(
            key=REFRESH_TOKEN_COOKIE,
            value=refresh_token,
            httponly=True,
            secure=secure,
            samesite="lax",
            max_age=settings.app.jwt_refresh_ttl_days * 24 * 60 * 60,
            path="/",
        )

    def clear_auth_cookies(self, response: Response):
        response.delete_cookie(ACCESS_TOKEN_COOKIE, path="/")
        response.delete_cookie(REFRESH_TOKEN_COOKIE, path="/")

    async def register(self, payload: RegisterRequest, response: Response) -> AuthResponse:
        async with UnitOfWork() as uow:
            existing_by_email = await uow.user.get_one_or_none(email=payload.email)
            if existing_by_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User with this email already exists",
                )

            existing_by_username = await uow.user.get_one_or_none(username=payload.username)
            if existing_by_username:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User with this username already exists",
                )

            user = await uow.user.create(
                {
                    "username": payload.username,
                    "email": payload.email,
                    "password": hash_password(payload.password),
                }
            )

        access_token = create_access_token(str(user.id))
        refresh_token = create_refresh_token(str(user.id))
        self._set_auth_cookies(response, access_token, refresh_token)

        return AuthResponse(
            message="Registration successful",
            user_id=user.id,
            username=user.username,
            email=user.email,
        )

    async def login(self, payload: LoginRequest, response: Response) -> AuthResponse:
        async with UnitOfWork() as uow:
            user = await uow.user.get_one_or_none(email=payload.email)
            if not user or not user.password or not verify_password(
                payload.password, user.password
            ):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials",
                )

        access_token = create_access_token(str(user.id))
        refresh_token = create_refresh_token(str(user.id))
        self._set_auth_cookies(response, access_token, refresh_token)

        return AuthResponse(
            message="Login successful",
            user_id=user.id,
            username=user.username,
            email=user.email,
        )

    async def refresh(self, request: Request, response: Response) -> AuthResponse:
        refresh_token = request.cookies.get(REFRESH_TOKEN_COOKIE)
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token not found",
            )

        try:
            payload = decode_token(refresh_token)
            if payload.get("type") != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token type",
                )
            user_id = payload.get("sub")
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token subject",
                )
        except jwt.PyJWTError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            ) from exc

        async with UnitOfWork() as uow:
            user = await uow.user.get_one_or_none(id=UUID(user_id))
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found",
                )

        access_token = create_access_token(str(user.id))
        rotated_refresh = create_refresh_token(str(user.id))
        self._set_auth_cookies(response, access_token, rotated_refresh)

        return AuthResponse(
            message="Token refreshed",
            user_id=user.id,
            username=user.username,
            email=user.email,
        )

    async def me(self, request: Request) -> MeResponse:
        access_token = request.cookies.get(ACCESS_TOKEN_COOKIE)
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token not found",
            )

        try:
            payload = decode_token(access_token)
            if payload.get("type") != "access":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid access token type",
                )
            user_id = payload.get("sub")
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid access token subject",
                )
        except jwt.PyJWTError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
            ) from exc

        async with UnitOfWork() as uow:
            user = await uow.user.get_one_or_none(id=UUID(user_id))
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found",
                )
            return MeResponse(user_id=user.id, username=user.username, email=user.email)
