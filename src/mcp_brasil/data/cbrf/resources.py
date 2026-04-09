"""Reference resources for the CBRF (Central Bank of Russia) feature."""

from __future__ import annotations

from .constants import MOEDAS_PRINCIPAIS


def moedas_disponiveis() -> str:
    """Список валют, доступных через API ЦБ РФ."""
    return (
        "Центральный банк Российской Федерации устанавливает официальные курсы "
        "более 40 иностранных валют по отношению к рублю. "
        "Данные обновляются ежедневно в рабочие дни."
    )


def referencia_cursos() -> str:
    """Справочная информация об официальных курсах ЦБ РФ."""
    return (
        "**Источники данных ЦБ РФ**\n\n"
        "- Основные курсы: https://www.cbr-xml-daily.ru/daily_json.js\n"
        "- Исторические данные: https://www.cbr-xml-daily.ru/dynamics/{CODE}/dynamic_json.js\n"
        "- Официальный сайт: https://www.cbr.ru\n\n"
        "Курсы устанавливаются на каждый рабочий день. "
        "Для выходных и праздников используется последний рабочий курс."
    )


def moedas_principais() -> str:
    """Основные валюты для быстрого запроса."""
    return (
        f"Основные коды валют: {', '.join(MOEDAS_PRINCIPAIS[:10])}...\n"
        f"Всего доступно: {len(MOEDAS_PRINCIPAIS)} валют.\n"
        "Используйте listar_moedas() для полного списка."
    )
