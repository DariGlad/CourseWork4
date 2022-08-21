from flask_restx import Namespace, Resource

from project.container import genre_service, genre_schema
from project.setup.api.parsers import page_parser

api = Namespace('genres')


@api.route('/')
class GenresView(Resource):
    @api.expect(page_parser)
    def get(self):
        """
        Get all genres.
        """
        genres = genre_service.get_all(**page_parser.parse_args())
        return genre_schema.dump(genres, many=True), 200


@api.route('/<int:genre_id>/')
class GenreView(Resource):
    @api.response(404, 'Not Found')
    def get(self, genre_id: int):
        """
        Get genre by id.
        """
        genre = genre_service.get_item(genre_id)
        return genre_schema.dump(genre), 200
