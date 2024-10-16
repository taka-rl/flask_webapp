from datetime import date
from flask_app.models import db, BlogPost, Comment


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
    post = BlogPost.query.filter_by(title='Test Post').first()
    assert post is not None
    assert post.subtitle == 'Test Subtitle'
    assert post.body == 'This is a test body content for the post.'


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
    post = BlogPost.query.filter_by(title='Test Post').first()
    assert post is not None
    assert post.subtitle == 'Test Subtitle'
    assert post.body == 'This is a test body content for the post.'

    # Edit the post
    edit_response = super_admin_client.post(f'/edit-post/{post.id}', data={
        'title': 'Test Post edited',
        'subtitle': 'Edited: Test Subtitle',
        'img_url': 'https://pixabay.com/illustrations/test-testing-sign-laboratory-670091/',
        'body': 'Edited. This is a test body content for the post.'
    }, follow_redirects=True)

    # Check if the response indicates success
    assert edit_response.status_code == 200

    # Reload the post from the database to check the updated values
    updated_post = BlogPost.query.get(post.id)
    assert updated_post is not None
    assert updated_post.title == 'Test Post edited'
    assert updated_post.subtitle == 'Edited: Test Subtitle'
    assert updated_post.body == 'Edited. This is a test body content for the post.'


def test_delete_post(super_admin_client):
    # Create a post
    new_post = BlogPost(title='Test Post',
                        subtitle='Test Subtitle',
                        img_url='https://www.abcdefg/test',
                        body='This is a test body content for the post.',
                        author_id=1,
                        date=date.today().strftime("%B %d, %Y")
                        )
    with super_admin_client.application.app_context():
        db.session.add(new_post)
        db.session.commit()

    # Verify whether the post is registered in the database
    post = BlogPost.query.filter_by(title='Test Post').first()
    assert post is not None
    assert post.subtitle == 'Test Subtitle'
    assert post.body == 'This is a test body content for the post.'

    # Delete a post
    delete_response = super_admin_client.post(f'/delete-post/{post.id}')
    print(delete_response.data)
    assert delete_response.status_code == 302

    # Verify whether the blog is deleted
    delete_post = BlogPost.query.filter_by(title='Test Post').first()
    assert delete_post is None


def test_add_comment(super_admin_client):
    # Create a post
    new_post = BlogPost(title='Test Post',
                        subtitle='Test Subtitle',
                        img_url='https://www.abcdefg/test',
                        body='This is a test body content for the post.',
                        author_id=1,
                        date=date.today().strftime("%B %d, %Y")
                        )
    with super_admin_client.application.app_context():
        db.session.add(new_post)
        db.session.commit()

    # Verify whether the post is registered in the database
    new_post = BlogPost.query.filter_by(title='Test Post').first()
    assert new_post is not None
    assert new_post.subtitle == 'Test Subtitle'
    assert new_post.body == 'This is a test body content for the post.'

    # Move to the post page
    response = super_admin_client.get(f'/post/{new_post.id}')
    assert response.status_code == 200
    assert b'Test Post' in response.data

    # Add a comment
    comment_text = 'This is a test comment'
    comment_response = super_admin_client.post(f'post/{new_post.id}', data={
        'comment_text': comment_text
    }, follow_redirects=True)

    assert comment_response.status_code == 200
    assert b'Test Post' in comment_response.data

    # Verify whether the comment exists
    comment = Comment.query.filter_by(text=comment_text).first()
    assert comment is not None
    assert comment.text == comment_text
    assert comment.post_id == new_post.id
    assert comment.comment_author is not None

