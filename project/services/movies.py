from typing import Optional

from project.services.base import BaseService


class MoviesService(BaseService):
    """ Сервис фильмов """

    def get_all(self, page: Optional[int] = None, status: Optional[str] = None) -> list:
        """
        Получаем все данные:
        :param page: выдаёт указанную страницу с определённым в конфигурации количеством элементов
        :param status: сортировка фильмов по году выпуска
        """
        return self.dao.get_all(page=page, status=status)
