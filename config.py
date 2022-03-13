import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    SECRET_KEY = os.environ.get("SECRET_KEY") or "you_will_never_guess"

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(
        basedir, "app.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT"))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSOWRD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")
    MAIL_API_KEY = os.environ.get("MAIL_API_KEY")
    ADMINS = os.environ.get("ADMINS")
    POSTS_PER_PAGE = 3
