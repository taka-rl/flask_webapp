from flask_app.models import User, db
from werkzeug.security import generate_password_hash
from parameters import TEST_NAME, TEST_EMAIL, TEST_PASSWORD, SUPER_ADMIN_EMAIL, SUPER_ADMIN_PASSWORD


def test_check_super_admin_exist(client):
    # Verify the super admin exists in the database
    super_admin_user = User.query.filter_by(email=SUPER_ADMIN_EMAIL).first()
    assert super_admin_user is not None
    assert super_admin_user.role == 'Super Admin'


def test_admin_dashboard_access(super_admin_client):
    response = super_admin_client.get('/admin-dashboard')

    print(response.data)  # Add logging for debugging

    assert response.status_code == 200  # Check if registration redirects after success
    assert b'Admin Dashboard' in response.data


def test_change_user_role(super_admin_client):
    # Create a new user manually for testing
    new_user = User(name=TEST_NAME,
                    email=TEST_EMAIL,
                    password=generate_password_hash(TEST_PASSWORD)
                    )

    with super_admin_client.application.app_context():
        db.session.add(new_user)
        db.session.commit()

    # Verify the user exists in the database
    user = User.query.filter_by(email=TEST_EMAIL).first()
    assert user is not None
    assert user.role == 'user'

    # Super admin changes the role of the new user
    response = super_admin_client.post(f'/admin/change-role/{user.id}')
    assert response.status_code == 302

    # Verify the role has been changed
    user = db.session.get(User, user.id)
    assert user.role == 'admin'


def test_delete_user(super_admin_client):
    # Create a new user manually for testing
    new_user = User(name=TEST_NAME,
                    email=TEST_EMAIL,
                    password=generate_password_hash(TEST_PASSWORD)
                    )

    with super_admin_client.application.app_context():
        db.session.add(new_user)
        db.session.commit()

    # Verify the user exists in the database
    user = User.query.filter_by(email=TEST_EMAIL).first()
    assert user is not None

    # Super admin changes the role of the new user
    response = super_admin_client.post(f'/admin/delete-user/{user.id}')
    assert response.status_code == 302

    # Verify the user exists in the database
    user = User.query.filter_by(email=TEST_EMAIL).first()
    assert user is None
