from app.repositories.base import SQLAlchemyRepository
from app.db.models.card import Card


class CardRepository(SQLAlchemyRepository[Card]):
    model = Card
