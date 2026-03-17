from fastapi import HTTPException
from uuid import UUID
from app.schemas.card import CardSchema
from app.engine.utils.unit_of_work import UnitOfWork


class CardService:

    async def get_card(self, card_id: UUID) -> CardSchema | None:
        async with UnitOfWork() as uow:
            return await uow.card.get_one_or_none(id=card_id)

    async def get_cards(self) -> list[CardSchema]:
        async with UnitOfWork() as uow:
            return await uow.card.get_multi()

    async def create_card(self, card: CardSchema) -> CardSchema:
        async with UnitOfWork() as uow:
            if await uow.card.get_one_or_none(name=card.name):
                raise HTTPException(status_code=400, detail="Card already exists")
        return await uow.card.create(card)

    async def update_card(self, card_id: UUID, card: CardSchema) -> CardSchema:
        async with UnitOfWork() as uow:
            if not await uow.card.get_one_or_none(id=card_id):
                raise HTTPException(status_code=404, detail="Card not found")
        return await uow.card.update(card_id, card, return_object=True)

    async def delete_card(self, card_id: UUID) -> CardSchema:
        async with UnitOfWork() as uow:
            if not await uow.card.get_one_or_none(id=card_id):
                raise HTTPException(status_code=404, detail="Card not found")
        return await uow.card.delete(card_id, return_object=True)

    async def get_card_count(self) -> int:
        async with UnitOfWork() as uow:
            return await uow.card.get_count()
