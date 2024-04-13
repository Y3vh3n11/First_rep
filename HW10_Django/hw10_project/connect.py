import configparser
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import json
from datetime import datetime

config = configparser.ConfigParser()
config.read('config.ini')

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')
uri = f'mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority'

client = MongoClient(uri, server_api=ServerApi('1'))
db = client.HW10




with open("utils/authors.json", "r", encoding="utf-8") as file:
    readjsonAuthor = json.load(file)

with open("utils/quotes.json", "r", encoding="utf-8") as file:
    readjsonQoutes = json.load(file)

db.authors.drop()
for author in readjsonAuthor:
    insrt = db.authors.insert_one(
        {
            "fullname": author["fullname"],
            "born_date": datetime.strptime(author["born_date"], "%B %d, %Y"),
            "born_location": author["born_location"],
            "description": author["description"],
        }
    )

db.quotes.drop()
for quote in readjsonQoutes:
    insrt = db.quotes.insert_one(
        {
            "tags": quote["tags"],
            "author": db.authors.find_one({"fullname": quote["author"]}),
            "quote": quote["quote"],
        }
    )

