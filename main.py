from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_bootstrap import Bootstrap5
from weather import get_weather_info
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
Bootstrap5(app)


# Database
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


# configure the SQLite database, relative to the app instance folder
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
# initialize the app with the extension
db.init_app(app)


class Restaurants(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)


class Cafes(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    open_time: Mapped[str] = mapped_column(String(250), nullable=True)
    close_time: Mapped[str] = mapped_column(String(250), nullable=True)
    rating: Mapped[float] = mapped_column(Float, nullable=True)


with app.app_context():
    db.create_all()


# WTForms
class CafeForm(FlaskForm):
    name = StringField('Cafe Name', validators=[DataRequired()])
    location = StringField('Cafe Location on Google Map', validators=[DataRequired(), URL(message="Invalid URL")])
    open_time = StringField('Opening Time e.g. 8AM')
    close_time = StringField('Closing Time e.g. 4:30PM')
    rating = StringField('Cafe Rating e.g. 9.5 out of 10')

    submit = SubmitField('Submit')


class RateCafeForm(FlaskForm):
    rating = StringField("Cafe Rating e.g. 9.5 out of 10", validators=[DataRequired()])
    submit = SubmitField('Submit')


# Flask app
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/cafes')
def show_cafes():
    all_cafes = db.session.execute(db.select(Cafes).order_by(Cafes.id)).scalars().all()
    return render_template('cafes.html', cafes=all_cafes)


@app.route("/add", methods=["POST", "GET"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        cafe = Cafes(name=form.name.data,
                     location=form.location.data,
                     open_time=form.open_time.data,
                     close_time=form.close_time.data,
                     rating=form.rating.data)
        db.session.add(cafe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html", form=form)


@app.route('/edit', methods=["POST", "GET"])
def edit():
    form = RateCafeForm()
    cafe_id = request.args.get("id")
    cafe = db.get_or_404(Cafes, cafe_id)  # to check if the movie_id exists among Movie database.
    if form.validate_on_submit():
        cafe.rating = float(form.rating.data)
        db.session.commit()  # Commit the changes
        return redirect(url_for('home'))
    return render_template('edit.html', cafe=cafe, form=form)


@app.route('/delete')
def delete():
    print("access")
    cafe_id = request.args.get("id")
    cafe = db.get_or_404(Cafes, cafe_id)
    print(cafe_id)
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


if __name__ == "__main__":
    app.run(debug=True)
