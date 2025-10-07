from flask import Flask, render_template, request, redirect, jsonify, session, url_for
from db import *
from functools import wraps
import os, secrets
from features.todos.routes import todo_bp

app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False

#authentication route
# app.secret_key = '158-1997-pAdma'
app.secret_key = secrets.token_hex(16)  # Generate a random secret key

app.register_blueprint(todo_bp)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated'):
            return redirect(url_for('auth'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        if request.form.get('password') == PASSWORD:
            session['authenticated'] = True
            return redirect(url_for('home'))  
        return render_template('auth.html', error='Wrong password')
    return render_template('auth.html')


#base page routs
@app.route('/')
def home():
    if not session.get('authenticated'):
        return redirect(url_for('auth'))
    return render_template('home.html')


@app.route('/portfolio')
@login_required
def portfolio():
    portfolio_data = get_portfolio()
    return render_template('portfolio.html', portfolio=portfolio_data)

#Balance Routes
@app.route('/balance')
@login_required
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

@app.route('/resetDaily', methods=['POST'])
def reset_daily_route():
    reset_daily_and_distribute() 
    return jsonify({"success": True})

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


@app.route('/vault')
@login_required
def vault():
    return render_template('vault.html')


@app.route('/save_vault', methods=['POST'])
def save_vault_route():
    data = request.get_json()
    platform = data.get('platform')
    username = data.get('username')
    password = data.get('password')
    
    save_vault(platform, username, password)  
    return jsonify({"success": True})


@app.route('/get_vault', methods=['POST'])
def get_vault_route():
    data = request.get_json()
    platform = data.get('platform')
    credentials = get_platform_info(platform) 
    return jsonify({"credentials": credentials})

if __name__ == '__main__':
    app.run(debug=True)
