"""Исключения проекта mcp-russia."""


class OshibkaMcpRussia(Exception):
    """Базовое исключение для всех ошибок mcp-russia."""


class OshibkaFunktsii(OshibkaMcpRussia):
    """Ошибка, связанная с функцией (обнаружение, валидация и т.д.)."""  # noqa: RUF002


class OshibkaHttpClienta(OshibkaMcpRussia):
    """Ошибка HTTP-соединения с внешним API."""  # noqa: RUF002


class OshibkaAutentifikatsii(OshibkaMcpRussia):
    """Отсутствует или недействительна учётная запись для доступа к защищённому API."""


OshibkaFunktsii.__module__ = __name__
OshibkaHttpClienta.__module__ = __name__
OshibkaAutentifikatsii.__module__ = __name__
