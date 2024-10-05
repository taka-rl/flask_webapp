def test_register_page(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b"Register" in response.data  # Check if "Register" is in the page


def test_register_form(client):
    response = client.post('/register', data={
        'email': 'test@email.com',
        'password': 'test',
        'name': 'Test User'
    })
    assert response.status_code == 302  # Expecting a redirect after a successful registration


def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b"Login" in response.data


def test_login_form(client):
    # Register first
    client.post('/register', data={
        'email': 'test@email.com',
        'password': 'test',
        'name': 'Test User'
    })

    # Test for login
    response = client.post('/login', data={
        'email': 'test@email.com',
        'password': 'test'
    })
    assert response.status_code == 302  # Expecting a redirect after a successful registration


def test_logout(client):
    # Register
    client.post('/register', data={
        'email': 'test@email.com',
        'password': 'test',
        'name': 'Test User'
    })

    # Log in
    client.post('/login', data={
        'email': 'test@email.com',
        'password': 'test',
        'name': 'Test User'
    })

    # Test for logout
    response = client.get('/logout')
    assert response.status_code == 302
    assert b"logout" in response.data
