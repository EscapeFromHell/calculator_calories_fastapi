from fastapi import FastAPI, APIRouter, Query, HTTPException, Request, Depends

from typing import Optional, Any
from pathlib import Path
from sqlalchemy.orm import Session


from app.schemas.day import DayBase, DayMeal, DaySearchResults
from app.schemas.meal import MealBase, MealCreate, MealSearchResults
from app import deps
from app import crud


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


@api_router.get("/meal/{date}", status_code=200, response_model=DayMeal)
def fetch_day(*, date: str) -> Any:
    """
    Получение списка блюд и общего числа калорий за день.
    """
    result = [meal for meal in DAILY_CALORIES if meal["meal_date"] == date]
    if not result:
        raise HTTPException(
            status_code=404, detail=f"Day {date} not found"
        )
    calories_list = []
    for calorie in result:
        calories_list.append(calorie["calories"])
    daily_calories = sum(calories_list)
    results = {
        "date": date,
        "meals": list(result),
        "daily_calories": daily_calories
    }
    return results


@api_router.get(
    "/search/meal/", status_code=200,
    response_model=MealSearchResults
)
def search_meal(
    *,
    keyword: Optional[str] = Query(None, min_length=3, example="йогурт"),
    max_results: Optional[int] = 10
) -> Any:
    """
    Поиск блюда по ключевому слову.
    """
    if not keyword:
        return {"results": DAILY_CALORIES[:max_results]}

    results = filter(
        lambda meal: keyword.lower() in meal["name"].lower(), DAILY_CALORIES
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
    max_results: Optional[int] = 10
) -> Any:
    """
    Поиск дней.
    """
    if not date:
        return {"results": DAYS[:max_results]}

    results = filter(lambda meal: date in meal["date"], DAYS)
    return {"results": list(results)[:max_results]}


@api_router.post("/meal/", status_code=201, response_model=MealBase)
def create_meal(*, meal_in: MealCreate) -> dict:
    """
    Добавление блюда. (in memory only)
    """
    meal_entry = MealBase(
        name=meal_in.name,
        calories=meal_in.calories,
        meal_date=meal_in.meal_date,
    )
    DAILY_CALORIES.append(meal_entry.dict())
    return meal_entry


@api_router.post("/day/", status_code=201, response_model=DayBase)
def create_day(*, day_in: DayBase) -> dict:
    """
    Добавление дня. (in memory only)
    """
    day_entry = DayBase(
        date=day_in.date,
        weight=day_in.weight
    )
    DAYS.append(day_entry)
    return day_entry


app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
