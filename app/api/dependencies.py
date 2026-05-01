from fastapi import Depends, Request
from typing import Annotated

from app.services.card import CardService
from app.services.auth import AuthService
from app.schemas.auth import MeResponse

card_service = Annotated[CardService, Depends(CardService)]
auth_service = Annotated[AuthService, Depends(AuthService)]


async def get_current_user(request: Request, service: auth_service) -> MeResponse:
    return await service.me(request)


current_user = Annotated[MeResponse, Depends(get_current_user)]
