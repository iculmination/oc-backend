from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, Integer, String, ForeignKey, JSON, Index

from app.db.models.base import Base


class GameLog(Base):
    __tablename__ = "game_log"

    game_id: Mapped[UUID] = mapped_column(UUID, ForeignKey("game.id"), nullable=False)
    round_number: Mapped[int] = mapped_column(Integer, nullable=False)
    sequence: Mapped[int] = mapped_column(Integer, nullable=False)

    actor_type: Mapped[str] = mapped_column(String(32), nullable=False)
    actor_player_id: Mapped[UUID | None] = mapped_column(
        UUID, ForeignKey("player.id"), nullable=True
    )
    actor_card_id: Mapped[UUID | None] = mapped_column(
        UUID, ForeignKey("game_card.id"), nullable=True
    )
    action_type: Mapped[str] = mapped_column(String(64), nullable=False)

    payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    message: Mapped[str] = mapped_column(String(255), nullable=False)

    game: Mapped["Game"] = relationship("Game", back_populates="logs")
    actor_player: Mapped["Player | None"] = relationship("Player")
    actor_card: Mapped["GameCard | None"] = relationship(
        "GameCard", back_populates="logs"
    )


Index(
    "ix_game_log_game_round_seq",
    GameLog.game_id,
    GameLog.round_number,
    GameLog.sequence,
)
Index("ix_game_log_game_created", GameLog.game_id, GameLog.created_at)
