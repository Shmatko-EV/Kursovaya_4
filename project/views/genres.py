from flask_restx import abort, Namespace, Resource

from implemented import genre_service
from project.exceptions import ItemNotFound
from project.utils import auth_required

genre_ns = Namespace("genres")


@genre_ns.route("/")
class GenresView(Resource):
    @auth_required
    @genre_ns.response(200, "OK")
    def get(self):
        """Get all genres"""
        return genre_service.get_all_genres()


@genre_ns.route("/<int:genre_id>")
class GenreView(Resource):
    @auth_required
    @genre_ns.response(200, "OK")
    @genre_ns.response(404, "Genre not found")
    def get(self, genre_id: int):
        """Get genre by id"""
        try:
            return genre_service.get_item_by_id(genre_id), 200
        except ItemNotFound:
            abort(404)
