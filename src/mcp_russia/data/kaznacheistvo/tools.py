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
    razdel: str = "",
    podrazdel: str = "",
) -> str:
    """Получить данные об исполнении бюджета.

    Аргументы:
        god: Год (необязательно).
        tip: Тип бюджета (необязательно).
        razdel: Код раздела бюджетной классификации (необязательно).
        podrazdel: Код подраздела бюджетной классификации (необязательно).

    Возвращает:
        Данные об исполнении бюджета.
    """
    await kontekst.info("Запрос данных об исполнении бюджета...")
    dannye = await client.poluchit_ispolnenie_byudzheta(
        god=god, tip=tip, razdel=razdel, podrazdel=podrazdel
    )
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
            uchrezhdenie.get("osnovnoy_vid_deyatelnosti", "")[:40],
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


async def spisok_razdelov_byudzheta(kontekst: Context) -> str:
    """Получить справочник разделов бюджетной классификации РФ.

    Возвращает:
        Справочник разделов БК с кодами.
    """
    await kontekst.info("Запрос справочника разделов БК...")
    razdely = client.poluchit_spisok_razdelov_byudzheta()
    stroki_tablitsy = [(razdel["kod"], razdel["nazvanie"]) for razdel in razdely]
    zagolovok = "**Разделы бюджетной классификации РФ**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Раздел"], stroki_tablitsy)


async def spisok_podrazdelov_byudzheta(kontekst: Context, razdel: str = "") -> str:
    """Получить справочник подразделов бюджетной классификации.

    Аргументы:
        razdel: Код раздела БК для фильтрации (необязательно).

    Возвращает:
        Справочник подразделов БК.
    """
    await kontekst.info("Запрос справочника подразделов БК...")
    podrazdely = client.poluchit_spisok_podrazdelov_byudzheta(razdel=razdel)
    stroki_tablitsy = [
        (podrazdel["kod"], podrazdel["razdel"], podrazdel["nazvanie"]) for podrazdel in podrazdely
    ]
    zagolovok = "**Подразделы бюджетной классификации РФ**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Раздел", "Подраздел"], stroki_tablitsy)


async def byudzhetnaya_smeta(nomer: str, kontekst: Context) -> str:
    """Получить бюджетную смету по номеру.

    Аргументы:
        nomer: Номер бюджетной сметы.

    Возвращает:
        Данные бюджетной сметы.
    """
    await kontekst.info(f"Запрос бюджетной сметы {nomer}...")
    dannye = await client.poluchit_byudzhetnuyu_smetu(nomer)
    if not dannye:
        return f"Бюджетная смета '{nomer}' не найдена.\n\nРеестр смет доступен на: roskazna.gov.ru"
    stroki = [
        f"**Бюджетная смета № {dannye.get('nomer', nomer)}**",
        f"- Участник: {dannye.get('uchastnik', '')}",
        f"- Период: {dannye.get('period', '')}",
    ]
    if dannye.get("limity_byudzhetnykh_obyazatelstv"):
        stroki.append(
            f"- Лимиты бюджетных обязательств: "
            f"{formatirovat_chislo_ru(dannye['limity_byudzhetnykh_obyazatelstv'], 2)} руб."
        )
    if dannye.get("obshchaya_summa"):
        stroki.append(
            f"- Общая сумма: {formatirovat_chislo_ru(dannye['obshchaya_summa'], 2)} руб."
        )
    stroki.append(f"- Источник: {dannye.get('istochnik', 'roskazna.gov.ru')}")
    return "\n".join(stroki)
