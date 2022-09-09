from pydantic import BaseModel

from typing import Sequence


class MealBase(BaseModel):
    name: str
    calories: int


class MealCreate(MealBase):
    name: str
    calories: int
    day_id: int
    # meal_date: str


class MealUpdate(MealBase):
    name: str
    calories: int


class MealInDBBase(MealBase):
    id: int
    day_id: int
    # meal_date: str

    class Config:
        orm_mode = True


class Meal(MealInDBBase):
    name: str
    calories: int


class MealInDB(MealInDBBase):
    pass


class MealSearchResults(BaseModel):
    results: Sequence[Meal]
