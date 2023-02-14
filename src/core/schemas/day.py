import datetime

from pydantic import BaseModel
from pydantic import schema, PositiveInt, PositiveFloat

from typing import Sequence

from src.core.schemas import MealBase


class DayBase(BaseModel):
    date: schema.date = datetime.date.today()
    weight: PositiveFloat


class DayCreate(DayBase):
    pass


class DayUpdate(DayBase):
    pass


class DayInDB(DayBase):
    id: int

    class Config:
        orm_mode = True


class Day(DayInDB):
    meals: Sequence[MealBase]
    calories_sum: PositiveInt
