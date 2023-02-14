from typing import Optional

from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.crud.crud_meal import meal as meal_crud
from app.schemas.meal import Meal, MealCreate, MealSearchResults


router = APIRouter()


@router.get("/search/", status_code=200, response_model=MealSearchResults)
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


@router.post("/", status_code=201, response_model=Meal)
def create_meal(
    *, meal_in: MealCreate, db: Session = Depends(deps.get_db)
) -> dict:
    """
    Добавление блюда.
    """
    meal = meal_crud.create(db=db, obj_in=meal_in)

    return meal
