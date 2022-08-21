from flask_restx import Namespace, Resource

from project.container import movie_service, movie_schema
from project.setup.api.parsers import page_parser, status_parser

api = Namespace('movies')


@api.route('/')
class MoviesView(Resource):
    @api.expect(page_parser, status_parser)
    def get(self):
        """
        Get all movies.
        """
        movies = movie_service.get_all(**page_parser.parse_args(), **status_parser.parse_args())
        return movie_schema.dump(movies, many=True), 200


@api.route('/<int:movie_id>/')
class MovieView(Resource):
    @api.response(404, 'Not Found')
    def get(self, movie_id: int):
        """
        Get movie by id.
        """
        movie = movie_service.get_item(movie_id)
        return movie_schema.dump(movie), 200
