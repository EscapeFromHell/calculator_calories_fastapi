from sqlalchemy import Column, Date, Float, Integer
from sqlalchemy.orm import relationship

from src.core.models import Base


class Day(Base):
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, unique=True)
    weight = Column(Float, nullable=False)
    meals = relationship(
        "Meal",
        cascade="all,delete-orphan",
        back_populates="day",
        uselist=True,
    )
