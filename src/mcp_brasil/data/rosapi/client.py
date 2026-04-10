"""HTTP client for the RosAPI feature.

Provides access to Russian reference data via various public APIs:
- FIAS (Федеральная информационная адресная система) for addresses
- DADATA for INN/OGRN organization lookups
- CBR for bank directories
- Public holiday APIs

Note: This module uses free public APIs where possible.
For production use, consider registering for API keys at:
- https://dadata.ru/api/ (generous free tier)
- https://fias.nalog.ru/ (official FIAS)
"""

from __future__ import annotations

from typing import Any

from mcp_brasil._shared.http_client import http_get

from .constants import PRAZDNIKI_RF
from .schemas import AdresRF, BankRF, Organizatsiya

# ─── Address / FIAS helpers ───────────────────────────────────────────

# Public API for Russian postal codes (open source alternative)
# Using dadata.ru suggestions API (free tier: 10k requests/day)
DADATA_SUGGEST_URL = "https://suggestions.dadata.ru/api/v4/suggest"
DADATA_FIND_URL = "https://suggestions.dadata.ru/api/v4/find"

# Alternative: use open public APIs without auth
FIAS_PUBLIC = "https://fias.nalog.ru/api"
POSTAL_PUBLIC = "https://api.postal-api.ru/v1"


async def _suggest_address(query: str, token: str | None = None) -> dict[str, Any]:
    """Query Dadata suggestions API for addresses."""
    headers: dict[str, str] = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    if token:
        headers["Authorization"] = f"Token {token}"

    body = {"query": query, "count": 10}
    try:
        return await http_get(f"{DADATA_SUGGEST_URL}/address", json=body, headers=headers)
    except Exception:
        # Fallback: return empty result if API unavailable
        return {"suggestions": []}


async def _find_by_fias(fias_id: str, token: str | None = None) -> dict[str, Any]:
    """Find address by FIAS ID."""
    headers: dict[str, str] = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    if token:
        headers["Authorization"] = f"Token {token}"

    body = {"query": fias_id}
    try:
        return await http_get(f"{DADATA_FIND_URL}/address", json=body, headers=headers)
    except Exception:
        return {"suggestions": []}


# ─── Public postal code API (no auth required) ───────────────────────

async def _postal_by_index(index: str) -> dict[str, Any]:
    """Look up postal office by index using public API.

    Uses api.postal-api.ru or similar open service.
    """
    # Note: This is a placeholder. Replace with actual working API.
    # For now, we provide a reference implementation structure.
    return {
        "error": (
            "Требуется интеграция с API почтовых индексов РФ.\n"
            "Рекомендуемые источники:\n"
            "- Dadata (бесплатный тариф): https://dadata.ru/api/address\n"
            "- Почта России API: https://www.pochta.ru/api\n"
            "- FIAS: https://fias.nalog.ru/"
        ),
        "index": index,
    }


# ─── Organization lookup (INN/OGRN) ─────────────────────────────────

async def _find_org_by_inn(inn: str, token: str | None = None) -> dict[str, Any]:
    """Find organization by INN via Dadata."""
    headers: dict[str, str] = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    if token:
        headers["Authorization"] = f"Token {token}"

    body = {"query": inn}
    try:
        return await http_get(
            f"{DADATA_SUGGEST_URL}/party",
            json=body,
            headers=headers,
        )
    except Exception:
        return {
            "error": (
                "Требуется API-ключ Dadata для поиска организаций.\n"
                "Регистрация: https://dadata.ru/api/ (бесплатный тариф: 10k/день)"
            ),
            "inn": inn,
        }


async def _find_org_by_ogrn(ogrn: str, token: str | None = None) -> dict[str, Any]:
    """Find organization by OGRN via Dadata."""
    return await _find_org_by_inn(ogrn, token)


# ─── Bank directory ──────────────────────────────────────────────────

async def _list_banks(token: str | None = None) -> list[dict[str, Any]]:
    """List all Russian banks via Dadata suggestions."""
    headers: dict[str, str] = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    if token:
        headers["Authorization"] = f"Token {token}"

    body = {"query": "", "count": 1000}
    try:
        result = await http_get(
            f"{DADATA_SUGGEST_URL}/bank",
            json=body,
            headers=headers,
        )
        return result.get("suggestions", [])
    except Exception:
        return []


# ─── Holidays ────────────────────────────────────────────────────────

def get_holidays(year: int) -> list[dict[str, str]]:
    """Generate Russian national holidays for a given year.

    Uses built-in reference data. Does not require API call.
    Note: This does not account for official government decrees
    that may shift weekend days for a specific year.
    """
    holidays = []
    for date_str, name in PRAZDNIKI_RF.items():
        full_date = f"{year}-{date_str}"
        holidays.append({
            "date": full_date,
            "name": name,
            "type": "national" if date_str in [
                "01-01", "01-07", "02-23", "03-08",
                "05-01", "05-09", "06-12", "11-04",
            ] else "weekend",
        })
    return holidays


# ─── Public API wrappers (no auth) ───────────────────────────────────

async def consult_address_by_postal(postal_code: str) -> AdresRF | dict[str, str]:
    """Look up address by Russian postal code.

    Args:
        postal_code: 6-digit postal code.

    Returns:
        Address data or error message.
    """
    result = await _postal_by_index(postal_code)
    if "error" in result:
        return {"error": result["error"]}

    return AdresRF(
        postal_code=result.get("postal_code", postal_code),
        region=result.get("region", ""),
        city=result.get("city", ""),
        street=result.get("street"),
        house=result.get("house"),
        full_address=result.get("full_address", ""),
    )


async def search_address(query: str) -> list[dict[str, str]]:
    """Search Russian addresses via FIAS/Dadata.

    Args:
        query: Free-form address query string.

    Returns:
        List of address suggestions.
    """
    result = await _suggest_address(query)
    suggestions = result.get("suggestions", [])

    results = []
    for s in suggestions:
        data = s.get("data", {})
        results.append({
            "value": s.get("value", ""),
            "postal_code": data.get("postal_code", ""),
            "region": data.get("region", ""),
            "city": data.get("city", ""),
            "street": data.get("street", ""),
            "house": data.get("house", ""),
            "fias_id": data.get("fias_id", ""),
        })
    return results


async def find_org_by_inn(inn: str) -> Organizatsiya | dict[str, str]:
    """Find organization by INN.

    Args:
        inn: INN (10 or 12 digits).

    Returns:
        Organization data or error message.
    """
    result = await _find_org_by_inn(inn)
    if "error" in result:
        return {"error": result["error"]}

    suggestions = result.get("suggestions", [])
    if not suggestions:
        return {"error": f"Организация с ИНН {inn} не найдена"}

    s = suggestions[0]
    data = s.get("data", {})
    return Organizatsiya(
        inn=data.get("inn", inn),
        kpp=data.get("kpp"),
        ogrn=data.get("ogrn"),
        name_full=data.get("name", {}).get("full"),
        name_short=data.get("name", {}).get("short"),
        status=data.get("state", {}).get("status"),
        address=data.get("address", {}).get("value"),
        registration_date=data.get("state", {}).get("registration_date"),
    )


async def list_banks_public() -> list[BankRF]:
    """List Russian banks from reference data.

    Returns:
        List of banks with BIK, name, city.
    """
    banks_raw = await _list_banks()
    banks = []
    for b in banks_raw:
        data = b.get("data", {})
        banks.append(BankRF(
            bik=data.get("bic", b.get("value", "")),
            name=data.get("name", b.get("value", "")),
            name_short=data.get("short_name"),
            city=data.get("city"),
            region=data.get("region"),
            swift=data.get("swift"),
        ))
    return banks


async def find_bank_by_bik(bik: str) -> BankRF | dict[str, str]:
    """Find bank by BIK.

    Args:
        bik: 9-digit BIK code.

    Returns:
        Bank data or error message.
    """
    # Note: proper implementation would call /suggest/bank endpoint
    return {"error": "Поиск банка по БИК требует отдельной интеграции"}
