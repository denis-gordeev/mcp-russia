"""Инструменты модуля ЕИС Закупок.

Инструменты для поиска данных о закупках, контрактах, поставщиках и заказчиках.

Правила (CONTRIBUTING.md):
    - tools.py НЕ делает HTTP-запросы напрямую — делегирует client.py
    - Возвращает форматированные строки для LLM
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import formatirovat_rubli, tablitsa_v_markdown

from . import client


def _zametka_ob_avtorizatsii() -> str:
    """Заметка о необходимости настройки API-токена при его отсутствии."""
    if not client._poluchit_api_token():
        return "\n\n*Для полного доступа к API настройте MCP_RUSSIA_ZAKUPKI_API_TOKEN*"
    return ""


async def poisk_zakupok(
    zapros: str = "",
    zakon: str = "",
    subiekt: str = "",
    sostoyanie: str = "",
    kontekst: Context | None = None,
) -> str:
    """Поиск закупок в Единой информационной системе.

    Аргументы:
        zapros: Поисковый запрос (предмет закупки).
        zakon: Тип закона ("44-ФЗ" или "223-ФЗ").
        subiekt: Регион заказчика.
        sostoyanie: Статус закупки.

    Возвращает:
        Результаты поиска закупок.
    """
    if kontekst:
        await kontekst.info(f"Поиск закупок: {zapros or 'все'}...")

    zakupki = await client.poisk_zakupok(
        zapros=zapros,
        zakon=zakon,
        subiekt=subiekt,
        sostoyanie=sostoyanie,
    )

    if not zakupki:
        zagolovok = "**Результаты поиска в ЕИС закупок**\n\n"
        filtry = []
        if zapros:
            filtry.append(f"Запрос: {zapros}")
        if zakon:
            filtry.append(f"Закон: {zakon}")
        if subiekt:
            filtry.append(f"Регион: {subiekt}")
        if sostoyanie:
            filtry.append(f"Статус: {sostoyanie}")
        if filtry:
            zagolovok += "Фильтры: " + ", ".join(filtry) + "\n\n"

        zagolovok += (
            "Не удалось получить данные через API ЕИС.\n\n"
            "Данные о закупках доступны через:\n"
            "- Портал ЕИС: https://zakupki.gov.ru\n"
            "- Открытые данные: https://data.zakupki.gov.ru\n\n"
            "Для поиска используйте параметры:\n"
            "- `zapros` — предмет закупки\n"
            "- `zakon` — 44-ФЗ или 223-ФЗ\n"
            "- `subiekt` — субъект РФ\n"
            "- `sostoyanie` — статус закупки"
        )
        return zagolovok

    stroki_tablitsy = [
        (
            zakupka.nomer,
            zakupka.nazvanie[:60],
            zakupka.zakon,
            zakupka.sostoyanie,
            formatirovat_rubli(zakupka.nachalnaya_tsena),
        )
        for zakupka in zakupki[:30]
    ]
    zagolovok = "**Результаты поиска в ЕИС закупок**\n\n"
    zagolovok += f"Найдено: {len(zakupki)} закупок\n\n"
    return (
        zagolovok
        + tablitsa_v_markdown(["Номер", "Название", "Закон", "Статус", "Цена"], stroki_tablitsy)
        + _zametka_ob_avtorizatsii()
    )


async def info_zakupki(
    nomer_zakupki: str,
    kontekst: Context,
) -> str:
    """Получить подробную информацию о конкретной закупке по номеру.

    Аргументы:
        nomer_zakupki: Номер закупки в ЕИС.

    Возвращает:
        Подробная информация о закупке.
    """
    await kontekst.info(f"Запрос информации о закупке {nomer_zakupki}...")
    zakupka = await client.poluchit_zakupku(nomer_zakupki)

    if not zakupka:
        return (
            f"Закупка с номером {nomer_zakupki} не найдена.\n\n"
            f"Используйте poisk_zakupok() для поиска."
        )

    stroki = [
        f"**Закупка {zakupka.nomer}**",
        f"- Название: {zakupka.nazvanie}",
    ]
    if zakupka.zakon:
        stroki.append(f"- Закон: {zakupka.zakon}")
    if zakupka.sposob:
        stroki.append(f"- Способ: {zakupka.sposob}")
    if zakupka.sostoyanie:
        stroki.append(f"- Статус: {zakupka.sostoyanie}")
    if zakupka.nachalnaya_tsena:
        stroki.append(f"- Начальная цена: {formatirovat_rubli(zakupka.nachalnaya_tsena)}")
    if zakupka.data_publikatsii:
        stroki.append(f"- Дата публикации: {zakupka.data_publikatsii}")
    if zakupka.srok_podachi:
        stroki.append(f"- Срок подачи заявок: {zakupka.srok_podachi}")
    if zakupka.nazvanie_organizatora:
        stroki.append(f"- Заказчик: {zakupka.nazvanie_organizatora}")
    if zakupka.organizator_inn:
        stroki.append(f"- ИНН заказчика: {zakupka.organizator_inn}")

    stroki.append("\nИсточник: ЕИС закупок / zakupki.gov.ru")
    return "\n".join(stroki)


async def poisk_kontraktov(
    inn_postavshchika: str = "",
    inn_zakazchika: str = "",
    kontekst: Context | None = None,
) -> str:
    """Поиск контрактов в реестре контрактов.

    Аргументы:
        inn_postavshchika: ИНН поставщика.
        inn_zakazchika: ИНН заказчика.

    Возвращает:
        Результаты поиска контрактов.
    """
    if kontekst:
        await kontekst.info("Поиск контрактов в ЕИС...")

    kontrakty = await client.poisk_kontraktov(
        inn_podryadchika=inn_postavshchika,
        inn_zakazchika=inn_zakazchika,
    )

    if not kontrakty:
        return (
            "**Результаты поиска контрактов**\n\n"
            "Не удалось получить данные через API ЕИС.\n\n"
            "Реестр контрактов доступен на: https://zakupki.gov.ru"
        )

    stroki_tablitsy = [
        (
            kontrakt.nomer,
            kontrakt.nazvanie_podryadchika[:40],
            formatirovat_rubli(kontrakt.tsena),
            kontrakt.sostoyanie,
            kontrakt.data_podpisaniya,
        )
        for kontrakt in kontrakty[:30]
    ]
    zagolovok = f"**Контракты в ЕИС**\n\nНайдено: {len(kontrakty)}\n\n"
    return (
        zagolovok
        + tablitsa_v_markdown(["Номер", "Поставщик", "Цена", "Статус", "Дата"], stroki_tablitsy)
        + _zametka_ob_avtorizatsii()
    )


async def info_zakazchika(
    inn: str,
    kontekst: Context,
) -> str:
    """Получить информацию о заказчике по ИНН.

    Аргументы:
        inn: ИНН заказчика.

    Возвращает:
        Информация о заказчике.
    """
    await kontekst.info(f"Запрос информации о заказчике ИНН {inn}...")
    zakazchik = await client.info_zakazchika(inn)

    if not zakazchik:
        return f"Заказчик с ИНН {inn} не найден в ЕИС.\n\nПроверьте корректность ИНН."

    stroki = [
        f"**Заказчик: {zakazchik.nazvanie}**",
        f"- ИНН: {zakazchik.inn}",
    ]
    if zakazchik.kpp:
        stroki.append(f"- КПП: {zakazchik.kpp}")
    if zakazchik.subiekt:
        stroki.append(f"- Регион: {zakazchik.subiekt}")
    if zakazchik.adres:
        stroki.append(f"- Адрес: {zakazchik.adres}")
    if zakazchik.zakupki_kolichestvo:
        stroki.append(f"- Количество закупок: {zakazchik.zakupki_kolichestvo}")
    if zakazchik.obshchie_raskhody:
        stroki.append(
            f"- Общая сумма контрактов: {formatirovat_rubli(zakazchik.obshchie_raskhody)}"
        )

    stroki.append("\nИсточник: ЕГРЮЛ / egrul.nalog.ru")
    return "\n".join(stroki)


async def info_postavshchika(
    inn: str,
    kontekst: Context,
) -> str:
    """Получить информацию о поставщике по ИНН.

    Аргументы:
        inn: ИНН поставщика.

    Возвращает:
        Информация о поставщике.
    """
    await kontekst.info(f"Запрос информации о поставщике ИНН {inn}...")
    postavshchik = await client.info_postavshchika(inn)

    if not postavshchik:
        return f"Поставщик с ИНН {inn} не найден.\n\nПроверьте корректность ИНН."

    sostoyanie = (
        "Добросовестный" if postavshchik.is_dobrosovestny else "В реестре недобросовестных"
    )
    stroki = [
        f"**Поставщик: {postavshchik.nazvanie}**",
        f"- ИНН: {postavshchik.inn}",
    ]
    if postavshchik.subiekt:
        stroki.append(f"- Регион: {postavshchik.subiekt}")
    stroki.append(f"- Статус: {sostoyanie}")
    if postavshchik.kontraktov_vyigrano:
        stroki.append(f"- Выиграно контрактов: {postavshchik.kontraktov_vyigrano}")
    if postavshchik.kontraktov_ispolneno:
        stroki.append(f"- Исполнено контрактов: {postavshchik.kontraktov_ispolneno}")
    if postavshchik.obshchiy_dokhod:
        stroki.append(f"- Общая выручка: {formatirovat_rubli(postavshchik.obshchiy_dokhod)}")

    stroki.append("\nИсточник: ЕГРЮЛ/ЕГРИП / egrul.nalog.ru")
    return "\n".join(stroki)


async def statusy_zakupok(kontekst: Context) -> str:
    """Получить справочник статусов закупок.

    Возвращает:
        Справочник статусов.
    """
    await kontekst.info("Запрос справочника статусов закупок...")
    statusy = client.poluchit_statusy_zakupok()

    stroki_tablitsy = [(sostoyanie["kod"], sostoyanie["nazvanie"]) for sostoyanie in statusy]
    zagolovok = "**Статусы закупок в ЕИС**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Статус"], stroki_tablitsy)


async def sposoby_zakupok(kontekst: Context) -> str:
    """Получить справочник способов определения поставщиков.

    Возвращает:
        Справочник способов.
    """
    await kontekst.info("Запрос справочника способов закупок...")
    sposoby = client.poluchit_sposoby_zakupok()

    stroki_tablitsy = [(sposob["kod"], sposob["nazvanie"]) for sposob in sposoby]
    zagolovok = "**Способы определения поставщиков**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Способ закупки"], stroki_tablitsy)


async def plany_zakupok(
    god: int = 2026,
    kontekst: Context | None = None,
) -> str:
    """Получить планы-графики закупок на указанный год.

    Аргументы:
        god: Год плана-графика.

    Возвращает:
        Информация о планах-графиках.
    """
    if kontekst:
        await kontekst.info(f"Запрос планов закупок на {god} год...")

    plany = await client.plany_zakupok(god=god)

    if not plany:
        return (
            f"**Планы-графики закупок на {god} год**\n\n"
            f"Не удалось получить данные через API ЕИС.\n\n"
            f"Планы-графики формируются заказчиками до начала финансового года.\n"
            f"Доступны через ЕИС: https://zakupki.gov.ru\n\n"
            f"Для поиска планов по конкретному заказчику укажите ИНН организатора."
        )

    stroki_tablitsy = [
        (
            plan.nazvanie_organizatora[:40],
            plan.organizator_inn,
            str(plan.kolichestvo_pozitsiy),
            formatirovat_rubli(plan.obshchiy_byudzhet),
        )
        for plan in plany[:30]
    ]
    zagolovok = f"**Планы-графики закупок на {god} год**\n\n"
    zagolovok += f"Найдено: {len(plany)}\n\n"
    return (
        zagolovok
        + tablitsa_v_markdown(["Заказчик", "ИНН", "Позиций", "Бюджет"], stroki_tablitsy)
        + _zametka_ob_avtorizatsii()
    )


async def poisk_rnp(
    inn: str = "",
    nazvanie: str = "",
    god: int = 0,
    kontekst: Context | None = None,
) -> str:
    """Поиск в реестре недобросовестных поставщиков (РНП).

    Аргументы:
        inn: ИНН поставщика (необязательно).
        nazvanie: Название организации (необязательно).
        god: Год включения в РНП (необязательно).

    Возвращает:
        Список недобросовестных поставщиков.
    """
    if kontekst:
        await kontekst.info("Поиск в реестре недобросовестных поставщиков...")

    zapisi = await client.poisk_rnp(inn=inn, nazvanie=nazvanie, god=god)

    if not zapisi:
        return (
            "**Реестр недобросовестных поставщиков (РНП)**\n\n"
            "Записи не найдены.\n\n"
            "Реестр РНП доступен на: https://zakupki.gov.ru/epz/dishonestsupplier/quicksearch/search.html"
        )

    stroki_tablitsy = [
        (
            zapis.nazvanie[:40],
            zapis.inn,
            zapis.data_vklyucheniya,
            zapis.osnovanie[:40],
            zapis.sostoyanie,
        )
        for zapis in zapisi
    ]
    zagolovok = f"**Реестр недобросовестных поставщиков** — найдено: {len(zapisi)}\n\n"
    return (
        zagolovok
        + tablitsa_v_markdown(
            ["Организация", "ИНН", "Дата включения", "Основание", "Статус"],
            stroki_tablitsy,
        )
        + _zametka_ob_avtorizatsii()
    )
