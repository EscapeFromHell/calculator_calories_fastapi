from pydantic import BaseModel

from typing import Sequence


class Meal(BaseModel):
    name: str
    calories: int


class DayMeal(BaseModel):
    date: str
    meals: Sequence[Meal]
    daily_calories: int


class MealSearchResults(BaseModel):
    results: Sequence[Meal]


class MealCreate(BaseModel):
    name: str
    calories: int
    meal_date: str


class Day(BaseModel):
    date: str
    weight: float


class DaySearchResults(BaseModel):
    results: Sequence[Day]
