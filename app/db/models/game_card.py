from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, Integer, String, Boolean, ForeignKey, JSON, Index

from app.db.models.base import Base


class GameCard(Base):
    __tablename__ = "game_card"

    game_id: Mapped[UUID] = mapped_column(UUID, ForeignKey("game.id"), nullable=False)
    player_id: Mapped[UUID] = mapped_column(
        UUID, ForeignKey("player.id"), nullable=False
    )
    card_definition_id: Mapped[UUID | None] = mapped_column(
        UUID, ForeignKey("card.id"), nullable=True
    )

    zone: Mapped[str] = mapped_column(String(32), nullable=False, default="board")
    position: Mapped[int | None] = mapped_column(Integer, nullable=True)

    attack_current: Mapped[int] = mapped_column(Integer, nullable=False)
    health_current: Mapped[int] = mapped_column(Integer, nullable=False)
    max_health_current: Mapped[int] = mapped_column(Integer, nullable=False)
    is_alive: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    statuses: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    last_action: Mapped[str | None] = mapped_column(String(255), nullable=True)

    game: Mapped["Game"] = relationship("Game", back_populates="cards")
    player: Mapped["Player"] = relationship("Player", back_populates="cards")
    card_definition: Mapped["Card | None"] = relationship(
        "Card", back_populates="game_cards"
    )
    logs: Mapped[list["GameLog"]] = relationship("GameLog", back_populates="actor_card")


Index("ix_game_card_game_player", GameCard.game_id, GameCard.player_id)
Index("ix_game_card_game_zone", GameCard.game_id, GameCard.zone)
