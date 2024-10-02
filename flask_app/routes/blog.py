from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user
from flask_app.utils import with_translations, admin_only
from flask_app.models import db, BlogPost, Comment
from flask_app.forms import CommentForm, CreatePostForm
from datetime import date

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/')
@with_translations
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()

    return render_template("index.html",
                           all_posts=posts, current_user=current_user)


# Allow logged-in users to comment on posts
@blog_bp.route("/post/<int:post_id>", methods=["GET", "POST"])
@with_translations
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    comment_form = CommentForm()

    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.")
            return redirect(url_for("auth.login"))

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
@blog_bp.route("/new-post", methods=["GET", "POST"])
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
@blog_bp.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
@with_translations
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
@blog_bp.route("/delete-post/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))
