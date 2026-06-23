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

from mcp_russia._shared.http_client import http_post
from mcp_russia.exceptions import OshibkaAutentifikatsii
from mcp_russia.settings import DADATA_API_KEY

from .constants import PRAZDNIKI_RF
from .schemas import AdresRF, BankRF, Organizatsiya

DADATA_SUGGEST_URL = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest"
DADATA_FIND_URL = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById"


def _dadata_headers(token: str | None = None) -> dict[str, str]:
    """Сформировать заголовки для авторизации в API Dadata."""
    headers: dict[str, str] = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    key = token or DADATA_API_KEY
    if not key:
        raise OshibkaAutentifikatsii(
            "Для работы с Dadata API необходим ключ MCP_RUSSIA_DADATA_API_KEY. "
            "Зарегистрируйтесь: https://dadata.ru/api/"
        )
    headers["Authorization"] = f"Token {key}"
    return headers


def _nested_get(data: dict, *keys: str, default: Any = None) -> Any:
    """Безопасное извлечение вложенного значения из словаря."""
    for key in keys:
        if not isinstance(data, dict):
            return default
        data = data.get(key, default)
    return data


def _parse_org_data(data: dict[str, Any]) -> dict[str, Any]:
    """Разбор данных организации из ответа Dadata."""
    name_obj = data.get("name")
    name_full = name_obj.get("full") if isinstance(name_obj, dict) else None
    name_short = name_obj.get("short") if isinstance(name_obj, dict) else None
    state_obj = data.get("state")
    status = state_obj.get("status") if isinstance(state_obj, dict) else None
    addr_obj = data.get("address")
    address = addr_obj.get("value") if isinstance(addr_obj, dict) else None
    mgmt_obj = data.get("management")
    director = mgmt_obj.get("name") if isinstance(mgmt_obj, dict) else None
    reg_date = state_obj.get("registration_date") if isinstance(state_obj, dict) else None
    return {
        "nazvanie_polnoe": name_full,
        "nazvanie_kratkoe": name_short,
        "status": status,
        "adres": address,
        "rukovoditel": director,
        "data_registratsii": reg_date,
    }


def _parse_bank_data(data: dict[str, Any], rezervnoe_imya: str = "") -> dict[str, Any]:
    """Разбор данных банка из ответа Dadata."""
    name_obj = data.get("name")
    name_full = name_obj.get("full") if isinstance(name_obj, dict) else rezervnoe_imya
    name_short = name_obj.get("short") if isinstance(name_obj, dict) else None
    addr_obj = data.get("address")
    city = _nested_get(addr_obj, "data", "city") if isinstance(addr_obj, dict) else None
    return {
        "nazvanie_polnoe": name_full,
        "nazvanie_kratkoe": name_short,
        "gorod": city,
    }


async def _suggest_address(zapros: str, token: str | None = None) -> dict[str, Any]:
    """Получить подсказки по адресу через Dadata API."""
    body = {"query": zapros, "count": 10}
    try:
        return await http_post(
            f"{DADATA_SUGGEST_URL}/address",
            json_body=body,
            headers=_dadata_headers(token),
        )
    except Exception:
        return {"suggestions": []}


async def _find_by_fias(identifikator_fias: str, token: str | None = None) -> dict[str, Any]:
    """Найти адрес по ФИАС-идентификатору через Dadata API."""
    body = {"query": identifikator_fias}
    try:
        return await http_post(
            f"{DADATA_FIND_URL}/address",
            json_body=body,
            headers=_dadata_headers(token),
        )
    except Exception:
        return {"suggestions": []}


async def _postal_by_index(indeks: str, token: str | None = None) -> dict[str, Any]:
    """Найти адрес по почтовому индексу через Dadata API."""
    body = {"query": indeks, "count": 1}
    try:
        return await http_post(
            f"{DADATA_SUGGEST_URL}/address",
            json_body=body,
            headers=_dadata_headers(token),
        )
    except Exception:
        return {"suggestions": []}


async def _find_org_by_inn(inn: str, token: str | None = None) -> dict[str, Any]:
    """Найти организацию по ИНН через Dadata API."""
    body = {"query": inn}
    try:
        return await http_post(
            f"{DADATA_SUGGEST_URL}/party",
            json_body=body,
            headers=_dadata_headers(token),
        )
    except Exception:
        return {
            "suggestions": [],
            "error": (
                "Не удалось подключиться к API Dadata.\n"
                "Проверьте MCP_RUSSIA_DADATA_API_KEY или зарегистрируйтесь: "
                "https://dadata.ru/api/"
            ),
        }


async def _find_org_by_ogrn(ogrn: str, token: str | None = None) -> dict[str, Any]:
    """Найти организацию по ОГРН через Dadata API."""
    body = {"query": ogrn}
    try:
        return await http_post(
            f"{DADATA_SUGGEST_URL}/party",
            json_body=body,
            headers=_dadata_headers(token),
        )
    except Exception:
        return {
            "suggestions": [],
            "error": "Не удалось подключиться к API Dadata.",
        }


async def _list_banks(token: str | None = None) -> list[dict[str, Any]]:
    """Получить список банков через Dadata API."""
    body = {"query": "", "count": 100}
    try:
        result = await http_post(
            f"{DADATA_SUGGEST_URL}/bank",
            json_body=body,
            headers=_dadata_headers(token),
        )
        return result.get("suggestions", [])
    except Exception:
        return []


async def _find_bank_by_bik(bik: str, token: str | None = None) -> dict[str, Any]:
    """Найти банк по БИК через Dadata API."""
    body = {"query": bik}
    try:
        return await http_post(
            f"{DADATA_SUGGEST_URL}/bank",
            json_body=body,
            headers=_dadata_headers(token),
        )
    except Exception:
        return {"suggestions": []}


def get_holidays(god: int) -> list[dict[str, str]]:
    """Вернуть список государственных праздников РФ на указанный год."""
    holidays = []
    for date_str, name in PRAZDNIKI_RF.items():
        full_date = f"{god}-{date_str}"
        holidays.append(
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
    return holidays


async def consult_address_by_postal(pochtovyy_indeks: str) -> AdresRF | dict[str, str]:
    """Получить адрес по почтовому индексу.

    Аргументы:
        pochtovyy_indeks: Почтовый индекс.

    Возвращает:
        Адрес или словарь с ошибкой.
    """
    result = await _postal_by_index(pochtovyy_indeks)
    suggestions = result.get("suggestions", [])

    if not suggestions:
        return {
            "error": (
                f"Адрес по индексу {pochtovyy_indeks} не найден.\n"
                "Для работы с адресами подключите API Dadata:\n"
                "https://dadata.ru/api/address/"
            ),
        }

    s = suggestions[0]
    data = s.get("data", {})
    return AdresRF(
        pochtovyy_indeks=data.get("postal_code", pochtovyy_indeks),
        region=data.get("region_with_type", ""),
        gorod=data.get("city_with_type") or data.get("settlement_with_type", ""),
        ulitsa=data.get("street_with_type"),
        dom=data.get("house"),
        polnyy_adres=s.get("unrestricted_value") or s.get("value", ""),
    )


async def search_address(zapros: str) -> list[dict[str, str]]:
    """Поиск адресов по строковому запросу.

    Аргументы:
        zapros: Поисковый запрос.

    Возвращает:
        Список найденных адресов.
    """
    result = await _suggest_address(zapros)
    suggestions = result.get("suggestions", [])

    results = []
    for s in suggestions:
        data = s.get("data", {})
        city = data.get("city_with_type") or data.get("settlement_with_type", "")
        results.append(
            {
                "value": s.get("value", ""),
                "pochtovyy_indeks": data.get("postal_code", ""),
                "region": data.get("region_with_type", ""),
                "gorod": city,
                "ulitsa": data.get("street_with_type", ""),
                "dom": data.get("house", ""),
                "fias_id": data.get("fias_id", ""),
            }
        )
    return results


async def find_org_by_inn(inn: str) -> Organizatsiya | dict[str, str]:
    """Найти организацию по ИНН через ЕГРЮЛ/ЕГРИП.

    Аргументы:
        inn: ИНН организации.

    Возвращает:
        Данные организации или словарь с ошибкой.
    """
    result = await _find_org_by_inn(inn)
    if "error" in result and not result.get("suggestions"):
        return {"error": result["error"]}

    suggestions = result.get("suggestions", [])
    if not suggestions:
        return {"error": f"Организация с ИНН {inn} не найдена"}

    data = suggestions[0].get("data", {})
    parsed = _parse_org_data(data)
    return Organizatsiya(
        inn=data.get("inn", inn),
        kpp=data.get("kpp"),
        ogrn=data.get("ogrn"),
        nazvanie_polnoe=parsed["nazvanie_polnoe"],
        nazvanie_kratkoe=parsed["nazvanie_kratkoe"],
        status=parsed["status"],
        adres=parsed["adres"],
        rukovoditel=parsed["rukovoditel"],
        data_registratsii=parsed["data_registratsii"],
    )


async def find_org_by_ogrn(ogrn: str) -> Organizatsiya | dict[str, str]:
    """Найти организацию по ОГРН через ЕГРЮЛ/ЕГРИП.

    Аргументы:
        ogrn: ОГРН организации.

    Возвращает:
        Данные организации или словарь с ошибкой.
    """
    result = await _find_org_by_ogrn(ogrn)
    if "error" in result and not result.get("suggestions"):
        return {"error": result["error"]}

    suggestions = result.get("suggestions", [])
    if not suggestions:
        return {"error": f"Организация с ОГРН {ogrn} не найдена"}

    data = suggestions[0].get("data", {})
    parsed = _parse_org_data(data)
    return Organizatsiya(
        inn=data.get("inn", ""),
        kpp=data.get("kpp"),
        ogrn=data.get("ogrn", ogrn),
        nazvanie_polnoe=parsed["nazvanie_polnoe"],
        nazvanie_kratkoe=parsed["nazvanie_kratkoe"],
        status=parsed["status"],
        adres=parsed["adres"],
    )


async def list_banks_public() -> list[BankRF]:
    """Получить список банков из справочника ЦБ РФ через Dadata."""
    banks_raw = await _list_banks()
    banks = []
    for b in banks_raw:
        data = b.get("data", {})
        parsed = _parse_bank_data(data, b.get("value", ""))
        banks.append(
            BankRF(
                bik=data.get("bic", ""),
                nazvanie=parsed["nazvanie_polnoe"],
                nazvanie_kratkoe=parsed["nazvanie_kratkoe"],
                gorod=parsed["gorod"],
                region=None,
                svift=data.get("swift"),
            )
        )
    return banks


async def find_bank_by_bik(bik: str) -> BankRF | dict[str, str]:
    """Найти банк по БИК через справочник ЦБ РФ.

    Аргументы:
        bik: БИК банка.

    Возвращает:
        Данные банка или словарь с ошибкой.
    """
    result = await _find_bank_by_bik(bik)
    suggestions = result.get("suggestions", [])

    if not suggestions:
        return {"error": f"Банк с БИК {bik} не найден"}

    data = suggestions[0].get("data", {})
    parsed = _parse_bank_data(data, suggestions[0].get("value", ""))
    return BankRF(
        bik=data.get("bic", bik),
        nazvanie=parsed["nazvanie_polnoe"],
        nazvanie_kratkoe=parsed["nazvanie_kratkoe"],
        gorod=parsed["gorod"],
        region=None,
        svift=data.get("swift"),
    )
