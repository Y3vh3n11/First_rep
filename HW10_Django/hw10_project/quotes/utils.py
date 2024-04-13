import configparser
from pymongo import MongoClient
from pymongo.server_api import ServerApi

def get_mongo():
    config = configparser.ConfigParser()
    config.read('config.ini')

    mongo_user = config.get('DB', 'user')
    mongodb_pass = config.get('DB', 'pass')
    db_name = config.get('DB', 'db_name')
    domain = config.get('DB', 'domain')
    uri = f'mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority'

    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client.HW10
    
    return db


