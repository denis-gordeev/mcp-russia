"""HTTP-клиент для API Госдумы.

Интеграция с реальными API:
    - Депутаты: https://api.duma.gov.ru/api/v1/deputies
    - Законопроекты: https://sozd.duma.gov.ru/api/open-api
    - Голосования: https://api.duma.gov.ru/api/v1/votes

API Госдумы предоставляет открытые данные о депутатах, законопроектах и голосованиях.
Некоторые эндпоинты могут требовать API-токен (переменная окружения DUMA_API_TOKEN).
"""

from __future__ import annotations

from typing import Any

from mcp_russia import settings
from mcp_russia._shared.http_client import http_poluchit

from .constants import DUMA_DEPUTATY, DUMA_GOLOSOVANIYA, DUMA_ZAKONOPROEKTY, FRAKCII, SOZYVY
from .schemas import Deputat, Frakciya, Golosovanie, Zakonoproekt


def _poluchit_api_token() -> str:
    """Получение токена API Госдумы из настроек."""
    return settings.TOKEN_GOSDUMY_API


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
        return []


def _razobrat_deputatov(dannye: Any) -> list[Deputat]:
    """Разбор данных депутатов из ответа API."""
    if isinstance(dannye, dict):
        elementy = dannye.get("deputies", dannye.get("items", []))
    elif isinstance(dannye, list):
        elementy = dannye
    else:
        return []

    rezultaty = []
    for deputat in elementy:
        if not isinstance(deputat, dict):
            continue
        frakciya_syraya = deputat.get("factionName", deputat.get("faction", ""))
        rezultaty.append(
            Deputat(
                identifikator=deputat.get("id", 0),
                familiya=deputat.get("surname", deputat.get("lastName", "")),
                imya=deputat.get("name", deputat.get("firstName", "")),
                otchestvo=deputat.get("patronymic", deputat.get("middleName", "")),
                frakciya=frakciya_syraya,
                komitet=deputat.get("committeeName", deputat.get("committee", "")),
                subiekt=deputat.get("districtName", deputat.get("region", "")),
                sozyv=str(deputat.get("convocation", deputat.get("sozyv", ""))),
                foto_ssylka=deputat.get("photoUrl", deputat.get("photo", "")),
            )
        )
    return rezultaty


async def poluchit_deputata(identifikator: int) -> Deputat | None:
    """Получение конкретного депутата по ID.

    Аргументы:
        identifikator: ID депутата.

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
        pass

    deputats = await poluchit_deputatov()
    for deputat in deputats:
        if deputat.identifikator == identifikator:
            return deputat
    return None


def _razobrat_odnogo_deputata(dannye: dict[str, Any]) -> Deputat | None:
    """Разбор данных одного депутата из ответа API."""
    if not isinstance(dannye, dict):
        return None
    return Deputat(
        identifikator=dannye.get("id", 0),
        familiya=dannye.get("surname", dannye.get("lastName", "")),
        imya=dannye.get("name", dannye.get("firstName", "")),
        otchestvo=dannye.get("patronymic", dannye.get("middleName", "")),
        frakciya=dannye.get("factionName", dannye.get("faction", "")),
        komitet=dannye.get("committeeName", dannye.get("committee", "")),
        subiekt=dannye.get("districtName", dannye.get("region", "")),
        sozyv=str(dannye.get("convocation", dannye.get("sozyv", ""))),
        foto_ssylka=dannye.get("photoUrl", dannye.get("photo", "")),
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
        return []


def _razobrat_zakonoproekty(dannye: Any) -> list[Zakonoproekt]:
    """Разбор данных законопроектов из ответа API."""
    if isinstance(dannye, dict):
        elementy = dannye.get("bills", dannye.get("items", []))
    elif isinstance(dannye, list):
        elementy = dannye
    else:
        return []

    rezultaty = []
    for zapis in elementy:
        if not isinstance(zapis, dict):
            continue
        rezultaty.append(
            Zakonoproekt(
                identifikator=str(zapis.get("id", "")),
                nomer=zapis.get("number", ""),
                nazvanie=zapis.get("name", zapis.get("title", "")),
                sostoyanie=zapis.get("statusName", zapis.get("status", "")),
                data_vneseniya=zapis.get("dateIntroduction", zapis.get("introductionDate", "")),
                avtor=zapis.get("subjectName", zapis.get("author", "")),
                chteniya=zapis.get("readingsCount", zapis.get("readings", 0)),
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
        return []


def _razobrat_golosovaniya(dannye: Any) -> list[Golosovanie]:
    """Разбор результатов голосований из ответа API."""
    if isinstance(dannye, dict):
        elementy = dannye.get("votes", dannye.get("items", []))
    elif isinstance(dannye, list):
        elementy = dannye
    else:
        return []

    rezultaty = []
    for zapis in elementy:
        if not isinstance(zapis, dict):
            continue
        rezultaty.append(
            Golosovanie(
                zakonoproekt_identifikator=str(zapis.get("billId", zapis.get("id", ""))),
                nazvanie=zapis.get("subject", zapis.get("title", "")),
                data=zapis.get("date", zapis.get("voteDate", "")),
                za=zapis.get("totalFor", zapis.get("for", 0)),
                protiv=zapis.get("totalAgainst", zapis.get("against", 0)),
                vozhderzhalsya=zapis.get("totalAbstain", zapis.get("abstain", 0)),
                ne_golosoval=zapis.get("totalNotVoting", zapis.get("notVoting", 0)),
            )
        )
    return rezultaty


async def poluchit_frakcii() -> list[Frakciya]:
    """Получение текущих фракций Госдумы.

    Возвращает:
        Список фракций.
    """
    return [Frakciya(kod=f["kod"], nazvanie=f["nazvanie"]) for f in FRAKCII]


def poluchit_sozyvy() -> list[dict[str, str]]:
    """Возвращает список созывов Государственной Думы."""
    return SOZYVY


def poluchit_fraktsii() -> list[dict[str, str]]:
    """Возвращает список текущих фракций."""
    return FRAKCII


def poluchit_komitety() -> list[dict[str, str]]:
    """Возвращает список комитетов Государственной Думы."""
    from .constants import KOMITETY

    return KOMITETY
