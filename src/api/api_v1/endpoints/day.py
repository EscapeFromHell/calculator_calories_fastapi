import datetime

from fastapi import APIRouter, Depends
from pydantic import schema

from src.core.repository import DayMealRepository
from src.core.schemas import Day, DayCreate, DayUpdate
from src.deps import day_meal_repo as deps_day_meal_repo

router = APIRouter()


@router.get("/", status_code=200, response_model=Day)
def get_day(
    *, date: schema.date = datetime.date.today(), day_meal_repo: DayMealRepository = Depends(deps_day_meal_repo)
) -> Day:
    """Получение списка блюд и общего числа калорий за день."""
    return day_meal_repo.get_day(date=date)


@router.post("/", status_code=201, response_model=DayCreate)
def create_day(*, new_day: DayCreate, day_meal_repo: DayMealRepository = Depends(deps_day_meal_repo)) -> DayCreate:
    """Добавление нового дня."""
    return day_meal_repo.create_day(new_day=new_day)


@router.patch("/", status_code=201, response_model=DayUpdate)
def update_day(*, update_day: DayUpdate, day_meal_repo: DayMealRepository = Depends(deps_day_meal_repo)) -> DayUpdate:
    """Изменение дня."""
    return day_meal_repo.update_day(update_day=update_day)
