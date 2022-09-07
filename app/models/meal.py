from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Meal(Base):
    pass
    # id=
    # name: "Яичница",
    # calories: 500,
    # day_id: 1,