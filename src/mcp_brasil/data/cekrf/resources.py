"""Справочные данные модуля ЦИК РФ."""

import json

from .constants import PARTII_RF, SUBYEKTY_RF, TIPOVY_VYBORY


def tipy_vyborov_resource() -> str:
    """Справочник типов выборов (JSON)."""
    return json.dumps(
        {"tipy_vyborov": list(TIPOVY_VYBORY.values())},
        ensure_ascii=False,
        indent=2,
    )


def subyekty_rf_resource() -> str:
    """Справочник субъектов РФ (JSON)."""
    return json.dumps(
        {"subyekty_rf": SUBYEKTY_RF},
        ensure_ascii=False,
        indent=2,
    )


def partii_rf_resource() -> str:
    """Справочник партий РФ (JSON)."""
    return json.dumps(
        {"partii_rf": PARTII_RF},
        ensure_ascii=False,
        indent=2,
    )


def info_api() -> str:
    """Информация об API ЦИК РФ."""
    return json.dumps(
        {
            "name": "ЦИК РФ / ГАС «Выборы»",
            "base_url": "https://cikrf.ru",
            "vybory_url": "https://vybory.izbirkom.ru",
            "auth_required": False,
            "format": "HTML / REST (частично документирован)",
            "coverage": "Федеральные и региональные выборы РФ",
            "note": (
                "Для программного доступа рекомендуется "
                "парсинг ГАС «Выборы» или использование "
                "публичных данных cikrf.ru"
            ),
        },
        ensure_ascii=False,
        indent=2,
    )
