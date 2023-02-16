from pydantic import BaseModel, PositiveInt


class MealBase(BaseModel):
    name: str
    calories: PositiveInt


class MealCreate(MealBase):
    pass


class MealWithDate(MealBase):
    day_id: int


class MealUpdate(MealBase):
    pass


class MealInDB(MealBase):
    id: int

    class Config:
        orm_mode = True


class Meal(MealInDB):
    pass
