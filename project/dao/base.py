from typing import Generic, List, Optional, TypeVar

from flask import current_app
from flask_sqlalchemy import BaseQuery
from sqlalchemy.orm import scoped_session
from werkzeug.exceptions import NotFound
from project.setup.db.models import Base

T = TypeVar('T', bound=Base)


class BaseDAO(Generic[T]):
    """ Базовый доступ к данным """
    __model__ = Base

    def __init__(self, db_session: scoped_session) -> None:
        self._db_session = db_session

    @property
    def _items_per_page(self) -> int:
        return current_app.config['ITEMS_PER_PAGE']

    def get_by_id(self, pk: int) -> Optional[T]:
        """ Возвращает данные по id """
        return self._db_session.query(self.__model__).get_or_404(pk)

    def get_all(self, page: Optional[int] = None) -> List[T]:
        """
        Получаем все данные:
        :param page: выдаёт указанную страницу с определённым в конфигурации количеством элементов
        """
        stmt: BaseQuery = self._db_session.query(self.__model__)
        if page:
            try:
                return stmt.paginate(page, self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()

    def create(self, data):
        """ Создаёт запись в базе данных """

        model = self.__model__(**data)
        self._db_session.add(model)
        self._db_session.commit()

    def delete(self, pk):
        """ Удаляем запись из базы данных по id """

        model = self.get_by_id(pk)
        self._db_session.delete(model)
        self._db_session.commit()

    def check_is_dict(self, data):
        """ Проверка на то, что данные являются словарём """

        if not isinstance(data, dict):
            raise TypeError("Неверный формат данных")
