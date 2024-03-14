from fastapi import FastAPI
from routers.main.main_api import router as main_api
from os import environ, system
from contextlib import asynccontextmanager
import uvicorn

app = FastAPI()
app.include_router(main_api)


HOST = environ.get("APP_HOST")
PORT = int(environ.get("APP_PORT"))

def init_db():
    system("alembic revision --autogenerate -m \"Init tables\"")
    system("alembic upgrade head")

if __name__ == "__main__":
    init_db()
    uvicorn.run(app, host=HOST, port=PORT)
