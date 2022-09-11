from app.crud.base import CRUDBase
from app.models.day import Day
from app.schemas.day import DayCreate, DayUpdate


class CRUDDay(CRUDBase[Day, DayCreate, DayUpdate]):
    ...


day = CRUDDay(Day)
