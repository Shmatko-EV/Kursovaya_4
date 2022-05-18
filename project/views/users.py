from flask import request
from flask_restx import Namespace, Resource, abort

from project.schemas.user import UserSchema
from implemented import user_service, auth_service
from project.utils import auth_required

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        """ Возвращает данные обо всех пользователях. """

        rs = user_service.get_all()
        res = UserSchema(many=True).dump(rs)
        return res, 200


@user_ns.route('/<int:uid>')
class UserView(Resource):
    @auth_required
    def get(self, uid):
        """ Возвращает данные об одном пользователе. """

        user = user_service.get_user(uid)
        sm_u = UserSchema().dump(user)
        return sm_u, 200

    @auth_required
    def put(self, uid):
        """ Обновляет данные пользователя."""

        # Получаем из запроса данные в виде JSON формата.
        req_json = request.json
        # Если не указан id пользователя в запросе, то приравниваем id к тому, что указано после /.
        if "id" not in req_json:
            req_json["id"] = uid
        # Обновляем строку в БД с новыми данными с помощью созданного сервера.
        user_service.update(req_json)
        return "", 204


@user_ns.route('/password')
class PasswordView(Resource):
    @auth_required
    def put(self):
        """ Обновляет пароль пользователя. """

        # Получаем из запроса данные о паролях в формате json.
        passwords = request.json
        # Если данных нет хотя бы в одном из полей, то возвращаем ошибку.
        if passwords.get('old_password') or passwords.get('new_password') is None:
            return abort(403)

        # Получаем токен пользователя из параметра запроса авторизации.
        user_data = request.headers['Authorization']
        token = user_data.split(' ')[-1]

        user = user_service.update_user_password(token, passwords)
        new_tokens = auth_service.login(user)

        return new_tokens, 204

