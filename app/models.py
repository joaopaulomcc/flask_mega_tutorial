import jwt

from datetime import datetime
from hashlib import md5
from time import time

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import database, login, application


followers = database.Table(
    "followers",
    database.Column("follower_id", database.Integer, database.ForeignKey("user.id")),
    database.Column("followed_id", database.Integer, database.ForeignKey("user.id")),
)


class User(UserMixin, database.Model):

    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(64), index=True, unique=True)
    email = database.Column(database.String(120), index=True, unique=True)
    password_hash = database.Column(database.String(128))
    about_me = database.Column(database.String(140))
    last_seen = database.Column(database.DateTime, default=datetime.utcnow)

    posts = database.relationship("Post", backref="author", lazy="dynamic")
    followed = database.relationship(
        "User",
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=database.backref("followers", lazy="dynamic"),
        lazy="dynamic",
    )

    def __repr__(self):

        return f"<User {self.username}>"

    def set_password(self, password):

        self.password_hash = generate_password_hash(password)

    def check_password(self, password):

        return check_password_hash(self.password_hash, password)

    def avatar(self, size):

        digest = md5(self.email.lower().encode("utf-8")).hexdigest()

        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"

    def is_following(self, user):

        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def follow(self, user):

        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):

        if self.is_following(user):
            self.followed.remove(user)

    def followed_posts(self):

        followed = Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(
            followers.c.follower_id == self.id
        )
        own = Post.query.filter_by(user_id=self.id)

        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):

        return jwt.encode(
            {"reset_password": self.id, "exp": time() + expires_in},
            application.config["SECRET_KEY"],
            algorithm="HS256",
        )

    @staticmethod
    def verify_reset_password_token(token):

        try:
            id = jwt.decode(token, application.config["SECRET_KEY"], algorithms=["HS256"])[
                "reset_password"
            ]
        except:
            return None

        return User.query.get(id)


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
