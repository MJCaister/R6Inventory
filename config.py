import os

# Gets the absolute path of the flaskapps location
basedir = os.path.abspath((os.path.dirname(__file__)))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'proleague'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Horrifically stored in plaintext because school computers
    # Email authentication should be moved to environment vairables for deployment
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or 1
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'nukescrew@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'xxeyapfthufrnrdg'
    ADMINS = ['nukescrew@gmail.com', 'support@r6inventory.com', '16086@burnside.school.nz']
