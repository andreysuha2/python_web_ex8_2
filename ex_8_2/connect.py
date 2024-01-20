from mongoengine import connect
from ex_8_2.definitions import DB_CONNECTION_STRING

connect(host=DB_CONNECTION_STRING, ssl=True)