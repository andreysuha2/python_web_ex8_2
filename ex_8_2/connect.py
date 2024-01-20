from mongoengine import connect
from ex_8_2.definitions import DB_CONNECTION_STRING
import os
import pika

connect(host=DB_CONNECTION_STRING, ssl=True)

def create_channel():
    credentials = pika.PlainCredentials(os.getenv("RABBIT_MQ_LOGIN"), os.getenv("RABBIT_MQ_PASSWORD"))
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=os.getenv("RABBIT_MQ_HOST"),
            port=os.getenv("RABBIT_MQ_PORT"),
            credentials=credentials
            )
        )
    channel = connection.channel()
    return channel, connection