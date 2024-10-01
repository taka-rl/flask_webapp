from datetime import date
from flask import Flask, render_template, redirect, url_for, flash, request, session, make_response
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm, CreatePlaceForm
from utils import with_translations, admin_only, send_email, get_weather_info, get_currency_info
from models import User, Place, BlogPost, Comment, Base
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
ckeditor = CKEditor()
bootstrap = Bootstrap5()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

    # Initialize app with extentions
    db.init_app(app)
    login_manager.init_app(app)
    ckeditor.init_app(app)
    bootstrap.init_app(app)
    return app


app = create_app()


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


@app.route('/switch_language/<lang>')
def switch_language(lang):
    session['lang'] = lang  # Store in session
    response = make_response(redirect(request.referrer))
    response.set_cookie('lang', lang, max_age=30*24*60*60)  # Store in cookie (30 days)
    return response


# Use Werkzeug to hash the user's password when creating a new user.
@app.route('/register', methods=["POST", "GET"])
@with_translations
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Find user by email entered if it's already existed or not
        email = form.email.data
        user = db.session.execute(db.select(User).where(User.email == email)).scalar()

        if user:
            flash("You've already sighed up with that email, login instead!")
            return redirect(url_for('login'))

        else:
            hash_and_salted_password = generate_password_hash(password=form.password.data,
                                                              method='pbkdf2:sha256',
                                                              salt_length=8)
            new_user = User(email=form.email.data,
                            password=hash_and_salted_password,
                            name=form.name.data)

            db.session.add(new_user)
            db.session.commit()

            # Log in and authenticate user after adding details to database
            login_user(new_user)

            return redirect(url_for('get_all_posts'))

    return render_template('register.html', form=form, current_user=current_user)


# Retrieve a user from the database based on their email.
@app.route('/login', methods=["POST", "GET"])
@with_translations
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # Find user by email entered
        user = db.session.execute(db.select(User).where(User.email == email)).scalar()

        # Check stored password hash against entered password hashed
        if not user:
            flash("That email does not exist, please try again!")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash("Password incorrect, please try again!")
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('get_all_posts'))

    return render_template("login.html", form=form, current_user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route('/')
@with_translations
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()

    return render_template("index.html",
                           all_posts=posts, current_user=current_user)


# Allow logged-in users to comment on posts
@app.route("/post/<int:post_id>", methods=["GET", "POST"])
@with_translations
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    comment_form = CommentForm()

    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.")
            return redirect(url_for("login"))

        new_comment = Comment(text=comment_form.comment_text.data,
                              comment_author=current_user,
                              parent_post=requested_post)
        db.session.add(new_comment)
        db.session.commit()

    return render_template("post.html",
                           post=requested_post,
                           current_user=current_user,
                           form=comment_form)


# Use a decorator so only an admin user can create a new post
@app.route("/new-post", methods=["GET", "POST"])
@admin_only
@with_translations
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            blog_author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


# Use a decorator so only an admin user can edit a post
@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        blog_author=post.blog_author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)


# Use a decorator so only an admin user can delete a post
@app.route("/delete-post/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/about")
@with_translations
def about():
    return render_template("about.html")


@app.route("/collection")
@with_translations
def collection():
    return render_template("collection.html")


@app.route('/places')
@with_translations
def show_places():
    result = db.session.execute(db.select(Place))
    all_places = result.scalars().all()
    return render_template('places.html', places=all_places, current_user=current_user)


@app.route("/add-place", methods=["POST", "GET"])
@with_translations
def add_place():
    form = CreatePlaceForm()
    if form.validate_on_submit():
        place = Place(name=form.name.data,
                      location=form.location.data,
                      location_url=form.location_url.data,
                      open_time=form.open_time.data,
                      close_time=form.close_time.data,
                      rating=form.rating.data,
                      pricing=form.pricing.data,
                      category=form.category.data,
                      place_author=current_user)
        db.session.add(place)
        db.session.commit()
        return redirect(url_for('show_places'))
    return render_template("add-place.html", form=form)


@app.route('/edit-place/<int:place_id>', methods=["POST", "GET"])
@with_translations
def edit_place(place_id):
    place = db.get_or_404(Place, place_id)

    edit_form = CreatePlaceForm(
        name=place.name,
        location=place.location,
        location_url=place.location_url,
        open_time=place.open_time,
        close_time=place.close_time,
        rating=place.rating,
        pricing=place.pricing,
        category=place.category)

    if edit_form.validate_on_submit():
        place.name = edit_form.name.data
        place.location = edit_form.location.data
        place.location_url = edit_form.location_url.data
        place.open_time = edit_form.open_time.data
        place.close_time = edit_form.close_time.data
        place.rating = edit_form.rating.data
        place.pricing = edit_form.pricing.data
        place.category = edit_form.category.data

        db.session.commit()  # Commit the changes
        return redirect(url_for('show_places'))
    return render_template('add-place.html', place=place, form=edit_form, is_edit=True)


@app.route('/delete-place/<int:place_id>')
@admin_only
def delete_place(place_id):
    place_to_delete = db.get_or_404(Place, place_id)
    db.session.delete(place_to_delete)
    db.session.commit()
    return redirect(url_for('show_places'))


@app.route("/contact")
@with_translations
def contact():
    return render_template("contact.html")


@app.route("/contact", methods=["POST", "GET"])
def receive_data():
    if request.method == "POST":
        subject = request.form["subject"]
        name = request.form["name"]
        to_email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]

        # automatically send to the questioner
        send_email(to_email=to_email, name=name, phone=phone, subject=subject, message=message)

        return render_template('contact.html', msg_sent=True)
    else:
        return render_template('contact.html')


@app.route("/useful_info")
@with_translations
def useful_info():
    return render_template("useful_info.html")


@app.route('/weather', methods=["POST", "GET"])
@admin_only
@with_translations
def show_weather():
    if request.method == "POST":
        location = request.form["loc"]
        weather_data = get_weather_info(location)

    return render_template('weather.html', loc=location, weather_data=weather_data)


@app.route('/currency', methods=["POST"])
@admin_only
@with_translations
def get_currency():
    currency_data = get_currency_info()
    return currency_data


if __name__ == "__main__":
    app.run(debug=True)
