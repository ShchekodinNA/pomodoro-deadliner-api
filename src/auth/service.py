from typing import List
from .utils import AuthenticateRepo
from .models import User
from .exceptions import NotAuthenticated
from .costants import secret_controller, TOKEN_TYPE, BaseRolesEnum
from .hash_controller import JWTBody, AuthenticationToken
from .schemas import ReadUserInner
from datetime import timedelta


class Authenticator:
    def __init__(self, repo: AuthenticateRepo) -> None:
        self.__repo = repo

    @property
    def repo(self):
        return self.__repo

    async def authenticate_user(
        self,
        username: str,
        password: str,
        expires_delta: timedelta = timedelta(minutes=15),
    ) -> AuthenticationToken:
        db_user = await self.repo.get_user_by_uname(username)
        hashed_pswd = db_user.hashed_pswd

        if not secret_controller.is_secret_correct(hashed_pswd, password):
            raise NotAuthenticated("Username or password isn't correct")

        auth_token = secret_controller.generate_jwt_token(
            JWTBody(sub=username), expires_delta
        )
        return AuthenticationToken(access_token=auth_token, token_type=TOKEN_TYPE)


class Authorizator:
    @classmethod
    def is_admin(cls, role: BaseRolesEnum) -> bool:
        if role == BaseRolesEnum.ADMIN:
            return True
        return False

    @classmethod
    def is_supervizor(cls, ole: BaseRolesEnum) -> bool:
        if role == BaseRolesEnum.SUPERVIZOR:
            return True
        return False

    @classmethod
    def is_user_element(cls, cur_user_id: int, object_id: int) -> bool:
        if cur_user_id == object_id:
            return True
        return False

    @classmethod
    def is_in_roles(cls, role: BaseRolesEnum, check_roles: List[BaseRolesEnum]) -> True:
        if role in check_roles:
            return True
        return False

    @classmethod
    def can_control(cls, user: ReadUserInner, user_id_in_obj: int) -> bool:
        if cls.is_admin(user.role) or user.id == user_id_in_obj:
            return True
        return False

    @classmethod
    def can_read(cls, user: ReadUserInner, user_id_in_obj: int) -> bool:
        if (
            cls.is_in_roles(user.role, [BaseRolesEnum.ADMIN, BaseRolesEnum.SUPERVIZOR])
            or user.id == user_id_in_obj
        ):
            return True
        return False
