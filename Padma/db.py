from pymongo import MongoClient
from config import MONGO_URI
from datetime import datetime
from bson import ObjectId

client = MongoClient(MONGO_URI)
db = client["padma"]
collection = db["balances"]
portfolio_collection = db["portfolio"]
todos_collection = db["todos"]


#balance functions
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


def get_monthly_expense():
    data = collection.find_one({"type": "monthly"}, {"_id": 0})
    current_month = datetime.today().strftime("%Y-%m")

    if not data:
        data = {
            "type": "monthly",
            "month": current_month,
            "expenses": [
                {"name": "Rent", "budget": 10000, "spent": 0},
                {"name": "Gas", "budget": 1500, "spent": 0},
                {"name": "Electricity", "budget": 1500, "spent": 0}
            ],
            "savedLastMonth": 0
        }
        collection.insert_one(data)
    elif data["month"] != current_month:
        total_budget = sum(exp["budget"] for exp in data["expenses"])
        total_spent = sum(exp["spent"] for exp in data["expenses"])
        saved_last_month = total_budget - total_spent

        for exp in data["expenses"]:
            exp["spent"] = 0

        collection.update_one(
            {"type": "monthly"},
            {"$set": {
                "month": current_month,
                "savedLastMonth": saved_last_month,
                "expenses": data["expenses"]
            }}
        )
        data["month"] = current_month
        data["savedLastMonth"] = saved_last_month
        
    return data


def update_monthly_expense(expense_name, field, value):
    collection.update_one(
        {"type": "monthly", "expenses.name": expense_name},
        {"$set": {f"expenses.$.{field}": value}}
    )


def add_wish_item(name):
    wish_data = collection.find_one({"type": "wish_list"})
    new_wish = {
        "name": name,
        "priority": "",
        "price_tag": 0,	
        "accumulated": 0
    }

    if not wish_data:
        data = {
            "type": "wish_list",
            "wishes": [new_wish]
        }
        collection.insert_one(data)
    else:
        collection.update_one(
            {"type": "wish_list"},
            {"$push": {"wishes": new_wish}}
        )


def get_wish_list():
    wish_data = collection.find_one({"type": "wish_list"}, {"_id": 0})
    
    if not wish_data:
        wish_data = {
            "type": "wish_list",
            "wishes": []
        }
        collection.insert_one(wish_data)

    return wish_data

def update_wish(name, field, value):
    collection.update_one(
        {"type": "wish_list", "wishes.name": name},
        {"$set": {f"wishes.$.{field}": value}}
    )

def delete_wish(name):
    collection.update_one(
        {"type": "wish_list"},
        {"$pull": {"wishes": {"name": name}}}
    )

def get_balance_and_donation():
    data = collection.find_one({"type": "balance_donation"}, {"_id": 0})
    if not data:
        data = {
            "type": "balance_donation",
            "donations": {
                "mosque": 0,
                "madrasa": 0,
                "sadqah": 0,
                "empowerment": 0,
                "others": 0
            },
            "balances": {
                "dbbl": 0,
                "bkash": 0,
                "nagad": 0
            }
        }
        collection.insert_one(data)
    return data

def update_balance_donation(field_type, field_name, value):
    collection.update_one(
        {"type": "balance_donation"},
        {"$set": {f"{field_type}.{field_name}": value}},
        upsert=True
    )


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


# Todo functions
def get_all_todos():
    todos = todos_collection.find({}, {"_id": 1, "text": 1})
    return [{"_id": str(todo["_id"]), "text": todo["text"]} for todo in todos]


def add_todo(text):
    todo = {"text": text}
    todos_collection.insert_one(todo)


def update_todo(todo_id, text):
    todos_collection.update_one({"_id": ObjectId(todo_id)}, {"$set": {"text": text}})


def delete_todo(todo_id):
    todos_collection.delete_one({"_id": ObjectId(todo_id)})
