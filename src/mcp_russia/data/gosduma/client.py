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

from .constants import DUMA_DEPUTATS, DUMA_LAWS, DUMA_VOTES, FRAKCII, SOZYVY
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
        dannye = await http_poluchit(DUMA_DEPUTATS, parametry=parametry)
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
    for d in elementy:
        if not isinstance(d, dict):
            continue
        frakciya_syraya = d.get("factionName", d.get("faction", ""))
        rezultaty.append(
            Deputat(
                identifikator=d.get("id", 0),
                фамилия=d.get("surname", d.get("lastName", "")),
                имя=d.get("name", d.get("firstName", "")),
                отчество=d.get("patronymic", d.get("middleName", "")),
                фракция=frakciya_syraya,
                комитет=d.get("committeeName", d.get("committee", "")),
                регион=d.get("districtName", d.get("region", "")),
                созыв=str(d.get("convocation", d.get("sozyv", ""))),
                foto_ssylka=d.get("photoUrl", d.get("photo", "")),
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

    adres_url = f"{DUMA_DEPUTATS}/{identifikator}"
    try:
        dannye = await http_poluchit(adres_url, parametry=parametry)
        if isinstance(dannye, dict):
            return _razobrat_odnogo_deputata(dannye)
    except Exception:
        pass

    deputats = await poluchit_deputatov()
    for d in deputats:
        if d.identifikator == identifikator:
            return d
    return None


def _razobrat_odnogo_deputata(dannye: dict[str, Any]) -> Deputat | None:
    """Разбор данных одного депутата из ответа API."""
    if not isinstance(dannye, dict):
        return None
    return Deputat(
        identifikator=dannye.get("id", 0),
        фамилия=dannye.get("surname", dannye.get("lastName", "")),
        имя=dannye.get("name", dannye.get("firstName", "")),
        отчество=dannye.get("patronymic", dannye.get("middleName", "")),
        фракция=dannye.get("factionName", dannye.get("faction", "")),
        комитет=dannye.get("committeeName", dannye.get("committee", "")),
        регион=dannye.get("districtName", dannye.get("region", "")),
        созыв=str(dannye.get("convocation", dannye.get("sozyv", ""))),
        foto_ssylka=dannye.get("photoUrl", dannye.get("photo", "")),
    )


async def poluchit_zakonoproekty(
    status: str = "",
    ogranichenie: int = 20,
    stranitsa: int = 1,
) -> list[Zakonoproekt]:
    """Получение законопроектов из API СОЗД.

    Аргументы:
        status: Фильтр по статусу (необязательно).
        ogranichenie: Максимальное количество результатов.
        stranitsa: Номер страницы.

    Возвращает:
        Список законопроектов.
    """
    parametry: dict[str, str | int] = {"limit": min(ogranichenie, 50), "page": stranitsa}
    if status:
        parametry["status"] = status

    zheton = _poluchit_api_token()
    if zheton:
        parametry["app_token"] = zheton

    try:
        dannye = await http_poluchit(f"{DUMA_LAWS}/bills", parametry=parametry)
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
    for element in elementy:
        if not isinstance(element, dict):
            continue
        rezultaty.append(
            Zakonoproekt(
                identifikator=str(element.get("id", "")),
                nomer=element.get("number", ""),
                nazvanie=element.get("name", element.get("title", "")),
                sostoyanie=element.get("statusName", element.get("status", "")),
                data_vneseniya=element.get(
                    "dateIntroduction", element.get("introductionDate", "")
                ),
                avtor=element.get("subjectName", element.get("author", "")),
                chteniya=element.get("readingsCount", element.get("readings", 0)),
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
        dannye = await http_poluchit(DUMA_VOTES, parametry=parametry)
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
    for element in elementy:
        if not isinstance(element, dict):
            continue
        rezultaty.append(
            Golosovanie(
                zakonoproekt_identifikator=str(element.get("billId", element.get("id", ""))),
                nazvanie=element.get("subject", element.get("title", "")),
                data=element.get("date", element.get("voteDate", "")),
                za=element.get("totalFor", element.get("for", 0)),
                protiv=element.get("totalAgainst", element.get("against", 0)),
                vozhderzhalsya=element.get("totalAbstain", element.get("abstain", 0)),
                ne_golosoval=element.get("totalNotVoting", element.get("notVoting", 0)),
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
