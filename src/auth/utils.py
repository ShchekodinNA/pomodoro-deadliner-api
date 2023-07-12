from typing import Optional
from sqlalchemy import select, exc
from sqlalchemy.orm import selectinload
from src.base_repo import IAsyncRepo
from .schemas import CreateUserOuter, ReadUser, UpdateUser
from .models import User
from .costants import secret_controller, BaseRolesEnum


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
        key_error_text = f"User with {username=} isn't found."
        try:
            stmt = (
                select(User)
                .where(User.username == username)
                .options(selectinload(User.user_role))
            )
        except exc.ArgumentError as excp:
            raise KeyError(key_error_text) from excp

        exec_result = await self._execute(stmt)
        db_user = exec_result.scalar()
        if not db_user:
            raise KeyError(key_error_text)
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
