from datetime import datetime

from app import database


class User(database.Model):

    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(64), index=True, unique=True)
    email = database.Column(database.String(120), index=True, unique=True)
    password_hash = database.Column(database.String(128))
    posts = database.relationship("Post", backref="author", lazy="dynamic")

    def __repr__(self):

        return f"<User {self.username}>"


class Post(database.Model):

    id = database.Column(database.Integer, primary_key=True)
    body = database.Column(database.String(140))
    timestamp = database.Column(database.DateTime, index=True, default=datetime.utcnow)
    user_id = database.Column(database.Integer, database.ForeignKey("user.id"))

    def __repr__(self):

        return f"<Post {self.body}>"
