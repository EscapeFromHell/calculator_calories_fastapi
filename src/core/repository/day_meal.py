from typing import Optional, Sequence

from fastapi import Query
from fastapi.exceptions import HTTPException
from pydantic import schema

from src.core.crud import crud_day, crud_meal
from src.core.repository.repository import Repository
from src.core.schemas import Day, DayCreate, DayUpdate, Meal, MealCreate, MealUpdate, MealWithDate


class DayMealRepository(Repository):
    def get_day(self, date: schema.date) -> Day:
        """Получение списка блюд и общего числа калорий за день."""
        day = crud_day.get_day(db=self.db, date=date)
        if not day:
            raise HTTPException(status_code=404, detail=f"Day {date} not found")
        calories_sum = sum([meal.calories for meal in day.meals])
        return Day(id=day.id, date=day.date, weight=day.weight, meals=day.meals, calories_sum=calories_sum)

    def create_day(self, new_day: DayCreate) -> DayCreate:
        """Добавление нового дня."""
        day_in_db = crud_day.get_day(db=self.db, date=new_day.date)
        if day_in_db:
            raise HTTPException(status_code=400, detail=f"Day {new_day.date} already exist")
        day = crud_day.create(db=self.db, obj_in=new_day)
        return DayCreate(date=day.date, weight=day.weight)

    def update_day(self, update_day: DayUpdate) -> DayUpdate:
        """Изменение дня."""
        day_in_db = crud_day.get_day(db=self.db, date=update_day.date)
        if not day_in_db:
            raise HTTPException(status_code=404, detail=f"Day {update_day.date} not found")
        day = crud_day.update(db=self.db, db_obj=day_in_db, obj_in=update_day)
        return DayUpdate(date=day.date, weight=day.weight)

    def search_meal(
        self, keyword: Optional[str] = Query(None, min_length=3, example="йогурт"), max_results: Optional[int] = 10
    ) -> Sequence[Meal]:
        """Поиск блюда по ключевому слову."""
        meals = crud_meal.get_multi(db=self.db)
        if not keyword:
            return meals
        search_result = list(filter(lambda meal: keyword.lower() in meal.name.lower(), meals))[:max_results]
        if not search_result:
            raise HTTPException(status_code=404, detail="Meal not found")
        return search_result

    def create_meal(self, date: schema.date, new_meal: MealCreate) -> MealCreate:
        """Добавление блюда."""
        day = crud_day.get_day(db=self.db, date=date)
        meal = crud_meal.create(
            db=self.db, obj_in=MealWithDate(name=new_meal.name, calories=new_meal.calories, day_id=day.id)
        )
        return MealCreate(name=meal.name, calories=meal.calories)

    def update_meal(self, id: int, update_meal: MealUpdate) -> MealUpdate:
        """Изменение блюда."""
        meal_in_db = crud_meal.get(db=self.db, id=id)
        if not meal_in_db:
            raise HTTPException(status_code=404, detail=f"Meal with ID: {id} not found")
        meal = crud_meal.update(db=self.db, db_obj=meal_in_db, obj_in=update_meal)
        return MealUpdate(name=meal.name, calories=meal.calories)
