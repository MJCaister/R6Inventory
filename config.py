import os

basedir = os.path.abspath((os.path.dirname(__file__)))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'proleague'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'mail.privateemail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or 1
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'support@r6inventory.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'Xosd1L4o!!'
    ADMINS = ['support@r6inventory.com', 'nukescrew@gmail.com', '16086@burnside.school.nz']
