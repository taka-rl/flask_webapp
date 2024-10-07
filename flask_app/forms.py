from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField


class CSRFProtectionForm(FlaskForm):
    """ This form has no fields, but it includes a CSRF token"""
    pass


# WTForm for creating a blog post
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL")
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


# Create a RegisterForm to register new users
class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(message="Invalid email address")])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Register User")


# Create a LoginForm to login existing users
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(message="Invalid email address")])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In")


# Create a CommentForm so users can leave comments below posts
class CommentForm(FlaskForm):
    comment_text = CKEditorField('Comment', validators=[DataRequired()])
    submit = SubmitField('Submit Comment')


# WTForms
class CreatePlaceForm(FlaskForm):
    name = StringField('Place Name', validators=[DataRequired()])
    location = StringField('Place Address')
    location_url = StringField('Place Location on Google Map', validators=[DataRequired(), URL(message="Invalid URL")])
    open_time = StringField('Opening Time e.g. 8AM')
    close_time = StringField('Closing Time e.g. 4:30PM')
    rating = StringField('Place Rating e.g. 9.5 out of 10')
    pricing = StringField('Pricing range e.g. 1000-2000 Ft')
    category = SelectField('Category',
                           choices=[('Restaurant', 'Restaurant'),
                                    ('Cafe', 'Cafe'),
                                    ('Sightseeing Spot', 'Sightseeing Spot')])
    submit = SubmitField('Submit')
