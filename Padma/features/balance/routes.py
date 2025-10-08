from flask import Flask, render_template, request, redirect, jsonify, session, url_for
from flask import Blueprint, jsonify, request
from .crud import *

balance_bp = Blueprint('balance_bp', __name__)


#Balance Routes
@balance_bp.route('/balance')
def balance():
    dailyData = get_daily_balances()
    monthlyData = get_monthly_expense()
    wishlistData = get_wish_list()
    balanceDonation = get_balance_and_donation()
    return render_template('balance.html', dailyData=dailyData, monthlyData=monthlyData, wishlistData=wishlistData, balanceDonation=balanceDonation)


@balance_bp.route('/updateDaily', methods=['POST'])
def update_daily():
    data = request.json
    field, value = data["field"], int(data["value"])

    update_daily_balance(field, value)
    updated_data = get_daily_balances()
    return jsonify({"success": True, "balance": updated_data["balance"],
                    "saved": updated_data["saved"], "date": updated_data["date"]})

@balance_bp.route('/resetDaily', methods=['POST'])
def reset_daily_route():
    reset_daily_and_distribute() 
    return jsonify({"success": True})

@balance_bp.route('/updateMonthlyExpense', methods=['POST'])
def update_monthly_expense_route():
    data = request.json
    expense_name, field, value = data["name"], data["field"], int(data["value"])

    update_monthly_expense(expense_name, field, value)
    updated_data = get_monthly_expense()
    return jsonify({"success": True, "expenses": updated_data["expenses"]})


@balance_bp.route('/addWish', methods=['POST'])
def add_wish_route():
    data = request.json
    name = data.get("name", "").strip()
    
    if not name:
        return jsonify({"success": False, "error": "Wish name cannot be empty."})
    
    add_wish_item(name)
    wishlist = get_wish_list()
    return jsonify({"success": True, "wishes": wishlist["wishes"]})


@balance_bp.route('/updateWish', methods=['POST'])
def update_wish_route():
    data = request.json
    name, field, value = data["name"], data["field"], data["value"]

    update_wish(name, field, value)
    return jsonify({"success": True})


@balance_bp.route('/deleteWish', methods=['POST'])   
def delete_wish_route():
    data = request.json
    name = data["name"]

    delete_wish(name)
    wishlist = get_wish_list()
    return jsonify({"success": True, "wishes": wishlist["wishes"]})


@balance_bp.route('/update_balance_donation', methods=['POST'])
def update_balance_donation_route():
    data = request.json
    field_type, name, value = data["field_type"], data["name"], int(data["value"])
    update_balance_donation(field_type, name, value)
    return jsonify({"success": True})
