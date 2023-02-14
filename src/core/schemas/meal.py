from pydantic import BaseModel
from pydantic import PositiveInt


class MealBase(BaseModel):
    name: str
    calories: PositiveInt


class MealCreate(MealBase):
    pass


class MealUpdate(MealBase):
    pass


class MealInDBBase(MealBase):
    id: int

    class Config:
        orm_mode = True
