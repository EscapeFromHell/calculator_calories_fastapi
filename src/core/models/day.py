from sqlalchemy import Column, Date, Float, Integer

from src.core.models import Base


class Day(Base):
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, unique=True)
    weight = Column(Float, nullable=False)
