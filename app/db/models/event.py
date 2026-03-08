from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum, String

from app.db.models.base import Base

from app.enums.event import EventRarity, EventStatus, EventSource


class Event(Base):
    __tablename__ = "event"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    rarity: Mapped[EventRarity] = mapped_column(Enum(EventRarity), nullable=False)
    status: Mapped[EventStatus] = mapped_column(Enum(EventStatus), nullable=False)
    source: Mapped[EventSource] = mapped_column(Enum(EventSource), nullable=False)

    effect: Mapped[str] = mapped_column(String(255), nullable=False)

    description: Mapped[str] = mapped_column(String(255), nullable=False)
