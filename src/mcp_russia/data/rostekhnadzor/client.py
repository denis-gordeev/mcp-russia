"""HTTP-клиент для модуля Ростехнадзора.

Интеграция с реальными источниками:
    - Ростехнадзор: rostechnadzor.gov.ru
    - Открытые данные: data.gov.ru
"""

from __future__ import annotations

import csv
import io
import logging
from typing import Any

from mcp_russia._shared.http_client import http_poluchit

from .constants import (
    DATA_GOV_RU_RT,
    ROSTEKHNADZOR_BAZA,
    STATISTIKA_PROMBEZ_2024,
)

logger = logging.getLogger(__name__)


async def poisk_intsidentov(
    vid: str = "",
    subiekt: str = "",
    ogranichenie: int = 20,
) -> list[dict[str, Any]]:
    """Поиск инцидентов и аварий на ОПО.

    Аргументы:
        vid: Вид инцидента (авария, инцидент, пожар, взрыв).
        subiekt: Регион.
        ogranichenie: Максимум результатов.

    Возвращает:
        Список инцидентов.
    """
    try:
        adres_url = f"{ROSTEKHNADZOR_BAZA}/api/incidents"
        parametry: dict[str, Any] = {"limit": ogranichenie}
        if vid:
            parametry["type"] = vid
        if subiekt:
            parametry["region"] = subiekt
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        if elementy:
            return [_razobrat_intsident(zapis) for zapis in elementy if isinstance(zapis, dict)]
    except Exception:
        logger.debug("rostechnadzor.gov.ru API недоступен для инцидентов")

    try:
        adres_url = f"{DATA_GOV_RU_RT}-incidents/data.csv"
        syrye_dannye = await http_poluchit(adres_url, taimaut=30.0)
        tekst = (
            syrye_dannye
            if isinstance(syrye_dannye, str)
            else syrye_dannye.decode("utf-8", errors="replace")
            if isinstance(syrye_dannye, bytes)
            else ""
        )
        if tekst.strip():
            return _razobrat_csv_intsidentov(
                tekst, vid=vid, subiekt=subiekt, ogranichenie=ogranichenie
            )
    except Exception:
        logger.debug("Открытые данные Ростехнадзора (инциденты) недоступны")

    return []


async def poisk_litsenziy(
    vid: str = "",
    organizatsiya: str = "",
) -> list[dict[str, Any]]:
    """Поиск лицензий Ростехнадзора.

    Аргументы:
        vid: Вид лицензии.
        organizatsiya: Название организации (частичное совпадение).

    Возвращает:
        Список лицензий.
    """
    try:
        adres_url = f"{ROSTEKHNADZOR_BAZA}/api/licenses"
        parametry: dict[str, Any] = {}
        if vid:
            parametry["type"] = vid
        if organizatsiya:
            parametry["org"] = organizatsiya
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        if elementy:
            return [_razobrat_litsenziyu(zapis) for zapis in elementy if isinstance(zapis, dict)]
    except Exception:
        logger.debug("rostechnadzor.gov.ru API недоступен для лицензий")

    try:
        adres_url = f"{DATA_GOV_RU_RT}-licenses/data.csv"
        syrye_dannye = await http_poluchit(adres_url, taimaut=30.0)
        tekst = (
            syrye_dannye
            if isinstance(syrye_dannye, str)
            else syrye_dannye.decode("utf-8", errors="replace")
            if isinstance(syrye_dannye, bytes)
            else ""
        )
        if tekst.strip():
            return _razobrat_csv_litsenziy(tekst, vid=vid, organizatsiya=organizatsiya)
    except Exception:
        logger.debug("Открытые данные Ростехнадзора (лицензии) недоступны")

    return []


async def reestr_opo(
    subiekt: str = "",
    klass_opasnosti: str = "",
    ogranichenie: int = 20,
) -> list[dict[str, Any]]:
    """Реестр опасных производственных объектов.

    Аргументы:
        subiekt: Регион.
        klass_opasnosti: Класс опасности.
        ogranichenie: Максимум результатов.

    Возвращает:
        Список ОПО.
    """
    try:
        adres_url = f"{ROSTEKHNADZOR_BAZA}/api/opo"
        parametry: dict[str, Any] = {"limit": ogranichenie}
        if subiekt:
            parametry["region"] = subiekt
        if klass_opasnosti:
            parametry["hazardClass"] = klass_opasnosti
        dannye = await http_poluchit(adres_url, parametry=parametry, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        if elementy:
            return [_razobrat_opo(zapis) for zapis in elementy if isinstance(zapis, dict)]
    except Exception:
        logger.debug("rostechnadzor.gov.ru API недоступен для реестра ОПО")

    return []


def poluchit_statistiku_prombez_staticheskie() -> dict[str, Any]:
    """Вернуть статическую статистику промышленной безопасности (2024)."""
    return STATISTIKA_PROMBEZ_2024


def _izvlech_spisok(dannye: Any) -> list[Any]:
    """Извлечь список из ответа API."""
    if isinstance(dannye, list):
        return dannye
    if isinstance(dannye, dict):
        for klyuch in ("data", "items", "results", "records"):
            znachenie_spiska = dannye.get(klyuch)
            if isinstance(znachenie_spiska, list):
                return znachenie_spiska
    return []


def _razobrat_intsident(dannye: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных об инциденте."""
    return {
        "nomer": dannye.get("id", "") or dannye.get("number", ""),
        "vid": dannye.get("type", "") or dannye.get("vid", ""),
        "data": dannye.get("date", "") or dannye.get("data", ""),
        "subiekt": dannye.get("region", "") or dannye.get("subject", ""),
        "opisanie": dannye.get("description", "") or dannye.get("opisanie", ""),
        "pogibshikh": dannye.get("deaths", 0) or 0,
        "postradavshikh": dannye.get("injured", 0) or 0,
        "istochnik": "Ростехнадзор (rostechnadzor.gov.ru)",
    }


def _razobrat_litsenziyu(dannye: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных о лицензии."""
    return {
        "nomer": dannye.get("number", "") or dannye.get("nomer", ""),
        "vid": dannye.get("type", "") or dannye.get("vid", ""),
        "organizatsiya": dannye.get("organization", "") or dannye.get("org", ""),
        "subiekt": dannye.get("region", "") or dannye.get("subject", ""),
        "data_vydachi": dannye.get("issueDate", "") or dannye.get("data_vydachi", ""),
        "srok_deystviya": dannye.get("validUntil", "") or dannye.get("srok", ""),
        "sostoyanie": dannye.get("status", "") or dannye.get("sostoyanie", ""),
        "istochnik": "Ростехнадзор (rostechnadzor.gov.ru)",
    }


def _razobrat_opo(dannye: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных об ОПО."""
    return {
        "registratsionnyy_nomer": dannye.get("regNumber", "")
        or dannye.get("registratsionnyy_nomer", ""),
        "nazvanie": dannye.get("name", "") or dannye.get("nazvanie", ""),
        "vid_deyatelnosti": dannye.get("activityType", "") or dannye.get("vid_deyatelnosti", ""),
        "klass_opasnosti": dannye.get("hazardClass", "") or dannye.get("klass_opasnosti", ""),
        "subiekt": dannye.get("region", "") or dannye.get("subject", ""),
        "organizatsiya": dannye.get("organization", "") or dannye.get("org", ""),
        "istochnik": "Ростехнадзор (rostechnadzor.gov.ru)",
    }


def _razobrat_csv_intsidentov(
    tekst: str,
    vid: str = "",
    subiekt: str = "",
    ogranichenie: int = 20,
) -> list[dict[str, Any]]:
    """Разбор CSV инцидентов."""
    chitatel = csv.DictReader(io.StringIO(tekst), delimiter=";", quotechar='"')
    rezultaty: list[dict[str, Any]] = []
    for stroka in chitatel:
        if len(rezultaty) >= ogranichenie:
            break
        try:
            zapis_vid = stroka.get("Вид", stroka.get("type", ""))
            zapis_subiekt = stroka.get("Регион", stroka.get("region", ""))
            if vid and vid.lower() not in str(zapis_vid).lower():
                continue
            if subiekt and subiekt.lower() not in str(zapis_subiekt).lower():
                continue
            rezultaty.append(
                {
                    "nomer": stroka.get("Номер", stroka.get("number", "")),
                    "vid": str(zapis_vid),
                    "data": stroka.get("Дата", stroka.get("date", "")),
                    "subiekt": str(zapis_subiekt),
                    "opisanie": stroka.get("Описание", stroka.get("description", "")),
                    "pogibshikh": _v_tseloe(stroka.get("Погибших", stroka.get("deaths", "0"))),
                    "postradavshikh": _v_tseloe(
                        stroka.get("Пострадавших", stroka.get("injured", "0"))
                    ),
                    "istochnik": "Ростехнадзор (rostechnadzor.gov.ru)",
                }
            )
        except Exception:
            continue
    return rezultaty


def _razobrat_csv_litsenziy(
    tekst: str,
    vid: str = "",
    organizatsiya: str = "",
) -> list[dict[str, Any]]:
    """Разбор CSV лицензий."""
    chitatel = csv.DictReader(io.StringIO(tekst), delimiter=";", quotechar='"')
    rezultaty: list[dict[str, Any]] = []
    for stroka in chitatel:
        try:
            zapis_vid = stroka.get("Вид лицензии", stroka.get("type", ""))
            zapis_org = stroka.get("Организация", stroka.get("organization", ""))
            if vid and vid.lower() not in str(zapis_vid).lower():
                continue
            if organizatsiya and organizatsiya.lower() not in str(zapis_org).lower():
                continue
            rezultaty.append(
                {
                    "nomer": stroka.get("Номер", stroka.get("number", "")),
                    "vid": str(zapis_vid),
                    "organizatsiya": str(zapis_org),
                    "subiekt": stroka.get("Регион", stroka.get("region", "")),
                    "data_vydachi": stroka.get("Дата выдачи", stroka.get("issueDate", "")),
                    "srok_deystviya": stroka.get("Срок", stroka.get("validUntil", "")),
                    "sostoyanie": stroka.get("Статус", stroka.get("status", "")),
                    "istochnik": "Ростехнадзор (rostechnadzor.gov.ru)",
                }
            )
        except Exception:
            continue
    return rezultaty


def _v_tseloe(znachenie: Any) -> int:
    """Безопасное приведение к целому."""
    try:
        return int(float(str(znachenie).replace(" ", "").replace(",", ".") or "0"))
    except (ValueError, TypeError):
        return 0
