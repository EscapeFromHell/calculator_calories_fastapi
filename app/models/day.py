from sqlalchemy import Column, Float, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Day(Base):
    date: Column(String(10), nullable=False)
    weight: Column(Float, nullable=False)
    meals = relationship(
        "Meal",
        cascade="all,delete-orphan",
        back_populates="day",
        uselist=True,
    )
