class BaseException(Exception):
    """
    Базовый класс для всех кастомных ошибок
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class DatabaseError(BaseException):
    """
    Ошибка, связанная с получением данных из бд
    """

    pass


class AsyncFunctionError(BaseException):
    """
    Ошибка, связанная с асинхронными функциями
    """

    pass
