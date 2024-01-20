from ex_8_2.connect import connect, create_channel
from ex_8_2.models import Contact, ContactChannel
import os
import random
import faker

fake_data = faker.Faker()

def generate_contact(fake: faker.Faker) -> dict:
    return {
        "name": fake.name(),
        "email": fake.email(),
        "phone": int(fake.msisdn()),
        "best_channel": random.choice(list(ContactChannel)),
        "message": fake.paragraph(nb_sentences=1)
    }

def main(fake: faker.Faker, channel, connection) -> None:
    contact_data = generate_contact(fake)
    contact = Contact(**contact_data)
    contact.save()
    channel.basic_publish(exchange='', routing_key=contact.best_channel.value, body=str(contact.id))
    print(contact_data, contact.id)
    connection.close()
    

if __name__ == "__main__":
    channel, connection = create_channel()
    channel.queue_declare(queue=ContactChannel.EMAIL.value)
    channel.queue_declare(queue=ContactChannel.SMS.value)
    main(fake=fake_data, channel=channel, connection=connection)