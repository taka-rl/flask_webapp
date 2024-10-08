from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, logout_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_app import login_manager
from flask_app.utils import with_translations
from flask_app.forms import RegisterForm, LoginForm
from flask_app.models import db, User


auth_bp = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Use Werkzeug to hash the user's password when creating a new user.
@auth_bp.route('/register', methods=["POST", "GET"])
@with_translations
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Find user by email entered if it's already existed or not
        email = form.email.data
        user = db.session.execute(db.select(User).where(User.email == email)).scalar()

        if user:
            flash("You've already sighed up with that email, login instead!")
            return redirect(url_for('auth.login'))

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

            return redirect(url_for('blog.get_all_posts'))

    return render_template('register.html', form=form, current_user=current_user)


# Retrieve a user from the database based on their email.
@auth_bp.route('/login', methods=["POST", "GET"])
@with_translations
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # Find user by email entered
        user = db.session.execute(db.select(User).where(User.email == email)).scalar()

        # Check stored password hash against entered password hashed
        if not user and not check_password_hash(user.password, password):
            flash("The email or password entered is wrong! Please try again!")
            return redirect(url_for('auth.login'))

        else:
            login_user(user)
            return redirect(url_for('blog.get_all_posts'))

    return render_template("login.html", form=form, current_user=current_user)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('blog.get_all_posts'))
