from pymongo import MongoClient
from config import MONGO_URI
from datetime import datetime
from bson import ObjectId
from cryptography.fernet import Fernet

client = MongoClient(MONGO_URI)
db = client["padma"]
collection = db["balances"]
portfolio_collection = db["portfolio"]
todos_collection = db["todos"]


def get_all_todos():
    todos = todos_collection.find({}, {"_id": 1, "text": 1, "order": 1}).sort("order", 1)
    return [{"_id": str(todo["_id"]), "text": todo["text"], "order": todo.get("order", 0)} for todo in todos]


def add_todo(text):
    max_order_todo = todos_collection.find_one(sort=[("order", -1)])
    next_order = (max_order_todo["order"] + 1) if max_order_todo and "order" in max_order_todo else 0
    todo = {"text": text, "order": next_order}
    todos_collection.insert_one(todo)


def update_todo(todo_id, text):
    todos_collection.update_one({"_id": ObjectId(todo_id)}, {"$set": {"text": text}})


def delete_todo(todo_id):
    todos_collection.delete_one({"_id": ObjectId(todo_id)})


def reorder_todos(ids_in_order):
    for index, todo_id in enumerate(ids_in_order):
        todos_collection.update_one(
            {"_id": ObjectId(todo_id)},
            {"$set": {"order": index}}
        )