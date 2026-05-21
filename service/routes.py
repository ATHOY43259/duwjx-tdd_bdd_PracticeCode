"""
Routes for Account Service
"""
from flask import jsonify, request, abort

from service import app
from service.models import Account


@app.route("/health")
def health():
    """Health check"""
    return jsonify(dict(status="OK")), 200


@app.route("/")
def index():
    """Root URL"""
    return jsonify(name="Account REST API Service", version="1.0"), 200


@app.route("/accounts", methods=["POST"])
def create_accounts():
    """Create an Account"""
    check_content_type("application/json")
    account = Account()
    account.deserialize(request.get_json())
    account.create()
    return jsonify(account.serialize()), 201


@app.route("/accounts", methods=["GET"])
def list_accounts():
    """List all Accounts"""
    accounts = Account.all()
    return jsonify([a.serialize() for a in accounts]), 200


@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_accounts(account_id):
    """Read an Account"""
    account = Account.find(account_id)
    if not account:
        abort(404, f"Account {account_id} not found.")
    return jsonify(account.serialize()), 200


@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_accounts(account_id):
    """Update an Account"""
    account = Account.find(account_id)
    if not account:
        abort(404, f"Account {account_id} not found.")
    account.deserialize(request.get_json())
    account.id = account_id
    account.update()
    return jsonify(account.serialize()), 200


@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_accounts(account_id):
    """Delete an Account"""
    account = Account.find(account_id)
    if account:
        account.delete()
    return "", 204


def check_content_type(content_type):
    """Check content type"""
    if request.headers.get("Content-Type") != content_type:
        abort(415, f"Content-Type must be {content_type}")
