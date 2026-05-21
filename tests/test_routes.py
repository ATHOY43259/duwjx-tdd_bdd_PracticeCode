"""
Test Cases for Account Service
"""
import pytest
from service import app, talisman
from service.models import db, Account

ACCOUNT_DATA = {
    "name": "John Doe",
    "email": "john@example.com",
    "address": "123 Main St",
    "phone_number": "555-1234",
    "date_joined": "2024-01-01",
}

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    talisman.force_https = False
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.query(Account).delete()
        db.session.commit()

def test_index(client):
    resp = client.get("/")
    assert resp.status_code == 200

def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200

def test_create_account(client):
    resp = client.post(
        "/accounts",
        json=ACCOUNT_DATA,
        content_type="application/json"
    )
    assert resp.status_code == 201

def test_list_accounts(client):
    resp = client.get("/accounts")
    assert resp.status_code == 200

def test_get_account(client):
    resp = client.post("/accounts", json=ACCOUNT_DATA, content_type="application/json")
    account_id = resp.get_json()["id"]
    resp = client.get(f"/accounts/{account_id}")
    assert resp.status_code == 200

def test_update_account(client):
    resp = client.post("/accounts", json=ACCOUNT_DATA, content_type="application/json")
    account_id = resp.get_json()["id"]
    updated = dict(ACCOUNT_DATA, name="Jane Doe")
    resp = client.put(f"/accounts/{account_id}", json=updated, content_type="application/json")
    assert resp.status_code == 200

def test_delete_account(client):
    resp = client.post("/accounts", json=ACCOUNT_DATA, content_type="application/json")
    account_id = resp.get_json()["id"]
    resp = client.delete(f"/accounts/{account_id}")
    assert resp.status_code == 204

def test_security_headers(client):
    resp = client.get("/")
    assert resp.status_code == 200

def test_cors_header(client):
    resp = client.get("/accounts", headers={"Origin": "http://example.com"})
    assert resp.status_code == 200
    assert "Access-Control-Allow-Origin" in resp.headers
