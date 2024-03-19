from connect import db
from datetime import datetime
import json

with open('authors.json', 'r', encoding='utf-8') as file:
    readjsonAuthor = json.load(file)

with open('qoutes.json', 'r', encoding='utf-8') as file:
    readjsonQoutes = json.load(file)


db.authors.drop()
for author in readjsonAuthor:
    insrt = db.authors.insert_one({'fullname':author['fullname'], 
            'born_date':datetime.strptime(author['born_date'], '%B %d, %Y'),
            'born_location':author['born_location'],
            'description':author['description']})
    print(insrt.inserted_id)

db.qoutes.drop()
for qoute in readjsonQoutes:
    i = db.qoutes.insert_one({'tags':qoute['tags'], 'author':db.authors.find_one({'fullname': qoute['author']}), 'qoute':qoute['quote']})
    print(insrt.inserted_id)
    