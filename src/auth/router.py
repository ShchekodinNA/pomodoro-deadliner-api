from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, delete
from src.database import AsyncSession
from src.dependencies import dep_get_async_db_session
from .models import User
from .dependencies import get_repo, get_cur_user_if_active
from .schemas import CreateUserOuter, UpdateUser, ReadUser
from .utils import AuthenticateRepo
from .service import Authenticator, AuthenticationToken
from .exceptions import NotAuthenticated
from .costants import BaseRolesEnum
from sqlalchemy import select

auth_router = APIRouter(prefix="/auth", tags=["AUTHORIZATION"])


@auth_router.post("", response_model=AuthenticationToken)
async def authenticate(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(dep_get_async_db_session),
):
    async_auth_repo = AuthenticateRepo(session)
    authenticator = Authenticator(async_auth_repo)
    try:
        token = await authenticator.authenticate_user(
            form_data.username, form_data.password
        )
    except KeyError as er:
        raise HTTPException(404, er.args)
    except NotAuthenticated as er:
        raise HTTPException(401, er.args)
    return token


@auth_router.post("/users")
async def register_user(
    new_user: CreateUserOuter, repo: AuthenticateRepo = Depends(get_repo)
):
    return await repo.create_user(new_user)


@auth_router.delete("/users/{user_id}")
async def delete_user(
    user_id: int, 
    repo: AuthenticateRepo = Depends(get_repo),
    cur_user: ReadUser = Depends(get_cur_user_if_active)
    ):
    role = await repo.get_user_role_by_schema(cur_user)
    if (
        role == BaseRolesEnum.ADMIN
        or role == BaseRolesEnum.SUPERVIZOR
        or user_id == cur_user.id
    ):
        return await repo.delete_user(user_id)
    raise HTTPException(401)

@auth_router.put("/users/{user_id}")
async def update_user(
    upd_schema: UpdateUser,
    repo: AuthenticateRepo = Depends(get_repo),
    cur_user: ReadUser = Depends(get_cur_user_if_active),
):
    role = await repo.get_user_role_by_schema(cur_user)
    if (
        role == BaseRolesEnum.ADMIN
        or role == BaseRolesEnum.SUPERVIZOR
        or upd_schema.id == cur_user.id
    ):
        return await repo.update_user(upd_schema)
    raise HTTPException(401)
