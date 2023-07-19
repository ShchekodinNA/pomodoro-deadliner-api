from tests.utils import IMockDbManager, get_uuid4_as_str
from src.database import Base
from src.auth.models import User


class MockDbUserManager(IMockDbManager):
    async def _get_unique_object(self, **kwagrs) -> Base:
        user = User(
            username=get_uuid4_as_str(),
            email=get_uuid4_as_str(),
            hashed_pswd="",
            user_role_id=None,
        )
        return user
