"""HTTP-клиент для API Госдумы.

Интеграция с реальными API:
    - Депутаты: https://api.duma.gov.ru/api/v1/deputies
    - Законопроекты: https://sozd.duma.gov.ru/api/open-api
    - Голосования: https://api.duma.gov.ru/api/v1/votes

API Госдумы предоставляет открытые данные о депутатах, законопроектах и голосованиях.
Некоторые эндпоинты могут требовать API-токен (переменная окружения DUMA_API_TOKEN).
"""

from __future__ import annotations

import logging
from typing import Any

from mcp_russia import settings
from mcp_russia._shared.http_client import http_poluchit

from .constants import DUMA_DEPUTATY, DUMA_GOLOSOVANIYA, DUMA_ZAKONOPROEKTY, FRAKCII, SOZYVY
from .schemas import Deputat, Fraktsiya, Golosovanie, Zakonoproekt

logger = logging.getLogger(__name__)


def _stroka(znachenie: object, po_umolchaniyu: str = "") -> str:
    """Безопасно приводит скалярное значение внешнего API к строке."""
    if znachenie is None or isinstance(znachenie, (bool, dict, list)):
        return po_umolchaniyu
    if isinstance(znachenie, str):
        return znachenie
    if isinstance(znachenie, (int, float)):
        return str(znachenie)
    return po_umolchaniyu


def _tseloe(znachenie: object, po_umolchaniyu: int = 0) -> int:
    """Безопасно приводит целочисленное значение внешнего API к числу."""
    if znachenie is None or isinstance(znachenie, bool):
        return po_umolchaniyu
    if isinstance(znachenie, int):
        return znachenie
    if isinstance(znachenie, float):
        return int(znachenie) if znachenie.is_integer() else po_umolchaniyu
    if isinstance(znachenie, str):
        try:
            return int(znachenie.strip())
        except ValueError:
            return po_umolchaniyu
    return po_umolchaniyu


def _pervoe_znachenie(zapis: dict[str, Any], *klyuchi: str) -> object:
    """Возвращает первое непустое по отсутствию значение из вариантов схемы API."""
    for klyuch in klyuchi:
        znachenie = zapis.get(klyuch)
        if znachenie is not None:
            return znachenie
    return None


def _spisok_iz_otveta(dannye: object, *klyuchi: str) -> list[object]:
    """Извлекает список из корневого массива или известных полей ответа."""
    if isinstance(dannye, list):
        return dannye
    if not isinstance(dannye, dict):
        return []
    for klyuch in klyuchi:
        elementy = dannye.get(klyuch)
        if isinstance(elementy, list):
            return elementy
    return []


def _poluchit_api_token() -> str:
    """Получение токена API Госдумы из настроек."""
    return settings.KLYUCH_GOSDUMY_API


async def poluchit_deputatov(sozyv: str = "") -> list[Deputat]:
    """Получение списка депутатов Государственной Думы из открытого API.

    Аргументы:
        sozyv: Номер созыва (напр., '8' для VIII созыва).

    Возвращает:
        Список депутатов.
    """
    parametry: dict[str, str] = {}
    if sozyv:
        parametry["convocation"] = sozyv

    zheton = _poluchit_api_token()
    if zheton:
        parametry["app_token"] = zheton

    try:
        dannye = await http_poluchit(DUMA_DEPUTATY, parametry=parametry)
        return _razobrat_deputatov(dannye)
    except Exception:
        logger.exception("Ошибка при получении списка депутатов")
        return []


def _razobrat_deputatov(dannye: object) -> list[Deputat]:
    """Разбор данных депутатов из ответа API."""
    elementy = _spisok_iz_otveta(dannye, "deputies", "items")

    rezultaty: list[Deputat] = []
    for deputat in elementy:
        if not isinstance(deputat, dict):
            continue
        rezultaty.append(
            Deputat(
                identifikator=_tseloe(deputat.get("id")),
                familiya=_stroka(_pervoe_znachenie(deputat, "surname", "lastName")),
                imya=_stroka(_pervoe_znachenie(deputat, "name", "firstName")),
                otchestvo=_stroka(_pervoe_znachenie(deputat, "patronymic", "middleName")),
                fraktsiya=_stroka(_pervoe_znachenie(deputat, "factionName", "faction")),
                komitet=_stroka(_pervoe_znachenie(deputat, "committeeName", "committee")),
                subiekt=_stroka(_pervoe_znachenie(deputat, "districtName", "region")),
                sozyv=_stroka(_pervoe_znachenie(deputat, "convocation", "sozyv")),
                foto_ssylka=_stroka(_pervoe_znachenie(deputat, "photoUrl", "photo")),
            )
        )
    return rezultaty


async def poluchit_deputata(identifikator: int) -> Deputat | None:
    """Получение конкретного депутата по идентификатору.

    Аргументы:
        identifikator: Идентификатор депутата.

    Возвращает:
        Данные депутата или None.
    """
    zheton = _poluchit_api_token()
    parametry: dict[str, str] = {}
    if zheton:
        parametry["app_token"] = zheton

    adres_url = f"{DUMA_DEPUTATY}/{identifikator}"
    try:
        dannye = await http_poluchit(adres_url, parametry=parametry)
        if isinstance(dannye, dict):
            return _razobrat_odnogo_deputata(dannye)
    except Exception:
        logger.exception("Ошибка при получении депутата %s напрямую", identifikator)

    deputats = await poluchit_deputatov()
    for deputat in deputats:
        if deputat.identifikator == identifikator:
            return deputat
    return None


def _razobrat_odnogo_deputata(dannye: object) -> Deputat | None:
    """Разбор данных одного депутата из ответа API."""
    if not isinstance(dannye, dict):
        return None
    return Deputat(
        identifikator=_tseloe(dannye.get("id")),
        familiya=_stroka(_pervoe_znachenie(dannye, "surname", "lastName")),
        imya=_stroka(_pervoe_znachenie(dannye, "name", "firstName")),
        otchestvo=_stroka(_pervoe_znachenie(dannye, "patronymic", "middleName")),
        fraktsiya=_stroka(_pervoe_znachenie(dannye, "factionName", "faction")),
        komitet=_stroka(_pervoe_znachenie(dannye, "committeeName", "committee")),
        subiekt=_stroka(_pervoe_znachenie(dannye, "districtName", "region")),
        sozyv=_stroka(_pervoe_znachenie(dannye, "convocation", "sozyv")),
        foto_ssylka=_stroka(_pervoe_znachenie(dannye, "photoUrl", "photo")),
    )


async def poluchit_zakonoproekty(
    sostoyanie: str = "",
    ogranichenie: int = 20,
    stranitsa: int = 1,
) -> list[Zakonoproekt]:
    """Получение законопроектов из API СОЗД.

    Аргументы:
        sostoyanie: Фильтр по статусу (необязательно).
        ogranichenie: Максимальное количество результатов.
        stranitsa: Номер страницы.

    Возвращает:
        Список законопроектов.
    """
    parametry: dict[str, str | int] = {"limit": min(ogranichenie, 50), "page": stranitsa}
    if sostoyanie:
        parametry["status"] = sostoyanie

    zheton = _poluchit_api_token()
    if zheton:
        parametry["app_token"] = zheton

    try:
        dannye = await http_poluchit(f"{DUMA_ZAKONOPROEKTY}/bills", parametry=parametry)
        return _razobrat_zakonoproekty(dannye)
    except Exception:
        logger.exception("Ошибка при получении законопроектов")
        return []


def _razobrat_zakonoproekty(dannye: object) -> list[Zakonoproekt]:
    """Разбор данных законопроектов из ответа API."""
    elementy = _spisok_iz_otveta(dannye, "bills", "items")

    rezultaty: list[Zakonoproekt] = []
    for zapis in elementy:
        if not isinstance(zapis, dict):
            continue
        rezultaty.append(
            Zakonoproekt(
                identifikator=_stroka(zapis.get("id")),
                nomer=_stroka(zapis.get("number")),
                nazvanie=_stroka(_pervoe_znachenie(zapis, "name", "title")),
                sostoyanie=_stroka(_pervoe_znachenie(zapis, "statusName", "status")),
                data_vneseniya=_stroka(
                    _pervoe_znachenie(zapis, "dateIntroduction", "introductionDate")
                ),
                avtor=_stroka(_pervoe_znachenie(zapis, "subjectName", "author")),
                chteniya=_tseloe(_pervoe_znachenie(zapis, "readingsCount", "readings")),
            )
        )
    return rezultaty


async def poluchit_golosovaniya(
    sozyv: str = "",
    ogranichenie: int = 20,
    stranitsa: int = 1,
) -> list[Golosovanie]:
    """Получение результатов голосований из API Госдумы.

    Аргументы:
        sozyv: Номер созыва.
        ogranichenie: Максимальное количество результатов.
        stranitsa: Номер страницы.

    Возвращает:
        Список результатов голосований.
    """
    parametry: dict[str, str | int] = {"limit": min(ogranichenie, 50), "page": stranitsa}
    if sozyv:
        parametry["convocation"] = sozyv

    zheton = _poluchit_api_token()
    if zheton:
        parametry["app_token"] = zheton

    try:
        dannye = await http_poluchit(DUMA_GOLOSOVANIYA, parametry=parametry)
        return _razobrat_golosovaniya(dannye)
    except Exception:
        logger.exception("Ошибка при получении голосований")
        return []


def _razobrat_golosovaniya(dannye: object) -> list[Golosovanie]:
    """Разбор результатов голосований из ответа API."""
    elementy = _spisok_iz_otveta(dannye, "votes", "items")

    rezultaty: list[Golosovanie] = []
    for zapis in elementy:
        if not isinstance(zapis, dict):
            continue
        rezultaty.append(
            Golosovanie(
                zakonoproekt_identifikator=_stroka(_pervoe_znachenie(zapis, "billId", "id")),
                nazvanie=_stroka(_pervoe_znachenie(zapis, "subject", "title")),
                data=_stroka(_pervoe_znachenie(zapis, "date", "voteDate")),
                za=_tseloe(_pervoe_znachenie(zapis, "totalFor", "for")),
                protiv=_tseloe(_pervoe_znachenie(zapis, "totalAgainst", "against")),
                vozhderzhalsya=_tseloe(_pervoe_znachenie(zapis, "totalAbstain", "abstain")),
                ne_golosoval=_tseloe(_pervoe_znachenie(zapis, "totalNotVoting", "notVoting")),
            )
        )
    return rezultaty


async def poluchit_fraktsii() -> list[Fraktsiya]:
    """Получение текущих фракций Госдумы.

    Возвращает:
        Список фракций.
    """
    return [
        Fraktsiya(kod=fraktsiya["kod"], nazvanie=fraktsiya["nazvanie"]) for fraktsiya in FRAKCII
    ]


def poluchit_sozyvy() -> list[dict[str, str]]:
    """Возвращает список созывов Государственной Думы."""
    return SOZYVY


def poluchit_komitety() -> list[dict[str, str]]:
    """Возвращает список комитетов Государственной Думы."""
    from .constants import KOMITETY

    return KOMITETY
