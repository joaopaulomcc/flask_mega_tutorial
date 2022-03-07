from datetime import datetime
from hashlib import md5

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import database
from app import login


class User(UserMixin, database.Model):

    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(64), index=True, unique=True)
    email = database.Column(database.String(120), index=True, unique=True)
    password_hash = database.Column(database.String(128))
    posts = database.relationship("Post", backref="author", lazy="dynamic")
    about_me = database.Column(database.String(140))
    last_seen = database.Column(database.DateTime, default=datetime.utcnow)

    def __repr__(self):

        return f"<User {self.username}>"

    def set_password(self, password):

        self.password_hash = generate_password_hash(password)

    def check_password(self, password):

        return check_password_hash(self.password_hash, password)

    def avatar(self, size):

        digest = md5(self.email.lower().encode("utf-8")).hexdigest()

        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"


class Post(database.Model):

    id = database.Column(database.Integer, primary_key=True)
    body = database.Column(database.String(140))
    timestamp = database.Column(database.DateTime, index=True, default=datetime.utcnow)
    user_id = database.Column(database.Integer, database.ForeignKey("user.id"))

    def __repr__(self):

        return f"<Post {self.body}>"


@login.user_loader
def load_user(id):

    return User.query.get(int(id))
