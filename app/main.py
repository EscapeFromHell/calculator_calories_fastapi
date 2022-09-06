from fastapi import FastAPI, APIRouter


DAILY_CALORIES = [
    {
        "id": 1,
        "meal": "Яичница",
        "ccal": 500,
        "day_id": 1,
    },
    {
        "id": 2,
        "meal": "Сок",
        "ccal": 200,
        "day_id": 1,
    },
    {
        "id": 3,
        "meal": "Куриная грудка и гречка",
        "ccal": 400,
        "day_id": 1,
    },
]


app = FastAPI(title="Calories Calculator API", openapi_url="/openapi.json")

api_router = APIRouter()


@api_router.get("/", status_code=200)
def root() -> dict:
    """
    Root GET
    """
    return {"Скоро тут будет": "Калькулятор калорий"}


@api_router.get("/calories/{day_id}", status_code=200)
def fetch_day(*, day_id: int) -> dict:
    """
    Get a list of meal and caloriesby Day ID
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


app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
