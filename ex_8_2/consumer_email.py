from ex_8_2.consumer import consume
from ex_8_2.models import ContactChannel, Contact

def handler(contact: Contact, *args, **kwargs):
    print(f"Send letter '{contact.message}' to {contact.email}")

if __name__ == "__main__":
    consume(queue=ContactChannel.EMAIL, handler=handler)