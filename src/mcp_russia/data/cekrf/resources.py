"""Справочные данные модуля ЦИК РФ."""

import json

from .constants import (
    CIK_BAZA_API,
    IZVESTNYE_VYBORY,
    PARTII_RF,
    SUBYEKTY_RF,
    TIPOVY_VYBORY,
    VYBORY_BAZA_API,
)


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


def izvestnye_vybory_resource() -> str:
    """Справочник известных выборов (JSON)."""
    return json.dumps(
        {"izvestnye_vybory": IZVESTNYE_VYBORY},
        ensure_ascii=False,
        indent=2,
    )


def info_api() -> str:
    """Информация об API ЦИК РФ."""
    return json.dumps(
        {
            "nazvanie": "ЦИК РФ / ГАС «Выборы»",
            "bazovyy_url": CIK_BAZA_API,
            "vybory_url": VYBORY_BAZA_API,
            "trebuet_avtentifikatsii": False,
            "format": "HTML / REST (частично документирован)",
            "pokrytie": "Федеральные и региональные выборы РФ",
            "izvestnye_vybory_kolichestvo": len(IZVESTNYE_VYBORY),
            "primechanie": (
                "Данные извлекаются парсингом ГАС «Выборы» "
                "(vybory.izbirkom.ru) и публичных данных cikrf.ru. "
                "Для известных федеральных выборов используются "
                "предопределённые идентификаторы (tvd/vrn)."
            ),
        },
        ensure_ascii=False,
        indent=2,
    )
