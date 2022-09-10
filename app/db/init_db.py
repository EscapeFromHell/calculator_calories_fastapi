import logging
from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud.crud_user import user as us
from app.db import base  # noqa: F401
from app.schemas.user import UserCreate


logger = logging.getLogger(__name__)


# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    if settings.FIRST_SUPERUSER:
        user = us.get_by_email(db, email=settings.FIRST_SUPERUSER)
        if not user:
            user_in = UserCreate(
                full_name="Initial Super User",
                email=settings.FIRST_SUPERUSER,
                is_superuser=True,
            )
            user = us.create(db, obj_in=user_in)  # noqa: F841
        else:
            logger.warning(
                "Skipping creating superuser. User with email "
                f"{settings.FIRST_SUPERUSER} already exists. "
            )
    else:
        logger.warning(
            "Skipping creating superuser.  FIRST_SUPERUSER needs to be "
            "provided as an env variable. "
            "e.g.  FIRST_SUPERUSER=admin@api.coursemaker.io"
        )
