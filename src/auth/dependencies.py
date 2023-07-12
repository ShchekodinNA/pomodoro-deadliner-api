from typing import Annotated, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from src.dependencies import dep_get_async_db_session
from .utils import AuthenticateRepo
from .costants import security_env, oauth2_scheme
from .schemas import ReadUserInner, ReadUser

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
) -> ReadUserInner:
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
    current_user = await repo.get_user_obj(username=username)
    r_schema: ReadUser = repo.get_read_shchema(current_user, ReadUser)
    role = await repo.get_user_role(current_user)
    out_schema = ReadUserInner(
        id=r_schema.id,
        username=r_schema.username,
        email=r_schema.email,
        is_active=r_schema.is_active,
        user_role_id=r_schema.user_role_id,
        role=role,
    )
    return out_schema


async def get_cur_user_if_active(
    user: ReadUserInner = Depends(get_current_user),
) -> ReadUserInner:
    if user.is_active is True:
        return user
    raise credentials_exception


DepCurUser = Annotated[ReadUserInner, Depends(get_current_user)]
DepActiveCurUser = Annotated[ReadUserInner, Depends(get_cur_user_if_active)]
