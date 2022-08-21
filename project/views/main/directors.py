from flask_restx import Namespace, Resource

from project.container import director_service, director_schema
from project.setup.api.parsers import page_parser

api = Namespace('directors')


@api.route('/')
class DirectorsView(Resource):
    @api.expect(page_parser)
    def get(self):
        """
        Get all directors.
        """
        directors = director_service.get_all(**page_parser.parse_args())
        return director_schema.dump(directors, many=True), 200


@api.route('/<int:director_id>/')
class DirectorView(Resource):
    @api.response(404, 'Not Found')
    def get(self, director_id: int):
        """
        Get director by id.
        """
        director = director_service.get_item(director_id)
        return director_schema.dump(director), 200
