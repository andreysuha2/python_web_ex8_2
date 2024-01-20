from ex_8_2.connect import connect, create_channel
from ex_8_2.models import Contact, ContactChannel
import sys

def create_callback(handler):
    def callback(ch, method, properties, body):
        print("")
        print(f" [x] Received {body}, start handling...")
        contact: Contact = Contact.objects(pk=body.decode()).first()
        handler(contact, ch, method, properties, body)
        contact.message_recived = True
        contact.save()
        print(f"handling finished!")
    return callback

def consumer(queue: ContactChannel, handler):
    channel, conn = create_channel()
    channel.queue_declare(queue=queue.value)
    channel.basic_consume(queue=queue.value, on_message_callback=create_callback(handler=handler), auto_ack=True)
    print(f' [*] Waiting for messages from queue {queue.value}. To exit press CTRL+C')
    channel.start_consuming()

def consume(queue: ContactChannel, handler):
    try:
        consumer(queue, handler)
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
        