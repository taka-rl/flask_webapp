import pytest
from flask_app import create_app
from flask_app.models import db, User
from werkzeug.security import generate_password_hash


SUPER_ADMIN_EMAIL = 'admin@email.com'
SUPER_ADMIN_PASSWORD = 'admin'


@pytest.fixture
def app():
    app = create_app(config_name='testing')

    with app.app_context():
        db.create_all()  # Create tables for tests

        # Create a super admin user
        super_admin = User(email=SUPER_ADMIN_EMAIL,
                           password=generate_password_hash(SUPER_ADMIN_PASSWORD),
                           name='Super Admin',
                           role='super_admin'
                           )
        db.session.add(super_admin)
        db.session.commit()

        yield app
        db.drop_all()  # Clean up after tests


@pytest.fixture
def client(app):
    """Return a Flask test client"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Return a Flask test CLI runner"""
    return app.test_cli_runner()


@pytest.fixture
def super_admin_client(client):
    """Log in as the super admin and return the authenticated client."""
    client.post('/login', data={
        'email': SUPER_ADMIN_EMAIL,
        'password': SUPER_ADMIN_PASSWORD
    })
    return client
