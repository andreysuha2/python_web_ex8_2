from enum import Enum
from mongoengine import Document
from mongoengine.fields import StringField, BooleanField, IntField, EnumField

class ContactChannel(Enum):
    EMAIL="email"
    SMS="phone"

class Contact(Document):
    name=StringField()
    email=StringField()
    phone=IntField()
    best_channel=EnumField(ContactChannel, default=ContactChannel.EMAIL) 
    message_recived=BooleanField(default=False)
    message=StringField()
    meta={ "collection": "contacts" }