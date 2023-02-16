import datetime
from typing import Sequence

from pydantic import BaseModel, PositiveFloat, schema

from src.core.schemas.meal import Meal


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
    meals: Sequence[Meal]
    calories_sum: int
