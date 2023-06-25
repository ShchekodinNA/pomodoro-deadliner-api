from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, delete
from src.database import AsyncSession
from src.dependencies import dep_get_async_db_session
from .models import User
from .dependencies import get_repo
from .schemas import CreateUserOuter, UpdateUser
from .utils import AuthenticateRepo

from sqlalchemy import select

auth_router = APIRouter(prefix="/auth", tags=["AUTHORIZATION"])
# @auth_router.post("")
# def authenticate(
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     session: AsyncSession = Depends(dep_get_async_db_session),
# ):
#     pass


@auth_router.post("/users")
async def register_user(
    new_user: CreateUserOuter, repo: AuthenticateRepo = Depends(get_repo)
):
    return await repo.create_user(new_user)

@auth_router.delete('/users/{user_id}')
async def delete_user(
    user_id: int, repo: AuthenticateRepo = Depends(get_repo)
):
    return await repo.delete_user(user_id)

@auth_router.put('/users/{user_id}')
async def update_user(
    upd_schema: UpdateUser, repo: AuthenticateRepo = Depends(get_repo)
):
    return await repo.update_user(upd_schema)