"""HTTP-клиент для модуля МВД России.

Интеграция с реальными источниками:
    - Открытые данные МВД: мвд.рф/открытые-данные (CSV)
    - Портал открытых данных: data.gov.ru
"""

from __future__ import annotations

import csv
import io
import logging
from typing import Any

from mcp_russia._shared.http_client import http_poluchit

from .constants import (
    DATA_GOV_RU_MVD,
    MVD_OTKRYTYE_DANNYE,
    NABORY_DANNYKH,
    STATISTIKA_DTP_2024,
    STATISTIKA_PRESTUPNOSTI_2024,
)

logger = logging.getLogger(__name__)


async def statistika_prestupnosti(
    subiekt: str = "",
    god: int = 0,
) -> list[dict[str, Any]]:
    """Получить статистику преступности из открытых данных МВД.

    Аргументы:
        subiekt: Субъект РФ.
        god: Год статистики.

    Возвращает:
        Список данных о преступности.
    """
    identifikator = NABORY_DANNYKH["prestupnost"]["identifikator"]
    try:
        adres_url = f"{DATA_GOV_RU_MVD}-{identifikator}/data.csv"
        syrye_dannye = await http_poluchit(adres_url, taimaut=30.0)
        if isinstance(syrye_dannye, str) and syrye_dannye.strip():
            return _razobrat_csv_prestupnosti(syrye_dannye, subiekt=subiekt, god=god)
        if isinstance(syrye_dannye, bytes):
            return _razobrat_csv_prestupnosti(
                syrye_dannye.decode("utf-8", errors="replace"),
                subiekt=subiekt,
                god=god,
            )
    except Exception:
        logger.debug("Открытые данные МВД (преступность) недоступны")

    try:
        adres_url = f"{MVD_OTKRYTYE_DANNYE}/{identifikator}"
        dannye = await http_poluchit(adres_url, taimaut=15.0)
        elementy = _izvlech_spisok(dannye)
        if elementy:
            return [
                _razobrat_zapis_prestupnosti(zapis, subiekt=subiekt, god=god)
                for zapis in elementy
                if isinstance(zapis, dict)
            ]
    except Exception:
        logger.debug("мвд.рф API недоступен")

    return []


async def statistika_dtp(
    subiekt: str = "",
    god: int = 0,
    vid_dtp: str = "",
) -> list[dict[str, Any]]:
    """Получить статистику ДТП из открытых данных МВД.

    Аргументы:
        subiekt: Субъект РФ.
        god: Год статистики.
        vid_dtp: Вид ДТП.

    Возвращает:
        Список данных о ДТП.
    """
    identifikator = NABORY_DANNYKH["dtp"]["identifikator"]
    try:
        adres_url = f"{DATA_GOV_RU_MVD}-{identifikator}/data.csv"
        syrye_dannye = await http_poluchit(adres_url, taimaut=30.0)
        tekst = (
            syrye_dannye
            if isinstance(syrye_dannye, str)
            else syrye_dannye.decode("utf-8", errors="replace")
            if isinstance(syrye_dannye, bytes)
            else ""
        )
        if tekst.strip():
            return _razobrat_csv_dtp(tekst, subiekt=subiekt, god=god, vid_dtp=vid_dtp)
    except Exception:
        logger.debug("Открытые данные МВД (ДТП) недоступны")

    return []


async def rozysk_del(
    kategoriya: str = "",
    subiekt: str = "",
    ogranichenie: int = 20,
) -> list[dict[str, Any]]:
    """Получить данные розыска из открытых данных МВД.

    Аргументы:
        kategoriya: Категория розыскного дела.
        subiekt: Регион.
        ogranichenie: Максимум результатов.

    Возвращает:
        Список розыскных дел.
    """
    identifikator = NABORY_DANNYKH["rozysk"]["identifikator"]
    try:
        adres_url = f"{DATA_GOV_RU_MVD}-{identifikator}/data.csv"
        syrye_dannye = await http_poluchit(adres_url, taimaut=30.0)
        tekst = (
            syrye_dannye
            if isinstance(syrye_dannye, str)
            else syrye_dannye.decode("utf-8", errors="replace")
            if isinstance(syrye_dannye, bytes)
            else ""
        )
        if tekst.strip():
            return _razobrat_csv_rozysk(
                tekst,
                kategoriya=kategoriya,
                subiekt=subiekt,
                ogranichenie=ogranichenie,
            )
    except Exception:
        logger.debug("Открытые данные МВД (розыск) недоступны")

    return []


async def narkotiki(
    subiekt: str = "",
    vid_narkotika: str = "",
) -> list[dict[str, Any]]:
    """Получить данные о наркотических преступлениях.

    Аргументы:
        subiekt: Регион.
        vid_narkotika: Вид наркотика.

    Возвращает:
        Список данных о наркотических преступлениях.
    """
    identifikator = NABORY_DANNYKH["narkotiki"]["identifikator"]
    try:
        adres_url = f"{DATA_GOV_RU_MVD}-{identifikator}/data.csv"
        syrye_dannye = await http_poluchit(adres_url, taimaut=30.0)
        tekst = (
            syrye_dannye
            if isinstance(syrye_dannye, str)
            else syrye_dannye.decode("utf-8", errors="replace")
            if isinstance(syrye_dannye, bytes)
            else ""
        )
        if tekst.strip():
            return _razobrat_csv_narkotiki(tekst, subiekt=subiekt, vid_narkotika=vid_narkotika)
    except Exception:
        logger.debug("Открытые данные МВД (наркотики) недоступны")

    return []


def poluchit_statistiku_prestupnosti_staticheskie() -> dict[str, Any]:
    """Вернуть статическую статистику преступности (2024)."""
    return STATISTIKA_PRESTUPNOSTI_2024


def poluchit_statistiku_dtp_staticheskie() -> dict[str, Any]:
    """Вернуть статическую статистику ДТП (2024)."""
    return STATISTIKA_DTP_2024


def poluchit_spisok_naborov_dannykh() -> list[dict[str, str]]:
    """Вернуть справочник доступных наборов открытых данных МВД."""
    return [
        {"kod": klyuch, "nazvanie": znach["nazvanie"]} for klyuch, znach in NABORY_DANNYKH.items()
    ]


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


def _razobrat_csv_prestupnosti(
    tekst: str,
    subiekt: str = "",
    god: int = 0,
) -> list[dict[str, Any]]:
    """Разбор CSV статистики преступности."""
    chitatel = csv.DictReader(io.StringIO(tekst), delimiter=";", quotechar='"')
    rezultaty: list[dict[str, Any]] = []
    for stroka in chitatel:
        try:
            zapis_subiekt = stroka.get("Субъект РФ", stroka.get("subject", ""))
            zapis_god = stroka.get("Год", stroka.get("year", "0"))
            if subiekt and subiekt.lower() not in str(zapis_subiekt).lower():
                continue
            if god and god != _v_tseloe(zapis_god):
                continue
            rezultaty.append(
                {
                    "subiekt": str(zapis_subiekt),
                    "god": _v_tseloe(zapis_god),
                    "zaregistrirovano": _v_tseloe(
                        stroka.get("Зарегистрировано", stroka.get("registered", "0"))
                    ),
                    "raskryto": _v_tseloe(stroka.get("Раскрыто", stroka.get("solved", "0"))),
                    "neraskryto": _v_tseloe(stroka.get("Нераскрыто", stroka.get("unsolved", "0"))),
                    "tyazhkie_osobo_tyazhkie": _v_tseloe(
                        stroka.get("Тяжкие и особо тяжкие", stroka.get("serious", "0"))
                    ),
                    "istochnik": "МВД России (мвд.рф)",
                }
            )
        except Exception:
            continue
    return rezultaty


def _razobrat_csv_dtp(
    tekst: str,
    subiekt: str = "",
    god: int = 0,
    vid_dtp: str = "",
) -> list[dict[str, Any]]:
    """Разбор CSV статистики ДТП."""
    chitatel = csv.DictReader(io.StringIO(tekst), delimiter=";", quotechar='"')
    rezultaty: list[dict[str, Any]] = []
    for stroka in chitatel:
        try:
            zapis_subiekt = stroka.get("Субъект РФ", stroka.get("subject", ""))
            zapis_god = stroka.get("Год", stroka.get("year", "0"))
            zapis_vid = stroka.get("Вид ДТП", stroka.get("type", ""))
            if subiekt and subiekt.lower() not in str(zapis_subiekt).lower():
                continue
            if god and god != _v_tseloe(zapis_god):
                continue
            if vid_dtp and vid_dtp.lower() not in str(zapis_vid).lower():
                continue
            rezultaty.append(
                {
                    "subiekt": str(zapis_subiekt),
                    "god": _v_tseloe(zapis_god),
                    "vid_dtp": str(zapis_vid),
                    "vsego_dtp": _v_tseloe(stroka.get("Всего ДТП", stroka.get("total", "0"))),
                    "pogibshikh": _v_tseloe(stroka.get("Погибших", stroka.get("deaths", "0"))),
                    "postradavshikh": _v_tseloe(
                        stroka.get("Пострадавших", stroka.get("injured", "0"))
                    ),
                    "istochnik": "МВД России (мвд.рф)",
                }
            )
        except Exception:
            continue
    return rezultaty


def _razobrat_csv_rozysk(
    tekst: str,
    kategoriya: str = "",
    subiekt: str = "",
    ogranichenie: int = 20,
) -> list[dict[str, Any]]:
    """Разбор CSV данных розыска."""
    chitatel = csv.DictReader(io.StringIO(tekst), delimiter=";", quotechar='"')
    rezultaty: list[dict[str, Any]] = []
    for stroka in chitatel:
        if len(rezultaty) >= ogranichenie:
            break
        try:
            zapis_kategoriya = stroka.get("Категория", stroka.get("category", ""))
            zapis_subiekt = stroka.get("Регион", stroka.get("region", ""))
            if kategoriya and kategoriya.lower() not in str(zapis_kategoriya).lower():
                continue
            if subiekt and subiekt.lower() not in str(zapis_subiekt).lower():
                continue
            rezultaty.append(
                {
                    "kategoriya": str(zapis_kategoriya),
                    "subiekt": str(zapis_subiekt),
                    "kolichestvo": _v_tseloe(stroka.get("Количество", stroka.get("count", "0"))),
                    "data": stroka.get("Дата", stroka.get("date", "")),
                    "istochnik": "МВД России (мвд.рф)",
                }
            )
        except Exception:
            continue
    return rezultaty


def _razobrat_csv_narkotiki(
    tekst: str,
    subiekt: str = "",
    vid_narkotika: str = "",
) -> list[dict[str, Any]]:
    """Разбор CSV данных о наркотических преступлениях."""
    chitatel = csv.DictReader(io.StringIO(tekst), delimiter=";", quotechar='"')
    rezultaty: list[dict[str, Any]] = []
    for stroka in chitatel:
        try:
            zapis_subiekt = stroka.get("Субъект РФ", stroka.get("subject", ""))
            zapis_vid = stroka.get("Вид наркотика", stroka.get("drugType", ""))
            if subiekt and subiekt.lower() not in str(zapis_subiekt).lower():
                continue
            if vid_narkotika and vid_narkotika.lower() not in str(zapis_vid).lower():
                continue
            rezultaty.append(
                {
                    "subiekt": str(zapis_subiekt),
                    "vid_prestupleniya": stroka.get(
                        "Вид преступления", stroka.get("crimeType", "")
                    ),
                    "kolichestvo_prestupleniy": _v_tseloe(
                        stroka.get("Количество", stroka.get("count", "0"))
                    ),
                    "izyato_gramm": _v_chislo(
                        stroka.get("Изъято (г)", stroka.get("seizedGrams", "0"))
                    ),
                    "vid_narkotika": str(zapis_vid),
                    "istochnik": "МВД России (мвд.рф)",
                }
            )
        except Exception:
            continue
    return rezultaty


def _razobrat_zapis_prestupnosti(
    zapis: dict[str, Any],
    subiekt: str = "",
    god: int = 0,
) -> dict[str, Any]:
    """Разбор JSON-записи преступности."""
    zapis_subiekt = zapis.get("subject", zapis.get("region", ""))
    zapis_god = zapis.get("year", 0)
    if subiekt and subiekt.lower() not in str(zapis_subiekt).lower():
        return {}
    if god and god != _v_tseloe(zapis_god):
        return {}
    return {
        "subiekt": str(zapis_subiekt),
        "god": _v_tseloe(zapis_god),
        "zaregistrirovano": _v_tseloe(zapis.get("registered", 0)),
        "raskryto": _v_tseloe(zapis.get("solved", 0)),
        "neraskryto": _v_tseloe(zapis.get("unsolved", 0)),
        "tyazhkie_osobo_tyazhkie": _v_tseloe(zapis.get("serious", 0)),
        "istochnik": "МВД России (мвд.рф)",
    }


def _v_tseloe(znachenie: Any) -> int:
    """Безопасное приведение к целому."""
    try:
        return int(float(str(znachenie).replace(" ", "").replace(",", ".") or "0"))
    except (ValueError, TypeError):
        return 0


def _v_chislo(znachenie: Any) -> float:
    """Безопасное приведение к числу."""
    try:
        return float(str(znachenie).replace(" ", "").replace(",", ".") or "0")
    except (ValueError, TypeError):
        return 0.0
