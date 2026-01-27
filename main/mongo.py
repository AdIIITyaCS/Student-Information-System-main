from functools import lru_cache

from django.conf import settings
from pymongo import MongoClient


@lru_cache(maxsize=1)
def get_mongo_client():
    if not settings.MONGO_URI:
        return None
    return MongoClient(settings.MONGO_URI, serverSelectionTimeoutMS=5000)


def get_mongo_collection():
    client = get_mongo_client()
    if client is None:
        return None

    db_name = settings.MONGO_DB_NAME
    if db_name:
        db = client.get_database(db_name)
    else:
        db = client.get_default_database()

    if db is None:
        return None

    return db[settings.MONGO_COLLECTION]
