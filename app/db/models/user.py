from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum, String, Boolean

from app.db.models.base import Base
from app.db.mixins.id import IdMixin
from app.db.mixins.timestamp import TimestampMixin

from app.enums.user import UserStatus


class User(Base, IdMixin, TimestampMixin):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    status: Mapped[UserStatus] = mapped_column(
        Enum(UserStatus), nullable=False, default=UserStatus.ACTIVE
    )
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
