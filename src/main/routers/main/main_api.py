from fastapi import status, Header, APIRouter
from fastapi.responses import JSONResponse

from functools import wraps
from typing_extensions import Annotated

from routers.main.request_body_types import LoginPass, UserInfo
from utilities.security import is_password_valid
from utilities.db_tools import *
from database.db_session import DBSession, get_db

router = APIRouter()


async def get_auth_error(db: DBSession, auth):
    if auth is None:
        return JSONResponse(content={"message": "No auth token"}, status_code=status.HTTP_403_FORBIDDEN)
    token_valid = await is_token_valid(db, auth)
    if not token_valid:
            return JSONResponse(content={"message": "Auth token is invalid"}, status_code=status.HTTP_403_FORBIDDEN)
    return None


@router.post("/api/signup")
async def register_user(db: DBSession, data: LoginPass):
    user = await get_user_by_login(db, data.login)
    if user is not None:
        return JSONResponse(content={"message": "Such user is already registered"}, status_code=status.HTTP_409_CONFLICT)
    await create_user(db, data.login, data.password)
    return JSONResponse(content={"message": "Successfully registered"}, status_code=status.HTTP_200_OK)
 

@router.post("/api/login")
async def login_user(db: DBSession, data: LoginPass):
    user = await get_user_by_login(db, data.login)
    if user is None or not is_password_valid(data.password, user["hashed_password"]):
        return JSONResponse(content={"message": "Incorrect login or password"}, status_code=status.HTTP_403_FORBIDDEN)
    token = await create_token(db, user["id"], 24)
    return JSONResponse(content={"message": "Successfully logined", "token": token}, status_code=status.HTTP_200_OK)


@router.put("/api/update")
async def update_user(db: DBSession, data: UserInfo, auth: Annotated[str, Header()] = None):
    auth_error = await get_auth_error(db, auth)
    if auth_error is not None:
        return auth_error
    user_id = await get_user_id_from_token(auth)
    await update_user_info(db, data, user_id)
    return JSONResponse(content={"message": "Info is successfully updated"}, status_code=status.HTTP_200_OK)


@router.get("/api/about/{user_login}")
async def get_about_user(db: DBSession, user_login):
    user = await get_user_by_login(db, user_login)
    if user is None:
        return JSONResponse(content={"message": "Such user doesn't exist"}, status_code=status.HTTP_404_NOT_FOUND)
    result = get_user_info_from_user(user)
    return JSONResponse(content=result, status_code=status.HTTP_200_OK)
