from project.dao import GenreDAO
from project.exceptions import ItemNotFound
from project.schemas.genre import GenreSchema
from project.services.base import BaseService


class GenresService(BaseService):
    def get_item_by_id(self, pk):
        """ Возвращает данные одной строки из таблицы с помощью DAO и сериализации (схемы)."""

        genre = GenreDAO(self._db_session).get_by_id(pk)
        if not genre:
            raise ItemNotFound
        return GenreSchema().dump(genre)

    def get_all_genres(self):
        """ Возвращает все данные из таблицы с помощью DAO и сериализации (схемы)."""

        genres = GenreDAO(self._db_session).get_all()
        return GenreSchema(many=True).dump(genres)
