from typing import Type, Optional
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from pydantic import BaseModel
from src.database import Base
from .schemas import CreateUserOuter, ReadUser, UpdateUser
from .models import User
from .costants import secret_controller, BaseRolesEnum
from .exceptions import NotAuthenticated
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

    async def _add_schema_out(
        self, object_: Base, read_schema: Type[BaseModel]
    ) -> BaseModel:
        await self._add(object_)
        return read_schema(**object_.__dict__)

    async def _get(
        self, model: Type[Base], id_: int, options: Optional[list] = None
    ) -> Base:
        stmt = select(model).where(model.id == id_)
        if options is not None:
            stmt = stmt.options(*options)
        exec_result = await self._execute(stmt)
        db_obj = exec_result.scalar()
        if db_obj is None:
            raise KeyError(f"{model.__name__} with id={id_} isnot found.")
        return db_obj

    def get_read_shchema(
        self, db_object: Base, read_schema: Type[BaseModel]
    ) -> BaseModel:
        return read_schema(**db_object.__dict__)

    async def _update(self, db_object: Base, update_schema: BaseModel) -> Base:
        obj_data = db_object.__dict__
        schema_data = update_schema.dict(
            exclude={
                "id",
            }
        )
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

    async def _update_by(
        self, model: Type[Base], update_schema: Type[BaseModel]
    ) -> BaseModel:
        db_object = await self._get(model, update_schema.id)
        db_object = await self._update(db_object, update_schema)
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
        db_object: User = await self._update_by(User, upd_user)
        if upd_user.password is not None:
            db_object.hashed_pswd = secret_controller.hash_secret(upd_user.password)
        return self.get_read_shchema(db_object, ReadUser)

    async def get_user_schema(
        self, id_: Optional[int] = None, username: Optional[str] = None
    ) -> ReadUser:
        user_db = await self.get_user_obj(id_, username)
        return self.get_read_shchema(user_db, ReadUser)

    async def get_user_obj(
        self, id_: Optional[int] = None, username: Optional[str] = None
    ) -> User:
        if id_ is not None:
            user_db = await self._get(User, id_, [selectinload(User.user_role)])
        elif username is not None:
            user_db = await self.get_user_by_uname(username)
        else:
            raise KeyError("Needed one of arguments present")
        return user_db

    async def get_user_by_uname(self, username: str) -> User:
        stmt = (
            select(User)
            .where(User.username == username)
            .options(selectinload(User.user_role))
        )
        exec_result = await self._execute(stmt)
        db_user = exec_result.scalar()
        if not db_user:
            raise KeyError(f"User with that {username=} isn't found.")
        return db_user

    async def get_user_role(self, user_obj: User) -> BaseRolesEnum:
        role_obj = user_obj.user_role
        role = getattr(BaseRolesEnum, role_obj.code_name)
        return role

    async def get_user_role_by_schema(
        self, schema: ReadUser | UpdateUser
    ) -> BaseRolesEnum:
        user_obj = await self.get_user_obj(schema.id)
        role = await self.get_user_role(user_obj)
        return role