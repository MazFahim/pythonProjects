from flask import Flask, render_template, request, redirect, jsonify, session, url_for
from db import *
from functools import wraps
import os, secrets
from features.todos.routes import todo_bp
from features.balance.routes import balance_bp

app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False

#authentication route
# app.secret_key = '158-1997-pAdma'
app.secret_key = secrets.token_hex(16)  # Generate a random secret key

app.register_blueprint(todo_bp)
app.register_blueprint(balance_bp)


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
