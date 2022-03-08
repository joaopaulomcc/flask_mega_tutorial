from flask import render_template
from app import application, database


@application.errorhandler(404)
def not_found_error(error):

    return render_template("404.html"), 404


@application.errorhandler(500)
def internal_error(error):

    database.session.rollback()

    return render_template("500.html"), 500
