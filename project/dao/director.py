from sqlalchemy.orm.scoping import scoped_session

from project.dao.models.director import Director


class DirectorDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_by_id(self, pk):
        """ Делает запрос и получает данные одной строки из таблицы
        с помощью запроса к БД по id. Если нет такого id, то возвращает none."""

        return self._db_session.query(Director).filter(Director.id == pk).one_or_none()

    def get_all(self):
        """ Делает запрос и получает все данные из таблицы с помощью запроса к БД."""

        return self._db_session.query(Director).all()
