def test_admin_dashboard_access(super_admin_client):
    response = super_admin_client.get('/admin-dashboard')
    assert response.status_code == 200  # Check if registration redirects after success
    assert b'Admin Dashboard' in response.data


def test_change_user_role(super_admin_client):
    # Create a new user manually for testing
    from flask_app.models import User, db
    from werkzeug.security import generate_password_hash
    new_user = User(name='Test User',
                    email='test@email.com',
                    password=generate_password_hash('test')
                    )

    with super_admin_client.application.app_context():
        db.session.add(new_user)
        db.session.commit()

    # Verify the user exists in the database
    user = User.query.filter_by(email='test@email.com').first()
    assert user is not None
    assert user.role == 'user'

    # Super admin changes the role of the new user
    response = super_admin_client.post(f'/admin/change-role/{user.id}')
    assert response.status_code == 302

    # Verify the role has been changed
    user = User.query.get(user.id)
    assert user.role == 'admin'


def test_delete_user(super_admin_client):
    # Create a new user manually for testing
    from flask_app.models import User, db
    new_user = User(name='Test User',
                    email='test@email.com',
                    password='test'
                    )

    with super_admin_client.application.app_context():
        db.session.add(new_user)
        db.session.commit()

    # Verify the user exists in the database
    user = User.query.filter_by(email='test@email.com').first()
    assert user is not None

    # Super admin changes the role of the new user
    response = super_admin_client.post(f'/admin/delete-user/{user.id}')
    assert response.status_code == 302

    # Verify the user exists in the database
    user = User.query.filter_by(email='test@email.com').first()
    assert user is None
