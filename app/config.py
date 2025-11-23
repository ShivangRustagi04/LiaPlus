import os

class BaseConfig:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "change-me-in-prod")
    JSON_SORT_KEYS = False
    SESSION_PERMANENT = False
    SESSION_TYPE = os.getenv("SESSION_TYPE", "filesystem")
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    MAX_CONTENT_LENGTH = 1024 * 20

class ProdConfig(BaseConfig):
    DEBUG = False
    SESSION_TYPE = os.getenv("SESSION_TYPE", "redis")

class DevConfig(BaseConfig):
    DEBUG = True

def get_config(env: str = None):
    env = env or os.getenv("FLASK_ENV", "development")
    if env == "production":
        return ProdConfig
    return DevConfig
