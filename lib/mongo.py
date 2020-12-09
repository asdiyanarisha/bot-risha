import pymongo


def connect(host, db):
    client = pymongo.MongoClient(host)
    return getattr(client, db)
