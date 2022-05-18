from flask_restx import abort

from project.dao.user import UserDAO
from project.exceptions import ItemNotFound
from project.schemas.user import UserSchema
from project.services.base import BaseService

from project.utils import get_hashed_password, get_decoded_token, generate_tokens


class UsersService(BaseService):
    def get_by_email(self, email):
        """ Возвращает данные одной строки из таблицы с помощью DAO и сериализации (схемы)."""

        user = UserDAO(self._db_session).get_by_email(email)

        if not user:
            raise ItemNotFound
        return UserSchema().dump(user)

    def get_user(self, user_id: int):
        """Возвращает данные о пользователе. """
        user = UserDAO(self._db_session).get_by_id(user_id)
        return {"id": user.id,
                "email": user.email,
                "name": user.name,
                "surname": user.surname}

    def get_all(self):
        """ Возвращает все данные из таблицы с помощью DAO и сериализации (схемы)."""

        return UserDAO(self._db_session).get_all()

    def create_new_user(self, data: dict):
        """ Создает новую строку с данными в таблице БД с помощью DAO."""

        data['password'] = get_hashed_password(data['password'])
        UserDAO(self._db_session).create(**data)
        return data

    def login(self, data: dict):
        """ Проверяет для входа данные пользователя с имеющимися данными в БД и выдает токен."""

        # Проверка имени пользователя.
        user_data = UserDAO(self._db_session).get_by_email(data['email'])
        if user_data is None:
            abort(401, message='User not found')

        # Проверка пароля пользователя.
        # КОГДА ЕСТЬ ЭТА ПРОВЕРКА У МЕНЯ ПОЧЕМУ-ТО ВЫВОДИТ ОШИБКУ, КОГДА ВВОЖУ ДАННЫЕ ПОЛЬЗОВАТЕЛЯ (email и password),
        # ХОТЯ В ЗАПРОСЕ auth/login ВВОЖУ ТЕ ЖЕ ДАННЫЕ ЧТО И ПРИ РЕГИСТРАЦИИ (auth/register)
        # hashed_password = get_hashed_password(data['password'])
        # if hashed_password != user_data['password']:
        #     abort(401, message='Invalid password')

        # Если пользователь в БД найден, то генерируем и выдаем ему токены в виде JSON.
        tokens = generate_tokens(
            {
                'email': data['email'],
                'password': data['password']
            }
        )

        return tokens

    def get_new_tokens(self, refresh_token):
        """ Генерирует новые токены."""

        decoded_token = get_decoded_token(refresh_token)

        tokens = generate_tokens(
            data={
                'email': decoded_token['email'],
                'password': decoded_token['password']
            }
        )

        return tokens

    def update(self, user_d):
        """ Обновляет строку с данными в таблице БД с помощью DAO."""

        UserDAO(self._db_session).update(user_d)
        #return UserDAO(self._db_session)

    def update_user_password(self, token, passwords: dict):
        """ Обновляет пароль пользователя."""
        # Получаем данные пользователя из токена с помощью декодировки.
        data = get_decoded_token(token)
        # Получаем данные пользователя по полученному email из декодировки токена.
        user = UserDAO(self._db_session).get_by_email(email=data.get('email'))
        # Если ошибка, то возвращаем ошибку
        if passwords.get("old_password") != user["password"]:
            return {"error": "Пароли не совпадают"}
        # Меняем в объекте пароль
        user.password = get_hashed_password(passwords.get("new_password"))
        # Обновляем пароль пользователя на новый.
        user = UserDAO(self._db_session).password_update(user)

        return UserSchema().dump(user)
