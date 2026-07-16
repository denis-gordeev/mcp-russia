"""Инструменты модуля Федерального казначейства.

Правила (ADR-001):
    - tools.py НЕ делает HTTP-запросы напрямую — делегирует client.py
    - Возвращает форматированные строки для LLM
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import formatirovat_chislo_ru, tablitsa_v_markdown

from . import client


async def spisok_vidov_byudzhetov(kontekst: Context) -> str:
    """Получить список видов бюджетов бюджетной системы РФ."""
    await kontekst.info("Запрос списка видов бюджетов...")
    vidy = client.poluchit_spisok_vidov_byudzhetov()
    stroki_tablitsy = [(vid["kod"], vid["nazvanie"]) for vid in vidy]
    zagolovok = "**Виды бюджетов бюджетной системы РФ**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Вид бюджета"], stroki_tablitsy)


async def spisok_kategoriy_raskhodov(kontekst: Context) -> str:
    """Получить список категорий расходов бюджета."""
    await kontekst.info("Запрос списка категорий расходов...")
    kategorii = client.poluchit_spisok_kategoriy_raskhodov()
    stroki_tablitsy = [(kategoriya["kod"], kategoriya["nazvanie"]) for kategoriya in kategorii]
    zagolovok = "**Категории расходов бюджета**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Категория"], stroki_tablitsy)


async def ispolnenie_byudzheta(
    kontekst: Context,
    god: int = 0,
    tip: str = "",
) -> str:
    """Получить данные об исполнении бюджета.

    Аргументы:
        god: Год (необязательно).
        tip: Тип бюджета (необязательно).

    Возвращает:
        Данные об исполнении бюджета.
    """
    await kontekst.info("Запрос данных об исполнении бюджета...")
    dannye = await client.poluchit_ispolnenie_byudzheta(god=god, tip=tip)
    if not dannye:
        tip_tekst = f" ({tip})" if tip else ""
        god_tekst = f" за {god} год" if god else ""
        return (
            f"Данные об исполнении бюджета{tip_tekst}{god_tekst} недоступны.\n\n"
            f"Данные доступны на:\n"
            f"- Федеральное казначейство: roskazna.gov.ru\n"
            f"- Портал бюджетных данных: budget.gov.ru"
        )
    stroki = [f"**Исполнение бюджета за {dannye.get('period', '')}**"]
    if dannye.get("tip"):
        stroki.append(f"- Тип бюджета: {dannye['tip']}")
    if dannye.get("dohody"):
        stroki.append(f"- Доходы: {formatirovat_chislo_ru(dannye['dohody'], 2)} млрд руб.")
    if dannye.get("raskhody"):
        stroki.append(f"- Расходы: {formatirovat_chislo_ru(dannye['raskhody'], 2)} млрд руб.")
    if dannye.get("defitsit") is not None:
        stroki.append(f"- Дефицит: {formatirovat_chislo_ru(dannye['defitsit'], 2)} млрд руб.")
    if dannye.get("sostoyanie"):
        stroki.append(f"- Статус: {dannye['sostoyanie']}")
    stroki.append(f"- Источник: {dannye.get('istochnik', 'budget.gov.ru')}")
    return "\n".join(stroki)


async def poisk_uchastnikov_bp(
    kontekst: Context,
    inn: str = "",
    nazvanie: str = "",
) -> str:
    """Поиск участников бюджетного процесса.

    Аргументы:
        inn: ИНН организации (необязательно).
        nazvanie: Название организации (необязательно).

    Возвращает:
        Список участников бюджетного процесса.
    """
    await kontekst.info("Поиск участников бюджетного процесса...")
    uchastniki = await client.poisk_uchastnikov_bp(inn=inn, nazvanie=nazvanie)
    if not uchastniki:
        filtry = []
        if inn:
            filtry.append(f"ИНН: {inn}")
        if nazvanie:
            filtry.append(f"название: {nazvanie}")
        tekst_filtra = f" ({', '.join(filtry)})" if filtry else ""
        return (
            f"Участники бюджетного процесса{tekst_filtra} не найдены.\n\n"
            f"Реестр участников доступен на: roskazna.gov.ru"
        )
    stroki_tablitsy = [
        (
            uchastnik.get("inn", ""),
            uchastnik.get("nazvanie", "")[:50],
            uchastnik.get("tip_uchastnika", ""),
            uchastnik.get("byudzhet", ""),
        )
        for uchastnik in uchastniki
    ]
    zagolovok = f"**Участники бюджетного процесса** — найдено: {len(uchastniki)}\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["ИНН", "Название", "Тип", "Бюджет"],
        stroki_tablitsy,
    )


async def poisk_uchrezhdeniy(
    kontekst: Context,
    inn: str = "",
    nazvanie: str = "",
    tip: str = "",
) -> str:
    """Поиск учреждений в сводном реестре.

    Аргументы:
        inn: ИНН учреждения (необязательно).
        nazvanie: Название учреждения (необязательно).
        tip: Тип учреждения (необязательно).

    Возвращает:
        Список учреждений.
    """
    await kontekst.info("Поиск учреждений...")
    uchrezhdeniya = await client.poisk_uchrezhdeniy(inn=inn, nazvanie=nazvanie, tip=tip)
    if not uchrezhdeniya:
        filtry = []
        if inn:
            filtry.append(f"ИНН: {inn}")
        if nazvanie:
            filtry.append(f"название: {nazvanie}")
        if tip:
            filtry.append(f"тип: {tip}")
        tekst_filtra = f" ({', '.join(filtry)})" if filtry else ""
        return (
            f"Учреждения{tekst_filtra} не найдены.\n\n"
            f"Сводный реестр учреждений доступен на: roskazna.gov.ru"
        )
    stroki_tablitsy = [
        (
            uchrezhdenie.get("inn", ""),
            uchrezhdenie.get("nazvanie", "")[:50],
            uchrezhdenie.get("tip", ""),
            uchrezhdenie.get("osnovnoj_vid_deyatelnosti", "")[:40],
        )
        for uchrezhdenie in uchrezhdeniya
    ]
    zagolovok = f"**Учреждения** — найдено: {len(uchrezhdeniya)}\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["ИНН", "Название", "Тип", "Основной вид деятельности"],
        stroki_tablitsy,
    )


async def mezhbyudzhetnye_transferty(
    kontekst: Context,
    god: int = 0,
    subiekt: str = "",
) -> str:
    """Получить данные о межбюджетных трансфертах.

    Аргументы:
        god: Год (необязательно).
        subiekt: Код региона (необязательно).

    Возвращает:
        Данные о межбюджетных трансфертах.
    """
    await kontekst.info("Запрос данных о межбюджетных трансфертах...")
    transferty = await client.poluchit_mezhbyudzhetnye(god=god, subiekt=subiekt)
    if not transferty:
        god_tekst = f" за {god} год" if god else ""
        tekst_regiona = f", регион: {subiekt}" if subiekt else ""
        return (
            f"Межбюджетные трансферты{god_tekst}{tekst_regiona} не найдены.\n\n"
            f"Данные доступны на: budget.gov.ru"
        )
    stroki_tablitsy = [
        (
            transfer.get("vid", ""),
            transfer.get("otpravitel", "")[:30],
            transfer.get("poluchatel", "")[:30],
            str(transfer.get("summa", "")),
            transfer.get("god", ""),
        )
        for transfer in transferty
    ]
    zagolovok = f"**Межбюджетные трансферты** — найдено: {len(transferty)}\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["Вид", "Отправитель", "Получатель", "Сумма (руб.)", "Год"],
        stroki_tablitsy,
    )
