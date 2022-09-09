from pydantic import BaseModel

from typing import Sequence

from app.schemas.meal import Meal


class DayBase(BaseModel):
    date: str


class DayCreate(DayBase):
    date: str
    weight: float


class DayUpdate(DayBase):
    date: str
    weight: float


class DayInDBBase(DayBase):
    id: int
    weight: float

    class Config:
        orm_mode = True


class Day(DayInDBBase):
    pass


class DayMeal(Day):
    meals: Sequence[Meal]
    daily_calories: int


class DaySearchResults(BaseModel):
    results: Sequence[Day]
