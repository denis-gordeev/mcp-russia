"""Инструменты модуля Ростехнадзора.

Правила (ADR-001):
    - tools.py НЕ делает HTTP-запросы напрямую — делегирует client.py
    - Возвращает форматированные строки для LLM
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import tablitsa_v_markdown

from . import client
from .constants import KLASSY_OPASNOSTI, VIDY_INTSIDENTOV, VIDY_LITSENZIY, VIDY_NADZORA


async def spisok_vidov_nadzora(kontekst: Context) -> str:
    """Получить справочник видов надзора Ростехнадзора."""
    await kontekst.info("Запрос справочника видов надзора...")
    stroki_tablitsy = [(vid["kod"], vid["nazvanie"]) for vid in VIDY_NADZORA]
    zagolovok = "**Виды надзора Ростехнадзора**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Вид надзора"], stroki_tablitsy)


async def spisok_klassov_opasnosti(kontekst: Context) -> str:
    """Получить справочник классов опасности ОПО."""
    await kontekst.info("Запрос справочника классов опасности...")
    stroki_tablitsy = [(klass["kod"], klass["nazvanie"]) for klass in KLASSY_OPASNOSTI]
    zagolovok = "**Классы опасности ОПО**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Класс опасности"], stroki_tablitsy)


async def spisok_vidov_litsenziy(kontekst: Context) -> str:
    """Получить справочник видов лицензий Ростехнадзора."""
    await kontekst.info("Запрос справочника видов лицензий...")
    stroki_tablitsy = [(vid["kod"], vid["nazvanie"]) for vid in VIDY_LITSENZIY]
    zagolovok = "**Виды лицензий Ростехнадзора**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Вид лицензии"], stroki_tablitsy)


async def spisok_vidov_intsidentov(kontekst: Context) -> str:
    """Получить справочник видов инцидентов."""
    await kontekst.info("Запрос справочника видов инцидентов...")
    stroki_tablitsy = [(vid["kod"], vid["nazvanie"]) for vid in VIDY_INTSIDENTOV]
    zagolovok = "**Виды инцидентов на ОПО**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Вид инцидента"], stroki_tablitsy)


async def poisk_intsidentov(
    kontekst: Context,
    vid: str = "",
    subiekt: str = "",
) -> str:
    """Поиск инцидентов и аварий на опасных производственных объектах.

    Аргументы:
        vid: Вид инцидента (необязательно).
        subiekt: Регион (необязательно).

    Возвращает:
        Список инцидентов.
    """
    await kontekst.info("Поиск инцидентов на ОПО...")
    dannye = await client.poisk_intsidentov(vid=vid, subiekt=subiekt)
    if not dannye:
        statika = client.poluchit_statistiku_prombez_staticheskie()
        if statika:
            stroki = [
                "**Статистика промышленной безопасности (2024, резервные данные)**\n",
                f"- Всего аварий: {statika['vsego_avariy']}",
                f"- Всего инцидентов: {statika['vsego_intsidentov']}",
                f"- Погибших при авариях: {statika['pogibshikh_pri_avariyakh']}",
                f"- Пострадавших при авариях: {statika['postradavshikh_pri_avariyakh']}",
                f"- Зарегистрировано ОПО: {statika['zaregistrirovano_opo']:,}",
                f"- Выдано лицензий: {statika['vydano_litsenziy']:,}",
                f"- Проведено проверок: {statika['provedeno_proverok']:,}\n",
                "| Вид надзора | Аварий | Инцидентов | Проверок |",
                "|------------|--------|------------|----------|",
            ]
            for vid_kod, vid_dannye in statika["po_vidu_nadzora"].items():
                vid_nazvanie = _kod_v_nazvanie_vida(vid_kod)
                stroki.append(
                    f"| {vid_nazvanie} | {vid_dannye['avariy']} | "
                    f"{vid_dannye['intsidentov']} | {vid_dannye['proverok']:,} |"
                )
            stroki.append("\nАктуальные данные: https://rostechnadzor.gov.ru")
            return "\n".join(stroki)
        return "Инциденты не найдены.\n\nАктуальные данные: https://rostechnadzor.gov.ru"

    stroki_tablitsy = [
        (
            intsident.get("nomer", ""),
            intsident.get("vid", ""),
            intsident.get("data", ""),
            intsident.get("subiekt", "")[:30],
            str(intsident.get("pogibshikh", "")),
            str(intsident.get("postradavshikh", "")),
        )
        for intsident in dannye
    ]
    zagolovok = f"**Инциденты на ОПО** — найдено: {len(dannye)}\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["№", "Вид", "Дата", "Регион", "Погибших", "Пострад."],
        stroki_tablitsy,
    )


async def poisk_litsenziy(
    kontekst: Context,
    vid: str = "",
    organizatsiya: str = "",
) -> str:
    """Поиск лицензий Ростехнадзора.

    Аргументы:
        vid: Вид лицензии (необязательно).
        organizatsiya: Название организации (необязательно).

    Возвращает:
        Список лицензий.
    """
    await kontekst.info("Поиск лицензий Ростехнадзора...")
    dannye = await client.poisk_litsenziy(vid=vid, organizatsiya=organizatsiya)
    if not dannye:
        return (
            "Лицензии не найдены.\n\n"
            "Реестр лицензий: https://rostechnadzor.gov.ru/activities/licensing/"
        )

    stroki_tablitsy = [
        (
            litsenziya.get("nomer", ""),
            litsenziya.get("vid", "")[:40],
            litsenziya.get("organizatsiya", "")[:30],
            litsenziya.get("sostoyanie", ""),
        )
        for litsenziya in dannye
    ]
    zagolovok = f"**Лицензии Ростехнадзора** — найдено: {len(dannye)}\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["Номер", "Вид", "Организация", "Статус"],
        stroki_tablitsy,
    )


async def reestr_opo(
    kontekst: Context,
    subiekt: str = "",
    klass_opasnosti: str = "",
) -> str:
    """Реестр опасных производственных объектов.

    Аргументы:
        subiekt: Регион (необязательно).
        klass_opasnosti: Класс опасности (необязательно).

    Возвращает:
        Список ОПО.
    """
    await kontekst.info("Запрос реестра ОПО...")
    dannye = await client.reestr_opo(
        subiekt=subiekt,
        klass_opasnosti=klass_opasnosti,
    )
    if not dannye:
        return (
            "Опасные производственные объекты не найдены.\n\n"
            "Реестр ОПО: https://rostechnadzor.gov.ru/activities/registers/"
        )

    stroki_tablitsy = [
        (
            opo.get("registratsionnyy_nomer", ""),
            opo.get("nazvanie", "")[:30],
            opo.get("klass_opasnosti", ""),
            opo.get("subiekt", "")[:30],
        )
        for opo in dannye
    ]
    zagolovok = f"**Реестр ОПО** — найдено: {len(dannye)}\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["Рег. номер", "Название", "Класс", "Регион"],
        stroki_tablitsy,
    )


def _kod_v_nazvanie_vida(kod: str) -> str:
    """Преобразование кода вида надзора в название."""
    sootvetstviya = {
        "promyshlennyy": "Промышленная безопасность",
        "atomnyy": "Атомный надзор",
        "gornyy": "Горный надзор",
        "ekologicheskiy": "Экологический надзор",
    }
    return sootvetstviya.get(kod, kod)
