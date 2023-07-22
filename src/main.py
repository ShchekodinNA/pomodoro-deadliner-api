from fastapi import FastAPI, APIRouter
from src.auth.router import auth_router
from src.task import tag_router, task_router
from src.pomodoro.router import pomodoro_router

app = FastAPI()
api_router = APIRouter(prefix="/api")
# submodules{
## api_router.include(...)
routers_to_include = [auth_router,tag_router, task_router, pomodoro_router]
# }
for router in routers_to_include:
    api_router.include_router(router)
app.include_router(api_router)
