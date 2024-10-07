import pytest
from flask_app import create_app
from flask_app.models import db


@pytest.fixture
def app():
    app = create_app(config_name='testing')

    with app.app_context():
        db.create_all()  # Create tables for tests
        yield app
        db.drop_all()  # Clean up after tests


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
