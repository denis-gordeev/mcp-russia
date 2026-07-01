"""Инструменты модуля Совета Федерации РФ.

Правила (ADR-001):
    - tools.py НЕ делает HTTP-запросы напрямую — делегирует client.py
    - Возвращает форматированные строки для LLM
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import tablitsa_v_markdown

from . import client


async def spisok_senatorov(ctx: Context) -> str:
    """Получить список сенаторов Совета Федерации."""
    await ctx.info("Запрос списка сенаторов...")
    senatory = await client.poisk_senatorov()
    if not senatory:
        return "Сенаторы не найдены.\n\nАктуальные данные доступны на: https://sovfed.ru/senators"
    stroki_tablitsy = [
        (
            s.get("nomer", ""),
            s.get("familiya", ""),
            s.get("imya", ""),
            s.get("subiekt", ""),
            s.get("komitet", "")[:40],
        )
        for s in senatory
    ]
    zagolovok = f"**Сенаторы Совета Федерации РФ** — найдено: {len(senatory)}\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["№", "Фамилия", "Имя", "Регион", "Комитет"],
        stroki_tablitsy,
    )


async def info_senatora(identifikator_senatora: str, ctx: Context) -> str:
    """Получить информацию о сенаторе Совета Федерации.

    Аргументы:
        identifikator_senatora: Идентификатор сенатора.

    Возвращает:
        Информация о сенаторе.
    """
    await ctx.info(f"Запрос информации о сенаторе {identifikator_senatora}...")
    dannye = await client.info_senatora(identifikator_senatora)
    if not dannye:
        return (
            f"Сенатор '{identifikator_senatora}' не найден.\n\n"
            f"Проверьте идентификатор на сайте Совета Федерации: sovfed.ru/senators"
        )
    fio = f"{dannye.get('familiya', '')} {dannye.get('imya', '')} {dannye.get('otchestvo', '')}".strip()
    stroki = [
        f"**{fio}** (№ {dannye.get('nomer', identifikator_senatora)})",
        f"- Регион: {dannye.get('subiekt', '')}",
        f"- Должность: {dannye.get('dolzhnost', '')}",
    ]
    if dannye.get("komitet"):
        stroki.append(f"- Комитет: {dannye['komitet']}")
    if dannye.get("frakciya"):
        stroki.append(f"- Фракция: {dannye['frakciya']}")
    if dannye.get("data_naznacheniya"):
        stroki.append(f"- Дата назначения: {dannye['data_naznacheniya']}")
    stroki.append(f"- Источник: {dannye.get('istochnik', 'sovfed.ru')}")
    return "\n".join(stroki)


async def spisok_komitetov(ctx: Context) -> str:
    """Получить список комитетов Совета Федерации."""
    await ctx.info("Запрос списка комитетов...")
    komitety_api = await client.spisok_komitetov()
    if komitety_api:
        stroki_tablitsy = [
            (
                k.get("nazvanie", ""),
                k.get("predsedatel", ""),
                str(k.get("kolichestvo_chlenov", "")),
            )
            for k in komitety_api
        ]
        zagolovok = "**Комитеты Совета Федерации РФ**\n\n"
        return zagolovok + tablitsa_v_markdown(
            ["Комитет", "Председатель", "Членов"], stroki_tablitsy
        )
    komitety = client.poluchit_spisok_komitetov()
    stroki_tablitsy = [(k["kod"], k["nazvanie"]) for k in komitety]
    zagolovok = "**Комитеты Совета Федерации РФ** (справочник)\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Комитет"], stroki_tablitsy)


async def spisok_komissiy(ctx: Context) -> str:
    """Получить список комиссий Совета Федерации."""
    await ctx.info("Запрос списка комиссий...")
    komissii_api = await client.spisok_komissiy()
    if komissii_api:
        stroki_tablitsy = [
            (
                k.get("nazvanie", ""),
                k.get("predsedatel", ""),
                str(k.get("kolichestvo_chlenov", "")),
            )
            for k in komissii_api
        ]
        zagolovok = "**Комиссии Совета Федерации РФ**\n\n"
        return zagolovok + tablitsa_v_markdown(
            ["Комиссия", "Председатель", "Членов"], stroki_tablitsy
        )
    komissii = client.poluchit_spisok_komissiy()
    stroki_tablitsy = [(k["kod"], k["nazvanie"]) for k in komissii]
    zagolovok = "**Комиссии Совета Федерации РФ** (справочник)\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Комиссия"], stroki_tablitsy)


async def poisk_zakonoproektov(
    ctx: Context,
    sostoyanie: str = "",
    god: int = 0,
) -> str:
    """Поиск законопроектов, рассмотренных Советом Федерации.

    Аргументы:
        sostoyanie: Статус законопроекта (необязательно).
        god: Год (необязательно).

    Возвращает:
        Список законопроектов.
    """
    await ctx.info("Поиск законопроектов...")
    zakonoproekty = await client.poisk_zakonoproektov(
        sostoyanie=sostoyanie,
        god=god,
    )
    if not zakonoproekty:
        filtry = []
        if sostoyanie:
            filtry.append(f"статус: {sostoyanie}")
        if god:
            filtry.append(f"год: {god}")
        tekst_filtra = f" ({', '.join(filtry)})" if filtry else ""
        return (
            f"Законопроекты{tekst_filtra} не найдены.\n\n"
            f"Данные доступны на: https://sovfed.ru/bills"
        )
    stroki_tablitsy = [
        (
            z.get("nomer", ""),
            z.get("nazvanie", "")[:50],
            z.get("sostoyanie", ""),
            z.get("data_rassmotreniya", ""),
        )
        for z in zakonoproekty
    ]
    zagolovok = f"**Законопроекты Совета Федерации РФ** — найдено: {len(zakonoproekty)}\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["№", "Название", "Статус", "Дата рассмотрения"],
        stroki_tablitsy,
    )


async def spisok_zasedaniy(ctx: Context, god: int = 0) -> str:
    """Получить список заседаний Совета Федерации.

    Аргументы:
        god: Год (необязательно).

    Возвращает:
        Список заседаний.
    """
    await ctx.info("Запрос списка заседаний...")
    zasedaniya = await client.spisok_zasedaniy(god=god)
    if not zasedaniya:
        god_text = f" за {god} год" if god else ""
        return f"Заседания{god_text} не найдены.\n\nДанные доступны на: https://sovfed.ru/sessions"
    stroki_tablitsy = [
        (
            z.get("nomer", ""),
            z.get("data", ""),
            z.get("sostoyanie", ""),
            z.get("povestka", "")[:50],
        )
        for z in zasedaniya
    ]
    zagolovok = f"**Заседания Совета Федерации РФ** — найдено: {len(zasedaniya)}\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["№", "Дата", "Статус", "Повестка"],
        stroki_tablitsy,
    )
