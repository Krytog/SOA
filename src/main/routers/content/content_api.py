from fastapi import status, Header, APIRouter
from fastapi.responses import JSONResponse

from functools import wraps
from typing_extensions import Annotated

from routers.main.main_api import get_auth_error
from routers.content.request_body_types import PostContent, PostsList

from os import environ
import grpc
from proto.protocols_pb2_grpc import *
from proto.protocols_pb2 import *
from database.db_session import DBSession
from utilities.db_tools import get_user_id_from_token
import datetime


grpc_channel = grpc.insecure_channel(environ.get("GRPC_SERVER_CONTENT"))
grpc_stub = ContentServiceStub(grpc_channel)

router = APIRouter()


@router.post("/api/content/create_post")
async def create_post(db: DBSession, content: PostContent, auth: Annotated[str, Header()] = None):
    auth_error = await get_auth_error(db, auth)
    if auth_error is not None:
        return auth_error
    user_id = await get_user_id_from_token(auth)
    result = grpc_stub.CreatePost(CreatePostRequest(
        author_id=user_id,
        content=content.content
    ))
    return JSONResponse(content={"message": "created post id is " + str(result.post_id)}, status_code=status.HTTP_200_OK)


@router.put("/api/content/update_post/{post_id}")
async def update_post(db: DBSession, post_id: int, content: PostContent, auth: Annotated[str, Header()] = None):
    auth_error = await get_auth_error(db, auth)
    if auth_error is not None:
        return auth_error
    user_id = await get_user_id_from_token(auth)
    result = grpc_stub.UpdatePost(UpdatePostRequest(
        user_id=user_id,
        post_id=post_id,
        new_content=content.content
    ))
    if result:
        return JSONResponse(content={"message": "updated"}, status_code=status.HTTP_200_OK)
    return JSONResponse(content={"message": "failed to update"}, status_code=status.HTTP_406_NOT_ACCEPTABLE)


@router.put("/api/content/delete_post/{post_id}")
async def delete_post(db: DBSession, post_id: int, auth: Annotated[str, Header()] = None):
    auth_error = await get_auth_error(db, auth)
    if auth_error is not None:
        return auth_error
    user_id = await get_user_id_from_token(auth)
    result = grpc_stub.DeletePost(DeletePostRequest(
        user_id=user_id,
        post_id=post_id
    ))
    if result:
        return JSONResponse(content={"message": "deleted"}, status_code=status.HTTP_200_OK)
    return JSONResponse(content={"message": "failed to delete"}, status_code=status.HTTP_406_NOT_ACCEPTABLE)


@router.get("/api/content/get_post/{post_id}")
async def get_post(db: DBSession, post_id: int, auth: Annotated[str, Header()] = None):
    auth_error = await get_auth_error(db, auth)
    if auth_error is not None:
        return auth_error   
    try:
        result = grpc_stub.GetPost(PostId(
            post_id=post_id
        ))
        return JSONResponse(content=get_json_from_post_response(result), status_code=status.HTTP_200_OK)
    except:
        return JSONResponse(content={"message": "no such post"}, status_code=status.HTTP_404_NOT_FOUND)


@router.get("/api/content/get_postslist")
async def get_postslist(db: DBSession, data: PostsList, auth: Annotated[str, Header()] = None):
    auth_error = await get_auth_error(db, auth)
    if auth_error is not None:
        return auth_error
    result = grpc_stub.GetPostsList(PostsListRequest(
        user_id=data.user_id,
        page_num=data.page,
        page_size=data.per_page
    ))
    return JSONResponse(content={"post": result}, status_code=status.HTTP_200_OK)


def get_json_from_post_response(data):
    output = {"post_id": data.post_id, "content": data.content, 
              "author_id": data.author_id, "last_modified": data.last_modified.ToDatetime().isoformat(),
              "created": data.created.ToDatetime().isoformat()}
    return output
