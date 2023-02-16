from fastapi import APIRouter

from src.api.api_v1.endpoints import router_day, router_meal

api_router = APIRouter()
api_router.include_router(router_day, prefix="/days", tags=["days"])
api_router.include_router(router_meal, prefix="/meals", tags=["meals"])
