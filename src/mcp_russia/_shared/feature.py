"""Метаданные функций и автоматический реестр mcp-russia.

Модуль реализует автоматическое обнаружение функций на основе конвенции.
Любой подпакет mcp_russia, экспортирующий FEATURE_META и содержащий
server.py с объектом `mcp`, будет автоматически обнаружен,
провалидирован и смонтирован на корневой сервер.

Подход вдохновлён: Flask blueprints, Django app registry,
pytest plugin discovery, FastAPI router auto-include.

Полное обоснование — см. ADR-002.

Использование:
    from fastmcp import FastMCP
    from mcp_russia._shared.feature import FeatureRegistry

    mcp = FastMCP("mcp-russia")
    registry = FeatureRegistry()
    registry.discover()
    registry.mount_all(mcp)
"""

from __future__ import annotations

import importlib
import logging
import os
import pkgutil
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import mcp_russia.settings  # noqa: F401 — убедиться, что .env загружен до проверки переменных окружения

if TYPE_CHECKING:
    from fastmcp import FastMCP

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class FeatureMeta:
    """Декларативные метаданные функции.

    Каждая функция должна экспортировать экземпляр FEATURE_META в своём __init__.py.
    Реестр использует эти метаданные для обнаружения, валидации, документации
    и решений во время выполнения (авторизация, флаги функций).

    Example:
        # src/mcp_russia/rosstat/__init__.py
        from mcp_russia._shared.feature import FeatureMeta

        FEATURE_META = FeatureMeta(
            name="rosstat",
            description="Росстат: демография, ВРП, социальные показатели",
            api_base="https://rosstat.gov.ru/api",
        )
    """

    name: str
    description: str
    version: str = "0.1.0"
    api_base: str = ""
    requires_auth: bool = False
    auth_env_var: str | None = None
    enabled: bool = True
    tags: list[str] = field(default_factory=list)

    def is_auth_available(self) -> bool:
        """Проверка доступности учётных данных аутентификации."""
        if not self.requires_auth:
            return True
        if self.auth_env_var is None:
            return False
        return bool(os.environ.get(self.auth_env_var))


@dataclass
class RegisteredFeature:
    """Обнаруженная, провалидированная и зарегистрированная функция."""

    meta: FeatureMeta
    server: FastMCP
    module_path: str


class FeatureRegistry:
    """Автоматический реестр: обнаружение, валидация и монтирование функций.

    Использует pkgutil.iter_modules() для сканирования подпакетов mcp_russia,
    импортирует те, что следуют конвенции (FEATURE_META + server.mcp),
    и монтирует их на корневой FastMCP-сервер.

    Конвенция (все условия обязательны для автообнаружения):
        1. Подпакет mcp_russia/ (директория с __init__.py)
        2. Имя НЕ начинается с '_'
        3. __init__.py экспортирует FEATURE_META: FeatureMeta
        4. server.py экспортирует mcp: FastMCP
        5. Если requires_auth=True, auth_env_var должен быть задан в окружении

    Для отключения функции: установите enabled=False в FEATURE_META.
    """

    def __init__(self) -> None:
        """Инициализация пустого реестра функций."""
        self._features: dict[str, RegisteredFeature] = {}
        self._skipped: dict[str, str] = {}

    @property
    def features(self) -> dict[str, RegisteredFeature]:
        """Все обнаруженные и зарегистрированные функции."""
        return dict(self._features)

    @property
    def skipped(self) -> dict[str, str]:
        """Пропущенные функции с причинами."""
        return dict(self._skipped)

    def discover(self, package_name: str = "mcp_russia") -> FeatureRegistry:
        """Обнаружение всех функций в пакете.

        Сканирует подпакеты `package_name` и регистрирует те, что
        следуют конвенции. Функции с ошибками валидации логируются
        как предупреждения и пропускаются — они не ломают сервер.

        Args:
            package_name: Базовый пакет для сканирования. По умолчанию: «mcp_russia».

        Returns:
            self для цепочки вызовов: registry.discover().mount_all(mcp)
        """
        package = importlib.import_module(package_name)

        for _finder, name, ispkg in pkgutil.iter_modules(package.__path__, package.__name__ + "."):
            short_name = name.rsplit(".", 1)[-1]

            # Пропуск не-пакетов и приватных модулей
            if not ispkg or short_name.startswith("_"):
                continue

            try:
                self._try_register(name, short_name)
            except Exception as exc:
                reason = str(exc)
                self._skipped[short_name] = reason
                logger.warning("Feature '%s' skipped: %s", short_name, reason)

        return self

    def _try_register(self, module_path: str, short_name: str) -> None:
        """Попытка импорта и регистрации отдельной функции."""
        # Шаг 1: Импорт __init__.py функции
        feature_module = importlib.import_module(module_path)

        # Шаг 2: Проверка наличия и корректности FEATURE_META
        meta = getattr(feature_module, "FEATURE_META", None)
        if meta is None:
            raise ValueError(f"No FEATURE_META in {module_path}")

        if not isinstance(meta, FeatureMeta):
            raise TypeError(f"FEATURE_META in {module_path} is not a FeatureMeta instance")

        # Шаг 3: Проверка активности функции
        if not meta.enabled:
            self._skipped[short_name] = "disabled (enabled=False)"
            logger.info("Feature '%s' is disabled, skipping.", short_name)
            return

        # Шаг 4: Проверка аутентификации при необходимости
        if not meta.is_auth_available():
            self._skipped[short_name] = f"missing env var {meta.auth_env_var}"
            logger.warning(
                "Feature '%s' requires %s (not set), skipping.",
                short_name,
                meta.auth_env_var,
            )
            return

        # Шаг 5: Импорт server.py и получение объекта mcp
        server_module = importlib.import_module(f"{module_path}.server")
        server = getattr(server_module, "mcp", None)

        if server is None:
            raise ValueError(f"No `mcp` object in {module_path}.server")

        # Шаг 6: Регистрация
        self._features[short_name] = RegisteredFeature(
            meta=meta,
            server=server,
            module_path=module_path,
        )
        logger.info(
            "Registered feature '%s' v%s",
            meta.name,
            meta.version,
        )

    def mount_all(self, root_server: FastMCP) -> None:
        """Монтирование всех обнаруженных функций на корневой сервер.

        Каждая функция получает пространство имён по названию
        (напр. инструменты становятся rosstat_poluchit_*).

        Args:
            root_server: Корневой FastMCP-сервер для монтирования функций.
        """
        for name, feature in sorted(self._features.items()):
            root_server.mount(feature.server, namespace=name)
            logger.info("Mounted '%s' — %s", name, feature.meta.description)

    def summary(self) -> str:
        """Читаемая сводка зарегистрированных функций.

        Полезно для логирования при запуске и генерации документации.
        """
        lines = [
            f"mcp-russia — {len(self._features)} feature(s) active, {len(self._skipped)} skipped\n"
        ]

        if self._features:
            lines.append("Активные:")
            for name, feat in sorted(self._features.items()):
                auth_icon = (
                    "🔑" if feat.meta.requires_auth else ("🔏" if feat.meta.auth_env_var else "🔓")
                )
                lines.append(f"  /{name:<20} {auth_icon} {feat.meta.description}")

        if self._skipped:
            lines.append("\nПропущенные:")
            for name, reason in sorted(self._skipped.items()):
                lines.append(f"  {name:<20} ⏭️  {reason}")

        return "\n".join(lines)

    def get_feature(self, name: str) -> RegisteredFeature | None:
        """Получение зарегистрированной функции по имени."""
        return self._features.get(name)
