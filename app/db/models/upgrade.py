from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum, Integer, String

from app.db.models.base import Base

from app.enums.upgrade import UpgradeRarity, UpgradeType


class Upgrade(Base):
    __tablename__ = "upgrade"

    rarity: Mapped[UpgradeRarity] = mapped_column(Enum(UpgradeRarity), nullable=False)
    type: Mapped[UpgradeType] = mapped_column(Enum(UpgradeType), nullable=False)
    cost: Mapped[int] = mapped_column(Integer, nullable=False)

    effect: Mapped[str] = mapped_column(String(255), nullable=False)

    description: Mapped[str] = mapped_column(String(255), nullable=False)
