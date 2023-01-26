from os import environ

class Config(object):
    """Base configuration."""
    SECRET_KEY = "secret"
    DEBUG = False
    TESTING = False
    JWT_SECRET_KEY="secret_key"
    JWT_TOKEN_LOCATION=["cookies"]
    JWT_ACCESS_COOKIE_NAME="access_token_cookie"
    JWT_COOKIE_DOMAIN = ".proyecto2022.linti.unlp.edu.ar"


class ProductionConfig(Config):
    """Production configuration."""

    DB_USER = environ.get("DB_USER")
    DB_PASS = environ.get("DB_PASS")
    DB_HOST = environ.get("DB_HOST")
    DB_NAME = environ.get("DB_NAME")
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
    )

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

    DB_USER =  "postgres"
    DB_PASS =  "postgres"
    DB_HOST =  "localhost"
    DB_NAME =  "postgres"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
    )

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
config = {
    "development": DevelopmentConfig, 
    "test": TestingConfig,
    "production": ProductionConfig,
}
