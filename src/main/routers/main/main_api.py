from fastapi import status, Header
from fastapi.responses import JSONResponse

from functools import wraps
from typing_extensions import Annotated

from routers.main.request_body_types import LoginPass, UserInfo
from utilities.utils import get_hash_of_password


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
    query = user
    user_id = await users


@app.post("/api/login")
async def login_user(data: LoginPass):
    if data.login:
        return JSONResponse(content={"message": "Incorrect login or password"}, status_code=status.HTTP_403_FORBIDDEN)


@app.put("/api/update")
@authorized_only
async def update_user(data: UserInfo, auth: Annotated[str, Header()] = None):
    # do stuff
    print(data.name)
    print(data.surname)
    return JSONResponse(content={"message": "Info is successfully updated"}, status_code=status.HTTP_200_OK)


@app.get("/api/about/{user_id}")
async def update_user(user_id):
    # do stuff
    print(data.name)
    print(data.surname)
    return JSONResponse(content={"message": "Info is successfully updated"}, status_code=status.HTTP_200_OK)
