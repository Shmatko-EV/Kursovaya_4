from flask_restx import abort, Namespace, Resource

from implemented import director_service
from project.exceptions import ItemNotFound
from project.utils import auth_required

director_ns = Namespace("directors")


@director_ns.route("/")
class DirectorsView(Resource):
    @auth_required
    @director_ns.response(200, "OK")
    def get(self):
        """Get all directors"""

        return director_service.get_all_directors()


@director_ns.route("/<int:director_id>")
class DirectorView(Resource):
    @auth_required
    @director_ns.response(200, "OK")
    @director_ns.response(404, "Director not found")
    def get(self, director_id: int):
        """Get director by id"""

        try:
            return director_service.get_item_by_id(director_id)
        except ItemNotFound:
            abort(404)
