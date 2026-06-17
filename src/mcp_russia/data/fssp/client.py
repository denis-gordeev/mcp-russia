"""HTTP-клиент для модуля ФССП.

Интеграция с Банком данных исполнительных производств:
    https://fssp.gov.ru/iss/ip
"""

from __future__ import annotations

import logging
from typing import Any

from mcp_russia._shared.http_client import http_get, http_post

from .constants import FSSP_IP_BASE, FSSP_SEARCH_API

logger = logging.getLogger(__name__)


def _parse_fio(fio: str) -> dict[str, str]:
    """Разбор ФИО на компоненты (фамилия, имя, отчество)."""
    parts = fio.strip().split()
    result: dict[str, str] = {}
    if len(parts) >= 1:
        result["lastName"] = parts[0]
    if len(parts) >= 2:
        result["firstName"] = parts[1]
    if len(parts) >= 3:
        result["patronymic"] = " ".join(parts[2:])
    return result


def _parse_proizvodstva(data: Any) -> list[dict[str, Any]]:
    """Разбор ответа API ФССП в список исполнительных производств."""
    if not isinstance(data, dict):
        return []
    inner = data.get("data", data)
    if not isinstance(inner, dict):
        return []
    result = inner.get("result", [])
    if not isinstance(result, list):
        return []
    records = []
    for item in result:
        if not isinstance(item, dict):
            continue
        records.append(_normalise_proizvodstvo(item))
    return records


def _normalise_proizvodstvo(item: dict[str, Any]) -> dict[str, Any]:
    """Нормализация записи исполнительного производства."""
    return {
        "nomer": item.get("number", item.get("номер", "")),
        "dolzhnik": item.get("name", item.get("должник", item.get("nameRaw", ""))),
        "data_vozbuzhdeniya": item.get("date", item.get("дата_возбуждения", "")),
        "subject": item.get("subject", item.get("предмет", "")),
        "summa": item.get("sum", item.get("сумма", "")),
        "otdel_pristavov": item.get("department", item.get("отдел", "")),
        "pristav": item.get("bailiff", item.get("пристав", "")),
        "ip_end": item.get("ip_end", item.get("окончание", "")),
        "osnovanie": item.get("basis", item.get("основание", "")),
        "region": item.get("region", item.get("регион", "")),
    }


async def poisk_proizvodstv(
    fio: str,
    data_rozhdeniya: str = "",
    region: str = "",
) -> list[dict[str, Any]]:
    """Поиск исполнительных производств по ФИО должника.

    Аргументы:
        fio: ФИО должника.
        data_rozhdeniya: Дата рождения должника.
        region: Код региона.

    Возвращает:
        Список исполнительных производств.
    """
    fio_parts = _parse_fio(fio)
    body: dict[str, Any] = {"is": fio_parts}
    if data_rozhdeniya:
        body["is"]["date"] = data_rozhdeniya
    if region:
        body["is"]["region"] = region
    try:
        data = await http_post(FSSP_SEARCH_API, json_body=body)
        return _parse_proizvodstva(data)
    except Exception:
        logger.exception("Ошибка при поиске производств по ФИО «%s»", fio)
        try:
            params: dict[str, Any] = {}
            if "lastName" in fio_parts:
                params["is[lastName]"] = fio_parts["lastName"]
            if "firstName" in fio_parts:
                params["is[firstName]"] = fio_parts["firstName"]
            if "patronymic" in fio_parts:
                params["is[patronymic]"] = fio_parts["patronymic"]
            if data_rozhdeniya:
                params["is[date]"] = data_rozhdeniya
            if region:
                params["is[region]"] = region
            data = await http_get(FSSP_IP_BASE, params=params)
            return _parse_proizvodstva(data)
        except Exception:
            logger.exception("Ошибка при резервном поиске производств по ФИО «%s»", fio)
            return []


async def info_proizvodstva(nomer: str) -> dict[str, Any] | None:
    """Получить информацию об исполнительном производстве по номеру.

    Аргументы:
        nomer: Номер исполнительного производства.

    Возвращает:
        Данные производства или None.
    """
    try:
        data = await http_get(f"{FSSP_IP_BASE}", params={"number": nomer})
        records = _parse_proizvodstva(data)
        for r in records:
            if r.get("nomer") == nomer:
                return r
        return records[0] if records else None
    except Exception:
        logger.exception("Ошибка при получении информации о производстве %s", nomer)
        return None


async def ogranicheniya_dolzhnika(
    fio: str,
    data_rozhdeniya: str = "",
) -> list[dict[str, Any]]:
    """Найти ограничения, наложенные на должника (запрет на выезд, арест и т.д.).

    Аргументы:
        fio: ФИО должника.
        data_rozhdeniya: Дата рождения должника.

    Возвращает:
        Список производств с ограничениями.
    """
    proizvodstva = await poisk_proizvodstv(fio, data_rozhdeniya)
    restrictions = []
    for p in proizvodstva:
        subject = p.get("subject", "").lower()
        ip_end = p.get("ip_end", "")
        if (
            any(kw in subject for kw in ("ограничен", "запрет", "арест", "выезд", "управлен"))
            or ip_end
        ):
            restrictions.append(p)
    return restrictions


async def rozysk_dolzhnika(fio: str) -> list[dict[str, Any]]:
    """Найти производства с розыском должника.

    Аргументы:
        fio: ФИО должника.

    Возвращает:
        Список производств с розыском.
    """
    proizvodstva = await poisk_proizvodstv(fio)
    wanted = []
    for p in proizvodstva:
        subject = p.get("subject", "").lower()
        if "розыск" in subject or "разыск" in subject:
            wanted.append(p)
    return wanted
