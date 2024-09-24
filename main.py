from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, Float
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm, CafeForm, RateCafeForm
from weather import get_weather_info
from currency import get_currency_info
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
ckeditor = CKEditor(app)
Bootstrap5(app)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLES
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(20))

    # This will act like a List of BlogPost objects attached to each User.
    # The "author" refers to the author property in the BlogPost class.
    posts = relationship("BlogPost", back_populates="blog_author")

    # ******* Parent relationship*******#
    # "comment_author" refers to the comment_author property in the Comment class.
    comments = relationship("Comment", back_populates="comment_author")

    places = relationship("Place", back_populates="place_author")


class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Create Foreign Key, "user.id" the users refers to the tablename of User.
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    # Create reference to the User object. The "posts" refers to the posts property in the User class.
    blog_author = relationship("User", back_populates="posts")

    title: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(10), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

    # *************** Parent Relationship *************#
    comments = relationship("Comment", back_populates="parent_post")


class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # *******Add child relationship******* #
    # "users.id" The users refers to the tablename of the Users class.
    # "comments" refers to the comments property in the User class.
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    comment_author = relationship("User", back_populates="comments")

    # *************** Child Relationship *************#
    post_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("blog_posts.id"))
    parent_post = relationship("BlogPost", back_populates="comments")
    text: Mapped[str] = mapped_column(Text, nullable=False)


class Place(db.Model):
    __tablename__ = "places"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    location: Mapped[str] = mapped_column(String(50), nullable=False)
    open_time: Mapped[str] = mapped_column(String(10), nullable=True)
    close_time: Mapped[str] = mapped_column(String(10), nullable=True)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    category: Mapped[str] = mapped_column(String(15), nullable=True)
    location_url: Mapped[str] = mapped_column(String(250), nullable=True)

    # ***************Child Relationship*************#
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    place_author = relationship("User", back_populates="places")


with app.app_context():
    db.create_all()


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.id != 1:
            return abort(code=403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


# Use Werkzeug to hash the user's password when creating a new user.
@app.route('/register', methods=["POST", "GET"])
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
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts, current_user=current_user)


# Allow logged-in users to comment on posts
@app.route("/post/<int:post_id>", methods=["GET", "POST"])
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
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
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
        author=post.author,
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
@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/hobby")
def hobby():
    return render_template("hobby.html")


@app.route("/useful_info")
def useful_info():
    return render_template("useful_info.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route('/cafes')
def show_cafes():
    all_cafes = []
    return render_template('cafes.html', cafes=all_cafes)


@app.route("/add", methods=["POST", "GET"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        place = Place(name=form.name.data,
                      location=form.location.data,
                      open_time=form.open_time.data,
                      close_time=form.close_time.data,
                      rating=form.rating.data)
        db.session.add(place)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html", form=form)


@app.route('/edit-place/<int:place_id>', methods=["POST", "GET"])
def edit_place(place_id):
    form = RateCafeForm()
    cafe = db.get_or_404(Place, place_id)  # to check if the movie_id exists among Movie database.
    if form.validate_on_submit():
        cafe.rating = float(form.rating.data)
        db.session.commit()  # Commit the changes
        return redirect(url_for('home'))
    return render_template('edit.html', cafe=cafe, form=form)


@app.route('/delete/<int:place_id>')
def delete_place(place_id):
    print("access")
    cafe = db.get_or_404(Place, place_id)
    print(place_id)
    if not cafe == 404:
        db.session.delete(cafe)
        db.session.commit()
    else:
        print("access fail")
    return redirect(url_for('home'))


@app.route('/weather', methods=["POST", "GET"])
def show_weather():
    if request.method == "POST":
        location = request.form["loc"]
        weather_data = get_weather_info(location)

    return render_template('weather.html', loc=location, weather_data=weather_data)


@app.route('/currency', methods=["POST"])
def get_currency():
    currency_data = get_currency_info()
    return currency_data


if __name__ == "__main__":
    app.run(debug=True, port=5002)
