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


# Portfolio functions
def get_portfolio():
    data = portfolio_collection.find_one({}, {"_id": 0})
    if not data:
        data = {"type": "portfolio", "freelancing": [], "trading": []}
        portfolio_collection.insert_one(data)
    else:
        updated_fields = {}
        if "freelancing" not in data:
            updated_fields["freelancing"] = []
        if "trading" not in data:
            updated_fields["trading"] = []
        if updated_fields:
            portfolio_collection.update_one({"_id": data["_id"]}, {"$set": updated_fields})
            data.update(updated_fields)
    return data


def add_portfolio_item(category, item):
    portfolio_collection.update_one({}, {"$push": {category: item}}, upsert=True)


def update_portfolio_item(category, old_item, new_item):
    portfolio_collection.update_one({}, {
        "$set": {f"{category}.$[elem]": new_item}
    }, array_filters=[{"elem": old_item}])


def delete_portfolio_item(category, item):
    portfolio_collection.update_one({}, {"$pull": {category: item}})


#Vault functions
def save_vault(platform, username, password):
    vault_data = collection.find_one({"type": "vault"})
    new_insert = {
        "platform": platform,
        "username": username,
        "password": password,	
    }

    if not vault_data:
        data = {
            "type": "vault",
            "credentials": [new_insert]
        }
        collection.insert_one(data)
    else:
        collection.update_one(
            {"type": "vault"},
            {"$push": {"credentials": new_insert}}
        )


def get_platform_info(platform):
    vault_data = collection.find_one({"type": "vault"}, {"_id": 0, "credentials": 1})
    if not vault_data or "credentials" not in vault_data:
        return []

    return [cred for cred in vault_data["credentials"] if cred["platform"] == platform]
