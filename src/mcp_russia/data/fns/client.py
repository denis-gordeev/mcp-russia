"""HTTP-клиент для модуля ФНС.

Интеграция с реальными API:
    - ЕГРЮЛ/ЕГРИП: https://egrul.nalog.ru (публичные данные о юрлицах и ИП)

API ЕГРЮЛ использует двухшаговый процесс:
    1. POST для запуска поиска → получение ID задачи
    2. GET результата поиска по ID задачи → получение данных организации
"""

from __future__ import annotations

import asyncio
from typing import Any

from mcp_russia._shared.http_client import http_get, http_post

from .constants import EGRUL_API_BASE
from .schemas import (
    IPEGRIP,
    NalogovayaProverka,
    NalogovoeNachislenie,
    OrganizaciyaEGRUL,
    SvedeniyaOrganizacii,
)


async def poluchit_organizaciyu(inn: str) -> OrganizaciyaEGRUL | None:
    """Получение данных организации из ЕГРЮЛ через egrul.nalog.ru.

    Аргументы:
        inn: ИНН организации (10 цифр).

    Возвращает:
        Данные организации или None.
    """
    try:
        result = await _egrul_search(inn)
        if not result:
            return None

        entries = result.get("rows", []) if isinstance(result, dict) else []
        if not entries:
            return None

        entry = entries[0]
        return _parse_egrul_organization(entry)
    except Exception:
        return None


async def poluchit_ip(inn: str) -> IPEGRIP | None:
    """Получение данных об ИП из ЕГРИП через egrul.nalog.ru.

    Аргументы:
        inn: ИНН ИП (12 цифр).

    Возвращает:
        Данные ИП или None.
    """
    try:
        result = await _egrul_search(inn)
        if not result:
            return None

        entries = result.get("rows", []) if isinstance(result, dict) else []
        if not entries:
            return None

        entry = entries[0]
        return _parse_egrul_ip(entry)
    except Exception:
        return None


async def poluchit_proverki(inn: str) -> list[NalogovayaProverka]:
    """Получение данных налоговой инспекции (требуется авторизованный API).

    Аргументы:
        inn: ИНН организации.

    Возвращает:
        Пустой список — реальная интеграция требует токен API ФНС.
    """
    return []


async def poluchit_nachisleniya(inn: str, period: str = "") -> list[NalogovoeNachislenie]:
    """Получение начислений налогов (заглушка — требуется авторизованный API).

    Аргументы:
        inn: ИНН организации или ИП.
        period: Налоговый период.

    Возвращает:
        Пустой список — реальная интеграция требует токен API ФНС.
    """
    return []


async def poluchit_svedeniya(inn: str) -> SvedeniyaOrganizacii | None:
    """Получение данных об организации из ЕГРЮЛ через egrul.nalog.ru.

    Аргументы:
        inn: ИНН организации (10 цифр).

    Возвращает:
        Данные организации или None.
    """
    org = await poluchit_organizaciyu(inn)
    if not org:
        return None

    return SvedeniyaOrganizacii(
        inn=org.inn,
        nazvanie=org.nazvanie,
        registracionnyy_nomer=org.ogrn,
        data_postanovki_na_uchet=org.data_registracii,
        nalogovyy_organ="",
        rezhim_nalogooblozheniya="",
        srednespisochnaya_chislennost=None,
    )


async def _egrul_search(zapros: str) -> dict[str, Any] | None:
    """Двухшаговый поиск через API ЕГРЮЛ nalog.ru.

    Шаг 1: POST-запрос поиска → получение ID задачи.
    Шаг 2: GET-запрос результата поиска по ID задачи.

    Аргументы:
        zapros: ИНН, ОГРН или название организации для поиска.

    Возвращает:
        Данные результата поиска или None.
    """
    search_url = EGRUL_API_BASE
    result_url = f"{EGRUL_API_BASE}/search-result/"

    task_data = await http_post(
        search_url,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        json_body=None,
        params={"query": zapros},
    )

    token = task_data.get("t") if isinstance(task_data, dict) else None
    if not token:
        return None

    await asyncio.sleep(0.5)

    result = await http_get(f"{result_url}{token}")
    return result


def _parse_egrul_organization(entry: dict[str, Any]) -> OrganizaciyaEGRUL:
    """Разбор записи ЕГРЮЛ в схему OrganizaciyaEGRUL."""
    return OrganizaciyaEGRUL(
        inn=entry.get("inn", "") or entry.get("t", ""),
        ogrn=entry.get("ogrn", "") or entry.get("o", ""),
        nazvanie=entry.get("n", "") or entry.get("c", ""),
        polnoe_nazvanie=entry.get("n", ""),
        yuridicheskiy_adres=entry.get("a", ""),
        data_registracii=entry.get("r", "") or entry.get("g", ""),
        status=_parse_status(entry.get("s", "")),
        vid_deyatelnosti=entry.get("k", ""),
        ustroyennyy_kapital="",
        rukovoditel="",
    )


def _parse_egrul_ip(entry: dict[str, Any]) -> IPEGRIP:
    """Разбор записи ЕГРИП в схему IPEGRIP."""
    return IPEGRIP(
        inn=entry.get("inn", "") or entry.get("t", ""),
        ogrnip=entry.get("ogrn", "") or entry.get("o", ""),
        fio=entry.get("n", "") or entry.get("c", ""),
        data_registracii=entry.get("r", "") or entry.get("g", ""),
        status=_parse_status(entry.get("s", "")),
        vid_deyatelnosti=entry.get("k", ""),
    )


def _parse_status(kod_statusa: Any) -> str:
    """Преобразование кода статуса ЕГРЮЛ в русское описание."""
    karta_statusov = {
        "01": "Действующая",
        "02": "В процессе ликвидации",
        "03": "Ликвидирована",
        "04": "Исключение из ЕГРЮЛ",
        "05": "В процессе реорганизации",
        "06": "Прекратила деятельность",
        "07": "Прекратила деятельность через реорганизацию",
        "08": "Прекратила деятельность через присоединение",
        "09": "Прекратила деятельность через слияние",
        "10": "Прекратила деятельность через разделение",
        "11": "Прекратила деятельность через выделение",
        "12": "Прекратила деятельность через преобразование",
    }
    if isinstance(kod_statusa, str):
        return karta_statusov.get(kod_statusa, kod_statusa)
    return str(kod_statusa) if kod_statusa else ""
