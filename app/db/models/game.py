from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, UUID, Enum

from app.db.models.base import Base
from app.db.models.player import Player
from app.db.models.event import Event
from app.db.models.card import Card

from app.enums.game import GameStatus


class Game(Base):
    __tablename__ = "game_state"

    turn: Mapped[int] = mapped_column(Integer, nullable=False)
    turn_player_id: Mapped[UUID] = mapped_column(UUID, nullable=True)

    status: Mapped[GameStatus] = mapped_column(
        Enum(GameStatus), nullable=False, default=GameStatus.PENDING
    )

    players: Mapped[list[Player]] = relationship(
        "Player", back_populates="game", cascade="all, delete-orphan"
    )
    events: Mapped[list[Event]] = relationship(
        "Event", back_populates="game", cascade="all, delete-orphan"
    )
    board: Mapped[list[Card]] = relationship(
        "Card", back_populates="game", cascade="all, delete-orphan"
    )
