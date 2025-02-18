from pymongo import MongoClient
from config import MONGO_URI


client = MongoClient(MONGO_URI)
db = client["padma"]
collection = db["balances"]
mydict = { "name": "John", "address": "Highway 37" }

try:
    print("MongoDB Connection Successful:", db.name)
    x = collection.insert_one(mydict)
    print(x)

except Exception as e:
    print("MongoDB Connection Failed:", e)