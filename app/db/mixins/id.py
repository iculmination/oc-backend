from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UUID
from uuid import uuid4

class IdMixin:
    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid4)