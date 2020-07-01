import os

basedir = os.path.abspath((os.path.dirname(__file__)))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'proleague'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = 1
    # School passwords are already in plaintext but its about time to commit another sin
    MAIL_PASSWORD ='ruru2117' 
    ADMINS = ['16086@burnside.school.nz']
