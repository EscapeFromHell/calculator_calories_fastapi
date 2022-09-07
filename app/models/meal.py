from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Meal(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    calories = Column(Integer, nullable=False)
    meal_date = Column(String(10), ForeignKey("day.date"), nullable=False)
    day = relationship("Day", back_populates="meals")
