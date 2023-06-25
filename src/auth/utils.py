from typing import Type
from sqlalchemy import select, delete
from pydantic import BaseModel
from src.database import Base
from .schemas import CreateUserOuter, ReadUser, UpdateUser
from .models import User
from .costants import secret_controller
from sqlalchemy.ext.asyncio import AsyncSession


class IAsyncRepo:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def _execute(self, stmt) -> any:
        result = await self._session.execute(stmt)
        return result

    async def _delete(self, model: Type[Base], object_id: int) -> int:
        stmt = delete(model).where(model.id == object_id).returning(model.id)
        exec_result = await self._execute(stmt)
        (deleted_id,) = exec_result.one()
        return deleted_id

    async def _add(self, object_: Base) -> Base:
        self._session.add(object_)
        await self._session.flush()
    
    async def _add_schema_out(self, object_: Base, read_schema: Type[BaseModel]) -> BaseModel:
        await self._add(object_)
        return read_schema(**object_.__dict__)

    async def _get(self, model: Type[Base], id_: int) -> Base:
        stmt = select(model).where(model.id == id_)
        exec_result = await self._execute(stmt)
        db_obj = exec_result.scalar()
        return db_obj
    
    def get_read_shchema(self, db_object: Base, read_schema: Type[BaseModel]) -> BaseModel:
        return read_schema(**db_object.__dict__)
    
    async def _update(self, db_object: Base, update_schema: BaseModel) -> Base:
        obj_data = db_object.__dict__
        schema_data = update_schema.dict(exclude={"id",})
        table_fields = list(db_object.__table__.columns.keys())
        is_changed = False
        for field in obj_data:
            if field in schema_data and schema_data.get(field) is not None:
                if field in table_fields:
                    setattr(db_object, field, schema_data[field])
                    is_changed = True
                else:
                    table_name = (db_object.__table__.name).title().replace("_", "")
                    raise KeyError(
                        f"Update scheme for {table_name} have incorrect params"
                    )
        if is_changed:
            await self._add(db_object)
            await self._session.refresh(db_object)
        return db_object

class AuthenticateRepo(IAsyncRepo):
    async def create_user(self, user: CreateUserOuter) -> ReadUser:
        hashed_password = secret_controller.hash_secret(user.password)
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_pswd=hashed_password,
            is_active=user.is_active,
            user_role_id=user.user_role_id,
        )
        return await self._add_schema_out(db_user, ReadUser)

    async def delete_user(self, id_: int) -> int:
        return await self._delete(User, id_)

    async def update_user(self, upd_user: UpdateUser) -> ReadUser:
        db_object = await self._get(User, upd_user.id)
        db_object = await self._update(db_object,upd_user)        
        return self.get_read_shchema(db_object,ReadUser)
