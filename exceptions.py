"""Пользовательские исключения для психофармакологического бота-наставника."""


class DrugNotFoundError(Exception):
    """Исключение, возникающее при отсутствии информации о препарате."""
    pass


class InvalidInputError(Exception):
    """Исключение, возникающее при некорректном вводе пользователя."""
    pass


class QuizQuestionError(Exception):
    """Исключение, возникающее при ошибках в работе с викторинами."""
    pass


class DatabaseConnectionError(Exception):
    """Исключение, возникающее при проблемах с подключением к базе данных."""
    pass