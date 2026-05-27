"""Reference resources for the CBRF (Central Bank of Russia) feature."""

from __future__ import annotations

from .constants import OSNOVNYE_VALYUTY


def dostupnye_valyuty() -> str:
    """Список валют, доступных через API ЦБ РФ."""
    return (
        "Центральный банк Российской Федерации устанавливает официальные курсы "
        "более 40 иностранных валют по отношению к рублю. "
        "Данные обновляются ежедневно в рабочие дни."
    )


def spravochnik_kursov() -> str:
    """Справочная информация об официальных курсах ЦБ РФ."""
    return (
        "**Источники данных ЦБ РФ**\n\n"
        "- Основные курсы: https://www.cbr-xml-daily.ru/daily_json.js\n"
        "- Исторические данные: https://www.cbr-xml-daily.ru/dynamics/{CODE}/dynamic_json.js\n"
        "- Официальный сайт: https://www.cbr.ru\n\n"
        "Курсы устанавливаются на каждый рабочий день. "
        "Для выходных и праздников используется последний рабочий курс."
    )


def osnovnye_valyuty() -> str:
    """Основные валюты для быстрого запроса."""
    return (
        f"Основные коды валют: {', '.join(OSNOVNYE_VALYUTY[:10])}...\n"
        f"Всего доступно: {len(OSNOVNYE_VALYUTY)} валют.\n"
        "Используйте spisok_valyut() для полного списка."
    )
