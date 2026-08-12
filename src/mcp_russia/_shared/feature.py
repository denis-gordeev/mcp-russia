"""Метаданные функций и автоматический реестр mcp-russia.

Модуль реализует автоматическое обнаружение функций на основе конвенции.
Любой подпакет mcp_russia, экспортирующий META_FUNKTSII и содержащий
server.py с объектом `mcp`, будет автоматически обнаружен,
провалидирован и смонтирован на корневой сервер.

Подход вдохновлён: чертежами Flask, реестром приложений Django,
обнаружением плагинов pytest, автоподключением маршрутов FastAPI.

Полное обоснование — см. ADR-002.

Использование:
    from fastmcp import FastMCP
    from mcp_russia._shared.feature import ReyestrFunktsiy

    mcp = FastMCP("mcp-russia", instructions="...", version="0.5.0")
    reyestr = ReyestrFunktsiy()
    reyestr.obnaruzhit()
    reyestr.smontirovat_vse(mcp)
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
    operatsii_trebuyut_avtorizatsii: list[str] = field(default_factory=list)

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

    metadannye: MetaFunktsii
    server_funktsiya: FastMCP
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
        5. Если trebuet_autentifikatsii=True, peremennaya_avt_env должен быть задан в окружении

    Для отключения функции: установите vklyuchena=False в META_FUNKTSII.
    """

    def __init__(self) -> None:
        """Инициализация пустого реестра функций."""
        self._funktsii: dict[str, ZaregistrirovannayaFunktsiya] = {}
        self._propushcheno: dict[str, str] = {}

    @property
    def funktsii(self) -> dict[str, ZaregistrirovannayaFunktsiya]:
        """Все обнаруженные и зарегистрированные функции."""
        return dict(self._funktsii)

    @property
    def propushcheno(self) -> dict[str, str]:
        """Пропущенные функции с причинами."""
        return dict(self._propushcheno)

    def obnaruzhit(self, imya_paketa: str = "mcp_russia") -> ReyestrFunktsiy:
        """Обнаружение всех функций в пакете.

        Сканирует подпакеты `imya_paketa` и регистрирует те, что
        следуют конвенции. Функции с ошибками валидации логируются
        как предупреждения и пропускаются — они не ломают сервер.

        Аргументы:
            imya_paketa: Базовый пакет для сканирования. По умолчанию: «mcp_russia».

        Возвращает:
            self для цепочки вызовов: reyestr.obnaruzhit().smontirovat_vse(mcp)
        """
        paket = importlib.import_module(imya_paketa)

        for _poiskovik, imya, eto_paket in pkgutil.iter_modules(
            paket.__path__, paket.__name__ + "."
        ):
            korotkoe_imya = imya.rsplit(".", 1)[-1]

            # Пропуск не-пакетов и приватных модулей
            if not eto_paket or korotkoe_imya.startswith("_"):
                continue

            try:
                self._poprovat_zaregistrirovat(imya, korotkoe_imya)
            except Exception as isklyuchenie:
                prichina = str(isklyuchenie)
                self._propushcheno[korotkoe_imya] = prichina
                logger.warning("Функция '%s' пропущена: %s", korotkoe_imya, prichina)

        return self

    def _poprovat_zaregistrirovat(self, put_modulya: str, korotkoe_imya: str) -> None:
        """Попытка импорта и регистрации отдельной функции."""
        # Шаг 1: Импорт __init__.py функции
        importiruyemyy_modul = importlib.import_module(put_modulya)

        # Шаг 2: Проверка наличия и корректности META_FUNKTSII
        metadannye_ekz = getattr(importiruyemyy_modul, "META_FUNKTSII", None)
        if metadannye_ekz is None:
            raise ValueError(f"Нет META_FUNKTSII в {put_modulya}")
        if not isinstance(metadannye_ekz, MetaFunktsii):
            raise TypeError(f"META_FUNKTSII в {put_modulya} не является экземпляром MetaFunktsii")

        # Шаг 3: Проверка активности функции
        if not metadannye_ekz.vklyuchena:
            self._propushcheno[korotkoe_imya] = "отключена (vklyuchena=False)"
            logger.info("Функция '%s' отключена, пропуск.", korotkoe_imya)
            return

        # Шаг 4: Проверка аутентификации при необходимости
        if not metadannye_ekz.dostupna_li_autentifikatsiya():
            self._propushcheno[korotkoe_imya] = (
                f"отсутствует переменная {metadannye_ekz.peremennaya_avt_env}"
            )
            logger.warning(
                "Функция '%s' требует %s (не задано), пропуск.",
                korotkoe_imya,
                metadannye_ekz.peremennaya_avt_env,
            )
            return

        # Шаг 5: Импорт server.py и получение объекта mcp
        modul_servera = importlib.import_module(f"{put_modulya}.server")
        obekt_servera = getattr(modul_servera, "mcp", None)

        if obekt_servera is None:
            raise ValueError(f"Нет объекта `mcp` в {put_modulya}.server")

        # Шаг 6: Регистрация
        self._funktsii[korotkoe_imya] = ZaregistrirovannayaFunktsiya(
            metadannye=metadannye_ekz,
            server_funktsiya=obekt_servera,
            put_modulya=put_modulya,
        )
        logger.info(
            "Зарегистрирована функция '%s' v%s",
            metadannye_ekz.imya,
            metadannye_ekz.versiya,
        )

    def smontirovat_vse(self, kornevoy_server: FastMCP) -> None:
        """Монтирование всех обнаруженных функций на корневой сервер.

        Каждая функция получает пространство имён по названию
        (напр. инструменты становятся rosstat_poluchit_*).

        Аргументы:
            kornevoy_server: Корневой FastMCP-сервер для монтирования функций.
        """
        for imya, modul in sorted(self._funktsii.items()):
            kornevoy_server.mount(modul.server_funktsiya, namespace=imya)
            logger.info("Смонтирована '%s' — %s", imya, modul.metadannye.opisanie)

    def svodka(self) -> str:
        """Читаемая сводка зарегистрированных функций.

        Полезно для логирования при запуске и генерации документации.
        """
        stroki = [
            f"mcp-russia — {len(self._funktsii)} функция(й) активно, "
            f"{len(self._propushcheno)} пропущено\n"
        ]

        if self._funktsii:
            stroki.append("Активные:")
            for imya, funktsiya in sorted(self._funktsii.items()):
                ikona_avt = (
                    "🔑"
                    if funktsiya.metadannye.trebuet_autentifikatsii
                    else ("🔏" if funktsiya.metadannye.peremennaya_avt_env else "🔓")
                )
                stroki.append(f"  /{imya:<20} {ikona_avt} {funktsiya.metadannye.opisanie}")

        if self._propushcheno:
            stroki.append("\nПропущенные:")
            for imya, prichina in sorted(self._propushcheno.items()):
                stroki.append(f"  {imya:<20} ⏭️  {prichina}")

        return "\n".join(stroki)

    def poluchit_funktsiyu(self, imya: str) -> ZaregistrirovannayaFunktsiya | None:
        """Получение зарегистрированной функции по имени."""
        return self._funktsii.get(imya)
