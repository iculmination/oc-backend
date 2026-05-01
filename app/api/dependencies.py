from fastapi import Depends
from typing import Annotated
from app.services.card import CardService
from app.services.auth import AuthService

card_service = Annotated[CardService, Depends(CardService)]
auth_service = Annotated[AuthService, Depends(AuthService)]
