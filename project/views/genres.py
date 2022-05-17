from flask_restx import abort, Namespace, Resource

from implemented import genre_service
from project.exceptions import ItemNotFound

genre_ns = Namespace("genres")


@genre_ns.route("/")
class GenresView(Resource):
    @genre_ns.response(200, "OK")
    def get(self):
        """Get all genres"""
        return genre_service.get_all_genres()


@genre_ns.route("/<int:genre_id>")
class GenreView(Resource):
    @genre_ns.response(200, "OK")
    @genre_ns.response(404, "Genre not found")
    def get(self, genre_id: int):
        """Get genre by id"""
        try:
            return genre_service.get_item_by_id(genre_id)
        except ItemNotFound:
            abort(404, message="Genre not found")
