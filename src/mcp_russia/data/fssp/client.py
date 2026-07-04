"""HTTP-клиент для модуля ФССП.

Интеграция с Банком данных исполнительных производств:
    https://fssp.gov.ru/iss/ip
"""

from __future__ import annotations

import logging
from typing import Any

from mcp_russia._shared.http_client import http_otpravit, http_poluchit

from .constants import FSSP_IP_BASE, FSSP_SEARCH_API

logger = logging.getLogger(__name__)


def _razobrat_fio(fio: str) -> dict[str, str]:
    """Разбор ФИО на компоненты (фамилия, имя, отчество)."""
    chasti = fio.strip().split()
    rezultat: dict[str, str] = {}
    if len(chasti) >= 1:
        rezultat["lastName"] = chasti[0]
    if len(chasti) >= 2:
        rezultat["firstName"] = chasti[1]
    if len(chasti) >= 3:
        rezultat["patronymic"] = " ".join(chasti[2:])
    return rezultat


def _razobrat_proizvodstva(dannye: Any) -> list[dict[str, Any]]:
    """Разбор ответа API ФССП в список исполнительных производств."""
    if not isinstance(dannye, dict):
        return []
    vnutrennie = dannye.get("data", dannye)
    if not isinstance(vnutrennie, dict):
        return []
    rezultat = vnutrennie.get("result", [])
    if not isinstance(rezultat, list):
        return []
    zapisi = []
    for zapis in rezultat:
        if not isinstance(zapis, dict):
            continue
        zapisi.append(_normalizovat_proizvodstvo(zapis))
    return zapisi


def _normalizovat_proizvodstvo(zapis: dict[str, Any]) -> dict[str, Any]:
    """Нормализация записи исполнительного производства."""
    return {
        "nomer": zapis.get("number", zapis.get("номер", "")),
        "dolzhnik": zapis.get("name", zapis.get("должник", zapis.get("nameRaw", ""))),
        "data_vozbuzhdeniya": zapis.get("date", zapis.get("дата_возбуждения", "")),
        "subiekt": zapis.get("subject", zapis.get("предмет", "")),
        "summa": zapis.get("sum", zapis.get("сумма", "")),
        "otdel_pristavov": zapis.get("department", zapis.get("отдел", "")),
        "pristav": zapis.get("bailiff", zapis.get("пристав", "")),
        "okonchanie_ip": zapis.get("ip_end", zapis.get("окончание", "")),
        "osnovanie": zapis.get("basis", zapis.get("основание", "")),
        "subiekt_rf": zapis.get("region", zapis.get("регион", "")),
    }


async def poisk_proizvodstv(
    fio: str,
    data_rozhdeniya: str = "",
    subiekt: str = "",
) -> list[dict[str, Any]]:
    """Поиск исполнительных производств по ФИО должника.

    Аргументы:
        fio: ФИО должника.
        data_rozhdeniya: Дата рождения должника.
        subiekt: Код региона.

    Возвращает:
        Список исполнительных производств.
    """
    chasti_fio = _razobrat_fio(fio)
    telo: dict[str, Any] = {"is": chasti_fio}
    if data_rozhdeniya:
        telo["is"]["date"] = data_rozhdeniya
    if subiekt:
        telo["is"]["region"] = subiekt
    try:
        dannye = await http_otpravit(FSSP_SEARCH_API, json_body=telo)
        return _razobrat_proizvodstva(dannye)
    except Exception:
        logger.exception("Ошибка при поиске производств по ФИО «%s»", fio)
        try:
            parametry: dict[str, Any] = {}
            if "lastName" in chasti_fio:
                parametry["is[lastName]"] = chasti_fio["lastName"]
            if "firstName" in chasti_fio:
                parametry["is[firstName]"] = chasti_fio["firstName"]
            if "patronymic" in chasti_fio:
                parametry["is[patronymic]"] = chasti_fio["patronymic"]
            if data_rozhdeniya:
                parametry["is[date]"] = data_rozhdeniya
            if subiekt:
                parametry["is[region]"] = subiekt
            dannye = await http_poluchit(FSSP_IP_BASE, parametry=parametry)
            return _razobrat_proizvodstva(dannye)
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
        dannye = await http_poluchit(f"{FSSP_IP_BASE}", parametry={"number": nomer})
        zapisi = _razobrat_proizvodstva(dannye)
        for r in zapisi:
            if r.get("nomer") == nomer:
                return r
        return zapisi[0] if zapisi else None
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
    ogranicheniya = []
    for p in proizvodstva:
        predmet = p.get("subject", "").lower()
        okonchanie_ip = p.get("okonchanie_ip", "")
        if (
            any(kw in predmet for kw in ("ограничен", "запрет", "арест", "выезд", "управлен"))
            or okonchanie_ip
        ):
            ogranicheniya.append(p)
    return ogranicheniya


async def rozysk_dolzhnika(fio: str) -> list[dict[str, Any]]:
    """Найти производства с розыском должника.

    Аргументы:
        fio: ФИО должника.

    Возвращает:
        Список производств с розыском.
    """
    proizvodstva = await poisk_proizvodstv(fio)
    razyskivaemye = []
    for p in proizvodstva:
        predmet = p.get("subject", "").lower()
        if "розыск" in predmet or "разыск" in predmet:
            razyskivaemye.append(p)
    return razyskivaemye
