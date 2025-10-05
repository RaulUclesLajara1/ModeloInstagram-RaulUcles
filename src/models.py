from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
db = SQLAlchemy()

followers = Table(

    "followers",

    db.metadata,

    Column("user_from_id", ForeignKey("user.id")),

    Column("user_to_id", ForeignKey("user.id"))

)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    posts: Mapped[List["Post"]] = relationship(back_populates="author")
    comments : Mapped[List["Comment"]] = relationship(back_populates="author")



    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "posts": [p.id for p in self.posts],
        }

class Post(db.Model):
    id : Mapped[int] = mapped_column(primary_key=True)
    user_id : Mapped [int] = mapped_column(ForeignKey("user.id"))
    author: Mapped["User"] = relationship(back_populates="posts")

    comments : Mapped[List["Comment"]] = relationship(back_populates="post")
    medias : Mapped[List["Media"]] = relationship(back_populates="post")
    def serialize (self):
        return {
            "id" : self.id,
            "user" : self.user_id,
        }


class Comment(db.Model):
    id : Mapped[int] = mapped_column(primary_key=True)
    comment_text : Mapped[str] = mapped_column(nullable=False)
    post_id : Mapped[int] = mapped_column(ForeignKey("post.id"))
    author_id : Mapped[int] = mapped_column(ForeignKey("user.id"))
    post : Mapped["Post"] = relationship(back_populates = "comments")
    author : Mapped["User"] = relationship(back_populates = "comments")

    def serialize(self):
        return{
            "id" : self.id,
            "comment_text" : self.comment_text,
            "author" : self.author_id,
            "post" : self.post_id
        }


class Media(db.Model):
    id : Mapped[int] = mapped_column(primary_key=True)
    
    url : Mapped[str] = mapped_column(nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post : Mapped["Post"] = relationship(back_populates="medias")

    def serialize(self):
        return{
            "id" : self.id,
            "url" : self.url,
            "post" : self.post_id
        }