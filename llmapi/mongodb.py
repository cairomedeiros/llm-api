import pymongo
from django.conf import settings

def get_db_handle():
    client = pymongo.MongoClient(settings.MONGO_URI)
    db_handle = client[settings.MONGO_DB_NAME]

    return db_handle