from pymongo import MongoClient
from config import MONGO_URI
from datetime import datetime

client = MongoClient(MONGO_URI)
db = client["padma"]
collection = db["balances"]


def get_daily_balances():
    data = collection.find_one({}, {"_id": 0})
    today = datetime.today().strftime("%Y-%m-%d")
    
    if not data:
        data = {"date": today, "budget": 200, "expenses": 0, "balance": 200, "saved": 0}
        collection.insert_one(data)
    elif data["date"] != today:
        saved = data["saved"] + data["balance"]
        data = {"date": today, "budget": 200, "expenses": 0, "balance": 200, "saved": saved}
        collection.update_one({}, {"$set": data})

    return data

def update_daily_balance(field, value):
    collection.update_one({}, {"$set": {field: value}}, upsert=True)
