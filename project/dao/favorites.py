from project.dao.base import BaseDAO
from project.dao.models import Favorite, Movie


class FavoritesDAO(BaseDAO[Favorite]):
    __model__ = Favorite

    def get_user_favorite(self, user_id):
        """ Получает избранные фильмы по id пользователя """

        return self._db_session.query(Movie). \
            join(self.__model__). \
            filter(self.__model__.user_id == user_id). \
            all()

    def get_favorite(self, user_id, movie_id):
        """ Возвращает данные избранного фильма пользователя """

        return self._db_session.query(self.__model__). \
            filter(self.__model__.user_id == user_id, self.__model__.movie_id == movie_id). \
            first_or_404("Not Found")
