"""HTTP-клиент для API ЦБ РФ.

Эндпоинты:
- https://www.cbr-xml-daily.ru/daily_json.js  → все курсы валют
- https://www.cbr-xml-daily.ru/daily_json.js  → курсы на конкретную дату
"""

from __future__ import annotations

from typing import Any

from mcp_russia._shared.http_client import http_poluchit

from .constants import CBR_DAILY_JSON
from .schemas import ZnachenieValyuty


def _razobrat_valyutu(kod: str, data: dict[str, Any], date_str: str = "") -> ZnachenieValyuty:
    """Разбор данных о валютах из JSON API ЦБ РФ."""
    entry = data.get(kod, {})
    if not entry:
        return ZnachenieValyuty(
            kod=kod,
            nazvanie=kod,
            nominal=1,
            znachenie=0.0,
        )

    nominal = entry.get("Nominal", 1)
    value = entry.get("Value", 0.0)
    previous = entry.get("PreviousValue")

    znachenie_za_edinitsu = value / nominal if nominal else value

    return ZnachenieValyuty(
        kod=kod,
        nazvanie=entry.get("Name", kod),
        nominal=nominal,
        znachenie=znachenie_za_edinitsu,
        predydushchee_znachenie=previous / nominal if previous and nominal else previous,
        data=date_str,
    )


async def poluchit_vse_valyuty(data: str | None = None) -> dict[str, Any]:
    """Получение всех курсов валют ЦБ РФ.

    Аргументы:
        data: Дата в формате ГГГГ-ММ-ДД (необязательно, по умолчанию последние).

    Возвращает:
        Сырой JSON-ответ от API ЦБ РФ.
    """
    url = CBR_DAILY_JSON
    return await http_poluchit(url)


async def poluchit_valyutu(kod: str, data: str | None = None) -> ZnachenieValyuty | None:
    """Получение курса отдельной валюты.

    Аргументы:
        kod: Код валюты (напр. «USD», «EUR», «CNY»).
        data: Дата в формате ГГГГ-ММ-ДД (необязательно).

    Возвращает:
        Данные о валюте или None если не найдена.
    """
    result = await poluchit_vse_valyuty(data)
    valute_data = result.get("Valute", {})
    date_str = result.get("Date", "")

    if kod in valute_data:
        return _razobrat_valyutu(kod, valute_data, date_str)
    return None


async def poluchit_valyuty_spisok(kody: list[str]) -> list[ZnachenieValyuty]:
    """Получение нескольких курсов валют параллельно.

    Аргументы:
        kody: Список кодов валют.

    Возвращает:
        Список данных о валютах.
    """
    result = await poluchit_vse_valyuty()
    valute_data = result.get("Valute", {})
    date_str = result.get("Date", "")

    return [_razobrat_valyutu(c, valute_data, date_str) for c in kody if c in valute_data]


async def poluchit_osnovnye_valyuty() -> list[ZnachenieValyuty]:
    """Получение курсов основных валют (USD, EUR, CNY, GBP, JPY, CHF).

    Возвращает:
        Список данных об основных валютах.
    """
    osnovnyye = ["USD", "EUR", "CNY", "GBP", "JPY", "CHF"]
    return await poluchit_valyuty_spisok(osnovnyye)


async def poluchit_dinamiku_kursa(kod: str) -> dict[str, Any]:
    """Получение динамики исторических данных для валюты.

    Использует API динамики ЦБ РФ для исторических данных.
    API: https://www.cbr-xml-daily.ru/dynamics_json.js

    Аргументы:
        kod: Код валюты.

    Возвращает:
        Исторические данные о валюте.
    """
    url = f"https://www.cbr-xml-daily.ru/dynamics/{kod}/dynamic_json.js"
    try:
        return await http_poluchit(url)
    except Exception:
        return {"oshibka": f"Нет данных для валюты {kod}"}
