from app import application, database
from app.models import User, Post


@application.shell_context_processor
def make_shell_context():

    return {"database": database, "User": User, "Post": Post}
