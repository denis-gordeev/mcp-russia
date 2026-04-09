"""HTTP client for the CBRF (Central Bank of Russia) API.

Endpoints:
    - https://www.cbr-xml-daily.ru/daily_json.js  → все курсы валют
    - https://www.cbr-xml-daily.ru/daily_json.js  → курсы на конкретную дату
"""

from __future__ import annotations

from typing import Any

from mcp_brasil._shared.http_client import http_get

from .constants import CBR_DAILY_JSON
from .schemas import ValorMoeda


def _parse_moeda(code: str, data: dict[str, Any], date_str: str = "") -> ValorMoeda:
    """Parse currency data from the CBR JSON API."""
    entry = data.get(code, {})
    if not entry:
        return ValorMoeda(
            codigo=code,
            nome=code,
            nominal=1,
            valor=0.0,
        )

    nominal = entry.get("Nominal", 1)
    value = entry.get("Value", 0.0)
    previous = entry.get("PreviousValue")

    # Convert to per-unit value if nominal != 1
    valor_unitario = value / nominal if nominal else value

    return ValorMoeda(
        codigo=code,
        nome=entry.get("Name", code),
        nominal=nominal,
        valor=valor_unitario,
        valor_anterior=previous / nominal if previous and nominal else previous,
        data=date_str,
    )


async def buscar_todas_moedas(data: str | None = None) -> dict[str, Any]:
    """Fetch all currency exchange rates from CBR.

    Args:
        data: Date in YYYY-MM-DD format (optional, defaults to latest).

    Returns:
        Raw JSON response from the CBR API.
    """
    url = CBR_DAILY_JSON
    return await http_get(url)


async def buscar_moeda(code: str, data: str | None = None) -> ValorMoeda | None:
    """Fetch a single currency exchange rate.

    Args:
        code: Currency code (e.g. 'USD', 'EUR', 'CNY').
        data: Date in YYYY-MM-DD format (optional).

    Returns:
        Currency data or None if not found.
    """
    result = await buscar_todas_moedas(data)
    valute_data = result.get("Valute", {})
    date_str = result.get("Date", "")

    if code in valute_data:
        return _parse_moeda(code, valute_data, date_str)
    return None


async def buscar_moedas_varios(codes: list[str]) -> list[ValorMoeda]:
    """Fetch multiple currency exchange rates in parallel.

    Args:
        codes: List of currency codes.

    Returns:
        List of currency data.
    """
    result = await buscar_todas_moedas()
    valute_data = result.get("Valute", {})
    date_str = result.get("Date", "")

    return [_parse_moeda(c, valute_data, date_str) for c in codes if c in valute_data]


async def buscar_moedas_principais() -> list[ValorMoeda]:
    """Fetch main currency exchange rates (USD, EUR, CNY, GBP, JPY, CHF).

    Returns:
        List of main currency data.
    """
    principais = ["USD", "EUR", "CNY", "GBP", "JPY", "CHF"]
    return await buscar_moedas_varios(principais)


async def buscar_curso_dinamico(code: str) -> dict[str, Any]:
    """Fetch dynamic historical data for a currency.

    This uses the CBR's dynamic API for historical data.
    API: https://www.cbr-xml-daily.ru/dynamics_json.js

    Args:
        code: Currency code.

    Returns:
        Historical currency data.
    """
    url = f"https://www.cbr-xml-daily.ru/dynamics/{code}/dynamic_json.js"
    try:
        return await http_get(url)
    except Exception:
        return {"error": f"Нет данных для валюты {code}"}
