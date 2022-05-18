from flask import Flask
from flask_cors import CORS
from flask_restx import Api

from project.setup_db import db
from project.views.auth import auth_ns
from project.views.directors import director_ns
from project.views.genres import genre_ns
from project.views.movies import movie_ns
from project.views.users import user_ns

api = Api(
    authorizations={
        "Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}
    },
    title="Flask Course Project 3",
    doc="/docs",
)

# Нужно для работы с фронтендом.
cors = CORS()


def create_app(config_obj):
    """ Создает приложение: данные таблиц БД и регистрация эндпоинтов. """
    app = Flask(__name__)
    app.config.from_object(config_obj)

    cors.init_app(app)
    db.init_app(app)
    api.init_app(app)

    # Регистрация эндпоинтов
    api.add_namespace(genre_ns)
    api.add_namespace(movie_ns)
    api.add_namespace(director_ns)
    api.add_namespace(user_ns)
    api.add_namespace(auth_ns)

    return app
