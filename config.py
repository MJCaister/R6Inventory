import os

basedir = os.path.abspath((os.path.dirname(__file__)))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'proleague'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    # School passwords are already in plaintext but its about time to commit another sin
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'ruru2117'
    ADMINS = ['16086@burnside.school.nz']
