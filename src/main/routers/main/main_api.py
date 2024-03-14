from fastapi import status, Header, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import select

from functools import wraps
from typing_extensions import Annotated

from routers.main.request_body_types import LoginPass, UserInfo
from database.models import users_table, tokens_table
from utilities.utils import get_hash_of_password
from database.db_session import DBSession

router = APIRouter()


def authorized_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if auth is None:
            return JSONResponse(content={"message": "No auth token"}, status_code=status.HTTP_403_FORBIDDEN)
        print(auth)
        return func(*args, **kwargs)
    return wrapper


@router.post("/api/signup")
async def register_user(db: DBSession, data: LoginPass):
    query = users_table.select().where(users_table.c.login == data.login)
    result = await db.execute(query)
    result_as_dict = result.mappings().all()
    print(result_as_dict)
    if len(result_as_dict) > 0:
        return JSONResponse(content={"message": "Such user is already registered"}, status_code=status.HTTP_409_CONFLICT)
    query = users_table.insert().values(login=data.login, hashed_password=get_hash_of_password(data.password))
    user_id = await db.execute(query)
    await db.commit()
    print(user_id.mappings().all())
    return JSONResponse(content={"message": "Successfully registered"}, status_code=status.HTTP_200_OK)
 

@router.post("/api/login")
async def login_user(data: LoginPass):
    if data.login:
        return JSONResponse(content={"message": "Incorrect login or password"}, status_code=status.HTTP_403_FORBIDDEN)


@router.put("/api/update")
@authorized_only
async def update_user(data: UserInfo, auth: Annotated[str, Header()] = None):
    # do stuff
    print(data.name)
    print(data.surname)
    return JSONResponse(content={"message": "Info is successfully updated"}, status_code=status.HTTP_200_OK)


@router.get("/api/about/{user_id}")
async def update_user(user_id):
    # do stuff
    print(data.name)
    print(data.surname)
    return JSONResponse(content={"message": "Info is successfully updated"}, status_code=status.HTTP_200_OK)
