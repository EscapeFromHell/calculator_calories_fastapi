import datetime
from typing import Optional, Sequence

from fastapi import APIRouter, Depends, Query
from pydantic import schema

from src.core.repository import DayMealRepository
from src.core.schemas import Meal, MealCreate, MealUpdate
from src.deps import day_meal_repo as deps_day_meal_repo

router = APIRouter()


@router.get("/", status_code=200, response_model=Sequence[Meal])
def search_meal(
    *,
    keyword: Optional[str] = Query(None, min_length=3, example="йогурт"),
    max_results: Optional[int] = 10,
    day_meal_repo: DayMealRepository = Depends(deps_day_meal_repo)
) -> Sequence[Meal]:
    """Поиск блюда по ключевому слову."""
    return day_meal_repo.search_meal(keyword=keyword, max_results=max_results)


@router.post("/", status_code=201, response_model=MealCreate)
def create_meal(
    *,
    date: schema.date = datetime.date.today(),
    new_meal: MealCreate,
    day_meal_repo: DayMealRepository = Depends(deps_day_meal_repo)
) -> MealCreate:
    """Добавление блюда."""
    return day_meal_repo.create_meal(date=date, new_meal=new_meal)


@router.patch("/", status_code=201, response_model=MealUpdate)
def update_day(
    *, id: int, update_meal: MealUpdate, day_meal_repo: DayMealRepository = Depends(deps_day_meal_repo)
) -> MealUpdate:
    """Изменение блюда."""
    return day_meal_repo.update_meal(id=id, update_meal=update_meal)
