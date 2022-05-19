from flask import request
from flask_restx import Namespace, Resource, abort

from implemented import auth_service
from project.schemas.user import UserSchema
from project.utils import get_hashed_password, auth_required

auth_ns = Namespace('auth')


@auth_ns.route('/register')
class AuthView(Resource):

    @auth_ns.response(200, "OK")
    def post(self):
        """ Получая из запроса email и пароль, создаем пользователя в системе."""
        # Получаем данные из запроса.
        req_json = request.json

        # Выполняем добавление пользователя в таблицу.
        auth_service.create_new_user(req_json)

        return "", 201


@auth_ns.route('/login')
class LoginView(Resource):

    @auth_ns.response(200, "OK")
    def post(self):
        try:
            # Получаем данные из запроса.
            data = request.json

            # Получаем из таблицы БД данные о пользователя.
            user = auth_service.get_by_email(email=data.get('email'))

            if user['email'] != data['email']:
                return abort(404, message='Нет данных')

            email, password = data.get('email'), data.get('password')

            # Если есть None в одном из полей, то блокируем
            if None in [email, password]:
                return abort(404, message='Нет данных')

            # Получение токенов.
            tokens = auth_service.login(data)
            return tokens, 201

        except TypeError as e:
            return f'Ошибка загрузки данных {e}', 500

    @auth_required
    def put(self):
        """ Генерирует и возвращает словарь с новыми токенами."""

        return auth_service.get_new_tokens(request.json.get('refresh_token'))
