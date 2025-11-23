from flask import Flask
from .config import get_config
from .extensions import init_extensions
from .blueprints.chat import bp as chat_bp

def create_app(config_name: str = None):
    cfg = get_config(config_name)
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(cfg)
    init_extensions(app)
    app.register_blueprint(chat_bp)
    return app
