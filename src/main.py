from fastapi import FastAPI, APIRouter
from src.auth.router import auth_router

app = FastAPI()
api_router = APIRouter(prefix="/api")
# submodules{
## api_router.include(...)
api_router.include_router(auth_router)
# }
app.include_router(api_router)
