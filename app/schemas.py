from pydantic import BaseModel

from typing import Sequence


class Meal(BaseModel):
    id: int
    name: str
    calories: int
    day_id: int


class DayMeal(BaseModel):
    day_id: int
    meals: Sequence[Meal]
    daily_calories: int


class MealSearchResults(BaseModel):
    results: Sequence[Meal]


class MealCreate(BaseModel):
    name: str
    calories: int
    day_id: int


# class Day(BaseModel):
#     day_id: int
#     date: str
#     weight: float
#     meals: list[Meal]
