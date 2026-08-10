"""Инструменты модуля МВД России.

Правила (ADR-001):
    - tools.py НЕ делает HTTP-запросы напрямую — делегирует client.py
    - Возвращает форматированные строки для LLM
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import tablitsa_v_markdown

from . import client
from .constants import FEDERALNYE_OKRUGA, VIDY_DTP, VIDY_PRESTUPLENIY


async def spisok_naborov_dannykh(kontekst: Context) -> str:
    """Получить список доступных наборов открытых данных МВД России."""
    await kontekst.info("Запрос списка наборов данных МВД...")
    nabory = client.poluchit_spisok_naborov_dannykh()
    stroki_tablitsy = [(nabor["kod"], nabor["nazvanie"]) for nabor in nabory]
    zagolovok = "**Наборы открытых данных МВД России**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Название"], stroki_tablitsy)


async def spisok_vidov_prestupleniy(kontekst: Context) -> str:
    """Получить справочник видов преступлений."""
    await kontekst.info("Запрос справочника видов преступлений...")
    stroki_tablitsy = [(vid["kod"], vid["nazvanie"]) for vid in VIDY_PRESTUPLENIY]
    zagolovok = "**Виды преступлений**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Вид преступления"], stroki_tablitsy)


async def spisok_vidov_dtp(kontekst: Context) -> str:
    """Получить справочник видов ДТП."""
    await kontekst.info("Запрос справочника видов ДТП...")
    stroki_tablitsy = [(vid["kod"], vid["nazvanie"]) for vid in VIDY_DTP]
    zagolovok = "**Виды ДТП**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Вид ДТП"], stroki_tablitsy)


async def spisok_federalnykh_okrugov(kontekst: Context) -> str:
    """Получить справочник федеральных округов."""
    await kontekst.info("Запрос справочника федеральных округов...")
    stroki_tablitsy = [(fo["kod"], fo["nazvanie"]) for fo in FEDERALNYE_OKRUGA]
    zagolovok = "**Федеральные округа**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Округ"], stroki_tablitsy)


async def statistika_prestupnosti(
    kontekst: Context,
    subiekt: str = "",
    god: int = 0,
) -> str:
    """Статистика преступности с данными МВД России.

    Аргументы:
        subiekt: Субъект РФ или федеральный округ (необязательно).
        god: Год (необязательно).

    Возвращает:
        Статистика преступности.
    """
    await kontekst.info("Запрос статистики преступности...")
    dannye = await client.statistika_prestupnosti(subiekt=subiekt, god=god)
    if not dannye:
        statika = client.poluchit_statistiku_prestupnosti_staticheskie()
        if statika:
            stroki = [
                "**Статистика преступности в РФ (2024, резервные данные)**\n",
                f"- Зарегистрировано преступлений: {statika['zaregistrirovano_prestupleniy']:,}",
                f"- Раскрыто: {statika['raskryto_prestupleniy']:,}",
                f"- Нераскрыто: {statika['neraskryto_prestupleniy']:,}",
                f"- Тяжкие и особо тяжкие: {statika['tyazhkie_osobo_tyazhkie']:,}",
                f"- С потерпевшими: {statika['s_poterpavshimi']:,}",
                f"- Экономические: {statika['ekonomicheskie']:,}",
                f"- Наркотические: {statika['narkoticheskie']:,}\n",
                "| ФО | Преступлений | Раскрыто |",
                "|----|-------------|----------|",
            ]
            for fo_kod, fo_dannye in statika["po_fo"].items():
                fo_nazvanie = _kod_v_nazvanie_fo(fo_kod)
                stroki.append(
                    f"| {fo_nazvanie} | {fo_dannye['prestupleniy']:,} | "
                    f"{fo_dannye['raskryto']:,} |"
                )
            stroki.append(
                "\nАктуальные данные доступны на: https://мвд.рф/деятельность/статистика"
            )
            return "\n".join(stroki)
        return (
            "Статистика преступности не найдена.\n\n"
            "Актуальные данные доступны на: https://мвд.рф/деятельность/статистика"
        )

    stroki_tablitsy = [
        (
            zapis.get("subiekt", "")[:30],
            str(zapis.get("god", "")),
            str(zapis.get("zaregistrirovano", "")),
            str(zapis.get("raskryto", "")),
            str(zapis.get("neraskryto", "")),
        )
        for zapis in dannye
    ]
    zagolovok = f"**Статистика преступности** — найдено: {len(dannye)}\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["Регион", "Год", "Зарег.", "Раскрыто", "Нераскр."],
        stroki_tablitsy,
    )


async def statistika_dtp(
    kontekst: Context,
    subiekt: str = "",
    god: int = 0,
    vid_dtp: str = "",
) -> str:
    """Статистика ДТП с данными МВД России.

    Аргументы:
        subiekt: Субъект РФ (необязательно).
        god: Год (необязательно).
        vid_dtp: Вид ДТП (необязательно).

    Возвращает:
        Статистика ДТП.
    """
    await kontekst.info("Запрос статистики ДТП...")
    dannye = await client.statistika_dtp(subiekt=subiekt, god=god, vid_dtp=vid_dtp)
    if not dannye:
        statika = client.poluchit_statistiku_dtp_staticheskie()
        if statika:
            stroki = [
                "**Статистика ДТП в РФ (2024, резервные данные)**\n",
                f"- Всего ДТП: {statika['vsego_dtp']:,}",
                f"- Погибших: {statika['pogibshikh']:,}",
                f"- Пострадавших: {statika['postradavshikh']:,}",
                f"- ДТП с участием детей: {statika['dtp_s_detmi']:,}",
                f"- По вине водителей: {statika['po_vinu_voditeley']:,}",
                f"- По вине пешеходов: {statika['po_vinu_peshekhodov']:,}",
                "\nАктуальные данные: https://гибдд.рф",
            ]
            return "\n".join(stroki)
        return "Статистика ДТП не найдена.\n\nАктуальные данные: https://гибдд.рф"

    stroki_tablitsy = [
        (
            zapis.get("subiekt", "")[:30],
            str(zapis.get("god", "")),
            zapis.get("vid_dtp", ""),
            str(zapis.get("vsego_dtp", "")),
            str(zapis.get("pogibshikh", "")),
            str(zapis.get("postradavshikh", "")),
        )
        for zapis in dannye
    ]
    zagolovok = f"**Статистика ДТП** — найдено: {len(dannye)}\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["Регион", "Год", "Вид ДТП", "Всего", "Погибших", "Пострад."],
        stroki_tablitsy,
    )


async def rozysk_del(
    kontekst: Context,
    kategoriya: str = "",
    subiekt: str = "",
) -> str:
    """Данные розыска МВД России.

    Аргументы:
        kategoriya: Категория розыскного дела (необязательно).
        subiekt: Регион (необязательно).

    Возвращает:
        Данные розыска.
    """
    await kontekst.info("Запрос данных розыска...")
    dannye = await client.rozysk_del(kategoriya=kategoriya, subiekt=subiekt)
    if not dannye:
        return (
            "Данные розыска не найдены.\n\n"
            "Поиск лиц: https://мвд.рф/wanted\n"
            "Поиск детей: https://мвд.рф/wanted/Поиск_детей"
        )

    stroki_tablitsy = [
        (
            zapis.get("kategoriya", ""),
            zapis.get("subiekt", "")[:30],
            str(zapis.get("kolichestvo", "")),
            zapis.get("data", ""),
        )
        for zapis in dannye
    ]
    zagolovok = f"**Данные розыска** — найдено: {len(dannye)}\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["Категория", "Регион", "Количество", "Дата"],
        stroki_tablitsy,
    )


async def narkotiki(
    kontekst: Context,
    subiekt: str = "",
    vid_narkotika: str = "",
) -> str:
    """Данные о наркотических преступлениях МВД России.

    Аргументы:
        subiekt: Регион (необязательно).
        vid_narkotika: Вид наркотика (необязательно).

    Возвращает:
        Данные о наркотических преступлениях.
    """
    await kontekst.info("Запрос данных о наркотических преступлениях...")
    dannye = await client.narkotiki(subiekt=subiekt, vid_narkotika=vid_narkotika)
    if not dannye:
        return (
            "Данные о наркотических преступлениях не найдены.\n\n"
            "Статистика МВД: https://мвд.рф/деятельность/статистика"
        )

    stroki_tablitsy = [
        (
            zapis.get("subiekt", "")[:30],
            zapis.get("vid_prestupleniya", ""),
            str(zapis.get("kolichestvo_prestupleniy", "")),
            str(zapis.get("izyato_gramm", "")),
            zapis.get("vid_narkotika", ""),
        )
        for zapis in dannye
    ]
    zagolovok = f"**Наркотические преступления** — найдено: {len(dannye)}\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["Регион", "Вид преступления", "Кол-во", "Изъято (г)", "Вид наркотика"],
        stroki_tablitsy,
    )


def _kod_v_nazvanie_fo(kod: str) -> str:
    """Преобразование кода ФО в название."""
    sootvetstviya = {
        "ЦФО": "Центральный",
        "СЗФО": "Северо-Западный",
        "ЮФО": "Южный",
        "ПФО": "Приволжский",
        "УФО": "Уральский",
        "СФО": "Сибирский",
        "ДФО": "Дальневосточный",
        "СКФО": "Северо-Кавказский",
    }
    return sootvetstviya.get(kod, kod)
