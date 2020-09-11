from threading import Thread
from flask_mail import Message
from flask import render_template
from app import mail, app


# Uses threading to send emails without holding up the server/user
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


# Sends email to the requested email address using the templated html/txt files for the respective email
def send_email(subject, sender, recipients, text_body, html_body):
    # Sends message as BCC so that multiple recipients cannot see each others email addresses
    msg = Message(subject, sender=sender, bcc=recipients)
    msg.body = text_body
    msg.html = html_body
    # Starts new thread
    Thread(target=send_async_email, args=(app, msg)).start()


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('R6Inventory | Reset your password',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))


def send_profile_information_changed_email(user, new_email=None):
    # Checks for if email has been changed
    if new_email is not None:
        print('Sending new email to {}, {}'.format(new_email, user.email))
        send_email('R6Inventory | Account details changed',
        sender=app.config['ADMINS'][0],
        recipients=[user.email, new_email],
        text_body=render_template('email/details_changed.txt',
                                  user=user),
        html_body=render_template('email/details_changed.html',
                                  user=user))
    else:
        print('Sending new email to {}'.format(user.email))
        send_email('R6Inventory | Account details changed',
        sender=app.config['ADMINS'][0],
        recipients=[user.email],
        text_body=render_template('email/details_changed.txt',
                                  user=user),
        html_body=render_template('email/details_changed.html',
                                  user=user))
