from flask_app.models import db, BlogPost


def test_create_new_post(super_admin_client):
    post_response = super_admin_client.post('/new-post', data={
        'title': 'Test Post',
        'subtitle': 'Test Subtitle',
        'img_url': 'https://www.abcdefg/test',
        'body': 'This is a test body content for the post.'
    }, follow_redirects=True)

    # Check if it renders index.html after creating a post
    assert post_response.status_code == 200
    assert b"TakaTaka Blog" in post_response.data

    # Verify the post exists in the database
    blog = BlogPost.query.filter_by(title='Test Post').first()
    assert blog is not None
    assert blog.subtitle == 'Test Subtitle'
    assert blog.body == 'This is a test body content for the post.'


def test_edit_post(super_admin_client):
    # Create a post
    post_response = super_admin_client.post('/new-post', data={
        'title': 'Test Post',
        'subtitle': 'Test Subtitle',
        'img_url': 'https://www.abcdefg/test',
        'body': 'This is a test body content for the post.'
    }, follow_redirects=True)

    # Check if it renders index.html after creating a post
    assert post_response.status_code == 200
    assert b"TakaTaka Blog" in post_response.data

    # Verify the post exists in the database
    blog = BlogPost.query.filter_by(title='Test Post').first()
    assert blog is not None
    assert blog.subtitle == 'Test Subtitle'
    assert blog.body == 'This is a test body content for the post.'

    # Get post id
    edit_response = super_admin_client.post(f'/edit-post/{blog.id}', data={
        'title': 'Test Post edited',
        'subtitle': 'Edited: Test Subtitle',
        'img_url': 'https://pixabay.com/illustrations/test-testing-sign-laboratory-670091/',
        'body': 'Edited. This is a test body content for the post.'
    }, follow_redirects=True)

    # Check if the response indicates success
    assert edit_response.status_code == 200

    # Reload the post from the database to check the updated values
    updated_blog = BlogPost.query.get(blog.id)
    assert updated_blog is not None
    assert updated_blog.title == 'Test Post edited'
    assert updated_blog.subtitle == 'Edited: Test Subtitle'
    assert updated_blog.body == 'Edited. This is a test body content for the post.'


def test_delete_post(super_admin_client):
    pass


def test_add_comment(super_admin_client):
    pass

