from fastapi import FastAPI, APIRouter, Query, HTTPException

from typing import Optional, Any

from app.schemas import DayMeal, Meal, MealCreate, MealSearchResults


DAILY_CALORIES = [
    {
        "id": 1,
        "name": "Яичница",
        "calories": 500,
        "day_id": 1,
    },
    {
        "id": 2,
        "name": "Сок",
        "calories": 200,
        "day_id": 1,
    },
    {
        "id": 3,
        "name": "Куриная грудка и гречка",
        "calories": 400,
        "day_id": 1,
    },
    {
        "id": 4,
        "name": "Йогурт",
        "calories": 150,
        "day_id": 1,
    },
]


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
def fetch_day(*, day_id: int) -> Any:
    """
    Получение списка блюд и общего числа калорий за день.
    """

    result = [meal for meal in DAILY_CALORIES if meal["day_id"] == day_id]
    if not result:
        raise HTTPException(
            status_code=404, detail=f"Day with ID {day_id} not found"
        )
    calories_list = []
    for calorie in result:
        calories_list.append(calorie["calories"])
    daily_calories = sum(calories_list)
    results = {
        "day_id": day_id,
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


# Написать функцию для поиска day_id по дате.
@api_router.get("/search/day/", status_code=200)
def search_day():
    pass


@api_router.post("/meal/", status_code=201, response_model=Meal)
def create_meal(*, meal_in: MealCreate) -> dict:
    """
    Добавление блюда. (in memory only)
    """
    new_entry_id = len(DAILY_CALORIES) + 1
    meal_entry = Meal(
        id=new_entry_id,
        name=meal_in.name,
        calories=meal_in.calories,
        day_id=meal_in.day_id,
    )
    DAILY_CALORIES.append(meal_entry.dict())
    return meal_entry


app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
