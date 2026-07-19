"""Инструменты модуля Госдумы.

Инструменты для доступа к данным о депутатах, законопроектах, фракциях и голосованиях Госдумы.

Правила (ADR-001):
    - tools.py НЕ делает HTTP-запросы напрямую — делегирует client.py
    - Возвращает форматированные строки для LLM
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import tablitsa_v_markdown

from . import client


def _zametka_ob_avtorizatsii() -> str:
    """Заметка о необходимости настройки API-токена при его отсутствии."""
    if not client._poluchit_api_token():
        return "\n\n*Для полного доступа к API настройте MCP_RUSSIA_DUMA_API_TOKEN*"
    return ""


async def spisok_deputatov(sozyv: str = "", kontekst: Context | None = None) -> str:
    """Получить список депутатов Государственной Думы.

    Аргументы:
        sozyv: Номер созыва (например, '8'). По умолчанию — текущий.

    Возвращает:
        Список депутатов.
    """
    if kontekst:
        await kontekst.info(f"Запрос депутатов Госдумы (созыв: {sozyv or 'текущий'})...")
    deputats = await client.poluchit_deputatov(sozyv)

    if not deputats:
        sozyv_label = sozyv or "текущего"
        return (
            f"**Депутаты Государственной Думы ({sozyv_label} созыв)**\n\n"
            f"Не удалось получить данные через API Госдумы.\n\n"
            f"Открытые данные доступны на:\n"
            f"- https://api.duma.gov.ru\n"
            f"- https://download.data.duma.gov.ru\n\n"
            f"Для доступа к API может потребоваться токен (DUMA_API_TOKEN)."
        )

    stroki_tablitsy = [
        (
            str(deputat.identifikator),
            f"{deputat.familiya} {deputat.imya} {deputat.otchestvo}".strip(),
            deputat.frakciya,
            deputat.komitet,
        )
        for deputat in deputats[:50]
    ]
    zagolovok = f"**Депутаты Государственной Думы (созыв {sozyv or 'текущий'})**\n\n"
    zagolovok += f"Найдено: {len(deputats)} депутатов"
    if len(deputats) > 50:
        zagolovok += " (показано первых 50)"
    zagolovok += "\n\n"
    return (
        zagolovok
        + tablitsa_v_markdown(["Идентификатор", "ФИО", "Фракция", "Комитет"], stroki_tablitsy)
        + _zametka_ob_avtorizatsii()
    )


async def info_deputata(identifikator_deputata: int, kontekst: Context) -> str:
    """Получить информацию о конкретном депутате Госдумы.

    Аргументы:
        identifikator_deputata: Идентификатор депутата.

    Возвращает:
        Подробная информация о депутате.
    """
    await kontekst.info(f"Запрос информации о депутате {identifikator_deputata}...")
    deputat = await client.poluchit_deputata(identifikator_deputata)

    if not deputat:
        return (
            f"Депутат с идентификатором {identifikator_deputata} не найден.\n\n"
            f"Используйте spisok_deputatov() для поиска."
        )

    stroki = [
        f"**{deputat.familiya} {deputat.imya} {deputat.otchestvo}**",
        f"- Идентификатор: {deputat.identifikator}",
    ]
    if deputat.frakciya:
        stroki.append(f"- Фракция: {deputat.frakciya}")
    if deputat.komitet:
        stroki.append(f"- Комитет: {deputat.komitet}")
    if deputat.subiekt:
        stroki.append(f"- Регион: {deputat.subiekt}")
    if deputat.sozyv:
        stroki.append(f"- Созыв: {deputat.sozyv}")

    stroki.append("\nИсточник: api.duma.gov.ru / Госдума ФС РФ")

    return "\n".join(stroki)


async def spisok_frakcii(kontekst: Context) -> str:
    """Получить список фракций Государственной Думы.

    Возвращает:
        Список фракций.
    """
    await kontekst.info("Запрос списка фракций Госдумы...")
    frakcii = client.poluchit_fraktsii()

    stroki_tablitsy = [(fraktsiya["kod"], fraktsiya["nazvanie"]) for fraktsiya in frakcii]
    zagolovok = "**Фракции Государственной Думы**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Фракция"], stroki_tablitsy)


async def spisok_komitetov(kontekst: Context) -> str:
    """Получить список комитетов Государственной Думы.

    Возвращает:
        Список комитетов.
    """
    await kontekst.info("Запрос списка комитетов Госдумы...")
    komitety = client.poluchit_komitety()

    stroki_tablitsy = [(komitet["kod"], komitet["nazvanie"]) for komitet in komitety]
    zagolovok = "**Комитеты Государственной Думы**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Комитет"], stroki_tablitsy)


async def spisok_sozyvov(kontekst: Context) -> str:
    """Получить список созывов Государственной Думы.

    Возвращает:
        Список созывов.
    """
    await kontekst.info("Запрос списка созывов Госдумы...")
    sozyvy = client.poluchit_sozyvy()

    stroki_tablitsy = [(sozyv["kod"], sozyv["nazvanie"]) for sozyv in sozyvy]
    zagolovok = "**Созывы Государственной Думы**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Созыв"], stroki_tablitsy)


async def zakonoproekty(
    sostoyanie: str = "",
    ogranichenie: int = 20,
    kontekst: Context | None = None,
) -> str:
    """Получить список законопроектов Государственной Думы.

    Аргументы:
        sostoyanie: Фильтр по статусу (например, 'принят', 'рассматривается').
        ogranichenie: Максимальное количество результатов (до 50).

    Возвращает:
        Список законопроектов.
    """
    if kontekst:
        await kontekst.info(f"Запрос законопроектов (статус: {sostoyanie or 'все'})...")
    zakonoproekty = await client.poluchit_zakonoproekty(
        sostoyanie=sostoyanie, ogranichenie=ogranichenie
    )

    if not zakonoproekty:
        status_label = sostoyanie or "все"
        return (
            f"**Законопроекты Государственной Думы**\n\n"
            f"Не удалось получить данные через API СОЗД.\n\n"
            f"Данные о законопроектах доступны через:\n"
            f"- Система СОЗД: https://sozd.duma.gov.ru\n"
            f"- API: https://api.duma.gov.ru\n\n"
            f"Для поиска законопроектов по статусу '{status_label}' "
            f"используйте API СОЗД."
        )

    stroki_tablitsy = [
        (
            zakonoproekt.nomer,
            zakonoproekt.nazvanie[:80],
            zakonoproekt.sostoyanie,
            zakonoproekt.data_vneseniya,
        )
        for zakonoproekt in zakonoproekty
    ]
    zagolovok = "**Законопроекты Государственной Думы**\n\n"
    zagolovok += f"Найдено: {len(zakonoproekty)} законопроектов\n\n"
    return (
        zagolovok
        + tablitsa_v_markdown(["Номер", "Название", "Статус", "Дата внесения"], stroki_tablitsy)
        + _zametka_ob_avtorizatsii()
    )


async def golosovaniya(
    sozyv: str = "",
    ogranichenie: int = 20,
    kontekst: Context | None = None,
) -> str:
    """Получить результаты голосований Государственной Думы.

    Аргументы:
        sozyv: Номер созыва.
        ogranichenie: Максимальное количество результатов (до 50).

    Возвращает:
        Результаты голосований.
    """
    if kontekst:
        await kontekst.info(f"Запрос голосований (созыв: {sozyv or 'текущий'})...")
    golosovaniya_spisok = await client.poluchit_golosovaniya(
        sozyv=sozyv, ogranichenie=ogranichenie
    )

    if not golosovaniya_spisok:
        return (
            "**Голосования Государственной Думы**\n\n"
            "Не удалось получить данные через API Госдумы.\n\n"
            "Результаты голосований доступны на:\n"
            "- https://duma.gov.ru\n"
            "- https://api.duma.gov.ru\n\n"
            "Для доступа к API может потребоваться токен (DUMA_API_TOKEN)."
        )

    stroki_tablitsy = [
        (
            golosovanie.zakonoproekt_identifikator,
            golosovanie.nazvanie[:60],
            golosovanie.data,
            f"За: {golosovanie.za} / Против: {golosovanie.protiv}",
        )
        for golosovanie in golosovaniya_spisok
    ]
    zagolovok = "**Голосования Государственной Думы**\n\n"
    zagolovok += f"Найдено: {len(golosovaniya_spisok)} голосований\n\n"
    return (
        zagolovok
        + tablitsa_v_markdown(["Идентификатор", "Тема", "Дата", "Результат"], stroki_tablitsy)
        + _zametka_ob_avtorizatsii()
    )
