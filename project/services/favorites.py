from project.exceptions import ItemNotFound
from project.services.base import BaseService


class FavoritesService(BaseService):
    """ Сервис избранного"""

    def create(self, user_id, movie_id):
        data = {
            "user_id": user_id,
            "movie_id": movie_id
        }
        return self.dao.create(data)

    def get_user_favorite(self, user_id):
        favorites = self.dao.get_user_favorite(user_id)
        if not favorites:
            raise ItemNotFound("Not Found")
        return favorites

    def delete(self, user_id, movie_id):
        data = self.dao.get_favorite(user_id, movie_id)
        self.dao.delete(data)
