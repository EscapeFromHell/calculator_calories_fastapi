from typing import Optional

from pydantic import schema
from sqlalchemy.orm import Session

from src.core.crud import CRUDBase
from src.core.models import Day
from src.core.schemas import DayCreate, DayUpdate


class CRUDDay(CRUDBase[Day, DayCreate, DayUpdate]):
    def get_day(self, db: Session, date: schema.date) -> Optional[Day]:
        """Возвращает день."""
        return db.query(self.model).filter(self.model.date == date).first()


crud_day = CRUDDay(Day)
