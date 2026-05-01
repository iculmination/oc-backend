from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, UUID, Enum, ForeignKey, JSON

from app.db.models.base import Base


from app.enums.game import GameStatus


class Game(Base):
    __tablename__ = "game"

    turn: Mapped[int] = mapped_column(Integer, nullable=False)
    turn_player_id: Mapped[UUID | None] = mapped_column(
        UUID, ForeignKey("player.id"), nullable=True
    )
    winner_player_id: Mapped[UUID | None] = mapped_column(
        UUID, ForeignKey("player.id"), nullable=True
    )
    state_snapshot: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    status: Mapped[GameStatus] = mapped_column(
        Enum(GameStatus), nullable=False, default=GameStatus.PENDING
    )

    players: Mapped[list["Player"]] = relationship(
        "Player",
        back_populates="game",
        cascade="all, delete-orphan",
        foreign_keys="Player.game_id",
    )
    active_events: Mapped[list["GameEvent"]] = relationship(
        "GameEvent", back_populates="game", cascade="all, delete-orphan"
    )
    cards: Mapped[list["GameCard"]] = relationship(
        "GameCard", back_populates="game", cascade="all, delete-orphan"
    )
    logs: Mapped[list["GameLog"]] = relationship(
        "GameLog", back_populates="game", cascade="all, delete-orphan"
    )
