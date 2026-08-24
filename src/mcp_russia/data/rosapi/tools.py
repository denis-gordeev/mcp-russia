"""Инструменты модуля РосАПИ.

Инструменты для доступа к российским справочным данным:
- Поиск адресов по почтовому индексу / ФИАС (Дадата)
- Поиск организаций по ИНН/ОГРН (ЕГРЮЛ/ЕГРИП через Дадату)
- Справочник банков (ЦБ РФ через Дадату)
- Праздничные дни России
- Ставки налогов

Правила (CONTRIBUTING.md):
    - tools.py НЕ делает HTTP-запросы напрямую — делегирует client.py
    - Возвращает форматированные строки для LLM
    - Использует Context для структурированного логирования и отчётов о прогрессе
"""

from __future__ import annotations

from datetime import datetime

from fastmcp import Context

from mcp_russia._shared.formatting import tablitsa_v_markdown

from . import client
from .constants import NALOGOVYE_STAVKI, OSNOVNYE_BANKI
from .schemas import AdresRF, BankRF, Organizatsiya


async def konsul_adres_po_indeksu(indeks: str, kontekst: Context) -> str:
    """Найти адрес по почтовому индексу РФ.

    Аргументы:
        indeks: Почтовый индекс (6 цифр, например 101000).

    Возвращает:
        Адресная информация или сообщение об ошибке.
    """
    await kontekst.info(f"Поиск адреса по индексу {indeks}...")
    rezultat = await client.konsultirovat_adres_po_pochtovomu(indeks)

    if isinstance(rezultat, AdresRF):
        stroki = [
            f"**Почтовый индекс:** {rezultat.pochtovyy_indeks}",
            f"**Полный адрес:** {rezultat.polnyy_adres or 'Н/Д'}",
        ]
        if rezultat.subiekt:
            stroki.append(f"**Регион:** {rezultat.subiekt}")
        if rezultat.gorod:
            stroki.append(f"**Город:** {rezultat.gorod}")
        if rezultat.ulitsa:
            stroki.append(f"**Улица:** {rezultat.ulitsa}")
        if rezultat.dom:
            stroki.append(f"**Дом:** {rezultat.dom}")

        stroki.append("\nИсточник: ФИАС / Dadata")
        return "\n".join(stroki)

    return (
        f"**Почтовый индекс: {indeks}**\n\n"
        f"{rezultat['oshibka']}\n\n"
        f"Для получения данных подключите API Dadata (MCP_RUSSIA_DADATA_API_KEY):\n"
        f"https://dadata.ru/api/address/"
    )


async def poisk_adresa(zapros: str, kontekst: Context) -> str:
    """Найти адрес по свободному запросу через ФИАС.

    Аргументы:
        zapros: Строка запроса (например, "Москва, Красная площадь").

    Возвращает:
        Список найденных адресов.
    """
    await kontekst.info(f"Поиск адреса: {zapros}...")
    rezultaty = await client.poisk_adresa(zapros)

    if not rezultaty:
        return (
            f"Адреса по запросу '{zapros}' не найдены.\n\n"
            "Используйте более точный запрос или проверьте MCP_RUSSIA_DADATA_API_KEY."
        )

    stroki_tablitsy = []
    for i, adres_dannye in enumerate(rezultaty[:10], 1):
        stroki_tablitsy.append(
            (
                str(i),
                adres_dannye.get("znachenie", ""),
                adres_dannye.get("pochtovyy_indeks", ""),
            )
        )

    zagolovok = f"**Результаты поиска: {zapros}**\n\n"
    zagolovok += "Источник: ФИАС / Dadata\n\n"
    return zagolovok + tablitsa_v_markdown(["#", "Адрес", "Индекс"], stroki_tablitsy)


async def poisk_org_po_inn(inn: str, kontekst: Context) -> str:
    """Найти организацию по ИНН.

    Аргументы:
        inn: ИНН организации (10 или 12 цифр).

    Возвращает:
        Данные организации.
    """
    await kontekst.info(f"Поиск организации по ИНН {inn}...")
    rezultat = await client.nayti_organizatsiyu_po_inn(inn)

    if isinstance(rezultat, Organizatsiya):
        stroki = [
            f"**{rezultat.nazvanie_kratkoe or rezultat.nazvanie_polnoe or 'Организация'}**",
            f"- ИНН: {rezultat.inn}",
        ]
        if rezultat.kpp:
            stroki.append(f"- КПП: {rezultat.kpp}")
        if rezultat.ogrn:
            stroki.append(f"- ОГРН: {rezultat.ogrn}")
        if rezultat.sostoyanie:
            karta_statusov = {
                "ACTIVE": "Действующая",
                "LIQUIDATING": "Ликвидируется",
                "LIQUIDATED": "Ликвидирована",
                "BANKRUPT": "Банкрот",
                "REORGANIZING": "Реорганизуется",
            }
            status_tekst = karta_statusov.get(rezultat.sostoyanie, rezultat.sostoyanie)
            stroki.append(f"- Статус: {status_tekst}")
        if rezultat.adres:
            stroki.append(f"- Адрес: {rezultat.adres}")
        if rezultat.rukovoditel:
            stroki.append(f"- Руководитель: {rezultat.rukovoditel}")
        if rezultat.data_registratsii:
            stroki.append(f"- Дата регистрации: {rezultat.data_registratsii}")

        stroki.append("- Источник: ЕГРЮЛ/ЕГРИП через Dadata")
        return "\n".join(stroki)

    return (
        f"**ИНН: {inn}**\n\n"
        f"{rezultat['oshibka']}\n\n"
        f"Для получения данных подключите API Dadata (MCP_RUSSIA_DADATA_API_KEY):\n"
        f"https://dadata.ru/api/party/"
    )


async def poisk_org_po_ogrn(ogrn: str, kontekst: Context) -> str:
    """Найти организацию по ОГРН.

    Аргументы:
        ogrn: ОГРН организации (13 или 15 цифр).

    Возвращает:
        Данные организации.
    """
    await kontekst.info(f"Поиск организации по ОГРН {ogrn}...")
    rezultat = await client.nayti_organizatsiyu_po_ogrn(ogrn)

    if isinstance(rezultat, Organizatsiya):
        stroki = [
            f"**{rezultat.nazvanie_kratkoe or rezultat.nazvanie_polnoe or 'Организация'}**",
            f"- ОГРН: {rezultat.ogrn or ogrn}",
        ]
        if rezultat.inn:
            stroki.append(f"- ИНН: {rezultat.inn}")
        if rezultat.kpp:
            stroki.append(f"- КПП: {rezultat.kpp}")
        if rezultat.adres:
            stroki.append(f"- Адрес: {rezultat.adres}")

        stroki.append("- Источник: ЕГРЮЛ/ЕГРИП через Dadata")
        return "\n".join(stroki)

    return f"**ОГРН: {ogrn}**\n\n{rezultat['oshibka']}"


async def spisok_bankov(kontekst: Context) -> str:
    """Получить справочник банков России.

    Возвращает:
        Список банков с БИК и названиями.
    """
    await kontekst.info("Запрос справочника банков...")

    stroki_tablitsy = []
    for bank in OSNOVNYE_BANKI:
        stroki_tablitsy.append(
            (
                bank["bik"],
                bank["nazvanie"],
            )
        )

    zagolovok = "**Основные банки России** (справочник)\n\n"
    zagolovok += (
        "Для полного справочника всех банков ЦБ РФ "
        "используйте konsul_bank_po_bik или подключите API Dadata.\n\n"
    )
    return zagolovok + tablitsa_v_markdown(["БИК", "Название"], stroki_tablitsy)


async def konsul_bank_po_bik(bik: str, kontekst: Context) -> str:
    """Получить информацию о банке по БИК.

    Аргументы:
        bik: БИК банка (9 цифр).

    Возвращает:
        Данные банка.
    """
    await kontekst.info(f"Поиск банка по БИК {bik}...")

    rezultat = await client.nayti_bank_po_bik(bik)

    if isinstance(rezultat, BankRF):
        stroki = [
            f"**{rezultat.nazvanie}**",
            f"- БИК: {rezultat.bik}",
        ]
        if rezultat.nazvanie_kratkoe:
            stroki.append(f"- Краткое название: {rezultat.nazvanie_kratkoe}")
        if rezultat.gorod:
            stroki.append(f"- Город: {rezultat.gorod}")
        if rezultat.svift:
            stroki.append(f"- SWIFT: {rezultat.svift}")

        stroki.append("- Источник: ЦБ РФ через Dadata")
        return "\n".join(stroki)

    naydennye = None
    for bank in OSNOVNYE_BANKI:
        if bank["bik"] == bik:
            naydennye = bank
            break

    if naydennye:
        return (
            f"**{naydennye['nazvanie']}**\n\n"
            f"- БИК: {naydennye['bik']}\n"
            f"- Источник: Справочник ЦБ РФ"
        )

    return (
        f"Банк с БИК {bik} не найден.\n\n"
        f"Для поиска подключите API Dadata (MCP_RUSSIA_DADATA_API_KEY):\n"
        f"https://dadata.ru/api/bank/"
    )


async def prazdniki_rf(god: int | None = None, kontekst: Context | None = None) -> str:
    """Получить список национальных праздников РФ.

    Аргументы:
        god: Год запроса (например, 2025). По умолчанию — текущий.

    Возвращает:
        Список праздников с датами.
    """
    if god is None:
        god = datetime.now().year

    assert kontekst is not None
    await kontekst.info(f"Запрос праздников на {god} год...")
    prazdniki = client.poluchit_prazdniki(god)

    stroki_tablitsy = []
    for prazdnik in prazdniki:
        data_stroka = prazdnik["data"][5:]
        stroki_tablitsy.append((data_stroka, prazdnik["nazvanie"], prazdnik["tip"]))

    zagolovok = f"**Национальные праздники РФ ({god})**\n\n"
    return zagolovok + tablitsa_v_markdown(["Дата", "Праздник", "Тип"], stroki_tablitsy)


async def nalogovye_stavki(kontekst: Context) -> str:
    """Получить основные налоговые ставки РФ.

    Возвращает:
        Справочная информация о налогах.
    """
    await kontekst.info("Запрос налоговых ставок...")

    stavki_info = {
        "NDS": "20% (базовая), 10% (льготная), 0% (экспорт)",
        "NP": "20% (базовая)",
        "NDFL": "13% (резидент), 30% (нерезидент)",
        "USN_D": "6% (может быть снижен регионом до 1%)",
        "USN_DR": "15% (может быть снижен регионом до 5%)",
        "ESN": "6% (от дохода)",
    }

    stroki_tablitsy = []
    for kod, nazvanie in NALOGOVYE_STAVKI.items():
        stavka = stavki_info.get(kod, "Уточняйте в ФНС")
        stroki_tablitsy.append((kod, nazvanie, stavka))

    zagolovok = "**Основные налоговые ставки РФ**\n\n"
    zagolovok += "⚠️ Актуальные ставки уточняйте на сайте ФНС: https://www.nalog.ru\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Налог", "Ставка"], stroki_tablitsy)
