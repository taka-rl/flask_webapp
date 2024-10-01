from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, Float
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


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
    pricing: Mapped[float] = mapped_column(String(15), nullable=True)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    category: Mapped[str] = mapped_column(String(15), nullable=True)
    location_url: Mapped[str] = mapped_column(String(250), nullable=True)

    # ***************Child Relationship*************#
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    place_author = relationship("User", back_populates="places")
