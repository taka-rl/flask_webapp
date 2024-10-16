def test_about_access(client):
    response = client.get('/about')
    assert response.status_code == 200
    assert b"About Me" in response.data
