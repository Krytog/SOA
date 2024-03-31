from os import environ, system
import grpc
from proto import protocols_pb2 as protocols_pb2
from proto import protocols_pb2_grpc as protocols_pb2_grpc
from concurrent import futures
from utilities.db_tools import *
from database.db_session import get_db


HOST = environ.get("APP_HOST")
PORT = environ.get("APP_PORT")


class ContentService(protocols_pb2_grpc.ContentServiceServicer):
    async def CreatePost(self, request, context):
        db = await get_db()
        try:
            post_id = await create_post(db, request.author, request.content)
            return protocols_pb2.PostId(post_id=post_id)
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))

    async def UpdatePost(self, request, context):
        db = await get_db()
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
            context.abort(grpc.StatusCode.INTERNAL, str(e))

    async def DeletePost(self, request, context):
        db = await get_db()
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
            context.abort(grpc.StatusCode.INTERNAL, str(e))

    async def GetPost(self, request, context):
        db = await get_db()
        try:
            post_is_valid = await exists(db, request.post_id)
            if not post_is_valid:
                return protocols_pb2.StatusResponse(success=False)
            post = await get_post(db, request.post_id)
            return protocols_pb2.PostResponse(
                post_id=post["id"],
                author_id=post["author"],
                content=post["content"],
                last_modified=post["last_modified"].isoformat(),
                created=post["created"].isoformat()
            )
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))

    async def GetPostsList(self, request, context):
        db = await get_db()
        try:
            posts = await get_posts_list(db, request.user_id, request.page_num, request.page_size)
            output = []
            for post in posts:
                post_ready = protocols_pb2.PostResponse(
                    post_id=post["id"],
                    author_id=post["author"],
                    content=post["content"],
                    last_modified=post["last_modified"].isoformat(),
                    created=post["created"].isoformat()
                )
                output.append(post_ready)
            return output
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
    protocols_pb2_grpc.add_ContentServiceServicer_to_server(ContentService(), server)
    server.add_insecure_port(HOST + ":" + PORT)
    server.start()
    print("Server started, listening on " + PORT)
    server.wait_for_termination()


def init_db():
    system("alembic revision --autogenerate -m \"Init tables\"")
    system("alembic upgrade head")


if __name__ == "__main__":
    init_db()
    serve()
