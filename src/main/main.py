from fastapi import FastAPI, status, Request, Header
from fastapi.responses import JSONResponse

from functools import wraps
from typing_extensions import Annotated
from utils import get_hash_of_password

from RequestBodyTypes import LoginPass, UserInfo

from cringe_db import TIPO_DB

app = FastAPI()

def authorized_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if auth is None:
            return JSONResponse(content={"message": "No auth token"}, status_code=status.HTTP_403_FORBIDDEN)
        print(auth)
        return func(*args, **kwargs)
    return wrapper


@app.post("/api/signup")
async def register_user(data: LoginPass):
    if data.login in TIPO_DB:
        return JSONResponse(content={"message": "Login is already taken"}, status_code=status.HTTP_409_CONFLICT)
    TIPO_DB[data.login] = get_hash_of_password(data.password)
    return JSONResponse(content={"message": "Successfully registered"}, status_code=status.HTTP_200_OK)

@app.post("/api/login")
async def login_user(data: LoginPass):
    if data.login not in TIPO_DB:
        return JSONResponse(content={"message": "Incorrect login or password"}, status_code=status.HTTP_403_FORBIDDEN)
    if TIPO_DB[data.login] != get_hash_of_password(data.password):
        return JSONResponse(content={"message": "Incorrect login or password"}, status_code=status.HTTP_403_FORBIDDEN)

@app.put("/api/update")
@authorized_only
async def update_user(data: UserInfo, auth: Annotated[str, Header()] = None):
    # do stuff
    print(data.name)
    print(data.surname)
    return JSONResponse(content={"message": "Info is successfully updated"}, status_code=status.HTTP_200_OK)

@app.get("/api/aboutme")
@authorized_only
async def update_user(data: UserInfo, auth: Annotated[str, Header()] = None):
    # do stuff
    print(data.name)
    print(data.surname)
    return JSONResponse(content={"message": "Info is successfully updated"}, status_code=status.HTTP_200_OK)
    