from flask_login import current_user
from flask_app.models import Place, db
from tests.parameters import TEST_PLACE_NAME, TEST_PLACE_LOCATION, TEST_PLACE_LOCATION_URL, TEST_PLACE_OPEN_TIME
from tests.parameters import TEST_PLACE_CLOSE_TIME, TEST_PLACE_PRICING, TEST_PLACE_RATING, TEST_PLACE_CATEGORY


# access to collection page
def test_access_collection_page(client):
    response = client.get('/collection')
    assert response.status_code == 200
    assert b'Collection' in response.data
    assert b'These are what I love' in response.data


# add a place
def test_add_place(super_admin_client):
    # Add a place
    place_response = super_admin_client.post('/add-place', data={
        'name': TEST_PLACE_NAME,
        'location': TEST_PLACE_LOCATION,
        'location_url': TEST_PLACE_LOCATION_URL,
        'open_time': TEST_PLACE_OPEN_TIME,
        'close_time': TEST_PLACE_CLOSE_TIME,
        'pricing': TEST_PLACE_PRICING,
        'rating': TEST_PLACE_RATING,
        'category': TEST_PLACE_CATEGORY,
        'place_author': current_user
    }, follow_redirects=True)

    # Verify the place is added
    assert place_response.status_code == 200

    place = Place.query.filter_by(name=TEST_PLACE_NAME).first()
    assert place is not None
    assert place.name == TEST_PLACE_NAME
    assert place.location == TEST_PLACE_LOCATION
    assert place.location_url == TEST_PLACE_LOCATION_URL
    assert place.open_time == TEST_PLACE_OPEN_TIME
    assert place.close_time == TEST_PLACE_CLOSE_TIME
    assert place.pricing == TEST_PLACE_PRICING
    assert place.rating == TEST_PLACE_RATING
    assert place.category == TEST_PLACE_CATEGORY
    assert place.place_author == current_user


# edit a place
def test_edit_place(super_admin_client):
    # Add a place manually for testing
    new_place = Place(name=TEST_PLACE_NAME,
                      location=TEST_PLACE_LOCATION,
                      location_url=TEST_PLACE_LOCATION_URL,
                      open_time=TEST_PLACE_OPEN_TIME,
                      close_time=TEST_PLACE_CLOSE_TIME,
                      pricing=TEST_PLACE_PRICING,
                      rating=TEST_PLACE_RATING,
                      category=TEST_PLACE_CATEGORY,
                      author_id=current_user.id
                      )

    with super_admin_client.application.app_context():
        db.session.add(new_place)
        db.session.commit()

    # Verify the place is stored in the database
    place = Place.query.filter_by(name=TEST_PLACE_NAME).first()
    assert place is not None

    # Edit the place
    edit_response = super_admin_client.post(f'/edit-place/{place.id}', data={
        'name': TEST_PLACE_NAME + '_TEST',
        'location': 'Test_Location',
        'category': 'Restaurant'
    }, follow_redirects=True)

    assert edit_response.status_code == 200

    # Verify the place is edited
    edit_place = Place.query.filter_by(name=TEST_PLACE_NAME + '_TEST').first()
    assert edit_place is not None
    assert edit_place.name == TEST_PLACE_NAME + '_TEST'
    assert edit_place.location == 'Test_Location'
    assert edit_place.category == 'Restaurant'


# delete a place
def test_delete_place(super_admin_client):
    # Add a place manually for testing
    new_place = Place(name=TEST_PLACE_NAME,
                      location=TEST_PLACE_LOCATION,
                      location_url=TEST_PLACE_LOCATION_URL,
                      open_time=TEST_PLACE_OPEN_TIME,
                      close_time=TEST_PLACE_CLOSE_TIME,
                      pricing=TEST_PLACE_PRICING,
                      rating=TEST_PLACE_RATING,
                      category=TEST_PLACE_CATEGORY,
                      author_id=current_user.id
                      )

    with super_admin_client.application.app_context():
        db.session.add(new_place)
        db.session.commit()

    # Verify the place is stored in the database
    place = Place.query.filter_by(name=TEST_PLACE_NAME).first()
    assert place is not None

    # Delete the place
    delete_response = super_admin_client.post(f'delete-place/{place.id}')
    assert delete_response.status_code == 302

    # Verify the place is deleted
    delete_place = Place.query.filter_by(name=TEST_PLACE_NAME).first()
    assert delete_place is None
