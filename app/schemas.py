from pydantic import BaseModel

from typing import Sequence


class Meal(BaseModel):
    id: int
    name: str
    ccal: int


# class Day(BaseModel):
#     day_id: int
#     date: str
#     weight: float
#     meals: list[Meal]


class MealSearchResults(BaseModel):
    results: Sequence[Meal]


class MealCreate(BaseModel):
    name: str
    ccal: int
    day_id: int
