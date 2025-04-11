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
