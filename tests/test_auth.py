from flask_app.models import User, db
from werkzeug.security import generate_password_hash
from tests.parameters import TEST_NAME, TEST_EMAIL, TEST_PASSWORD


def test_register_page(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b"Register" in response.data  # Check if "Register" is in the page


def test_register_form(client):
    response = client.post('/register', data={
        'email': TEST_EMAIL,
        'password': TEST_PASSWORD,
        'name': TEST_NAME
    })
    assert response.status_code == 302  # Expecting a redirect after a successful registration


def test_duplicated_email_register(client):
    # Create a new user manually for testing
    new_user = User(name=TEST_NAME,
                    email=TEST_EMAIL,
                    password=generate_password_hash(TEST_PASSWORD)
                    )

    with client.application.app_context():
        db.session.add(new_user)
        db.session.commit()

    # Verify the user exists in the database
    user = User.query.filter_by(email=TEST_EMAIL).first()
    assert user is not None

    # Register the same user
    response = client.post('/register', data={
        'email': TEST_EMAIL,
        'password': TEST_PASSWORD,
        'name': TEST_NAME
    }, follow_redirects=True)

    # Check if the application redirects from registration page to log in page with a status code 200
    assert response.status_code == 200
    assert b"Log In" in response.data


def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b"Login" in response.data


def test_login_form(client):
    # Register first
    client.post('/register', data={
        'email': TEST_EMAIL,
        'password': TEST_PASSWORD,
        'name': TEST_NAME
    })

    # Test for login
    response = client.post('/login', data={
        'email': TEST_EMAIL,
        'password': TEST_PASSWORD
    })
    assert response.status_code == 302  # Expecting a redirect after a successful registration


def test_logout(client):
    # Register
    register_response = client.post('/register', data={
        'email': TEST_EMAIL,
        'password': TEST_PASSWORD,
        'name': TEST_NAME
    })

    assert register_response.status_code == 302  # Check if registration redirects after success

    # Test for logout
    logout_response = client.get('/logout')
    assert logout_response.status_code == 302

    # Log in
    login_response = client.post('/login', data={
        'email': TEST_EMAIL,
        'password': TEST_PASSWORD,
        'name': TEST_NAME
    })
    assert login_response.status_code == 302  # Check if login redirects after success

    # Test for logout
    logout_response = client.get('/logout')
    assert logout_response.status_code == 302

    response = client.get('/')
    assert response.status_code == 200

