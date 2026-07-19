"""HTTP-клиент для модуля ФНС.

Интеграция с реальными API:
    - ЕГРЮЛ/ЕГРИП: https://egrul.nalog.ru (публичные данные о юрлицах и ИП)

API ЕГРЮЛ использует двухшаговый процесс:
    1. POST для запуска поиска → получение идентификатора задачи
    2. GET результата поиска по идентификатору задачи → получение данных организации
"""

from __future__ import annotations

import asyncio
from typing import Any

from mcp_russia._shared.http_client import http_otpravit, http_poluchit

from .constants import EGRUL_BAZA_API
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
        rezultat = await _poisk_egrul(inn)
        if not rezultat:
            return None

        zapisi = rezultat.get("rows", []) if isinstance(rezultat, dict) else []
        if not zapisi:
            return None

        zapis = zapisi[0]
        return _razobrat_egrul_organizatsiyu(zapis)
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
        rezultat = await _poisk_egrul(inn)
        if not rezultat:
            return None

        zapisi = rezultat.get("rows", []) if isinstance(rezultat, dict) else []
        if not zapisi:
            return None

        zapis = zapisi[0]
        return _razobrat_egrul_ip(zapis)
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
    organizaciya = await poluchit_organizaciyu(inn)
    if not organizaciya:
        return None

    return SvedeniyaOrganizacii(
        inn=organizaciya.inn,
        nazvanie=organizaciya.nazvanie,
        registracionnyy_nomer=organizaciya.ogrn,
        data_postanovki_na_uchet=organizaciya.data_registracii,
        nalogovyy_organ="",
        rezhim_nalogooblozheniya="",
        srednespisochnaya_chislennost=None,
    )


async def _poisk_egrul(zapros: str) -> dict[str, Any] | None:
    """Двухшаговый поиск через API ЕГРЮЛ nalog.ru.

    Шаг 1: POST-запрос поиска → получение идентификатора задачи.
    Шаг 2: GET-запрос результата поиска по идентификатору задачи.

    Аргументы:
        zapros: ИНН, ОГРН или название организации для поиска.

    Возвращает:
        Данные результата поиска или None.
    """
    adres_poiska = EGRUL_BAZA_API
    adres_rezultata = f"{EGRUL_BAZA_API}/search-result/"

    dannye_zadachi = await http_otpravit(
        adres_poiska,
        zagolovki={"Content-Type": "application/x-www-form-urlencoded"},
        telo_json=None,
        parametry={"query": zapros},
    )

    zheton = dannye_zadachi.get("t") if isinstance(dannye_zadachi, dict) else None
    if not zheton:
        return None

    await asyncio.sleep(0.5)

    rezultat = await http_poluchit(f"{adres_rezultata}{zheton}")
    return rezultat


def _razobrat_egrul_organizatsiyu(zapis: dict[str, Any]) -> OrganizaciyaEGRUL:
    """Разбор записи ЕГРЮЛ в схему OrganizaciyaEGRUL."""
    return OrganizaciyaEGRUL(
        inn=zapis.get("inn", "") or zapis.get("t", ""),
        ogrn=zapis.get("ogrn", "") or zapis.get("o", ""),
        nazvanie=zapis.get("n", "") or zapis.get("c", ""),
        polnoe_nazvanie=zapis.get("n", ""),
        yuridicheskiy_adres=zapis.get("a", ""),
        data_registracii=zapis.get("r", "") or zapis.get("g", ""),
        sostoyanie=_razobrat_status(zapis.get("s", "")),
        vid_deyatelnosti=zapis.get("k", ""),
        ustroyennyy_kapital="",
        rukovoditel="",
    )


def _razobrat_egrul_ip(zapis: dict[str, Any]) -> IPEGRIP:
    """Разбор записи ЕГРИП в схему IPEGRIP."""
    return IPEGRIP(
        inn=zapis.get("inn", "") or zapis.get("t", ""),
        ogrnip=zapis.get("ogrn", "") or zapis.get("o", ""),
        fio=zapis.get("n", "") or zapis.get("c", ""),
        data_registracii=zapis.get("r", "") or zapis.get("g", ""),
        sostoyanie=_razobrat_status(zapis.get("s", "")),
        vid_deyatelnosti=zapis.get("k", ""),
    )


def _razobrat_status(kod_statusa: Any) -> str:
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
