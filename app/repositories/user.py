from app.repositories.base import SQLAlchemyRepository
from app.db.models.user import User


class UserRepository(SQLAlchemyRepository[User]):
    model = User
