import asyncio
from typing import Optional

import httpx
from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.crud.crud_meal import meal as meal_crud
from app.schemas.meal import Meal, MealCreate, MealSearchResults


router = APIRouter()
RECIPE_SUBREDDITS = ["recipes", "easyrecipes", "TopSecretRecipes"]


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


async def get_reddit_top_async(subreddit: str) -> list:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://www.reddit.com/r/{subreddit}/top.json?sort=top&t=day&limit=5",
            headers={"User-agent": "meal bot 0.1"},
        )

    subreddit_recipes = response.json()
    subreddit_data = []
    for entry in subreddit_recipes["data"]["children"]:
        score = entry["data"]["score"]
        title = entry["data"]["title"]
        link = entry["data"]["url"]
        subreddit_data.append(f"{str(score)}: {title} ({link})")
    return subreddit_data


@router.get("/ideas/async")
async def fetch_ideas_async() -> dict:
    results = await asyncio.gather(
        *[get_reddit_top_async(subreddit=subreddit) for subreddit in RECIPE_SUBREDDITS]
    )
    return dict(zip(RECIPE_SUBREDDITS, results))
