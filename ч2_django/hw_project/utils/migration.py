
import os
import django
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import sys

from dotenv import dotenv_values, load_dotenv


sys.path.append(os.path.abspath('..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hw_project.settings')
django.setup()



def get_mongodb():
    load_dotenv()
    mongo_user = os.environ.get('USER') 
    mongodb_pass = os.environ.get('PASS') 
    db_name = os.environ.get('DB_NAME') 
    domain = os.environ.get('DOMAIN') 

    # mongo_user = 'codepraktik'
    # mongodb_pass = 'it9AktJTWuXbqazI'
    # db_name = 'HW10'
    # domain = 'cluster0.esxaixs.mongodb.net'

    uri = f'mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority'

    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client.HW10

    return db

