import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# SQLite URI compatibility
WIN = sys.platform.startswith("win")
if WIN:
    prefix = "sqlite:///"
else:
    prefix = "sqlite:////"


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", 'long long string')
    CHAT_MESSAGES_PER_PAGE = 30
    CHAT_ADMIN_EMAIL = os.getenv('CHATROOM_ADMIN_EMAIL', '12@test.com')
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", prefix + os.path.join(basedir, "data.db"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


class HerokuConfig(ProductionConfig):
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///"
    WTF_CSRF_ENABLED = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "heroku": HerokuConfig
}
