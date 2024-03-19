from bson import ObjectId
from mongoengine import Document
from mongoengine.fields import StringField, BooleanField
from connect import db
from faker import Faker
import pika

fake = Faker()
class contact(Document):
    fullname = StringField()
    email = StringField()
    send_mess = BooleanField(default=False)


# створити з'єднання з RabbitMQ:
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

# створення черги повідомлень із ім'ям hello_world
channel.queue_declare(queue='objectidQUEUE')

db.contacts.drop()
for _ in range(5):
    insrt = db.contacts.insert_one({'fullname':fake.name(), 'email': fake.email(), 'send_mess': False})
    print(f'[x] Sent {insrt.inserted_id}')
    insrtID = insrt.inserted_id
    channel.basic_publish(exchange='', routing_key='objectidQUEUE', body=str(insrtID).encode())
connection.close()

