from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Day(Base):
    id = Column(Integer, primary_key=True, index=True)
    date = Column(String(10), nullable=False)
    weight = Column(Float, nullable=False)
    meals = relationship(
        "Meal",
        cascade="all,delete-orphan",
        back_populates="day",
        uselist=True,
    )
    submitter_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    submitter = relationship("User", back_populates="date")
