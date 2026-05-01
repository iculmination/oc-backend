from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, Integer, ForeignKey, Enum, Index

from app.db.models.base import Base
from app.enums.event import EventStatus


class GameEvent(Base):
    __tablename__ = "game_event"

    game_id: Mapped[UUID] = mapped_column(UUID, ForeignKey("game.id"), nullable=False)
    event_id: Mapped[UUID] = mapped_column(UUID, ForeignKey("event.id"), nullable=False)

    duration_left: Mapped[int] = mapped_column(Integer, nullable=False)
    applied_at_round: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[EventStatus] = mapped_column(
        Enum(EventStatus), nullable=False, default=EventStatus.ONGOING
    )

    game: Mapped["Game"] = relationship("Game", back_populates="active_events")
    event_definition: Mapped["Event"] = relationship(
        "Event", back_populates="game_events"
    )


Index("ix_game_event_game_status", GameEvent.game_id, GameEvent.status)
