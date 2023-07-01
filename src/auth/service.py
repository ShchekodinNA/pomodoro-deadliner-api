from .utils import AuthenticateRepo
from .models import User
from .exceptions import NotAuthenticated
from .costants import secret_controller, TOKEN_TYPE
from .hash_controller import JWTBody, AuthenticationToken
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
