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
            imya="rosstat",
            opisanie="Росстат: демография, ВРП, социальные показатели",
            baza_api="https://rosstat.gov.ru/api",
        )
    """

    imya: str
    opisanie: str
    versiya: str = "0.1.0"
    baza_api: str = ""
    trebuet_autentifikatsii: bool = False
    peremennaya_avt_env: str | None = None
    vklyuchena: bool = True
    tegi: list[str] = field(default_factory=list)

    def dostupna_li_autentifikatsiya(self) -> bool:
        """Проверка доступности учётных данных аутентификации."""
        if not self.trebuet_autentifikatsii:
            return True
        if self.peremennaya_avt_env is None:
            return False
        return bool(os.environ.get(self.peremennaya_avt_env))


@dataclass
class ZaregistrirovannayaFunktsiya:
    """Обнаруженная, провалидированная и зарегистрированная функция."""

    meta: MetaFunktsii
    server: FastMCP
    put_modulya: str


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

    def obnaruzhit(self, imya_paketa: str = "mcp_russia") -> ReyestrFunktsiy:
        """Обнаружение всех функций в пакете.

        Сканирует подпакеты `imya_paketa` и регистрирует те, что
        следуют конвенции. Функции с ошибками валидации логируются
        как предупреждения и пропускаются — они не ломают сервер.

        Аргументы:
            imya_paketa: Базовый пакет для сканирования. По умолчанию: «mcp_russia».

        Возвращает:
            self для цепочки вызовов: registry.obnaruzhit().smontirovat_vse(mcp)
        """
        paket = importlib.import_module(imya_paketa)

        for _finder, imya, ispkg in pkgutil.iter_modules(paket.__path__, paket.__name__ + "."):
            korotkoe_imya = imya.rsplit(".", 1)[-1]

            # Пропуск не-пакетов и приватных модулей
            if not ispkg or korotkoe_imya.startswith("_"):
                continue

            try:
                self._poprovat_zaregistrirovat(imya, korotkoe_imya)
            except Exception as exc:
                prichina = str(exc)
                self._skipped[korotkoe_imya] = prichina
                logger.warning("Функция '%s' пропущена: %s", korotkoe_imya, prichina)

        return self

    def _poprovat_zaregistrirovat(self, put_modulya: str, korotkoe_imya: str) -> None:
        """Попытка импорта и регистрации отдельной функции."""
        # Шаг 1: Импорт __init__.py функции
        importiruyemyy_modul = importlib.import_module(put_modulya)

        # Шаг 2: Проверка наличия и корректности META_FUNKTSII
        meta = getattr(importiruyemyy_modul, "META_FUNKTSII", None)
        if meta is None:
            raise ValueError(f"Нет META_FUNKTSII в {put_modulya}")
        if not isinstance(meta, MetaFunktsii):
            raise TypeError(f"META_FUNKTSII в {put_modulya} не является экземпляром MetaFunktsii")

        # Шаг 3: Проверка активности функции
        if not meta.vklyuchena:
            self._skipped[korotkoe_imya] = "отключена (vklyuchena=False)"
            logger.info("Функция '%s' отключена, пропуск.", korotkoe_imya)
            return

        # Шаг 4: Проверка аутентификации при необходимости
        if not meta.dostupna_li_autentifikatsiya():
            self._skipped[korotkoe_imya] = f"отсутствует переменная {meta.peremennaya_avt_env}"
            logger.warning(
                "Функция '%s' требует %s (не задано), пропуск.",
                korotkoe_imya,
                meta.peremennaya_avt_env,
            )
            return

        # Шаг 5: Импорт server.py и получение объекта mcp
        modul_servera = importlib.import_module(f"{put_modulya}.server")
        server = getattr(modul_servera, "mcp", None)

        if server is None:
            raise ValueError(f"Нет объекта `mcp` в {put_modulya}.server")

        # Шаг 6: Регистрация
        self._features[korotkoe_imya] = ZaregistrirovannayaFunktsiya(
            meta=meta,
            server=server,
            put_modulya=put_modulya,
        )
        logger.info(
            "Зарегистрирована функция '%s' v%s",
            meta.imya,
            meta.versiya,
        )

    def smontirovat_vse(self, kornevoy_server: FastMCP) -> None:
        """Монтирование всех обнаруженных функций на корневой сервер.

        Каждая функция получает пространство имён по названию
        (напр. инструменты становятся rosstat_poluchit_*).

        Аргументы:
            kornevoy_server: Корневой FastMCP-сервер для монтирования функций.
        """
        for imya, modul in sorted(self._features.items()):
            kornevoy_server.mount(modul.server, namespace=imya)
            logger.info("Смонтирована '%s' — %s", imya, modul.meta.opisanie)

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
            for imya, funktsiya in sorted(self._features.items()):
                ikona_avt = (
                    "🔑"
                    if funktsiya.meta.trebuet_autentifikatsii
                    else ("🔏" if funktsiya.meta.peremennaya_avt_env else "🔓")
                )
                lines.append(f"  /{imya:<20} {ikona_avt} {funktsiya.meta.opisanie}")

        if self._skipped:
            lines.append("\nПропущенные:")
            for imya, prichina in sorted(self._skipped.items()):
                lines.append(f"  {imya:<20} ⏭️  {prichina}")

        return "\n".join(lines)

    def poluchit_funktsiyu(self, imya: str) -> ZaregistrirovannayaFunktsiya | None:
        """Получение зарегистрированной функции по имени."""
        return self._features.get(imya)
