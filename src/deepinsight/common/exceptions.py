"""Custom Exceptions"""


class NotFoundError(Exception):
    """数据未找到异常"""

    def __init__(self, model: type, id: str | None = None, uuid: str | None = None):
        if id is not None:
            super().__init__(f"{model.__name__} with id={id} not found")
        elif uuid is not None:
            super().__init__(f"{model.__name__} with uuid={uuid} not found")
        else:
            super().__init__(f"{model.__name__} not found")


class AlreadyExistsError(Exception):
    """数据已存在异常"""

    def __init__(self, model: type, id: str | None = None, uuid: str | None = None):
        if id is not None or uuid is not None:
            super().__init__(f"{model.__name__}({id or uuid}) already exists")
        else:
            super().__init__(f"{model.__name__} already exists")


class DoesNotExistError(Exception):
    """数据不存在异常"""

    def __init__(self, model: type, id: str | None = None):
        if id is not None:
            super().__init__(f"{model.__name__} with id={id} does not exist in database")
        else:
            super().__init__(f"{model.__name__} does not exist in database")
