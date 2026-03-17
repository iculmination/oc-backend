from fastapi import APIRouter
from app.api.dependencies import card_service
from uuid import UUID
from app.schemas.card import CardSchema

router = APIRouter(prefix="/card", tags=["Card"])


@router.get("/{card_id}", response_model=CardSchema)
async def get_card(card_id: UUID, service: card_service):
    return await service.get_card(card_id)


@router.get("/", response_model=list[CardSchema])
async def get_cards(service: card_service):
    return await service.get_cards()


@router.post("/", response_model=CardSchema)
async def create_card(card: CardSchema, service: card_service):
    return await service.create_card(card)


@router.put("/{card_id}", response_model=CardSchema)
async def update_card(card_id: UUID, card: CardSchema, service: card_service):
    return await service.update_card(card_id, card)


@router.delete("/{card_id}", response_model=CardSchema)
async def delete_card(card_id: UUID, service: card_service):
    return await service.delete_card(card_id)
