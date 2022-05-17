from sqlalchemy import desc
from sqlalchemy.orm.scoping import scoped_session

from project.dao.models.movie import Movie


class MovieDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_by_id(self, pk):
        """ Делает запрос и получает данные одной строки из таблицы
        с помощью запроса к БД по id. Если нет такого id, то возвращает none."""

        return self._db_session.query(Movie).filter(Movie.id == pk).one_or_none()

    def get_all(self):
        """ Делает запрос и получает все данные из таблицы с помощью запроса к БД."""

        return self._db_session.query(Movie).all()

    def get_by_director_id(self, val):
        """ Возвращает список всех фильмов с id режиссера."""

        return self._db_session.query(Movie).filter(Movie.director_id == val).all()

    def get_by_genre_id(self, val):
        """ Возвращает список всех фильмов с id жанра."""

        return self._db_session.query(Movie).filter(Movie.genre_id == val).all()

    def get_by_year(self, val):
        """ Возвращает список всех фильмов с указанным годом."""

        return self._db_session.query(Movie).filter(Movie.year == val).all()

    def get_by_status(self):
        """ Возвращает список всех фильмов, отсортированных от большего года к меньшему,
         если указан статус new (из запроса)."""

        return self._db_session.query(Movie).order_by(desc("year")).all()

    def create(self, movie_d):
        """ Создает новый фильм в таблицу БД."""

        # Получаем данные о новом фильме.
        ent = Movie(**movie_d)
        # Добавляем и коммитим новые данные в таблицу БД.
        self._db_session.add(ent)
        self._db_session.commit()
        return ent

    def delete(self, rid):
        """ Удаляет данные фильма по его id."""

        movie = self.get_by_id(rid)
        self._db_session.delete(movie)
        self._db_session.commit()

    def update(self, movie_d):
        """ Обновляет данные фильма."""

        movie = self.get_by_id(movie_d.get("id"))

        movie.title = movie_d.get("title")
        movie.description = movie_d.get("description")
        movie.trailer = movie_d.get("trailer")
        movie.year = movie_d.get("year")
        movie.rating = movie_d.get("rating")
        movie.genre_id = movie_d.get("genre_id")
        movie.director_id = movie_d.get("director_id")

        self._db_session.add(movie)
        self._db_session.commit()
