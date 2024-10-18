def test_access_useful_info_page(super_admin_client):
    response = super_admin_client.get('/useful_info')
    assert response.status_code == 200
    assert b'Useful Information' in response.data
    assert b'Currency' in response.data
    assert b'Weather' in response.data


def test_currency_api(super_admin_client):
    pass
    '''
    response = super_admin_client.post('/currency')
    assert response.status_code == 200
    assert b'base_currency' in response.data
    assert b'exchange_rate' in response.data
    assert b'target_currency' in response.data
    '''


def test_weather_api(super_admin_client):
    pass
    '''
    response = super_admin_client.post('/weather', data={
        'loc': 'Budapest'
    })
    assert response.status_code == 200
    assert b'Weather forecast' in response.data
    assert b'Temperature' in response.data
    assert b'Max Temperature' in response.data
    assert b'Min Temperature' in response.data
    assert b'Feels like' in response.data
    assert b'Wind Speed' in response.data
    assert b'Pressure' in response.data
    assert b'Humidity' in response.data
    assert b'Description' in response.data
    '''