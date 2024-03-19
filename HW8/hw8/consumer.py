from time import sleep
import pika
import sys
from connect import db
from bson import ObjectId

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='objectidQUEUE')


def send_email(ObjtId):
    find = db.contacts.find_one({'_id': ObjectId(ObjtId)})
    eml = find['email']
    print(f'send message to {eml}')


def callback(ch, method, properties, body:str):
    print(f" [x] Received {body}")
    send_email(ObjectId(body.decode()))
    db.contacts.update_one({'_id': ObjectId(body.decode())}, {'$set':{'send_mess': True}})

    
channel.basic_consume(queue='objectidQUEUE', on_message_callback=callback, auto_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

channel.start_consuming()


