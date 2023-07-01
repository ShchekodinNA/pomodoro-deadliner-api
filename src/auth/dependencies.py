from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from src.dependencies import dep_get_async_db_session
from .utils import AuthenticateRepo
from .costants import security_env, oauth2_scheme
from .schemas import ReadUser

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_repo(
    session: AsyncSession = Depends(dep_get_async_db_session),
) -> AuthenticateRepo:
    yield AuthenticateRepo(session)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    repo: AuthenticateRepo = Depends(get_repo),
) -> ReadUser:
    try:
        payload = jwt.decode(
            token,
            security_env.SECRET_JWT_KEY,
            algorithms=[security_env.ENCRYPTING_ALGORITHM],
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc
    current_user = await repo.get_user(username=username)
    return current_user


async def get_cur_user_if_active(
    user: ReadUser = Depends(get_current_user),
) -> ReadUser:
    if user.is_active is True:
        return user
    raise credentials_exception
