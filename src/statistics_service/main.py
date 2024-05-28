from os import environ
import grpc
from proto import protocols_pb2 as protocols_pb2
from proto import protocols_pb2_grpc as protocols_pb2_grpc
from concurrent import futures
import asyncio

HOST = environ.get("APP_HOST")
PORT = environ.get("APP_PORT")

from clickhouse_driver import Client
host, port = environ.get("CLICKHOUSE_URL").split(':')

import time
time.sleep(10)  # time to let Clickhouse server to boot up
client = Client(host=host, port=port)


class StatisticsService(protocols_pb2_grpc.StatisticsServiceServicer):
    async def GetPostStatistics(self, request, context):
        post_id = request.post_id
        likes = client.execute(f'SELECT count() FROM statistics.likes WHERE post_id == {post_id}')[0][0]
        views = client.execute(f'SELECT count() FROM statistics.views WHERE post_id == {post_id}')[0][0]
        return protocols_pb2.PostStatisticsResponse(post_id=post_id, likes=likes, views=views)

    async def GetTopPosts(self, request, context):
        pass

    async def GetTopUsers(self, request, context):
        pass


async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=8))
    protocols_pb2_grpc.add_StatisticsServiceServicer_to_server(StatisticsService(), server)
    server.add_insecure_port(HOST + ":" + PORT)
    await server.start()
    print("Server started, listening on " + PORT)
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())
