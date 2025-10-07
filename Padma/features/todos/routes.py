from flask import Blueprint, jsonify, request
from .crud import *

todo_bp = Blueprint('todo_bp', __name__)

@todo_bp.route('/get_todos')
def get_todos_route():
    todos = get_all_todos()
    return jsonify({"todos": todos})

@todo_bp.route('/add_todo', methods=['POST'])
def add_todo_route():
    data = request.get_json()
    text = data.get("text")
    if text:
        add_todo(text)
    return jsonify({"success": True})

@todo_bp.route('/update_todo', methods=['POST'])
def update_todo_route():
    data = request.get_json()
    update_todo(data["id"], data["text"])
    return jsonify({"success": True})

@todo_bp.route('/delete_todo', methods=['POST'])
def delete_todo_route():
    data = request.get_json()
    delete_todo(data["id"])
    return jsonify({"success": True})

@todo_bp.route('/reorder_todos', methods=['POST'])
def reorder_todos_route():
    data = request.get_json()
    ids_in_order = data["ordered_ids"]
    reorder_todos(ids_in_order)
    return jsonify({"success": True})
