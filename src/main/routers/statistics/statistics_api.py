from fastapi import status, Header, APIRouter
from fastapi.responses import JSONResponse

from functools import wraps
from typing_extensions import Annotated

from routers.main.main_api import get_auth_error
from routers.statistics.request_body_types import TargetId

from os import environ
import grpc
from proto.protocols_pb2_grpc import *
from proto.protocols_pb2 import *
from database.db_session import DBSession
from utilities.message_broker_wrapper import BrokerSession
from utilities.db_tools import get_user_id_from_token
from utilities.message_broker_wrapper import send_to_broker
import datetime


from clickhouse_driver import Client
host, port = environ.get("CLICKHOUSE_URL").split(':')

import time
time.sleep(10)  # time to let Clickhouse server to boot up
client = Client(host=host, port=port)

grpc_channel = grpc.insecure_channel(environ.get("GRPC_SERVER_CONTENT"))
grpc_stub = ContentServiceStub(grpc_channel)

router = APIRouter()


@router.put("/api/statistics/view")
async def view_post(db: DBSession, producer: BrokerSession, post_id: TargetId, auth: Annotated[str, Header()] = None):
    auth_error = await get_auth_error(db, auth)
    if auth_error is not None:
        return auth_error
    user_id = await get_user_id_from_token(auth)
    try:
        result = grpc_stub.GetPost(PostId(
            post_id=post_id.id
        ))
    except:
        return JSONResponse(content={"message": "no such post"}, status_code=status.HTTP_404_NOT_FOUND)
    msg = {
        "post_id": post_id.id,
        "user_id": user_id
    }
    try:
        await send_to_broker(producer=producer, msg_topic="views", msg=msg)
        return JSONResponse(content={"viewed": post_id.id}, status_code=status.HTTP_200_OK)
    except:
        return JSONResponse(content={"message": "view failed"}, status_code=status.HTTP_406_NOT_ACCEPTABLE)


@router.put("/api/statistics/like")
async def like_post(db: DBSession, producer: BrokerSession, post_id: TargetId, auth: Annotated[str, Header()] = None):
    auth_error = await get_auth_error(db, auth)
    if auth_error is not None:
        return auth_error
    user_id = await get_user_id_from_token(auth)
    try:
        result = grpc_stub.GetPost(PostId(
            post_id=post_id.id
        ))
    except:
        return JSONResponse(content={"message": "no such post"}, status_code=status.HTTP_404_NOT_FOUND)
    msg = {
        "post_id": post_id.id,
        "user_id": user_id
    }
    try:
        await send_to_broker(producer=producer, msg_topic="likes", msg=msg)
        return JSONResponse(content={"liked": post_id.id}, status_code=status.HTTP_200_OK)
    except:
        return JSONResponse(content={"message": "like failed"}, status_code=status.HTTP_406_NOT_ACCEPTABLE)


@router.get("/api/statistics/views/{post_id}")
async def get_views(db: DBSession, producer: BrokerSession, post_id: int, auth: Annotated[str, Header()] = None):
    auth_error = await get_auth_error(db, auth)
    if auth_error is not None:
        return auth_error
    user_id = await get_user_id_from_token(auth)
    try:
        result = grpc_stub.GetPost(PostId(
            post_id=post_id
        ))
    except:
        return JSONResponse(content={"message": "no such post"}, status_code=status.HTTP_404_NOT_FOUND)
    data = client.execute(f'SELECT count() FROM statistics.views WHERE post_id == {post_id}')                          
    try:
        return JSONResponse(content={"views": data[0][0]}, status_code=status.HTTP_200_OK)
    except:
        return JSONResponse(content={"message": "get views failed"}, status_code=status.HTTP_406_NOT_ACCEPTABLE)
    

@router.get("/api/statistics/likes/{post_id}")
async def get_likes(db: DBSession, producer: BrokerSession, post_id: int, auth: Annotated[str, Header()] = None):
    auth_error = await get_auth_error(db, auth)
    if auth_error is not None:
        return auth_error
    user_id = await get_user_id_from_token(auth)
    try:
        result = grpc_stub.GetPost(PostId(
            post_id=post_id
        ))
    except:
        return JSONResponse(content={"message": "no such post"}, status_code=status.HTTP_404_NOT_FOUND)
    data = client.execute(f'SELECT count() FROM statistics.likes WHERE post_id == {post_id}')
    print(data, flush=True)                              
    try:
        return JSONResponse(content={"likes": data[0][0]}, status_code=status.HTTP_200_OK)
    except:
        return JSONResponse(content={"message": "get likes failed"}, status_code=status.HTTP_406_NOT_ACCEPTABLE)
