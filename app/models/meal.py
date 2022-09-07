from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Meal(Base):
    name = Column(String(256), nullable=False)
    calories = Column(Integer, nullable=False)
    meal_date = Column(String(10), ForeignKey("day.date"), nullable=False)
    day = relationship("Day", back_populates="meals")
