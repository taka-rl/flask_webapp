import pytest
from flask_app import create_app
from flask_app.models import db, User
from werkzeug.security import generate_password_hash
from parameters import SUPER_ADMIN_EMAIL, SUPER_ADMIN_PASSWORD, SUPER_ADMIN_NAME


@pytest.fixture
def app():
    app = create_app(config_name='testing')

    with app.app_context():
        db.create_all()  # Create tables for tests

        # Create a super admin user
        super_admin = User(email=SUPER_ADMIN_EMAIL,
                           password=generate_password_hash(SUPER_ADMIN_PASSWORD),
                           name=SUPER_ADMIN_NAME,
                           role='Super Admin'
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
    login_response = client.post('/login', data={
        'email': SUPER_ADMIN_EMAIL,
        'password': SUPER_ADMIN_PASSWORD
    }, follow_redirects=True)

    # Make sure if login was successful
    assert login_response.status_code == 200
    assert b"admin-dashboard" in login_response.data
    return client
