from connect import db

def find():
    while True:
        inp = input('>>> ').split()
        try:
            match inp[0]:
                case 'exit': 
                    break
                case 'name':
                    nameAuthor = ' '.join(map(str, inp[1:]))
                    find = db.qoutes.find({'author.fullname': nameAuthor})
                    qou = []
                    for i in find:
                        qou.append(i['qoute'])
                    print(qou)
                case 'tag':
                    tag = ' '.join(map(str, inp[1:]))
                    find = db.qoutes.find({'tags': tag})
                    for i in find:
                        print(i['qoute'])
                case 'tags':
                    tags = inp[1].split(',')            
                    find = db.qoutes.find({'tags': {'$all': tags}})
                    for i in find:
                        print(i['qoute'])
        except:
            print('Невірно введені дані')       
if __name__ == '__main__':
    find()
            
            

# db.authors.delete_many({"fullname": "Steve Martin"})

