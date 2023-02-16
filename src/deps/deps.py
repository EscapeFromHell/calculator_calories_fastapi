from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from src.core.db.session import SessionLocal
from src.core.repository import DayMealRepository


def get_db() -> Generator:
    with SessionLocal() as db:
        yield db


def day_meal_repo(db: Session = Depends(get_db, use_cache=True)) -> DayMealRepository:
    """DI для репозитория DayMealRepository."""
    return DayMealRepository(db)
