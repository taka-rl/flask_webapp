# utility functions for testing
def register_for_test(client, data):
    # Register
    response = client.post('/register', data={
        'email': data['email'],
        'password': data['password'],
        'name': data['name']
    }, follow_redirects=True)
    assert response.status_code == 200


def test_500_page(client):
    response = client.get('/trigger-500')
    assert response.status_code == 500
    assert b"500 - Internal Server Error" in response.data


def test_404_page(client):
    response = client.get('/nonexistent')
    assert response.status_code == 404
    assert b"Page Not Found" in response.data


def test_403_page(client):
    # Register as an admin
    register_for_test(client, data={
        'email': 'admin@email.com',
        'password': 'admin',
        'name': 'Super Admin'
    })

    logout_response = client.get('/logout')
    assert logout_response.status_code == 302

    # Register as a test user
    register_for_test(client, data={
        'email': 'test@email.com',
        'password': 'test',
        'name': 'Test User'
    })

    # Log in as test user
    response = client.post('/login', data={
        'email': 'test@email.com',
        'password': 'test'
    }, follow_redirects=True)

    # Ensure the login was successful
    assert response.status_code == 200

    # Move to /useful_info route, only allowed by admin
    response = client.get('/useful_info')

    # Check that the status code is 403 (forbidden) for non-admin users
    assert response.status_code == 403
    assert b"Forbidden" in response.data
