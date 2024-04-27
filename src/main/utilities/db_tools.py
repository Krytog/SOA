from database.db_session import DBSession
from database.models import users_table, tokens_table
from utilities.security import get_salt, get_hash_of_password
from routers.main.request_body_types import UserInfo
from os import environ
from sqlalchemy import and_
import datetime
import jwt

AUTH_KEY = environ.get("AUTH_KEY")


async def get_user_by_login(db: DBSession, login: str):
    query = users_table.select().where(users_table.c.login == login)
    result = await db.execute(query)
    result_as_dict = result.mappings().all()
    if len(result_as_dict) == 0:
        return None
    return result_as_dict[0] # there can be only one user with given login


async def create_user(db: DBSession, login: str, password: str):
    salt = get_salt(15)
    hashed_password = get_hash_of_password(password, salt) + " " + salt
    query = users_table.insert().values(
        login=login, 
        hashed_password=hashed_password
    )
    await db.execute(query)
    await db.commit()


async def create_token(db: DBSession, user_id, hours_available):
    expires = datetime.datetime.utcnow() + datetime.timedelta(hours=hours_available)
    token = jwt.encode({
        "id": user_id,
        "expires": str(expires.isoformat())
    }, AUTH_KEY, algorithm="HS256")
    query = tokens_table.insert().values(
        token=token,
        expires=expires,
        owner=user_id
    )
    decoded = jwt.decode(token, AUTH_KEY, algorithms=["HS256"])
    print(decoded)
    await db.execute(query)
    await db.commit()
    return token


async def get_user_id_from_token(token: str):
    print(token)
    try:
        decoded = jwt.decode(token, AUTH_KEY, algorithms=["HS256"])
        print(decoded)
        return decoded["id"]
    except:
        print("DECODE FAILED!")
        return None


async def is_token_valid(db: DBSession, token: str):
    user_id = await get_user_id_from_token(token)
    print("USER_ID:", user_id)
    if user_id is None:
        return False
    query = tokens_table.select().where(and_(
        tokens_table.c.owner == user_id,
        tokens_table.c.token == token
    ))
    result = await db.execute(query)
    result_as_dict = result.mappings().all()
    if len(result_as_dict) == 0:
        return False
    ready_result = result_as_dict[0]
    print(ready_result)
    return ready_result["expires"] >= datetime.datetime.utcnow()


async def update_user_info(db: DBSession, user_info: UserInfo, user_id):
    date = None
    try:
        date = datetime.datetime.strptime(user_info.birthdate, "%d.%m.%Y")
    except:
        pass
    query = users_table.update().where(users_table.c.id == user_id).values(
        email=user_info.email,
        name=user_info.name,
        surname=user_info.surname,
        birthdate=date,
        phone=user_info.phone,
        bio=user_info.bio
    )
    await db.execute(query)
    await db.commit()


def get_user_info_from_user(user):
    user_info = {}
    user_info["name"] = user["name"]
    user_info["surname"] = user["surname"]
    user_info["email"] = user["email"]
    user_info["birthdate"] = user["birthdate"].strftime("%d.%m.%Y")
    user_info["phone"] = user["phone"]
    user_info["bio"] = user["bio"]
    return user_info
