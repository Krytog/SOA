from aiokafka import AIOKafkaProducer
from os import environ
from typing_extensions import Annotated
from fastapi import Depends

import json

KAFKA_URL = environ.get("KAFKA_URL")

async def get_kafka_producer():
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_URL)
    await producer.start()
    async with producer as session:
        yield session

BrokerSession = Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]

async def send_to_broker(producer: BrokerSession, msg_topic: str, msg, key=None, headers=None):
    return await producer.send(msg_topic, json.dumps(msg).encode("ascii"), key=key, headers=headers)
