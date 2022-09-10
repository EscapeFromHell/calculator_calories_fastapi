import datetime as dt
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.schemas.day import Day, DayCreate, DayMeal, DaySearchResults
from app.crud.crud_day import day as day_crud


TODAY = dt.datetime.today().strftime("%d.%m.%Y")


router = APIRouter()


@router.get("/{day_id}", status_code=200, response_model=DayMeal)
def fetch_day(*, day_id: int, db: Session = Depends(deps.get_db),) -> Any:
    """
    Получение списка блюд и общего числа калорий за день.
    """
    day = day_crud.get(db=db, id=day_id)
    if not day:
        raise HTTPException(
            status_code=404, detail=f"Day with ID {day_id} not found"
        )
    meals = day.meals
    calories_list = []
    for meal in meals:
        calories_list.append(meal.calories)
    daily_calories = sum(calories_list)
    day.daily_calories = daily_calories

    return day


@router.get("/search/", status_code=200, response_model=DaySearchResults)
def search_day(
    *,
    date: Optional[str] = Query(None, min_length=3, example=f"{TODAY}"),
    max_results: Optional[int] = 10,
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Поиск дней.
    """
    days = day_crud.get_multi(db=db, limit=max_results)
    if not date:
        return {"results": days}

    results = filter(
        lambda day: date in day.date, days
    )
    return {"results": list(results)[:max_results]}


@router.post("/", status_code=201, response_model=Day)
def create_day(
    *, day_in: DayCreate, db: Session = Depends(deps.get_db)
) -> dict:
    """
    Добавление дня.
    """
    day = day_crud.create(db=db, obj_in=day_in)

    return day
