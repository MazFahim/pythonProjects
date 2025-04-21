from flask import Flask, render_template, request, redirect, jsonify
from db import *

app = Flask(__name__)

#base page routs
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/portfolio')
def portfolio():
    portfolio_data = get_portfolio()
    return render_template('portfolio.html', portfolio=portfolio_data)

#Balance Routes
@app.route('/balance')
def balance():
    dailyData = get_daily_balances()
    monthlyData = get_monthly_expense()
    wishlistData = get_wish_list()
    balanceDonation = get_balance_and_donation()
    return render_template('balance.html', dailyData=dailyData, monthlyData=monthlyData, wishlistData=wishlistData, balanceDonation=balanceDonation)


@app.route('/updateDaily', methods=['POST'])
def update_daily():
    data = request.json
    field, value = data["field"], int(data["value"])

    update_daily_balance(field, value)
    updated_data = get_daily_balances()
    return jsonify({"success": True, "balance": updated_data["balance"],
                    "saved": updated_data["saved"], "date": updated_data["date"]})


@app.route('/updateMonthlyExpense', methods=['POST'])
def update_monthly_expense_route():
    data = request.json
    expense_name, field, value = data["name"], data["field"], int(data["value"])

    update_monthly_expense(expense_name, field, value)
    updated_data = get_monthly_expense()
    return jsonify({"success": True, "expenses": updated_data["expenses"]})


@app.route('/addWish', methods=['POST'])
def add_wish_route():
    data = request.json
    name = data.get("name", "").strip()
    
    if not name:
        return jsonify({"success": False, "error": "Wish name cannot be empty."})
    
    add_wish_item(name)
    wishlist = get_wish_list()
    return jsonify({"success": True, "wishes": wishlist["wishes"]})


@app.route('/updateWish', methods=['POST'])
def update_wish_route():
    data = request.json
    name, field, value = data["name"], data["field"], data["value"]

    update_wish(name, field, value)
    return jsonify({"success": True})


@app.route('/deleteWish', methods=['POST'])   
def delete_wish_route():
    data = request.json
    name = data["name"]

    delete_wish(name)
    wishlist = get_wish_list()
    return jsonify({"success": True, "wishes": wishlist["wishes"]})


@app.route('/update_balance_donation', methods=['POST'])
def update_balance_donation_route():
    data = request.json
    field_type, name, value = data["field_type"], data["name"], int(data["value"])
    update_balance_donation(field_type, name, value)
    return jsonify({"success": True})


#portfolio related routes
@app.route('/add_portfolio_item', methods=['POST'])
def add_portfolio_item_route():
    data = request.json
    category = data["category"]
    item = data["item"]
    add_portfolio_item(category, item)
    return jsonify(success=True)


@app.route('/update_portfolio_item', methods=['POST'])
def update_portfolio_item_route():
    data = request.json
    category = data["category"]
    old_item = data["old_item"]
    new_item = data["new_item"]
    update_portfolio_item(category, old_item, new_item)
    return jsonify(success=True)


@app.route('/delete_portfolio_item', methods=['POST'])
def delete_portfolio_item_route():
    data = request.json
    category = data["category"]
    item = data["item"]
    delete_portfolio_item(category, item)
    return jsonify(success=True)


if __name__ == '__main__':
    app.run(debug=True)
