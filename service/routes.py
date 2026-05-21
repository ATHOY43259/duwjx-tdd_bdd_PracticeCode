"""
Routes for Account Service
"""
from flask import jsonify, request, abort
from service import app, db
from service.models import Account, DataValidationError

@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

@app.route("/")
def index():
    return jsonify(name="Account REST API Service", version="1.0"), 200

@app.route("/accounts", methods=["POST"])
def create_accounts():
    check_content_type("application/json")
    account = Account()
    account.deserialize(request.get_json())
    account.create()
    return jsonify(account.serialize()), 201

@app.route("/accounts", methods=["GET"])
def list_accounts():
    accounts = Account.all()
    return jsonify([a.serialize() for a in accounts]), 200

@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_accounts(account_id):
    account = Account.find(account_id)
    if not account:
        abort(404, f"Account {account_id} not found.")
    return jsonify(account.serialize()), 200

@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_accounts(account_id):
    account = Account.find(account_id)
    if not account:
        abort(404, f"Account {account_id} not found.")
    account.deserialize(request.get_json())
    account.id = account_id
    account.update()
    return jsonify(account.serialize()), 200

@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_accounts(account_id):
    account = Account.find(account_id)
    if account:
        account.delete()
    return "", 204

def check_content_type(content_type):
    if request.headers.get("Content-Type") != content_type:
        abort(415, f"Content-Type must be {content_type}")
