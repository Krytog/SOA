from os import environ, system
import grpc
from proto import protocols_pb2 as protocols_pb2
from proto import protocols_pb2_grpc as protocols_pb2_grpc
from concurrent import futures
from utilities.db_tools import *
from database.db_session import SessionLocal
import asyncio
from google.protobuf.timestamp_pb2 import Timestamp

HOST = environ.get("APP_HOST")
PORT = environ.get("APP_PORT")


class ContentService(protocols_pb2_grpc.ContentServiceServicer):
    async def CreatePost(self, request, context):
        db = SessionLocal()
        try:
            post_id = await create_post(db, request.author_id, request.content)
            return protocols_pb2.PostId(post_id=post_id)
        except Exception as e:
            await context.abort(grpc.StatusCode.INTERNAL, str(e))

    async def UpdatePost(self, request, context):
        db = SessionLocal()
        try:
            post_is_valid = await exists(db, request.post_id)
            if not post_is_valid:
                return protocols_pb2.StatusResponse(success=False)
            user_is_author = await is_author(db, request.post_id, request.user_id)
            if not user_is_author:
                return protocols_pb2.StatusResponse(success=False)
            await update_post(db, request.post_id, request.new_content)
            return protocols_pb2.StatusResponse(success=True)
        except Exception as e:
            await context.abort(grpc.StatusCode.INTERNAL, str(e))

    async def DeletePost(self, request, context):
        db = SessionLocal()
        try:
            post_is_valid = await exists(db, request.post_id)
            if not post_is_valid:
                return protocols_pb2.StatusResponse(success=False)
            user_is_author = await is_author(db, request.post_id, request.user_id)
            if not user_is_author:
                return protocols_pb2.StatusResponse(success=False)
            await delete_post(db, request.post_id)
            return protocols_pb2.StatusResponse(success=True)
        except Exception as e:
            await context.abort(grpc.StatusCode.INTERNAL, str(e))

    async def GetPost(self, request, context):
        db = SessionLocal()
        try:
            post_is_valid = await exists(db, request.post_id)
            if not post_is_valid:
                await context.abort(grpc.StatusCode.NOT_FOUND, "no such post")
            post = await get_post(db, request.post_id)
            created = Timestamp()
            created.FromDatetime(post["created"])
            last_modified = Timestamp()
            last_modified.FromDatetime(post["last_modified"])
            return protocols_pb2.PostResponse(
                post_id=post["id"],
                author_id=post["author_id"],
                content=post["content"],
                created=created,
                last_modified=last_modified
            )
        except Exception as e:
            await context.abort(grpc.StatusCode.INTERNAL, str(e))

    async def GetPostsList(self, request, context):
        db = SessionLocal()
        try:
            posts = await get_posts_list(db, request.user_id, request.page_num, request.page_size)
            output = protocols_pb2.PostsListResponse()
            for post in posts:
                created = Timestamp()
                created.FromDatetime(post["created"])
                last_modified = Timestamp()
                last_modified.FromDatetime(post["last_modified"])
                post_ready = protocols_pb2.PostResponse(
                    post_id=post["id"],
                    author_id=post["author_id"],
                    content=post["content"],
                    last_modified=last_modified,
                    created=created
                )
                output.posts.append(post_ready)
            return output
        except Exception as e:
            await context.abort(grpc.StatusCode.INTERNAL, str(e))


async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=8))
    protocols_pb2_grpc.add_ContentServiceServicer_to_server(ContentService(), server)
    server.add_insecure_port(HOST + ":" + PORT)
    await server.start()
    print("Server started, listening on " + PORT)
    await server.wait_for_termination()


def init_db():
    system("alembic revision --autogenerate -m \"Init tables\"")
    system("alembic upgrade head")


if __name__ == "__main__":
    init_db()
    asyncio.run(serve())
