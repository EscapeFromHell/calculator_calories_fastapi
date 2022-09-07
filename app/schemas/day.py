from pydantic import BaseModel

from typing import Optional, Sequence

from app.schemas.meal import Meal


class DayBase(BaseModel):
    date: str
    weight: float


class DayMeal(DayBase):
    date: str
    meals: Sequence[Meal]
    daily_calories: int


class DayInDBBase(DayBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class Day(DayInDBBase):
    pass


class DaySearchResults(BaseModel):
    results: Sequence[Day]
