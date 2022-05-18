import base64
import calendar
import datetime
import json
import jwt
from flask import request
from flask_restx import abort

from project.constants import SECRET_KEY, JWT_ALGORITHM, TOKEN_EXPIRE_MINUTES, TOKEN_EXPIRE_DAYS
from project.tools.security import generate_password_digest


def read_json(filename, encoding="utf-8"):
    with open(filename, encoding=encoding) as f:
        return json.load(f)


def get_hashed_password(password: str):
    """ Хеширование пароля."""

    return base64.b64encode(generate_password_digest(password)).decode('utf-8')


def generate_tokens(data: dict):
    """ Генерирует пару токенов и отдает их в виде JSON."""

    exp_minutes = datetime.datetime.utcnow() + datetime.timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    data['exp'] = calendar.timegm(exp_minutes.timetuple())
    data['refresh_token'] = False
    access_token = jwt.encode(data, SECRET_KEY, algorithm=JWT_ALGORITHM)

    exp_days = datetime.datetime.utcnow() + datetime.timedelta(days=TOKEN_EXPIRE_DAYS)
    data['exp'] = calendar.timegm(exp_days.timetuple())
    data['refresh_token'] = True
    refresh_token = jwt.encode(data, SECRET_KEY, algorithm=JWT_ALGORITHM)

    return {'access_token': access_token, 'refresh_token': refresh_token}


def get_decoded_token(token):
    """ Декодировка токена."""

    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=JWT_ALGORITHM)
    return decoded_token


def update_token(refresh_token):
    """ Проверяет refresh_token, если он валиден, то возвращает обновленные токены. """
    try:
        decoded_token = get_decoded_token(refresh_token)

    except Exception as e:
        return {"error": f"Ошибка обработки {e}"}, 401

    return generate_tokens(decoded_token)


def get_token_by_headers(headers):
    """ Возвращает токен из заголовка запроса."""

    # Проверяем есть ли в запросе заголовок авторизации с токеном.
    if 'Authorization' not in headers:
        abort(401, 'Необходимо авторизоваться для доступа')

    # Из запроса берем необходимую часть токена.
    data_request = headers['Authorization']
    token = data_request.split(' ')[-1]

    return token


def auth_required(func):
    def wrapper(*args, **kwargs):
        """ Проверка авторизации пользователя."""

        # Получаем токен из запроса.
        token = get_token_by_headers(request.headers)

        # Раскодируем токен.
        get_decoded_token(token)

        return func(*args, **kwargs)
    return wrapper
