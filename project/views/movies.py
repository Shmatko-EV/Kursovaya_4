from flask import request
from flask_restx import Resource, Namespace

from implemented import movie_service
from project.schemas.movie import MovieSchema

movie_ns = Namespace('movies')


@movie_ns.route('/')
class MoviesView(Resource):
    #@auth_required
    def get(self):
        """ Возвращает данные о всех фильмах. """

        # Если в аргументах запроса есть id режиссера/жанра, год, кол-во строк (page) или статус(new),
        # то выводим список фильмов с этим режиссером/жанром/годом/page/статусом.
        director = request.args.get("director_id")
        genre = request.args.get("genre_id")
        year = request.args.get("year")
        page = request.args.get("page")
        status = request.args.get("status")

        filters = {
            "director_id": director,
            "genre_id": genre,
            "year": year,
            "status": status
        }
        all_movies = movie_service.get_all_movies(filters)
        # Если в фильтрах (запросе) есть параметр pagination (кол-во строк, кот. нужно показать),
        # то выводим именно столько фильмов.
        if page:
            all_movies = all_movies[:int(page)]

        res = MovieSchema(many=True).dump(all_movies)
        return res, 200

    #@admin_required
    def post(self):
        """ Создает новые данные нового фильма."""

        # Получаем из запроса данные в виде JSON формата.
        req_json = request.json
        # Создаем строку в БД с новыми данными с помощью созданного сервера.
        movie = movie_service.create(req_json)
        return "", 201, {"location": f"/movies/{movie.id}"}


@movie_ns.route('/<int:m_id>')
class MovieView(Resource):
    #@auth_required
    def get(self, m_id):
        """ Возвращает данные об одном фильме. """

        movie = movie_service.get_item_by_id(m_id)
        sm_d = MovieSchema().dump(movie)
        return sm_d, 200

    #@admin_required
    def put(self, m_id):
        """ Обновляет данные фильма."""

        # Получаем из запроса данные в виде JSON формата.
        req_json = request.json
        # Если не указан id фильма в запросе, то приравниваем id к тому, что указано после /.
        if "id" not in req_json:
            req_json["id"] = m_id
        # Обновляем строку в БД с новыми данными с помощью созданного сервера.
        movie_service.update(req_json)
        return "", 204

    #@admin_required
    def delete(self, m_id):
        """ Удаляет данные фильма."""

        movie_service.delete(m_id)
        return "", 204
