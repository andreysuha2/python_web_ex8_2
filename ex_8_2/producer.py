from ex_8_2.connect import connect
from ex_8_2.models import Contact, ContactChannel
import os
import random
import faker
import pika

fake_data = faker.Faker()

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
    channel.queue_declare(queue=ContactChannel.EMAIL.value)
    channel.queue_declare(queue=ContactChannel.SMS.value)
    return channel, connection

def generate_contact(fake: faker.Faker) -> dict:
    return {
        "name": fake.name(),
        "email": fake.email(),
        "phone": int(fake.msisdn()),
        "best_channel": random.choice(list(ContactChannel)),
        "message": fake.paragraph(nb_sentences=1)
    }

def main(fake: faker.Faker) -> None:
    channel, connection = create_channel()
    contact_data = generate_contact(fake)
    contact = Contact(**contact_data)
    contact.save()
    channel.basic_publish(exchange='', routing_key=contact.best_channel.value, body=str(contact.id))
    print(contact_data, contact.id)
    connection.close()
    

if __name__ == "__main__":
    main(fake=fake_data)