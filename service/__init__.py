"""
Service Package
"""
import sys
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "s3cr3t-key"

db = SQLAlchemy(app)
talisman = Talisman(app)
CORS(app)

logging.basicConfig(
    stream=sys.stdout,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    level=logging.INFO,
)

from service import routes, models  # noqa: F401, E402

with app.app_context():
    db.create_all()
