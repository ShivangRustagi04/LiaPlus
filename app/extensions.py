from flask_session import Session
from redis import Redis
import logging

session_ext = Session()
redis_client = None

def init_extensions(app):
    # configure logging
    logging_level = getattr(logging, app.config.get("LOG_LEVEL", "INFO"))
    logging.basicConfig(level=logging_level,
                        format='%(asctime)s %(levelname)s %(name)s %(message)s')

    # Session (file or redis depending on config)
    if app.config.get("SESSION_TYPE") == "redis":
        host = app.config.get("REDIS_HOST", "redis")
        port = int(app.config.get("REDIS_PORT", 6379))
        db = int(app.config.get("REDIS_DB", 0))
        global redis_client
        redis_client = Redis(host=host, port=port, db=db, decode_responses=True)
        app.config['SESSION_REDIS'] = redis_client

    session_ext.init_app(app)
