"""HTTP client for the RosAPI feature.

Provides access to Russian reference data via Dadata API:
- Address suggestions (ФИАС)
- Organization lookup by INN/OGRN (ЕГРЮЛ/ЕГРИП)
- Bank directory (ЦБ РФ)

Dadata free tier: 10,000 requests/day.
Register at https://dadata.ru/api/ for an API key.
Set MCP_RUSSIA_DADATA_API_KEY in environment.
"""

from __future__ import annotations

from typing import Any

from mcp_russia._shared.http_client import http_post
from mcp_russia.settings import DADATA_API_KEY

from .constants import PRAZDNIKI_RF
from .schemas import AdresRF, BankRF, Organizatsiya

DADATA_SUGGEST_URL = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest"
DADATA_FIND_URL = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById"


def _dadata_headers(token: str | None = None) -> dict[str, str]:
    headers: dict[str, str] = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    key = token or DADATA_API_KEY
    if key:
        headers["Authorization"] = f"Token {key}"
    return headers


def _nested_get(data: dict, *keys: str, default: Any = None) -> Any:
    for key in keys:
        if not isinstance(data, dict):
            return default
        data = data.get(key, default)
    return data


def _parse_org_data(data: dict[str, Any]) -> dict[str, Any]:
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
        "name_full": name_full,
        "name_short": name_short,
        "status": status,
        "address": address,
        "director": director,
        "registration_date": reg_date,
    }


def _parse_bank_data(data: dict[str, Any], fallback_name: str = "") -> dict[str, Any]:
    name_obj = data.get("name")
    name_full = name_obj.get("full") if isinstance(name_obj, dict) else fallback_name
    name_short = name_obj.get("short") if isinstance(name_obj, dict) else None
    addr_obj = data.get("address")
    city = _nested_get(addr_obj, "data", "city") if isinstance(addr_obj, dict) else None
    return {
        "name_full": name_full,
        "name_short": name_short,
        "city": city,
    }


async def _suggest_address(query: str, token: str | None = None) -> dict[str, Any]:
    body = {"query": query, "count": 10}
    try:
        return await http_post(
            f"{DADATA_SUGGEST_URL}/address",
            json_body=body,
            headers=_dadata_headers(token),
        )
    except Exception:
        return {"suggestions": []}


async def _find_by_fias(fias_id: str, token: str | None = None) -> dict[str, Any]:
    body = {"query": fias_id}
    try:
        return await http_post(
            f"{DADATA_FIND_URL}/address",
            json_body=body,
            headers=_dadata_headers(token),
        )
    except Exception:
        return {"suggestions": []}


async def _postal_by_index(index: str, token: str | None = None) -> dict[str, Any]:
    body = {"query": index, "count": 1}
    try:
        return await http_post(
            f"{DADATA_SUGGEST_URL}/address",
            json_body=body,
            headers=_dadata_headers(token),
        )
    except Exception:
        return {"suggestions": []}


async def _find_org_by_inn(inn: str, token: str | None = None) -> dict[str, Any]:
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
    body = {"query": bik}
    try:
        return await http_post(
            f"{DADATA_SUGGEST_URL}/bank",
            json_body=body,
            headers=_dadata_headers(token),
        )
    except Exception:
        return {"suggestions": []}


def get_holidays(year: int) -> list[dict[str, str]]:
    holidays = []
    for date_str, name in PRAZDNIKI_RF.items():
        full_date = f"{year}-{date_str}"
        holidays.append(
            {
                "date": full_date,
                "name": name,
                "type": "national"
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
                else "weekend",
            }
        )
    return holidays


async def consult_address_by_postal(postal_code: str) -> AdresRF | dict[str, str]:
    result = await _postal_by_index(postal_code)
    suggestions = result.get("suggestions", [])

    if not suggestions:
        return {
            "error": (
                f"Адрес по индексу {postal_code} не найден.\n"
                "Для работы с адресами подключите API Dadata:\n"
                "https://dadata.ru/api/address/"
            ),
        }

    s = suggestions[0]
    data = s.get("data", {})
    return AdresRF(
        postal_code=data.get("postal_code", postal_code),
        region=data.get("region_with_type", ""),
        city=data.get("city_with_type") or data.get("settlement_with_type", ""),
        street=data.get("street_with_type"),
        house=data.get("house"),
        full_address=s.get("unrestricted_value") or s.get("value", ""),
    )


async def search_address(query: str) -> list[dict[str, str]]:
    result = await _suggest_address(query)
    suggestions = result.get("suggestions", [])

    results = []
    for s in suggestions:
        data = s.get("data", {})
        city = data.get("city_with_type") or data.get("settlement_with_type", "")
        results.append(
            {
                "value": s.get("value", ""),
                "postal_code": data.get("postal_code", ""),
                "region": data.get("region_with_type", ""),
                "city": city,
                "street": data.get("street_with_type", ""),
                "house": data.get("house", ""),
                "fias_id": data.get("fias_id", ""),
            }
        )
    return results


async def find_org_by_inn(inn: str) -> Organizatsiya | dict[str, str]:
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
        name_full=parsed["name_full"],
        name_short=parsed["name_short"],
        status=parsed["status"],
        address=parsed["address"],
        director=parsed["director"],
        registration_date=parsed["registration_date"],
    )


async def find_org_by_ogrn(ogrn: str) -> Organizatsiya | dict[str, str]:
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
        name_full=parsed["name_full"],
        name_short=parsed["name_short"],
        status=parsed["status"],
        address=parsed["address"],
    )


async def list_banks_public() -> list[BankRF]:
    banks_raw = await _list_banks()
    banks = []
    for b in banks_raw:
        data = b.get("data", {})
        parsed = _parse_bank_data(data, b.get("value", ""))
        banks.append(
            BankRF(
                bik=data.get("bic", ""),
                name=parsed["name_full"],
                name_short=parsed["name_short"],
                city=parsed["city"],
                region=None,
                swift=data.get("swift"),
            )
        )
    return banks


async def find_bank_by_bik(bik: str) -> BankRF | dict[str, str]:
    result = await _find_bank_by_bik(bik)
    suggestions = result.get("suggestions", [])

    if not suggestions:
        return {"error": f"Банк с БИК {bik} не найден"}

    data = suggestions[0].get("data", {})
    parsed = _parse_bank_data(data, suggestions[0].get("value", ""))
    return BankRF(
        bik=data.get("bic", bik),
        name=parsed["name_full"],
        name_short=parsed["name_short"],
        city=parsed["city"],
        region=None,
        swift=data.get("swift"),
    )
