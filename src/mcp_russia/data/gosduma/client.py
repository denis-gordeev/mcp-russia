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

from mcp_russia import settings
from mcp_russia._shared.http_client import http_poluchit
from mcp_russia._shared.normalizatsiya import (
    bezopasnaya_stroka,
    bezopasnoe_tseloe,
    izvlech_spisok,
    pervoe_znachenie,
)

from .constants import DUMA_DEPUTATY, DUMA_GOLOSOVANIYA, DUMA_ZAKONOPROEKTY, FRAKCII, SOZYVY
from .schemas import Deputat, Fraktsiya, Golosovanie, Zakonoproekt

logger = logging.getLogger(__name__)


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
    elementy = izvlech_spisok(dannye, "deputies", "items")

    rezultaty: list[Deputat] = []
    for deputat in elementy:
        if not isinstance(deputat, dict):
            continue
        rezultaty.append(
            Deputat(
                identifikator=bezopasnoe_tseloe(deputat.get("id")),
                familiya=bezopasnaya_stroka(pervoe_znachenie(deputat, "surname", "lastName")),
                imya=bezopasnaya_stroka(pervoe_znachenie(deputat, "name", "firstName")),
                otchestvo=bezopasnaya_stroka(
                    pervoe_znachenie(deputat, "patronymic", "middleName")
                ),
                fraktsiya=bezopasnaya_stroka(pervoe_znachenie(deputat, "factionName", "faction")),
                komitet=bezopasnaya_stroka(
                    pervoe_znachenie(deputat, "committeeName", "committee")
                ),
                subiekt=bezopasnaya_stroka(pervoe_znachenie(deputat, "districtName", "region")),
                sozyv=bezopasnaya_stroka(pervoe_znachenie(deputat, "convocation", "sozyv")),
                foto_ssylka=bezopasnaya_stroka(pervoe_znachenie(deputat, "photoUrl", "photo")),
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
        identifikator=bezopasnoe_tseloe(dannye.get("id")),
        familiya=bezopasnaya_stroka(pervoe_znachenie(dannye, "surname", "lastName")),
        imya=bezopasnaya_stroka(pervoe_znachenie(dannye, "name", "firstName")),
        otchestvo=bezopasnaya_stroka(pervoe_znachenie(dannye, "patronymic", "middleName")),
        fraktsiya=bezopasnaya_stroka(pervoe_znachenie(dannye, "factionName", "faction")),
        komitet=bezopasnaya_stroka(pervoe_znachenie(dannye, "committeeName", "committee")),
        subiekt=bezopasnaya_stroka(pervoe_znachenie(dannye, "districtName", "region")),
        sozyv=bezopasnaya_stroka(pervoe_znachenie(dannye, "convocation", "sozyv")),
        foto_ssylka=bezopasnaya_stroka(pervoe_znachenie(dannye, "photoUrl", "photo")),
    )


async def poluchit_zakonoproekty(
    sostoyanie: str = "",
    ogranichenie: int = 20,
    stranitsa: int = 1,
    avtor: str = "",
    sootvetstvie: str = "",
) -> list[Zakonoproekt]:
    """Получение законопроектов из API СОЗД.

    Аргументы:
        sostoyanie: Фильтр по статусу (необязательно).
        ogranichenie: Максимальное количество результатов.
        stranitsa: Номер страницы.
        avtor: Фильтр по автору/депутату (необязательно).
        sootvetstvie: Поиск по тексту названия (необязательно).

    Возвращает:
        Список законопроектов.
    """
    parametry: dict[str, str | int] = {"limit": min(ogranichenie, 50), "page": stranitsa}
    if sostoyanie:
        parametry["status"] = sostoyanie
    if avtor:
        parametry["author"] = avtor
    if sootvetstvie:
        parametry["searchString"] = sootvetstvie

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
    elementy = izvlech_spisok(dannye, "bills", "items")

    rezultaty: list[Zakonoproekt] = []
    for zapis in elementy:
        if not isinstance(zapis, dict):
            continue
        rezultaty.append(
            Zakonoproekt(
                identifikator=bezopasnaya_stroka(zapis.get("id")),
                nomer=bezopasnaya_stroka(zapis.get("number")),
                nazvanie=bezopasnaya_stroka(pervoe_znachenie(zapis, "name", "title")),
                sostoyanie=bezopasnaya_stroka(pervoe_znachenie(zapis, "statusName", "status")),
                data_vneseniya=bezopasnaya_stroka(
                    pervoe_znachenie(zapis, "dateIntroduction", "introductionDate")
                ),
                avtor=bezopasnaya_stroka(pervoe_znachenie(zapis, "subjectName", "author")),
                chteniya=bezopasnoe_tseloe(pervoe_znachenie(zapis, "readingsCount", "readings")),
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
    elementy = izvlech_spisok(dannye, "votes", "items")

    rezultaty: list[Golosovanie] = []
    for zapis in elementy:
        if not isinstance(zapis, dict):
            continue
        rezultaty.append(
            Golosovanie(
                zakonoproekt_identifikator=bezopasnaya_stroka(
                    pervoe_znachenie(zapis, "billId", "id")
                ),
                nazvanie=bezopasnaya_stroka(pervoe_znachenie(zapis, "subject", "title")),
                data=bezopasnaya_stroka(pervoe_znachenie(zapis, "date", "voteDate")),
                za=bezopasnoe_tseloe(pervoe_znachenie(zapis, "totalFor", "for")),
                protiv=bezopasnoe_tseloe(pervoe_znachenie(zapis, "totalAgainst", "against")),
                vozhderzhalsya=bezopasnoe_tseloe(
                    pervoe_znachenie(zapis, "totalAbstain", "abstain")
                ),
                ne_golosoval=bezopasnoe_tseloe(
                    pervoe_znachenie(zapis, "totalNotVoting", "notVoting")
                ),
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
