"""Метаданные функций и автоматический реестр mcp-russia.

Модуль реализует автоматическое обнаружение функций на основе конвенции.
Любой подпакет mcp_russia, экспортирующий META_FUNKTSII и содержащий
server.py с объектом `mcp`, будет автоматически обнаружен,
провалидирован и смонтирован на корневой сервер.

Подход вдохновлён: Flask blueprints, Django app registry,
pytest plugin discovery, FastAPI router auto-include.

Полное обоснование — см. ADR-002.

Использование:
    from fastmcp import FastMCP
    from mcp_russia._shared.feature import ReyestrFunktsiy

    mcp = FastMCP("mcp-russia")
    registry = ReyestrFunktsiy()
    registry.obnaruzhit()
    registry.smontirovat_vse(mcp)
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
class MetaFunktsii:
    """Декларативные метаданные функции.

    Каждая функция должна экспортировать экземпляр META_FUNKTSII в своём __init__.py.
    Реестр использует эти метаданные для обнаружения, валидации, документации
    и решений во время выполнения (авторизация, флаги функций).

    Пример:
        # src/mcp_russia/rosstat/__init__.py
        from mcp_russia._shared.feature import MetaFunktsii

        META_FUNKTSII = MetaFunktsii(
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

    def dostupna_li_autentifikatsiya(self) -> bool:
        """Проверка доступности учётных данных аутентификации."""
        if not self.requires_auth:
            return True
        if self.auth_env_var is None:
            return False
        return bool(os.environ.get(self.auth_env_var))


@dataclass
class ZaregistrirovannayaFunktsiya:
    """Обнаруженная, провалидированная и зарегистрированная функция."""

    meta: MetaFunktsii
    server: FastMCP
    module_path: str


class ReyestrFunktsiy:
    """Автоматический реестр: обнаружение, валидация и монтирование функций.

    Использует pkgutil.iter_modules() для сканирования подпакетов mcp_russia,
    импортирует те, что следуют конвенции (META_FUNKTSII + server.mcp),
    и монтирует их на корневой FastMCP-сервер.

    Конвенция (все условия обязательны для автообнаружения):
        1. Подпакет mcp_russia/ (директория с __init__.py)
        2. Имя НЕ начинается с '_'
        3. __init__.py экспортирует META_FUNKTSII: MetaFunktsii
        4. server.py экспортирует mcp: FastMCP
        5. Если requires_auth=True, auth_env_var должен быть задан в окружении

    Для отключения функции: установите enabled=False в META_FUNKTSII.
    """

    def __init__(self) -> None:
        """Инициализация пустого реестра функций."""
        self._features: dict[str, ZaregistrirovannayaFunktsiya] = {}
        self._skipped: dict[str, str] = {}

    @property
    def funktsii(self) -> dict[str, ZaregistrirovannayaFunktsiya]:
        """Все обнаруженные и зарегистрированные функции."""
        return dict(self._features)

    @property
    def propushcheno(self) -> dict[str, str]:
        """Пропущенные функции с причинами."""
        return dict(self._skipped)

    def obnaruzhit(self, package_name: str = "mcp_russia") -> ReyestrFunktsiy:
        """Обнаружение всех функций в пакете.

        Сканирует подпакеты `package_name` и регистрирует те, что
        следуют конвенции. Функции с ошибками валидации логируются
        как предупреждения и пропускаются — они не ломают сервер.

        Аргументы:
            package_name: Базовый пакет для сканирования. По умолчанию: «mcp_russia».

        Возвращает:
            self для цепочки вызовов: registry.obnaruzhit().smontirovat_vse(mcp)
        """
        package = importlib.import_module(package_name)

        for _finder, name, ispkg in pkgutil.iter_modules(package.__path__, package.__name__ + "."):
            short_name = name.rsplit(".", 1)[-1]

            # Пропуск не-пакетов и приватных модулей
            if not ispkg or short_name.startswith("_"):
                continue

            try:
                self._poprovat_zaregistrirovat(name, short_name)
            except Exception as exc:
                reason = str(exc)
                self._skipped[short_name] = reason
                logger.warning("Функция '%s' пропущена: %s", short_name, reason)

        return self

    def _poprovat_zaregistrirovat(self, module_path: str, short_name: str) -> None:
        """Попытка импорта и регистрации отдельной функции."""
        # Шаг 1: Импорт __init__.py функции
        importiruyemyy_modul = importlib.import_module(module_path)

        # Шаг 2: Проверка наличия и корректности META_FUNKTSII
        meta = getattr(importiruyemyy_modul, "META_FUNKTSII", None)
        if meta is None:
            raise ValueError(f"Нет META_FUNKTSII в {module_path}")
        if not isinstance(meta, MetaFunktsii):
            raise TypeError(f"META_FUNKTSII в {module_path} не является экземпляром MetaFunktsii")

        # Шаг 3: Проверка активности функции
        if not meta.enabled:
            self._skipped[short_name] = "отключена (enabled=False)"
            logger.info("Функция '%s' отключена, пропуск.", short_name)
            return

        # Шаг 4: Проверка аутентификации при необходимости
        if not meta.dostupna_li_autentifikatsiya():
            self._skipped[short_name] = f"отсутствует переменная {meta.auth_env_var}"
            logger.warning(
                "Функция '%s' требует %s (не задано), пропуск.",
                short_name,
                meta.auth_env_var,
            )
            return

        # Шаг 5: Импорт server.py и получение объекта mcp
        server_module = importlib.import_module(f"{module_path}.server")
        server = getattr(server_module, "mcp", None)

        if server is None:
            raise ValueError(f"Нет объекта `mcp` в {module_path}.server")

        # Шаг 6: Регистрация
        self._features[short_name] = ZaregistrirovannayaFunktsiya(
            meta=meta,
            server=server,
            module_path=module_path,
        )
        logger.info(
            "Зарегистрирована функция '%s' v%s",
            meta.name,
            meta.version,
        )

    def smontirovat_vse(self, root_server: FastMCP) -> None:
        """Монтирование всех обнаруженных функций на корневой сервер.

        Каждая функция получает пространство имён по названию
        (напр. инструменты становятся rosstat_poluchit_*).

        Аргументы:
            root_server: Корневой FastMCP-сервер для монтирования функций.
        """
        for name, modul in sorted(self._features.items()):
            root_server.mount(modul.server, namespace=name)
            logger.info("Смонтирована '%s' — %s", name, modul.meta.description)

    def svodka(self) -> str:
        """Читаемая сводка зарегистрированных функций.

        Полезно для логирования при запуске и генерации документации.
        """
        lines = [
            f"mcp-russia — {len(self._features)} функция(й) активно, "
            f"{len(self._skipped)} пропущено\n"
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

    def poluchit_funktsiyu(self, name: str) -> ZaregistrirovannayaFunktsiya | None:
        """Получение зарегистрированной функции по имени."""
        return self._features.get(name)
