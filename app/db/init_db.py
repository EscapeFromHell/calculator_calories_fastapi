import logging
from sqlalchemy.orm import Session

from app.crud.crud_user import user as us
from app.crud.crud_meal import meal as ml
from app.crud.crud_day import day as d
from app.schemas.user import UserCreate
from app.schemas.day import DayCreate
from app.schemas.meal import MealCreate
from app.db import base  # noqa: F401
from app.db_data import DAYS, MEALS


logger = logging.getLogger(__name__)

FIRST_SUPERUSER = "admin@mealapi.com"

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    if FIRST_SUPERUSER:
        user = us.get_by_email(db, email=FIRST_SUPERUSER)
        if not user:
            user_in = UserCreate(
                full_name="Initial Super User",
                email=FIRST_SUPERUSER,
                is_superuser=True,
            )
            user = us.create(db, obj_in=user_in)  # noqa: F841
        else:
            logger.warning(
                "Skipping creating superuser. User with email "
                f"{FIRST_SUPERUSER} already exists. "
            )
        if not user.date:
            for day in DAYS:
                day_in = DayCreate(
                    date=day["date"],
                    weight=day["weight"],
                    submitter_id=user.id,
                )
                d.create(db, obj_in=day_in)
            for meal in MEALS:
                meal_in = MealCreate(
                    name=meal["name"],
                    calories=meal["calories"],
                    meal_date=meal["meal_date"],
                )
                ml.create(db, obj_in=meal_in)
    else:
        logger.warning(
            "Skipping creating superuser.  FIRST_SUPERUSER needs to be "
            "provided as an env variable. "
            "e.g.  FIRST_SUPERUSER=admin@api.coursemaker.io"
        )
