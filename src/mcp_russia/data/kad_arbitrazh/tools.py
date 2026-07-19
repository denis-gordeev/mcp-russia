"""Инструменты модуля Картотеки арбитражных дел.

Инструменты для поиска судебных дел, судебных актов, судей и сторон.

Правила (ADR-001):
    - tools.py НЕ делает HTTP-запросы напрямую — делегирует client.py
    - Возвращает форматированные строки для LLM
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import formatirovat_rubli, tablitsa_v_markdown

from . import client


async def poisk_del(
    nomer: str = "",
    istorcz: str = "",
    otvetchik: str = "",
    inn: str = "",
    kategoriya: str = "",
    kontekst: Context | None = None,
) -> str:
    """Поиск дел в Картотеке арбитражных дел.

    Аргументы:
        nomer: Номер дела (например, 'А40-12345/2024').
        istorcz: Название истца.
        otvetchik: Название ответчика.
        inn: ИНН участника.
        kategoriya: Категория дела.

    Возвращает:
        Результаты поиска дел.
    """
    if kontekst:
        await kontekst.info(f"Поиск дел: {nomer or istorcz or otvetchik or 'все'}...")

    dela = await client.poisk_del(
        nomer=nomer,
        istorcz=istorcz,
        otvetchik=otvetchik,
        inn=inn,
        kategoriya=kategoriya,
    )

    zagolovok = "**Картотека арбитражных дел**\n\n"

    filtry = []
    if nomer:
        filtry.append(f"Номер: {nomer}")
    if istorcz:
        filtry.append(f"Истец: {istorcz}")
    if otvetchik:
        filtry.append(f"Ответчик: {otvetchik}")
    if inn:
        filtry.append(f"ИНН: {inn}")
    if kategoriya:
        filtry.append(f"Категория: {kategoriya}")

    if filtry:
        zagolovok += "Фильтры: " + ", ".join(filtry) + "\n\n"

    if not dela:
        zagolovok += (
            "Дела не найдены.\n\n"
            "Источник: Картотека арбитражных дел (kad.arbitr.ru)\n"
            "Попробуйте уточнить параметры поиска."
        )
        return zagolovok

    stroki_tablitsy = []
    for delo in dela[:20]:
        summa = formatirovat_rubli(delo.summa_iska) if delo.summa_iska > 0 else "—"
        stroki_tablitsy.append(
            (
                delo.nomer,
                delo.kategoriya or "—",
                delo.sostoyanie or "—",
                delo.nazvanie_suda or "—",
                summa,
            )
        )

    zagolovok += f"Найдено дел: {len(dela)}\n\n"
    zagolovok += tablitsa_v_markdown(
        ["Номер дела", "Категория", "Статус", "Суд", "Сумма иска"],
        stroki_tablitsy,
    )
    zagolovok += "\n\nИсточник: Картотека арбитражных дел (kad.arbitr.ru)"
    return zagolovok


async def info_dela(
    nomer_dela: str,
    kontekst: Context,
) -> str:
    """Получить подробную информацию о судебном деле.

    Аргументы:
        nomer_dela: Номер дела (например, 'А40-12345/2024').

    Возвращает:
        Подробная информация о деле.
    """
    await kontekst.info(f"Запрос информации о деле {nomer_dela}...")
    delo = await client.info_dela(nomer_dela)

    if not delo:
        return (
            f"Дело с номером {nomer_dela} не найдено в КАД.\n\nИспользуйте poisk_del() для поиска."
        )

    stroki = [
        f"**Дело {delo.nomer}**",
        f"- Категория: {delo.kategoriya}",
        f"- Статус: {delo.sostoyanie}",
        f"- Судья: {delo.sudya}",
        f"- Суд: {delo.nazvanie_suda}",
        f"- Дата возбуждения: {delo.data_vozbuzhdeniya}",
        f"- Последний акт: {delo.data_poslednego_akta}",
        f"- Истцы: {', '.join(delo.istorcy)}",
        f"- Ответчики: {', '.join(delo.otvetchiki)}",
    ]
    if delo.summa_iska > 0:
        stroki.append(f"- Сумма иска: {formatirovat_rubli(delo.summa_iska)}")
    return "\n".join(stroki)


async def akty_po_delu(
    nomer_dela: str,
    kontekst: Context,
) -> str:
    """Получить судебные акты по делу.

    Аргументы:
        nomer_dela: Номер дела.

    Возвращает:
        Судебные акты по делу.
    """
    await kontekst.info(f"Запрос актов по делу {nomer_dela}...")
    akty = await client.akty_po_delu(nomer_dela)

    if not akty:
        return (
            f"Судебные акты по делу {nomer_dela} не найдены.\n\n"
            f"Проверьте номер дела или используйте info_dela()."
        )

    stroki_tablitsy = [
        (akt.tip_akta, akt.data_akta, akt.sud, akt.rezolyutsiya[:50]) for akt in akty
    ]
    zagolovok = f"**Судебные акты по делу {nomer_dela}**\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["Тип акта", "Дата", "Суд", "Резолюция"], stroki_tablitsy
    )


async def storony_dela(
    nomer_dela: str,
    kontekst: Context,
) -> str:
    """Получить стороны судебного дела.

    Аргументы:
        nomer_dela: Номер дела.

    Возвращает:
        Стороны дела (истцы и ответчики).
    """
    await kontekst.info(f"Запрос сторон по делу {nomer_dela}...")
    storony = await client.storony_dela(nomer_dela)

    if not storony:
        return f"Стороны по делу {nomer_dela} не найдены.\n\nПроверьте номер дела."

    stroki = [f"**Стороны дела {nomer_dela}**\n"]
    for storona in storony:
        stroki.append(f"- **{storona.tip}**: {storona.nazvanie}")
        if storona.inn:
            stroki.append(f"  ИНН: {storona.inn}")
        if storona.subiekt:
            stroki.append(f"  Регион: {storona.subiekt}")
    return "\n".join(stroki)


async def spravochnik_kategoriy(kontekst: Context) -> str:
    """Получить справочник категорий дел.

    Возвращает:
        Категории дел.
    """
    await kontekst.info("Запрос справочника категорий дел...")
    kategorii = client.poluchit_kategorii_del()

    stroki_tablitsy = [(kategoriya["kod"], kategoriya["nazvanie"]) for kategoriya in kategorii]
    zagolovok = "**Категории арбитражных дел**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Категория"], stroki_tablitsy)


async def spravochnik_instantsiy(kontekst: Context) -> str:
    """Получить справочник инстанций арбитражных судов.

    Возвращает:
        Инстанции судов.
    """
    await kontekst.info("Запрос справочника инстанций судов...")
    instantsii = client.poluchit_instantsii()

    stroki_tablitsy = [(instantsiya["kod"], instantsiya["nazvanie"]) for instantsiya in instantsii]
    zagolovok = "**Инстанции арбитражных судов**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Инстанция"], stroki_tablitsy)


async def spravochnik_statusov(kontekst: Context) -> str:
    """Получить справочник статусов дел.

    Возвращает:
        Статусы дел.
    """
    await kontekst.info("Запрос справочника статусов дел...")
    statusy = client.poluchit_statusy_del()

    stroki_tablitsy = [(sostoyanie["kod"], sostoyanie["nazvanie"]) for sostoyanie in statusy]
    zagolovok = "**Статусы судебных дел**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Статус"], stroki_tablitsy)


async def spravochnik_aktov(kontekst: Context) -> str:
    """Получить справочник типов судебных актов.

    Возвращает:
        Типы актов.
    """
    await kontekst.info("Запрос справочника типов актов...")
    tipy = client.poluchit_tipy_aktov()

    stroki_tablitsy = [(tip["kod"], tip["nazvanie"]) for tip in tipy]
    zagolovok = "**Типы судебных актов**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Тип акта"], stroki_tablitsy)
