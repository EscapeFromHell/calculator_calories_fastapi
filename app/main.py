from pathlib import Path

from fastapi import FastAPI, APIRouter  # Request, Depends
# from fastapi.templating import Jinja2Templates
# from sqlalchemy.orm import Session

# from app import crud
# from app.api import deps
from app.api.api_v1.api import api_router
from app.core.config import settings


# ROOT = Path(__file__).resolve().parent.parent
BASE_PATH = Path(__file__).resolve().parent
# TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))

root_router = APIRouter()
app = FastAPI(title="Calories Calculator API")


# Сделать вывод статистики текущего дня. *Jinja **Optional
@root_router.get("/", status_code=200)
def root() -> dict:
    """
    Root GET
    """
    return {"Скоро тут будет": "Калькулятор калорий"}


app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
