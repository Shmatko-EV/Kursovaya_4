from project.dao import GenreDAO
from project.dao.director import DirectorDAO
from project.dao.movie import MovieDAO
from project.dao.user import UserDAO

from project.services import GenresService
from project.services.directors_service import DirectorsService
from project.services.movies_service import MoviesService
from project.services.users_service import UsersService
from project.setup_db import db

director_dao = DirectorDAO(session=db.session)
genre_dao = GenreDAO(session=db.session)
movie_dao = MovieDAO(session=db.session)
user_dao = UserDAO(session=db.session)

director_service = DirectorsService(db.session)
genre_service = GenresService(db.session)
movie_service = MoviesService(db.session)
user_service = UsersService(db.session)
auth_service = UsersService(db.session)
