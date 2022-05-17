from project.dao import GenreDAO
from project.dao.director import DirectorDAO
from project.dao.movie import MovieDAO
from project.services import GenresService
from project.services.base import BaseService
from project.services.directors_service import DirectorsService
from project.services.movies_service import MoviesService
from project.setup_db import db

director_dao = DirectorDAO(session=db.session)
genre_dao = GenreDAO(session=db.session)
movie_dao = MovieDAO(session=db.session)
#user_dao = UserDAO(session=db.session)
#auth_dao = AuthDAO(session=db.session)

director_service = DirectorsService(db.session)
genre_service = GenresService(db.session)
movie_service = MoviesService(db.session)
#user_service = UsersService(dao=user_dao)
#auth_service = AuthService(dao=auth_dao)