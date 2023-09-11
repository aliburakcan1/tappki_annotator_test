
import os
from pymongo.mongo_client import MongoClient

def split_lines(folder_name):
    for filename in os.listdir(os.path.join("data", folder_name)):
        with open(os.path.join("data", folder_name, filename), encoding="utf8") as f:
            lines = f.read().splitlines()
            for line in lines:
                yield line

def write_to_db(username, password, database, collection):

    uri = f"mongodb+srv://{username}:{password}@{database}.mongodb.net/?retryWrites=true&w=majority"

    # Create a new client and connect to the server
    client = MongoClient(uri)

    db = client.tepki
    annotation = db.video

    annotation.insert_one(collection)


def find_all_ids(username, password, database):

    uri = f"mongodb+srv://{username}:{password}@{database}.mongodb.net/?retryWrites=true&w=majority"

    # Create a new client and connect to the server
    client = MongoClient(uri)
    
    db = client.tepki
    annotation = db.video

    ids = annotation.find({}, {"tweet_id": 1, "_id": 0})

    return [id["tweet_id"] for id in ids]

def find_record_by_id(username, password, database, tweet_id):

    uri = f"mongodb+srv://{username}:{password}@{database}.mongodb.net/?retryWrites=true&w=majority"

    # Create a new client and connect to the server
    client = MongoClient(uri)
    
    db = client.tepki
    annotation = db.video

    record = annotation.find_one({"tweet_id": tweet_id})

    return record