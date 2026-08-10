"""Справочные ресурсы модуля Росстата."""

from .constants import (
    KLYUCHEVYE_INDIKATORY,
    OTRASLEVAYA_STRUKTURA_VRP,
    SUBIEKTY_RF,
)


def istochniki_dannyh() -> str:
    """Источники данных Росстата."""
    return (
        "**Источники статистических данных РФ**\n\n"
        "- ЕМИСС (Единая межведомственная статистическая система): https://fedstat.ru\n"
        "- Росстат (официальный сайт): https://rosstat.gov.ru\n"
        "- Открытые данные: https://data.gov.ru\n\n"
        "ЕМИСС предоставляет API для программного доступа к показателям. "
        "Росстат публикует официальные статистические сборники и бюллетени."
    )


def metodologiya() -> str:
    """Методологические пояснения Росстата."""
    return (
        "**Методология расчёта показателей**\n\n"
        "Росстат использует методологию, согласованную с международными стандартами "
        "(СНС ООН 2008, МСЭС). Основные особенности:\n"
        "- ВРП рассчитывается в текущих и сопоставимых ценах по ОКВЭД 2\n"
        "- ИПЦ рассчитывается по определённой корзине товаров и услуг\n"
        "- Демографические данные обновляются ежемесячно\n"
        "- Коды показателей ЕМИСС обновлены после перехода на ОКВЭД 2 (2017 г.)\n"
        "- Старые коды (24xxx, 27xxx, 31xxx) заморожены — данные по 2016 г."
    )


def pokazateli() -> str:
    """Справочник показателей Росстата."""
    stroki = []
    for pokazatel in KLYUCHEVYE_INDIKATORY:
        stroki.append(f"- **{pokazatel['kod']}** — {pokazatel['nazvanie']}")
    return (
        "**Справочник показателей Росстата**\n\n"
        + "\n".join(stroki)
        + "\n\nИспользуйте мнемонические коды в инструментах indikator_dannye(), "
        "sravnenie_regionov(), sravnenie_okrugov(), dinamika_regiona()."
    )


def okved() -> str:
    """Справочник разделов ОКВЭД 2."""
    stroki = []
    vse_kody = set()
    for otrasl in OTRASLEVAYA_STRUKTURA_VRP:
        if otrasl["kod"] not in vse_kody:
            vse_kody.add(otrasl["kod"])
            stroki.append(f"- **{otrasl['kod']}** — {otrasl['nazvanie']}")
    return (
        "**Разделы ОКВЭД 2 (для структуры ВРП и инвестиций)**\n\n"
        + "\n".join(stroki)
        + "\n\nИспользуйте коды ОКВЭД в инструментах "
        "otraslevaya_struktura_vrp() и investitsii_po_vidam()."
    )


def subiekty_rf() -> str:
    """Справочник субъектов РФ."""
    stroki = []
    for subiekt in SUBIEKTY_RF:
        okrug = subiekt.get("okrug", "")
        stroki.append(f"- **{subiekt['kod']}** — {subiekt['nazvanie']} ({okrug})")
    return (
        f"**Субъекты Российской Федерации** — {len(SUBIEKTY_RF)} субъектов\n\n"
        + "\n".join(stroki)
        + "\n\nИспользуйте коды в инструментах "
        "informatsiya_o_regionye(), dinamika_regiona(), poisk_regiona()."
    )
