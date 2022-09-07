from pydantic import BaseModel

from typing import Sequence


class MealBase(BaseModel):
    name: str
    calories: int


class MealCreate(MealBase):
    name: str
    calories: int
    meal_date: str


class RecipeUpdate(MealBase):
    name: str
    calories: int


class MealInDBBase(MealBase):
    id: int
    meal_date: str

    class Config:
        orm_mode = True


class Meal(MealInDBBase):
    pass


class MealInDB(MealInDBBase):
    pass


class MealSearchResults(BaseModel):
    results: Sequence[Meal]
