from fastapi import FastAPI, APIRouter, Query, HTTPException, Depends

from typing import Optional, Any
from pathlib import Path
from sqlalchemy.orm import Session

from app import deps
from app.schemas.day import Day, DayCreate, DayMeal, DaySearchResults
from app.schemas.meal import Meal, MealCreate, MealSearchResults
from app.crud.crud_day import day as day_crud
from app.crud.crud_meal import meal as meal_crud


ROOT = Path(__file__).resolve().parent.parent
BASE_PATH = Path(__file__).resolve().parent


app = FastAPI(title="Calories Calculator API", openapi_url="/openapi.json")

api_router = APIRouter()


# Сделать вывод статистики текущего дня. *Jinja **Optional
@api_router.get("/", status_code=200)
def root() -> dict:
    """
    Root GET
    """
    return {"Скоро тут будет": "Калькулятор калорий"}


@api_router.get("/meal/{day_id}", status_code=200, response_model=DayMeal)
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


@api_router.get(
    "/search/meal/", status_code=200,
    response_model=MealSearchResults
)
def search_meal(
    *,
    keyword: Optional[str] = Query(None, min_length=3, example="йогурт"),
    max_results: Optional[int] = 10,
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Поиск блюда по ключевому слову.
    """
    meals = meal_crud.get_multi(db=db, limit=max_results)
    if not keyword:
        return {"results": meals}

    results = filter(
        lambda meal: keyword.lower() in meal.name.lower(), meals
    )
    return {"results": list(results)[:max_results]}


# Настроить диапазон поиска. **Optional
@api_router.get(
    "/search/day/", status_code=200,
    response_model=DaySearchResults
)
def search_day(
    *,
    date: Optional[str] = Query(None, min_length=3, example="07.09.2022"),
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


@api_router.post("/meal/", status_code=201, response_model=Meal)
def create_meal(
    *, meal_in: MealCreate, db: Session = Depends(deps.get_db)
) -> dict:
    """
    Добавление блюда.
    """
    meal = meal_crud.create(db=db, obj_in=meal_in)

    return meal


@api_router.post("/day/", status_code=201, response_model=Day)
def create_day(
    *, day_in: DayCreate, db: Session = Depends(deps.get_db)
) -> dict:
    """
    Добавление дня.
    """
    day = day_crud.create(db=db, obj_in=day_in)

    return day


app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
