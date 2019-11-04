import hashlib
from datetime import datetime

from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    nickname = db.Column(db.String(36))
    password_hash = db.Column(db.String(250))
    access_token = db.Column(db.String(250))
    email_hash = db.Column(db.String(250))
    github = db.Column(db.String(50))
    website = db.Column(db.String(50))
    bio = db.Column(db.String(50))
    messages = db.relationship("Message", back_populates="author", cascade="all")

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.generate_email_hash()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_email_hash(self):
        if self.email is not None and self.email_hash is None:
            self.email_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()

    @property
    def gravatar(self):
        return 'https://gravatar.com/avatar/%s?d=monsterid' % self.email_hash

    @property
    def is_admin(self):
        return self.email == current_app.config['CHAT_ADMIN_EMAIL']


class Guest(AnonymousUserMixin):

    @property
    def is_admin(self):
        return False


login_manager.anonymous_user = Guest


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow(), index=True)
    author = db.relationship("User", back_populates="messages")
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))