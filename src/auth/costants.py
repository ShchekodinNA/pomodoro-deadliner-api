from enum import Enum
from pydantic import BaseSettings
from fastapi.security import OAuth2PasswordBearer
from .hash_controller import SecretController

TOKEN_TYPE = "Bearer"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth")


class SecurityEnv(BaseSettings):
    class Config:
        env_file = ".env"

    SECRET_JWT_KEY: str
    TOKEN_LIFETIME_IN_MINTUTES: int
    ENCRYPTING_ALGORITHM: str
    HASHING_SCHEME: str
    PEPER_SECRET: str


security_env = SecurityEnv()

secret_controller = SecretController(
    hashing_schema=security_env.HASHING_SCHEME,
    encypting_alg=security_env.ENCRYPTING_ALGORITHM,
    jwt_secret=security_env.SECRET_JWT_KEY,
    pepper_secret=security_env.PEPER_SECRET,
)


class BaseRolesEnum(Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPERVIZOR = "SUPERVIZOR"
