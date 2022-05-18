from sqlalchemy.orm.scoping import scoped_session
from project.dao.models.user import User


class UserDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_by_id(self, u_id):
        """ Делает запрос и получает данные одной строки (по id) из таблицы с помощью запроса к БД."""

        return self._db_session.query(User).filter(User.id == u_id).one_or_none()

    def get_by_email(self, email):
        """ Делает запрос и возвращает данные найденного пользователя по email. """

        return self._db_session.query(User).filter(User.email == email).one_or_none()

    def get_all(self):
        """ Делает запрос и получает все данные из таблицы с помощью запроса к БД."""

        return self._db_session.query(User).all()

    def create(self, **user_data):
        """ Создает нового пользователя в таблицу БД."""

        new_user = User(**user_data)
        self._db_session.add(new_user)
        self._db_session.commit()
        return new_user

    def update(self, user_data):
        """ Обновляет данные пользователя."""

        user = self.get_by_id(user_data.get("id"))
        user.name = user_data.get("name")
        user.surname = user_data.get("surname")
        user.favorite_genre = user_data.get("favorite_genre")

        self._db_session.add(user)
        self._db_session.commit()

    def password_update(self, user: User):
        """ Обновление пароля пользователя. """

        self._db_session.add(user)
        self._db_session.commit()

        return user
