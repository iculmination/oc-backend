from sqlalchemy.orm import DeclarativeBase
from app.db.mixins.id import IdMixin
from app.db.mixins.timestamp import TimestampMixin

class Base(DeclarativeBase, IdMixin, TimestampMixin):
    pass