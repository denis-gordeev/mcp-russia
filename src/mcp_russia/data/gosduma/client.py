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
from mcp_russia._shared.http_client import http_get

from .constants import DUMA_DEPUTATS, DUMA_LAWS, DUMA_VOTES, FRAKCII, SOZYVY
from .schemas import Deputat, Frakciya, Golosovanie, Zakonoproekt


def _get_api_token() -> str:
    """Получение токена API Госдумы из настроек."""
    return settings.DUMA_API_TOKEN


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

    token = _get_api_token()
    if token:
        params["app_token"] = token

    try:
        data = await http_get(DUMA_DEPUTATS, params=params)
        return _parse_deputats(data)
    except Exception:
        return []


def _parse_deputats(data: Any) -> list[Deputat]:
    """Разбор данных депутатов из ответа API."""
    if isinstance(data, dict):
        items = data.get("deputies", data.get("items", []))
    elif isinstance(data, list):
        items = data
    else:
        return []

    results = []
    for d in items:
        if not isinstance(d, dict):
            continue
        frakciya_raw = d.get("factionName", d.get("faction", ""))
        results.append(
            Deputat(
                id=d.get("id", 0),
                фамилия=d.get("surname", d.get("lastName", "")),
                имя=d.get("name", d.get("firstName", "")),
                отчество=d.get("patronymic", d.get("middleName", "")),
                фракция=frakciya_raw,
                комитет=d.get("committeeName", d.get("committee", "")),
                регион=d.get("districtName", d.get("region", "")),
                созыв=str(d.get("convocation", d.get("sozyv", ""))),
                foto_url=d.get("photoUrl", d.get("photo", "")),
            )
        )
    return results


async def poluchit_deputata(id: int) -> Deputat | None:
    """Получение конкретного депутата по ID.

    Аргументы:
        id: ID депутата.

    Возвращает:
        Данные депутата или None.
    """
    token = _get_api_token()
    params: dict[str, str] = {}
    if token:
        params["app_token"] = token

    url = f"{DUMA_DEPUTATS}/{id}"
    try:
        data = await http_get(url, params=params)
        if isinstance(data, dict):
            return _parse_one_deputat(data)
    except Exception:
        pass

    deputats = await poluchit_deputatov()
    for d in deputats:
        if d.id == id:
            return d
    return None


def _parse_one_deputat(data: dict[str, Any]) -> Deputat | None:
    """Разбор данных одного депутата из ответа API."""
    if not isinstance(data, dict):
        return None
    return Deputat(
        id=data.get("id", 0),
        фамилия=data.get("surname", data.get("lastName", "")),
        имя=data.get("name", data.get("firstName", "")),
        отчество=data.get("patronymic", data.get("middleName", "")),
        фракция=data.get("factionName", data.get("faction", "")),
        комитет=data.get("committeeName", data.get("committee", "")),
        регион=data.get("districtName", data.get("region", "")),
        созыв=str(data.get("convocation", data.get("sozyv", ""))),
        foto_url=data.get("photoUrl", data.get("photo", "")),
    )


async def poluchit_zakonoproekty(
    status: str = "",
    limit: int = 20,
    page: int = 1,
) -> list[Zakonoproekt]:
    """Получение законопроектов из API СОЗД.

    Аргументы:
        status: Фильтр по статусу (необязательно).
        limit: Максимальное количество результатов.
        page: Номер страницы.

    Возвращает:
        Список законопроектов.
    """
    params: dict[str, str | int] = {"limit": min(limit, 50), "page": page}
    if status:
        params["status"] = status

    token = _get_api_token()
    if token:
        params["app_token"] = token

    try:
        data = await http_get(f"{DUMA_LAWS}/bills", params=params)
        return _parse_zakonoproekty(data)
    except Exception:
        return []


def _parse_zakonoproekty(data: Any) -> list[Zakonoproekt]:
    """Разбор данных законопроектов из ответа API."""
    if isinstance(data, dict):
        items = data.get("bills", data.get("items", []))
    elif isinstance(data, list):
        items = data
    else:
        return []

    results = []
    for item in items:
        if not isinstance(item, dict):
            continue
        results.append(
            Zakonoproekt(
                id=str(item.get("id", "")),
                number=item.get("number", ""),
                title=item.get("name", item.get("title", "")),
                status=item.get("statusName", item.get("status", "")),
                date_vnesen=item.get("dateIntroduction", item.get("introductionDate", "")),
                author=item.get("subjectName", item.get("author", "")),
                readings=item.get("readingsCount", item.get("readings", 0)),
            )
        )
    return results


async def poluchit_golosovaniya(
    sozyv: str = "",
    limit: int = 20,
    page: int = 1,
) -> list[Golosovanie]:
    """Получение результатов голосований из API Госдумы.

    Аргументы:
        sozyv: Номер созыва.
        limit: Максимальное количество результатов.
        page: Номер страницы.

    Возвращает:
        Список результатов голосований.
    """
    params: dict[str, str | int] = {"limit": min(limit, 50), "page": page}
    if sozyv:
        params["convocation"] = sozyv

    token = _get_api_token()
    if token:
        params["app_token"] = token

    try:
        data = await http_get(DUMA_VOTES, params=params)
        return _parse_golosovaniya(data)
    except Exception:
        return []


def _parse_golosovaniya(data: Any) -> list[Golosovanie]:
    """Разбор результатов голосований из ответа API."""
    if isinstance(data, dict):
        items = data.get("votes", data.get("items", []))
    elif isinstance(data, list):
        items = data
    else:
        return []

    results = []
    for item in items:
        if not isinstance(item, dict):
            continue
        results.append(
            Golosovanie(
                zakonoproekt_id=str(item.get("billId", item.get("id", ""))),
                title=item.get("subject", item.get("title", "")),
                date=item.get("date", item.get("voteDate", "")),
                za=item.get("totalFor", item.get("for", 0)),
                protiv=item.get("totalAgainst", item.get("against", 0)),
                vozhderzhalsya=item.get("totalAbstain", item.get("abstain", 0)),
                ne_golosoval=item.get("totalNotVoting", item.get("notVoting", 0)),
            )
        )
    return results


async def poluchit_frakcii() -> list[Frakciya]:
    """Получение текущих фракций Госдумы.

    Возвращает:
        Список фракций.
    """
    return [Frakciya(code=f["code"], name=f["name"]) for f in FRAKCII]


def get_sozyvy() -> list[dict[str, str]]:
    """Возвращает список созывов Государственной Думы."""
    return SOZYVY


def get_frakcii() -> list[dict[str, str]]:
    """Возвращает список текущих фракций."""
    return FRAKCII


def get_komitety() -> list[dict[str, str]]:
    """Возвращает список комитетов Государственной Думы."""
    from .constants import KOMITETY

    return KOMITETY
