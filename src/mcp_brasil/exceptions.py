"""Исключения проекта mcp-russia."""


class McpRussiaError(Exception):
    """Базовое исключение для всех ошибок mcp-russia."""


McpBrasilError = McpRussiaError


class FeatureError(McpRussiaError):
    """Ошибка, связанная с функцией (обнаружение, валидация и т.д.)."""  # noqa: RUF002


class HttpClientError(McpRussiaError):
    """Ошибка HTTP-соединения с внешним API."""  # noqa: RUF002


class AuthError(McpRussiaError):
    """Отсутствует или недействительна учётная запись для доступа к защищённому API."""
