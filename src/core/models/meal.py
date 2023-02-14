from sqlalchemy import Column, Integer, String

from src.core.models import Base


class Meal(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    calories = Column(Integer, nullable=False)
