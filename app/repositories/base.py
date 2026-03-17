from typing import Type
from sqlalchemy.orm import Session
from app.db.models.base import Base
from uuid import UUID

class BaseRepository:
    def __init__(self, session: Session):
        self.session = session

    async def get_all(self, model: Type[Base]):
        return self.session.query(model).all()

    async def get_by_id(self, model: Type[Base], id: UUID):
        return self.session.query(model).filter(model.id == id).first()

    async def create(self, model: Type[Base], **kwargs):
        instance = model(**kwargs)
        self.session.add(instance)
        self.session.commit()
        return instance