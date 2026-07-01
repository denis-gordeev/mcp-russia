"""HTTP-клиент для модуля РосАПИ.

Обеспечивает доступ к российским справочным данным через API Дадаты:
- Подсказки по адресам (ФИАС)
- Поиск организаций по ИНН/ОГРН (ЕГРЮЛ/ЕГРИП)
- Справочник банков (ЦБ РФ)

Бесплатный тариф Дадаты: 10 000 запросов/день.
Зарегистрируйтесь на https://dadata.ru/api/ для получения API-ключа.
Установите MCP_RUSSIA_DADATA_API_KEY в переменных окружения.
"""

from __future__ import annotations

from typing import Any

from mcp_russia._shared.http_client import http_otpravit
from mcp_russia.exceptions import OshibkaAutentifikatsii
from mcp_russia.settings import KLYUCH_DADATA_API

from .constants import PRAZDNIKI_RF
from .schemas import AdresRF, BankRF, Organizatsiya

DADATA_SUGGEST_URL = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest"
DADATA_FIND_URL = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById"


def _zagolovki_dadaty(zheton: str | None = None) -> dict[str, str]:
    """Сформировать заголовки для авторизации в API Dadata."""
    zagolovki: dict[str, str] = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    klyuch_api = zheton or KLYUCH_DADATA_API
    if not klyuch_api:
        raise OshibkaAutentifikatsii(
            "Для работы с Dadata API необходим ключ MCP_RUSSIA_DADATA_API_KEY. "
            "Зарегистрируйтесь: https://dadata.ru/api/"
        )
    zagolovki["Authorization"] = f"Token {klyuch_api}"
    return zagolovki


def _vlozhennoe_poluchenie(dannye: dict, *keys: str, default: Any = None) -> Any:
    """Безопасное извлечение вложенного значения из словаря."""
    for key in keys:
        if not isinstance(dannye, dict):
            return default
        dannye = dannye.get(key, default)
    return dannye


def _razobrat_dannye_organizatsii(dannye: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных организации из ответа Dadata."""
    obiekt_imeni = dannye.get("name")
    polnoe_nazvanie = obiekt_imeni.get("full") if isinstance(obiekt_imeni, dict) else None
    kratkoe_nazvanie = obiekt_imeni.get("short") if isinstance(obiekt_imeni, dict) else None
    state_obj = dannye.get("state")
    sostoyanie_org = state_obj.get("status") if isinstance(state_obj, dict) else None
    addr_obj = dannye.get("address")
    adres_str = addr_obj.get("value") if isinstance(addr_obj, dict) else None
    mgmt_obj = dannye.get("management")
    rukovoditel_imya = mgmt_obj.get("name") if isinstance(mgmt_obj, dict) else None
    data_reg = state_obj.get("registration_date") if isinstance(state_obj, dict) else None
    return {
        "nazvanie_polnoe": polnoe_nazvanie,
        "nazvanie_kratkoe": kratkoe_nazvanie,
        "sostoyanie": sostoyanie_org,
        "adres": adres_str,
        "rukovoditel": rukovoditel_imya,
        "data_registratsii": data_reg,
    }


def _razobrat_dannye_banka(dannye: dict[str, Any], rezervnoe_imya: str = "") -> dict[str, Any]:
    """Разбор данных банка из ответа Dadata."""
    obiekt_imeni = dannye.get("name")
    polnoe_nazvanie = (
        obiekt_imeni.get("full") if isinstance(obiekt_imeni, dict) else rezervnoe_imya
    )
    kratkoe_nazvanie = obiekt_imeni.get("short") if isinstance(obiekt_imeni, dict) else None
    addr_obj = dannye.get("address")
    gorod = (
        _vlozhennoe_poluchenie(addr_obj, "data", "city") if isinstance(addr_obj, dict) else None
    )
    return {
        "nazvanie_polnoe": polnoe_nazvanie,
        "nazvanie_kratkoe": kratkoe_nazvanie,
        "gorod": gorod,
    }


async def _predlozhit_adres(zapros: str, zheton: str | None = None) -> dict[str, Any]:
    """Получить подсказки по адресу через Dadata API."""
    telo = {"query": zapros, "count": 10}
    try:
        return await http_otpravit(
            f"{DADATA_SUGGEST_URL}/address",
            json_body=telo,
            zagolovki=_zagolovki_dadaty(zheton),
        )
    except Exception:
        return {"predlozheniya": []}


async def _nayti_po_fias(identifikator_fias: str, zheton: str | None = None) -> dict[str, Any]:
    """Найти адрес по ФИАС-идентификатору через Dadata API."""
    telo = {"query": identifikator_fias}
    try:
        return await http_otpravit(
            f"{DADATA_FIND_URL}/address",
            json_body=telo,
            zagolovki=_zagolovki_dadaty(zheton),
        )
    except Exception:
        return {"predlozheniya": []}


async def _pochtovyy_po_indeksu(indeks: str, zheton: str | None = None) -> dict[str, Any]:
    """Найти адрес по почтовому индексу через Dadata API."""
    telo = {"query": indeks, "count": 1}
    try:
        return await http_otpravit(
            f"{DADATA_SUGGEST_URL}/address",
            json_body=telo,
            zagolovki=_zagolovki_dadaty(zheton),
        )
    except Exception:
        return {"predlozheniya": []}


async def _nayti_organizatsiyu_po_inn(inn: str, zheton: str | None = None) -> dict[str, Any]:
    """Найти организацию по ИНН через Dadata API."""
    telo = {"query": inn}
    try:
        return await http_otpravit(
            f"{DADATA_SUGGEST_URL}/party",
            json_body=telo,
            zagolovki=_zagolovki_dadaty(zheton),
        )
    except Exception:
        return {
            "predlozheniya": [],
            "oshibka": (
                "Не удалось подключиться к API Dadata.\n"
                "Проверьте MCP_RUSSIA_DADATA_API_KEY или зарегистрируйтесь: "
                "https://dadata.ru/api/"
            ),
        }


async def _nayti_organizatsiyu_po_ogrn(ogrn: str, zheton: str | None = None) -> dict[str, Any]:
    """Найти организацию по ОГРН через Dadata API."""
    telo = {"query": ogrn}
    try:
        return await http_otpravit(
            f"{DADATA_SUGGEST_URL}/party",
            json_body=telo,
            zagolovki=_zagolovki_dadaty(zheton),
        )
    except Exception:
        return {
            "predlozheniya": [],
            "oshibka": "Не удалось подключиться к API Dadata.",
        }


async def _spisok_bankov(zheton: str | None = None) -> list[dict[str, Any]]:
    """Получить список банков через Dadata API."""
    telo = {"query": "", "count": 100}
    try:
        rezultat = await http_otpravit(
            f"{DADATA_SUGGEST_URL}/bank",
            json_body=telo,
            zagolovki=_zagolovki_dadaty(zheton),
        )
        return rezultat.get("suggestions", [])
    except Exception:
        return []


async def _nayti_bank_po_bik(bik: str, zheton: str | None = None) -> dict[str, Any]:
    """Найти банк по БИК через Dadata API."""
    telo = {"query": bik}
    try:
        return await http_otpravit(
            f"{DADATA_SUGGEST_URL}/bank",
            json_body=telo,
            zagolovki=_zagolovki_dadaty(zheton),
        )
    except Exception:
        return {"predlozheniya": []}


def poluchit_prazdniki(god: int) -> list[dict[str, str]]:
    """Вернуть список государственных праздников РФ на указанный год."""
    prazdniki = []
    for date_str, name in PRAZDNIKI_RF.items():
        full_date = f"{god}-{date_str}"
        prazdniki.append(
            {
                "data": full_date,
                "nazvanie": name,
                "tip": "natsionalnyy"
                if date_str
                in [
                    "01-01",
                    "01-07",
                    "02-23",
                    "03-08",
                    "05-01",
                    "05-09",
                    "06-12",
                    "11-04",
                ]
                else "vykhodnoy",
            }
        )
    return prazdniki


async def konsultirovat_adres_po_pochtovomu(pochtovyy_indeks: str) -> AdresRF | dict[str, str]:
    """Получить адрес по почтовому индексу.

    Аргументы:
        pochtovyy_indeks: Почтовый индекс.

    Возвращает:
        Адрес или словарь с ошибкой.
    """
    rezultat = await _pochtovyy_po_indeksu(pochtovyy_indeks)
    predlozheniya = rezultat.get("suggestions", [])

    if not predlozheniya:
        return {
            "oshibka": (
                f"Адрес по индексу {pochtovyy_indeks} не найден.\n"
                "Для работы с адресами подключите API Dadata:\n"
                "https://dadata.ru/api/address/"
            ),
        }

    s = predlozheniya[0]
    dannye = s.get("data", {})
    return AdresRF(
        pochtovyy_indeks=dannye.get("postal_code", pochtovyy_indeks),
        subiekt=dannye.get("region_with_type", ""),
        gorod=dannye.get("city_with_type") or dannye.get("settlement_with_type", ""),
        ulitsa=dannye.get("street_with_type"),
        dom=dannye.get("house"),
        polnyy_adres=s.get("unrestricted_value") or s.get("value", ""),
    )


async def poisk_adresa(zapros: str) -> list[dict[str, str]]:
    """Поиск адресов по строковому запросу.

    Аргументы:
        zapros: Поисковый запрос.

    Возвращает:
        Список найденных адресов.
    """
    rezultat = await _predlozhit_adres(zapros)
    predlozheniya = rezultat.get("suggestions", [])

    rezultaty = []
    for s in predlozheniya:
        dannye = s.get("data", {})
        gorod = dannye.get("city_with_type") or dannye.get("settlement_with_type", "")
        rezultaty.append(
            {
                "znachenie": s.get("value", ""),
                "pochtovyy_indeks": dannye.get("postal_code", ""),
                "subiekt": dannye.get("region_with_type", ""),
                "gorod": gorod,
                "ulitsa": dannye.get("street_with_type", ""),
                "dom": dannye.get("house", ""),
                "identifikator_fias": dannye.get("fias_id", ""),
            }
        )
    return rezultaty


async def nayti_organizatsiyu_po_inn(inn: str) -> Organizatsiya | dict[str, str]:
    """Найти организацию по ИНН через ЕГРЮЛ/ЕГРИП.

    Аргументы:
        inn: ИНН организации.

    Возвращает:
        Данные организации или словарь с ошибкой.
    """
    rezultat = await _nayti_organizatsiyu_po_inn(inn)
    if "oshibka" in rezultat and not rezultat.get("suggestions"):
        return {"oshibka": rezultat["oshibka"]}

    suggestions = rezultat.get("suggestions", [])
    if not suggestions:
        return {"oshibka": f"Организация с ИНН {inn} не найдена"}

    dannye = suggestions[0].get("data", {})
    razobrannye = _razobrat_dannye_organizatsii(dannye)
    return Organizatsiya(
        inn=dannye.get("inn", inn),
        kpp=dannye.get("kpp"),
        ogrn=dannye.get("ogrn"),
        nazvanie_polnoe=razobrannye["nazvanie_polnoe"],
        nazvanie_kratkoe=razobrannye["nazvanie_kratkoe"],
        sostoyanie=razobrannye["sostoyanie"],
        adres=razobrannye["adres"],
        rukovoditel=razobrannye["rukovoditel"],
        data_registratsii=razobrannye["data_registratsii"],
    )


async def nayti_organizatsiyu_po_ogrn(ogrn: str) -> Organizatsiya | dict[str, str]:
    """Найти организацию по ОГРН через ЕГРЮЛ/ЕГРИП.

    Аргументы:
        ogrn: ОГРН организации.

    Возвращает:
        Данные организации или словарь с ошибкой.
    """
    rezultat = await _nayti_organizatsiyu_po_ogrn(ogrn)
    if "oshibka" in rezultat and not rezultat.get("suggestions"):
        return {"oshibka": rezultat["oshibka"]}

    predlozheniya = rezultat.get("suggestions", [])
    if not predlozheniya:
        return {"oshibka": f"Организация с ОГРН {ogrn} не найдена"}

    dannye = predlozheniya[0].get("data", {})
    razobrannye = _razobrat_dannye_organizatsii(dannye)
    return Organizatsiya(
        inn=dannye.get("inn", ""),
        kpp=dannye.get("kpp"),
        ogrn=dannye.get("ogrn", ogrn),
        nazvanie_polnoe=razobrannye["nazvanie_polnoe"],
        nazvanie_kratkoe=razobrannye["nazvanie_kratkoe"],
        sostoyanie=razobrannye["sostoyanie"],
        adres=razobrannye["adres"],
    )


async def spisok_bankov_publichnyy() -> list[BankRF]:
    """Получить список банков из справочника ЦБ РФ через Dadata."""
    banki_raw = await _spisok_bankov()
    banki = []
    for b in banki_raw:
        dannye = b.get("data", {})
        razobrannye = _razobrat_dannye_banka(dannye, b.get("value", ""))
        banki.append(
            BankRF(
                bik=dannye.get("bic", ""),
                nazvanie=razobrannye["nazvanie_polnoe"],
                nazvanie_kratkoe=razobrannye["nazvanie_kratkoe"],
                gorod=razobrannye["gorod"],
                subiekt=None,
                svift=dannye.get("swift"),
            )
        )
    return banki


async def nayti_bank_po_bik(bik: str) -> BankRF | dict[str, str]:
    """Найти банк по БИК через справочник ЦБ РФ.

    Аргументы:
        bik: БИК банка.

    Возвращает:
        Данные банка или словарь с ошибкой.
    """
    rezultat = await _nayti_bank_po_bik(bik)
    predlozheniya = rezultat.get("suggestions", [])

    if not predlozheniya:
        return {"oshibka": f"Банк с БИК {bik} не найден"}

    dannye = predlozheniya[0].get("data", {})
    razobrannye = _razobrat_dannye_banka(dannye, predlozheniya[0].get("value", ""))
    return BankRF(
        bik=dannye.get("bic", bik),
        nazvanie=razobrannye["nazvanie_polnoe"],
        nazvanie_kratkoe=razobrannye["nazvanie_kratkoe"],
        gorod=razobrannye["gorod"],
        subiekt=None,
        svift=dannye.get("swift"),
    )
