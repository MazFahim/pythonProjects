from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["padma"]
collection = db["balances"]


def get_daily_balances():
    data = collection.find_one({}, {"_id": 0})
    if not data:
        data = {"budget": 200, "expenses": 0}
        data["balance"] = data["budget"] - data["expenses"]
        collection.insert_one(data)
    else:
        data["balance"] = data["budget"] - data["expenses"]
        collection.update_one({}, {"$set": {"balance": data["balance"]}})

    return data

def update_daily_balance(field, value):
    value = int(value)
    collection.update_one({}, {"$set": {field: value}}, upsert=True)

    if field in ["budget", "expenses"]:
        data = collection.find_one({}, {"_id": 0})
        data["balance"] = data["budget"] - data["expenses"]
        collection.update_one({}, {"$set": {"balance": data["balance"]}})
