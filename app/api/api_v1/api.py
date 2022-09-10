from fastapi import APIRouter

from app.api.api_v1.endpoints import day, meal


api_router = APIRouter()
api_router.include_router(day.router, prefix="/days", tags=["days"])
api_router.include_router(meal.router, prefix="/meals", tags=["meals"])
