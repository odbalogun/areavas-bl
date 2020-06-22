from decouple import config


class ConfigObject(object):
    APP_HOST = config('APP_HOST')
    APP_PORT = config('APP_PORT')
    DEBUG = config('DEBUG')
    TESTING = config('TESTING')
    CSRF_ENABLED = config('CSRF_ENABLED')
    SECRET_KEY = config('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@localhost:5432/{}".format(config('DB_USER'), config('DB_PASSWORD'), config('DB_NAME'))
    SQLALCHEMY_TRACK_MODIFICATIONS = config('SQLALCHEMY_TRACK_MODIFICATIONS', default=False)

    SECURITY_URL_PREFIX = "/admin"
    SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
    SECURITY_PASSWORD_SALT = config('SECURITY_PASSWORD_SALT')

    SECURITY_LOGIN_URL = "/login/"
    SECURITY_LOGOUT_URL = "/logout/"
    SECURITY_REGISTER_URL = "/register/"
    SECURITY_RESET_URL = "/reset/"

    SECURITY_POST_LOGIN_VIEW = "/admin/"
    SECURITY_POST_LOGOUT_VIEW = "/admin/"
    SECURITY_POST_REGISTER_VIEW = "/admin/"
    SECURITY_POST_RESET_VIEW = "/admin/"

    SECURITY_REGISTERABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_CHANGEABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False

    PAYSTACK_KEY = config('PAYSTACK_KEY')
