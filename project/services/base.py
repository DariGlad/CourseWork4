from typing import Optional


class BaseService:
    def __init__(self, dao) -> None:
        self.dao = dao

    def get_item(self, pk: int):
        return self.dao.get_by_id(pk)

    def get_all(self, page: Optional[int] = None) -> list:
        return self.dao.get_all(page=page)

    def check_is_dict(self, data):
        return self.dao.check_is_dict(data)
