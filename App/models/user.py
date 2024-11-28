from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from App.database import db
from abc import ABC
from App.models import ReviewCommandHistory


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    faculty = db.Column(db.String(120), nullable=False)
    user_type = db.Column(db.String(50), nullable=False)  # Add this for polymorphism

    history = db.relationship(
        "ReviewCommandHistory",
        backref="user",
        lazy="dynamic",
        cascade="all, delete-orphan"
    )

    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": user_type,  # Use this field for polymorphic behavior
    }

    def __init__(self, username, first_name, last_name, password, email, faculty):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.faculty = faculty
        self.set_password(password)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method="sha256")

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "faculty": self.faculty,
        }
