from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, Enum

from app.db.models.base import Base
from app.db.models.game import Game
from app.db.models.user import User

from app.enums.player import PlayerStatus, PlayerRole


class Player(Base):
    __tablename__ = "player"

    user_id: Mapped[UUID] = mapped_column(UUID, nullable=False)
    game_id: Mapped[UUID] = mapped_column(UUID, nullable=False)

    role: Mapped[PlayerRole] = mapped_column(Enum(PlayerRole), nullable=False)
    status: Mapped[PlayerStatus] = mapped_column(Enum(PlayerStatus), nullable=False)

    game: Mapped[Game] = relationship("Game", back_populates="players")
    user: Mapped[User] = relationship("User", back_populates="players")
