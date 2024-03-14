from fastapi import FastAPI
from main.routers.main import main_api
from database import main_database
from os import environ
from contextlib import asynccontextmanager
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    await main_database.connect()
    yield
    await main_database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(main_api)


HOST = environ.get("HOST")
PORT = environ.get("PORT")


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
