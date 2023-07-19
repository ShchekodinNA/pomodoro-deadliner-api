from abc import ABC, abstractmethod
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import async_session_generator, Base


class IMockDbManager(ABC):
    def __init__(self, async_session: AsyncSession) -> None:
        self._session: AsyncSession = async_session
        self._exist_postitions: dict = {}

    async def get(self, object_number: int, **kwargs) -> Base:
        object_ = self._exist_postitions.get(object_number)
        if object_ is not None:
            return object_
        result = await self._get_unique_object(**kwargs)
        self._session.add(result)
        await self._session.flush()
        self._exist_postitions[object_number] = result
        return result

    @abstractmethod
    async def _get_unique_object(self, **kwagrs) -> Base:
        raise NotImplementedError("__get_unique_object")


class SessionFor_testing:
    def __init__(self) -> None:
        self.sess_gen = async_session_generator()
        self._session: AsyncSession | None = None

    @property
    def session(self):
        return self._session

    def start_testing_sesion(self) -> AsyncSession:
        self._session = self.sess_gen()
        return self.session

    async def finish_testing_session(self):
        await self._session.rollback()
        await self._session.close()

def get_uuid4_as_str() -> str:
    return str(uuid4())