from flask import Blueprint, render_template, redirect, url_for, flash
from flask_app.models import db, User
from flask_app.utils import with_translations, super_admin_only, is_super_admin
from flask_app.forms import CSRFProtectionForm


admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin-dashboard')
@super_admin_only
@with_translations
def show_admin_dashboard():
    result = db.session.execute(db.select(User))
    users = result.scalars().all()
    form = CSRFProtectionForm()
    return render_template('admin-dashboard.html', all_users=users, form=form)


@admin_bp.route('/admin/change-role/<int:user_id>', methods=['POST'])
@super_admin_only
def change_role(user_id):
    form = CSRFProtectionForm()
    if form.validate_on_submit():
        user_to_change = db.get_or_404(User, user_id)

        # if the user exists or not
        if not user_to_change:
            flash('User not found.')
            return redirect(url_for('admin.show_admin_dashboard'))

        if is_super_admin(user_to_change):
            flash('You cannot change the super admin!')
            return redirect(url_for('admin.show_admin_dashboard'))

        # simply switch the role
        if user_to_change.role == 'admin':
            user_to_change.role = 'user'
        else:
            user_to_change.role = 'admin'

        db.session.commit()
        flash(f"{user_to_change.name} is now assigned the role '{user_to_change.role}'.")
        return redirect(url_for('admin.show_admin_dashboard'))
    else:
        flash('CSRF token missing or incorrect')
        return redirect(url_for('admin.show_admin_dashboard'))


@admin_bp.route('/admin/delete-user/<int:user_id>', methods=['POST'])
@super_admin_only
def delete_user(user_id):
    form = CSRFProtectionForm()
    if form.validate_on_submit():
        user_to_delete = db.get_or_404(User, user_id)

        if not user_to_delete:
            flash('User not found.')
            return redirect(url_for('admin.show_admin_dashboard'))

        if is_super_admin(user_to_delete):
            flash('You cannot delete the super admin!')
            return redirect(url_for('admin.show_admin_dashboard'))

        db.session.delete(user_to_delete)
        db.session.commit()
        flash(f"User '{user_to_delete.name}' has been deleted.")
        return redirect(url_for('admin.show_admin_dashboard'))

    else:
        flash("CSRF token missing or incorrect.")
        return redirect(url_for('admin.show_admin_dashboard'))
