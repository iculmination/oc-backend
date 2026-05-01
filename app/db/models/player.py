from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, Enum, String, Boolean, Integer, ForeignKey
from app.db.models.base import Base

from app.enums.player import PlayerStatus, PlayerRole


class Player(Base):
    __tablename__ = "player"

    user_id: Mapped[UUID | None] = mapped_column(
        UUID, ForeignKey("users.id"), nullable=True
    )
    game_id: Mapped[UUID] = mapped_column(UUID, ForeignKey("game.id"), nullable=False)
    is_bot: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    seat: Mapped[int] = mapped_column(Integer, nullable=False)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)

    role: Mapped[PlayerRole] = mapped_column(Enum(PlayerRole), nullable=False)
    status: Mapped[PlayerStatus] = mapped_column(Enum(PlayerStatus), nullable=False)

    game: Mapped["Game"] = relationship(
        "Game", back_populates="players", foreign_keys=[game_id]
    )
    user: Mapped["User"] = relationship("User", back_populates="players")
    cards: Mapped[list["GameCard"]] = relationship(
        "GameCard", back_populates="player", cascade="all, delete-orphan"
    )
