# myapp/models.py

from myapp.extensions import db, login_manager
from datetime import datetime, timezone
from flask_login import UserMixin


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    honorific_title = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    added_on = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    removed_on = db.Column(db.DateTime(timezone=True), nullable=True)

    @property
    def is_active(self):
        return self.removed_on is None


class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    added_on = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    removed_on = db.Column(db.DateTime(timezone=True), nullable=True)

    @property
    def is_active(self):
        return self.removed_on is None


class RoleType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class RoleAssignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=True)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), nullable=False)
    role_type_id = db.Column(db.Integer, db.ForeignKey('role_type.id'), nullable=False)
    start_date = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    end_date = db.Column(db.DateTime(timezone=True), nullable=True)
    person = db.relationship('Person', backref='role_assignments')
    board = db.relationship('Board', backref='role_assignments')
    role_type = db.relationship('RoleType', backref='role_assignments')

    @property
    def is_active(self):
        return self.end_date is None

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    added_on = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    removed_on = db.Column(db.DateTime(timezone=True), nullable=True)

    @property
    def is_active(self):
        return self.removed_on is None

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))