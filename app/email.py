from threading import Thread

from flask import render_template
from flask_mail import Message
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from app import application, mail


def send_async_email(app, sg, message):

    with app.app_context():
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)


def send_email(subject, sender, recipients, text_body, html_body):

    message = Mail(
        from_email=sender,
        to_emails=recipients,
        subject=subject,
        plain_text_content=text_body,
        html_content=html_body,
    )
    try:
        sg = SendGridAPIClient(application.config["MAIL_API_KEY"])
        Thread(target=send_async_email, args=(application, sg, message)).start()

    except Exception as e:
        print(e.message)

    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)
    """


def send_password_reset_email(user):

    token = user.get_reset_password_token()
    send_email(
        subject="[Microblog] Reset Your Password",
        sender=application.config["MAIL_DEFAULT_SENDER"],
        recipients=[user.email],
        text_body=render_template("email/reset_password.txt", user=user, token=token),
        html_body=render_template("email/reset_password.html", user=user, token=token),
    )
