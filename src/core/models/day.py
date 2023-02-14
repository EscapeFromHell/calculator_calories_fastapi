from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Day(Base):
    id = Column(Integer, primary_key=True, index=True)
    date = Column(String(10), nullable=False, unique=True)
    weight = Column(Float, nullable=False)
    meals = relationship(
        "Meal",
        cascade="all,delete-orphan",
        back_populates="day",
        uselist=True,
    )
    daily_calories = Column(Integer, nullable=True)
