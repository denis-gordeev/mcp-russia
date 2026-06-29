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
    params: dict[str, str] = {}
    if sozyv:
        params["convocation"] = sozyv

    token = _poluchit_api_token()
    if token:
        params["app_token"] = token

    try:
        data = await http_poluchit(DUMA_DEPUTATS, params=params)
        return _razobrat_deputatov(data)
    except Exception:
        return []


def _razobrat_deputatov(data: Any) -> list[Deputat]:
    """Разбор данных депутатов из ответа API."""
    if isinstance(data, dict):
        elementy = data.get("deputies", data.get("items", []))
    elif isinstance(data, list):
        elementy = data
    else:
        return []

    rezultaty = []
    for d in elementy:
        if not isinstance(d, dict):
            continue
        frakciya_raw = d.get("factionName", d.get("faction", ""))
        rezultaty.append(
            Deputat(
                identifikator=d.get("id", 0),
                фамилия=d.get("surname", d.get("lastName", "")),
                имя=d.get("name", d.get("firstName", "")),
                отчество=d.get("patronymic", d.get("middleName", "")),
                фракция=frakciya_raw,
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
    token = _poluchit_api_token()
    params: dict[str, str] = {}
    if token:
        params["app_token"] = token

    url = f"{DUMA_DEPUTATS}/{identifikator}"
    try:
        data = await http_poluchit(url, params=params)
        if isinstance(data, dict):
            return _razobrat_odnogo_deputata(data)
    except Exception:
        pass

    deputats = await poluchit_deputatov()
    for d in deputats:
        if d.identifikator == identifikator:
            return d
    return None


def _razobrat_odnogo_deputata(data: dict[str, Any]) -> Deputat | None:
    """Разбор данных одного депутата из ответа API."""
    if not isinstance(data, dict):
        return None
    return Deputat(
        identifikator=data.get("id", 0),
        фамилия=data.get("surname", data.get("lastName", "")),
        имя=data.get("name", data.get("firstName", "")),
        отчество=data.get("patronymic", data.get("middleName", "")),
        фракция=data.get("factionName", data.get("faction", "")),
        комитет=data.get("committeeName", data.get("committee", "")),
        регион=data.get("districtName", data.get("region", "")),
        созыв=str(data.get("convocation", data.get("sozyv", ""))),
        foto_ssylka=data.get("photoUrl", data.get("photo", "")),
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
    params: dict[str, str | int] = {"limit": min(ogranichenie, 50), "page": stranitsa}
    if status:
        params["status"] = status

    token = _poluchit_api_token()
    if token:
        params["app_token"] = token

    try:
        data = await http_poluchit(f"{DUMA_LAWS}/bills", params=params)
        return _razobrat_zakonoproekty(data)
    except Exception:
        return []


def _razobrat_zakonoproekty(data: Any) -> list[Zakonoproekt]:
    """Разбор данных законопроектов из ответа API."""
    if isinstance(data, dict):
        elementy = data.get("bills", data.get("items", []))
    elif isinstance(data, list):
        elementy = data
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
    params: dict[str, str | int] = {"limit": min(ogranichenie, 50), "page": stranitsa}
    if sozyv:
        params["convocation"] = sozyv

    token = _poluchit_api_token()
    if token:
        params["app_token"] = token

    try:
        data = await http_poluchit(DUMA_VOTES, params=params)
        return _razobrat_golosovaniya(data)
    except Exception:
        return []


def _razobrat_golosovaniya(data: Any) -> list[Golosovanie]:
    """Разбор результатов голосований из ответа API."""
    if isinstance(data, dict):
        elementy = data.get("votes", data.get("items", []))
    elif isinstance(data, list):
        elementy = data
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
