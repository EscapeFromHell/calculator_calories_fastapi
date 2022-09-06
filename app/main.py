from fastapi import FastAPI, APIRouter

from typing import Optional


DAILY_CALORIES = [
    {
        "id": 1,
        "name": "Яичница",
        "ccal": 500,
        "day_id": 1,
    },
    {
        "id": 2,
        "name": "Сок",
        "ccal": 200,
        "day_id": 1,
    },
    {
        "id": 3,
        "name": "Куриная грудка и гречка",
        "ccal": 400,
        "day_id": 1,
    },
    {
        "id": 1,
        "name": "Йогурт",
        "ccal": 150,
        "day_id": 2,
    },
]


app = FastAPI(title="Calories Calculator API", openapi_url="/openapi.json")

api_router = APIRouter()


# Сделать вывод статистики текущего дня.
@api_router.get("/", status_code=200)
def root() -> dict:
    """
    Root GET
    """
    return {"Скоро тут будет": "Калькулятор калорий"}


@api_router.get("/calories/{day_id}", status_code=200)
def fetch_day(*, day_id: int) -> dict:
    """
    Получение списка блюд и общего числа калорий за день.
    """

    result = [
        calorie for calorie in DAILY_CALORIES if calorie["day_id"] == day_id
    ]
    if result:
        ccal_result = []
        for calorie in result:
            ccal_result.append(calorie["ccal"])
        result.append({"Калорий за день": sum(ccal_result)})
        return {f"День № {day_id}": result}


@api_router.get("/search/meal/", status_code=200)
def search_meal(
    keyword: Optional[str] = None, max_results: Optional[int] = 10
) -> dict:
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


app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
