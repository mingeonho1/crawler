from pymongo import MongoClient


def mongo_db(collection_name):
    client = MongoClient(host='000.000.000.000',  # 호스트명
                         port=00000,  # 포트번호
                         username='test',  # 유저 아이디
                         password='test1234',  # 유저 패스워드
                         directConnection=True)
    db = client.autogreen
    collection = db[collection_name]
    print(f'MONGO_DB [{collection_name}] CONNECT')

    return collection


mongo_collection = mongo_db()


def mongo_db_find(where, select):
    field = {}
    for c in select.split(' '):
        field[c] = 1
    return mongo_collection.find(where, field)


def mongo_db_insert_one_result(data):
    result = mongo_collection.insert_one(data)
    if 'InsertOneResult' in str(result):
        return True
    else:
        return False


def mongo_db_insert_many_result(data_list):
    result = mongo_collection.insert_many(data_list)
    if 'InsertManyResult' in str(result):
        return True
    else:
        return False


def mongo_db_update_one(where, query):
    result = mongo_collection.update_one(where, {"$set": query})
    if 'UpdateResult' in str(result):
        return True
    else:
        return False


def mongo_db_delete_one(where):
    result = mongo_collection.delete_one(where)
    if 'DeleteResult' in str(result):
        return True
    else:
        return False
