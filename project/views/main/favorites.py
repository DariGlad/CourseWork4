from flask import request
from flask_restx import Namespace, Resource

from project.container import auth_service, user_service, favorite_service, movie_schema

from project.tools import auth_required

api = Namespace('favorites')


@api.route('/movies/')
class FavoritesView(Resource):
    @auth_required
    def get(self):
        """
        Get all favorites users.
        """

        token = request.headers["Authorization"].split("Bearer ")[-1]
        data = auth_service.decode_token(token)
        email = data["email"]
        user = user_service.get_email(email)
        favorites = favorite_service.get_user_favorite(user.id)
        return movie_schema.dump(favorites, many=True), 200


@api.route('/movies/<int:movie_id>/')
class FavoriteView(Resource):
    @api.response(204, "Created")
    @auth_required
    def post(self, movie_id):
        """ Добавляет фильм в избранное """

        token = request.headers["Authorization"].split("Bearer ")[-1]
        data = auth_service.decode_token(token)
        email = data["email"]
        user = user_service.get_email(email)
        favorite_service.create(user.id, movie_id)
        return "", 204

    @api.response(204, "Created")
    @auth_required
    def delete(self, movie_id):
        """ Удаляет фильм из избранного """

        token = request.headers["Authorization"].split("Bearer ")[-1]
        data = auth_service.decode_token(token)
        email = data["email"]
        user = user_service.get_email(email)
        favorite_service.delete(user.id, movie_id)
        return "", 204
