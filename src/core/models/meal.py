from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.core.models import Base


class Meal(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    calories = Column(Integer, nullable=False)
    day = relationship("Day", back_populates="meals")
    day_id = Column(Integer, ForeignKey("day.id"), nullable=True)
