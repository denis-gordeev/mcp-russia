"""Исключения проекта mcp-russia."""


class McpRussiaError(Exception):
    """Базовое исключение для всех ошибок mcp-russia."""


class OshibkaFunktsii(McpRussiaError):
    """Ошибка, связанная с функцией (обнаружение, валидация и т.д.)."""  # noqa: RUF002


class OshibkaHttpClienta(McpRussiaError):
    """Ошибка HTTP-соединения с внешним API."""  # noqa: RUF002


class OshibkaAutentifikatsii(McpRussiaError):
    """Отсутствует или недействительна учётная запись для доступа к защищённому API."""


OshibkaFunktsii.__module__ = __name__
OshibkaHttpClienta.__module__ = __name__
OshibkaAutentifikatsii.__module__ = __name__

FeatureError = OshibkaFunktsii
HttpClientError = OshibkaHttpClienta
AuthError = OshibkaAutentifikatsii
