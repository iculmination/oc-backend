from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum, Integer, String

from app.db.models.base import Base

from app.enums.card import Rarity, CardNature, CardSpecialty, CardFaction

# from app.db.models.upgrade import Upgrade


class Card(Base):
    __tablename__ = "player"

    rarity: Mapped[Rarity] = mapped_column(Enum(Rarity), nullable=False)
    cost: Mapped[int] = mapped_column(Integer, nullable=False)

    health: Mapped[int] = mapped_column(Integer, nullable=False)
    energy: Mapped[int] = mapped_column(Integer, nullable=False)
    defense: Mapped[int] = mapped_column(Integer, nullable=False)
    cool_down: Mapped[int] = mapped_column(Integer, nullable=False)
    attack: Mapped[int] = mapped_column(Integer, nullable=False)
    speed: Mapped[int] = mapped_column(Integer, nullable=False)

    nature: Mapped[CardNature] = mapped_column(Enum(CardNature), nullable=False)
    specialty: Mapped[CardSpecialty] = mapped_column(
        Enum(CardSpecialty), nullable=False
    )
    faction: Mapped[CardFaction] = mapped_column(Enum(CardFaction), nullable=False)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)

    # idea: cards can have upgrades, some cards have them installed by default, some cards can have upgrades installed by the player
    # upgrades: Mapped[list[Upgrade]] = relationship("Upgrade", back_populates="card")
