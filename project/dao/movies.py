from typing import Optional, List

from flask_sqlalchemy import BaseQuery
from werkzeug.exceptions import NotFound

from project.dao.base import BaseDAO
from project.dao.models import Movie


class MoviesDAO(BaseDAO[Movie]):
    __model__ = Movie

    def get_all(self, page: Optional[int] = None, status: Optional[str] = None) -> List[Movie]:
        """
        Получаем все данные:
        :param page: выдаёт указанную страницу с определённым в конфигурации количеством элементов
        :param status: сортировка фильмов по году выпуска
        """
        stmt: BaseQuery = self._db_session.query(self.__model__)
        if status == "new":
            stmt = stmt.order_by(-self.__model__.year)
        if page:
            try:
                return stmt.paginate(page, self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()
