import pytest
from app import create_app
from app.extensions import init_extensions

@pytest.fixture
def app():
    app = create_app("development")
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "SESSION_TYPE": "filesystem",
    })
    with app.app_context():
        init_extensions(app)
    yield app

@pytest.fixture
def client(app):
    return app.test_client()
