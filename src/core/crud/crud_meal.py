from src.core.crud import CRUDBase
from src.core.models import Meal
from src.core.schemas import MealCreate, MealUpdate


class CRUDMeal(CRUDBase[Meal, MealCreate, MealUpdate]):
    ...


crud_meal = CRUDMeal(Meal)
