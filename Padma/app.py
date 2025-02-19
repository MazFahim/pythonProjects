from flask import Flask, render_template, request, redirect, jsonify
from db import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/balance')
def balance():
    dailyData = get_daily_balances()
    return render_template('balance.html', dailyData=dailyData)

@app.route('/update_daily', methods=['POST'])
def update_daily():
    data = request.json
    field, value = data.get("field"), data.get("value")
    update_daily_balance(field, value)
    updated_data = get_daily_balances()
    return jsonify({"success": True, "balance": updated_data["balance"]})

if __name__ == '__main__':
    app.run(debug=True)
