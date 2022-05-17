from project.dao.movie import MovieDAO
from project.exceptions import ItemNotFound
from project.schemas.movie import MovieSchema
from project.services.base import BaseService


class MoviesService(BaseService):
    def get_item_by_id(self, pk):
        """ Возвращает данные одной строки из таблицы с помощью DAO и сериализации (схемы)."""

        movie = MovieDAO(self._db_session).get_by_id(pk)
        if not movie:
            raise ItemNotFound
        return MovieSchema().dump(movie)

    def get_all_movies(self, filters):
        """ Возвращает все данные из таблицы с помощью DAO и сериализации (схемы),
        если есть доп. параметры запроса, то фильтруем по ним данные."""

        # Если, есть доп. параметры запроса, то фильтруем все данные по запросу.
        if filters.get("director_id") is not None:
            movies = MovieDAO(self._db_session).get_by_director_id(filters.get("director_id"))
        elif filters.get("genre_id") is not None:
            movies = MovieDAO(self._db_session).get_by_genre_id(filters.get("genre_id"))
        elif filters.get("year") is not None:
            movies = MovieDAO(self._db_session).get_by_year(filters.get("year"))
        elif filters.get("status") == "new":
            movies = MovieDAO(self._db_session).get_by_status()
        else:
            movies = MovieDAO(self._db_session).get_all()
        return movies

    def create(self, movie_d):
        """ Создает новую строку с данными в таблице БД с помощью DAO."""

        return MovieDAO(self._db_session).create(movie_d)

    def update(self, movie_d):
        """ Обновляет строку с данными в таблице БД с помощью DAO."""

        MovieDAO(self._db_session).update(movie_d)
        return MovieDAO(self._db_session)

    def delete(self, rid):
        """ Удаляет строку с данными в таблице БД с помощью DAO."""

        MovieDAO(self._db_session).delete(rid)

