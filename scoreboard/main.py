from os import getenv

from fastapi import FastAPI
from pydantic import BaseModel
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from scoreboard.routers import login, scoreboard

DB_URI = getenv("DATABASE_URL", "sqlite://db.sqlite3")

app = FastAPI(
    title="Scoreboard API",
    version="0.1.0",
    description="An API to manage a scoreboard for a particular tournament.",
)
register_tortoise(
    app=app,
    db_url=DB_URI,
    modules={"models": ["scoreboard.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

Tortoise.init_models(["scoreboard.models"], "models")


class Status(BaseModel):
    status: str
    success: bool


@app.get("/", tags=["Monitor API status"], response_model=Status)
def api_status():
    return Status(status="API is up", success=True)


app.include_router(login.router, tags=["Auth"])
app.include_router(scoreboard.router, tags=["Scoreboard"])
