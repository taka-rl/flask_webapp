from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from flask_app.utils import with_translations, admin_only
from flask_app.models import Place
from flask_app.forms import CreatePlaceForm
from flask_app.models import db

collection_bp = Blueprint('collection', __name__)


@collection_bp.route("/collection")
@with_translations
def collection():
    return render_template("collection.html")


@collection_bp.route('/places')
@with_translations
def show_places():
    result = db.session.execute(db.select(Place))
    all_places = result.scalars().all()
    return render_template('places.html', places=all_places, current_user=current_user)


@collection_bp.route("/add-place", methods=["POST", "GET"])
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
        return redirect(url_for('collection.show_places'))
    return render_template("add-place.html", form=form)


@collection_bp.route('/edit-place/<int:place_id>', methods=["POST", "GET"])
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
        return redirect(url_for('collection.show_places'))
    return render_template('add-place.html', place=place, form=edit_form, is_edit=True)


@collection_bp.route('/delete-place/<int:place_id>', methods=['POST'])
@admin_only
def delete_place(place_id):
    place_to_delete = db.get_or_404(Place, place_id)
    db.session.delete(place_to_delete)
    db.session.commit()
    return redirect(url_for('collection.show_places'))
