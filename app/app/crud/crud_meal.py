from app.crud.base import CRUDBase
from app.models.meal import Meal
from app.schemas.meal import MealCreate, MealUpdate


class CRUDMeal(CRUDBase[Meal, MealCreate, MealUpdate]):
    ...


meal = CRUDMeal(Meal)
