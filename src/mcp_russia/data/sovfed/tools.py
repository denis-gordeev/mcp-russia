"""Инструменты модуля Совета Федерации РФ.

Правила (ADR-001):
    - tools.py НЕ делает HTTP-запросы напрямую — делегирует client.py
    - Возвращает форматированные строки для LLM
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import tablitsa_v_markdown

from . import client


async def spisok_senatorov(kontekst: Context) -> str:
    """Получить список сенаторов Совета Федерации."""
    await kontekst.info("Запрос списка сенаторов...")
    senatory = await client.poisk_senatorov()
    if not senatory:
        return "Сенаторы не найдены.\n\nАктуальные данные доступны на: https://sovfed.ru/senators"
    stroki_tablitsy = [
        (
            senator.get("nomer", ""),
            senator.get("familiya", ""),
            senator.get("imya", ""),
            senator.get("subiekt", ""),
            senator.get("komitet", "")[:40],
        )
        for senator in senatory
    ]
    zagolovok = f"**Сенаторы Совета Федерации РФ** — найдено: {len(senatory)}\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["№", "Фамилия", "Имя", "Регион", "Комитет"],
        stroki_tablitsy,
    )


async def info_senatora(identifikator_senatora: str, kontekst: Context) -> str:
    """Получить информацию о сенаторе Совета Федерации.

    Аргументы:
        identifikator_senatora: Идентификатор сенатора.

    Возвращает:
        Информация о сенаторе.
    """
    await kontekst.info(f"Запрос информации о сенаторе {identifikator_senatora}...")
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
    if dannye.get("fraktsiya"):
        stroki.append(f"- Фракция: {dannye['fraktsiya']}")
    if dannye.get("data_naznacheniya"):
        stroki.append(f"- Дата назначения: {dannye['data_naznacheniya']}")
    stroki.append(f"- Источник: {dannye.get('istochnik', 'sovfed.ru')}")
    return "\n".join(stroki)


async def spisok_komitetov(kontekst: Context) -> str:
    """Получить список комитетов Совета Федерации."""
    await kontekst.info("Запрос списка комитетов...")
    komitety_api = await client.spisok_komitetov()
    if komitety_api:
        stroki_tablitsy = [
            (
                komitet.get("nazvanie", ""),
                komitet.get("predsedatel", ""),
                str(komitet.get("kolichestvo_chlenov", "")),
            )
            for komitet in komitety_api
        ]
        zagolovok = "**Комитеты Совета Федерации РФ**\n\n"
        return zagolovok + tablitsa_v_markdown(
            ["Комитет", "Председатель", "Членов"], stroki_tablitsy
        )
    komitety = client.poluchit_spisok_komitetov()
    stroki_tablitsy = [(komitet["kod"], komitet["nazvanie"], "") for komitet in komitety]
    zagolovok = "**Комитеты Совета Федерации РФ** (справочник)\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Комитет"], stroki_tablitsy)


async def spisok_komissiy(kontekst: Context) -> str:
    """Получить список комиссий Совета Федерации."""
    await kontekst.info("Запрос списка комиссий...")
    komissii_api = await client.spisok_komissiy()
    if komissii_api:
        stroki_tablitsy = [
            (
                komissiya.get("nazvanie", ""),
                komissiya.get("predsedatel", ""),
                str(komissiya.get("kolichestvo_chlenov", "")),
            )
            for komissiya in komissii_api
        ]
        zagolovok = "**Комиссии Совета Федерации РФ**\n\n"
        return zagolovok + tablitsa_v_markdown(
            ["Комиссия", "Председатель", "Членов"], stroki_tablitsy
        )
    komissii = client.poluchit_spisok_komissiy()
    stroki_tablitsy = [(komissiya["kod"], komissiya["nazvanie"], "") for komissiya in komissii]
    zagolovok = "**Комиссии Совета Федерации РФ** (справочник)\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Комиссия"], stroki_tablitsy)


async def poisk_zakonoproektov(
    kontekst: Context,
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
    await kontekst.info("Поиск законопроектов...")
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
            zakonoproekt.get("nomer", ""),
            zakonoproekt.get("nazvanie", "")[:50],
            zakonoproekt.get("sostoyanie", ""),
            zakonoproekt.get("data_rassmotreniya", ""),
        )
        for zakonoproekt in zakonoproekty
    ]
    zagolovok = f"**Законопроекты Совета Федерации РФ** — найдено: {len(zakonoproekty)}\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["№", "Название", "Статус", "Дата рассмотрения"],
        stroki_tablitsy,
    )


async def spisok_zasedaniy(kontekst: Context, god: int = 0) -> str:
    """Получить список заседаний Совета Федерации.

    Аргументы:
        god: Год (необязательно).

    Возвращает:
        Список заседаний.
    """
    await kontekst.info("Запрос списка заседаний...")
    zasedaniya = await client.spisok_zasedaniy(god=god)
    if not zasedaniya:
        god_tekst = f" за {god} год" if god else ""
        return (
            f"Заседания{god_tekst} не найдены.\n\nДанные доступны на: https://sovfed.ru/sessions"
        )
    stroki_tablitsy = [
        (
            zasedanie.get("nomer", ""),
            zasedanie.get("data", ""),
            zasedanie.get("sostoyanie", ""),
            zasedanie.get("povestka", "")[:50],
        )
        for zasedanie in zasedaniya
    ]
    zagolovok = f"**Заседания Совета Федерации РФ** — найдено: {len(zasedaniya)}\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["№", "Дата", "Статус", "Повестка"],
        stroki_tablitsy,
    )


async def poimennoe_golosovanie(
    identifikator_golosovaniya: str,
    kontekst: Context,
) -> str:
    """Получить результаты поимённого голосования Совета Федерации.

    Аргументы:
        identifikator_golosovaniya: Идентификатор голосования.

    Возвращает:
        Результаты поимённого голосования сенаторов.
    """
    await kontekst.info(f"Запрос поимённого голосования {identifikator_golosovaniya}...")
    rezultaty = await client.poimennoe_golosovanie(identifikator_golosovaniya)
    if not rezultaty:
        return (
            f"Результаты голосования '{identifikator_golosovaniya}' не найдены.\n\n"
            f"Данные доступны на: https://sovfed.ru/votes"
        )
    stroki_tablitsy = [
        (
            rezultat.get("fio", ""),
            rezultat.get("subiekt", "")[:30],
            rezultat.get("golos", ""),
            rezultat.get("fraktsiya", ""),
        )
        for rezultat in rezultaty
    ]
    zagolovok = f"**Поимённое голосование** — сенаторов: {len(rezultaty)}\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["ФИО", "Регион", "Голос", "Фракция"],
        stroki_tablitsy,
    )
