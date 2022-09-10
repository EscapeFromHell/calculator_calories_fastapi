import time
from pathlib import Path

from fastapi import FastAPI, APIRouter, Request

from app.api.api_v1.api import api_router
from app.core.config import settings


BASE_PATH = Path(__file__).resolve().parent


root_router = APIRouter()
app = FastAPI(title="Calories Calculator API")


@root_router.get("/", status_code=200)
def root() -> dict:
    """
    Root GET
    """
    return {"Скоро тут будет": "Калькулятор калорий"}


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
