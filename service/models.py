"""
Models for Account Service
"""
import logging
from datetime import date

from service import db

logger = logging.getLogger("flask.app")


class DataValidationError(Exception):
    """Used for data validation errors"""

    pass


class Account(db.Model):
    """Account model"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(256))
    phone_number = db.Column(db.String(32))
    date_joined = db.Column(db.Date())

    def create(self):
        """Create an account"""
        self.id = None
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Update an account"""
        db.session.commit()

    def delete(self):
        """Delete an account"""
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """Serialize account to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "phone_number": self.phone_number,
            "date_joined": self.date_joined.isoformat() if self.date_joined else None,
        }

    def deserialize(self, data):
        """Deserialize account from dictionary"""
        try:
            self.name = data["name"]
            self.email = data["email"]
            self.address = data.get("address")
            self.phone_number = data.get("phone_number")
            if data.get("date_joined"):
                self.date_joined = date.fromisoformat(data["date_joined"])
        except KeyError as e:
            raise DataValidationError("Missing " + e.args[0]) from e
        return self

    @classmethod
    def all(cls):
        """Return all accounts"""
        return cls.query.all()

    @classmethod
    def find(cls, account_id):
        """Find account by id"""
        return cls.query.get(account_id)
