from fastapi import Depends
from typing import Annotated
from app.services.card import CardService

card_service = Annotated[CardService, Depends(CardService)]
