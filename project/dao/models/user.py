from project.dao.models.base import BaseMixin
from project.setup_db import db


class User(BaseMixin, db.Model):
    """ Описывает модель пользователя."""

    __tablename__ = "users"

    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    favorite_genre = db.Column(db.String(100))
