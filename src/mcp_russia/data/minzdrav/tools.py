"""Инструменты модуля Минздрава РФ.

Правила (ADR-001):
    - tools.py НЕ делает HTTP-запросы напрямую — делегирует client.py
    - Возвращает форматированные строки для LLM
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import tablitsa_v_markdown

from . import client


async def poisk_med_organizatsiy(
    kontekst: Context,
    subiekt: str = "",
    tip: str = "",
    gorod: str = "",
) -> str:
    """Поиск медицинских организаций в ФРМО.

    Аргументы:
        subiekt: Субъект РФ (необязательно).
        tip: Тип организации — больница, поликлиника и т.д. (необязательно).
        gorod: Город (необязательно).

    Возвращает:
        Список медицинских организаций.
    """
    await kontekst.info(f"Поиск медицинских организаций: {subiekt or 'все'}...")
    organizatsii = await client.poisk_med_organizatsiy(
        subiekt=subiekt,
        tip=tip,
        gorod=gorod,
    )
    if not organizatsii:
        return (
            "Медицинские организации не найдены.\n\n"
            "Данные доступны через:\n"
            "- ФРМО: https://frrr.rosminzdrav.ru\n"
            "- Росздравнадзор: https://roszdravnadzor.gov.ru"
        )
    stroki_tablitsy = [
        (
            organizatsiya.get("nazvanie", ""),
            organizatsiya.get("tip", ""),
            organizatsiya.get("subiekt", ""),
            organizatsiya.get("gorod", ""),
        )
        for organizatsiya in organizatsii
    ]
    return tablitsa_v_markdown(
        ["Название", "Тип", "Регион", "Город"],
        stroki_tablitsy,
    )


async def info_med_organizatsii(
    kontekst: Context,
    identifikator_mo: str,
) -> str:
    """Получить информацию о конкретной медицинской организации.

    Аргументы:
        identifikator_mo: Идентификатор медицинской организации (ОГРН или ИНН).

    Возвращает:
        Подробная информация о медицинской организации.
    """
    await kontekst.info(f"Запрос информации о МО {identifikator_mo}...")
    mo = await client.info_med_organizatsii(identifikator_mo)

    if not mo:
        return (
            f"Медицинская организация с ID {identifikator_mo} не найдена.\n\n"
            f"Используйте poisk_med_organizatsiy() для поиска."
        )

    stroki = [
        f"**{mo.get('nazvanie', '')}**",
        f"- Тип: {mo.get('tip', '')}",
        f"- Адрес: {mo.get('adres', '')}",
        f"- Регион: {mo.get('subiekt', '')}",
        f"- Город: {mo.get('gorod', '')}",
        f"- Телефон: {mo.get('telefon', '')}",
        f"- Лицензия: {mo.get('litsenzia', '')}",
        f"- Коек: {mo.get('krovatey', 0)}",
        f"- Врачей: {mo.get('vrachey', 0)}",
        f"- Источник: {mo.get('istochnik', 'ФРМО')}",
    ]
    return "\n".join(stroki)


async def poisk_litsenziy(
    kontekst: Context,
    inn: str = "",
    vid: str = "",
    sostoyanie: str = "",
) -> str:
    """Поиск лицензий Росздравнадзора на медицинскую деятельность.

    Аргументы:
        inn: ИНН организации (необязательно).
        vid: Вид лицензируемой деятельности (необязательно).
        sostoyanie: Статус лицензии (необязательно).

    Возвращает:
        Список лицензий.
    """
    await kontekst.info("Поиск лицензий Росздравнадзора...")
    litsenzii = await client.poisk_litsenziy(inn=inn, vid=vid, sostoyanie=sostoyanie)
    if not litsenzii:
        return (
            "Лицензии не найдены.\n\n"
            "Реестр лицензий Росздравнадзора: https://roszdravnadzor.gov.ru"
        )
    stroki_tablitsy = [
        (
            lit.get("nomer", ""),
            lit.get("organizaciya", ""),
            lit.get("vid_deyatelnosti", ""),
            lit.get("sostoyanie", ""),
            lit.get("data_okonchaniya", ""),
        )
        for lit in litsenzii
    ]
    return tablitsa_v_markdown(
        ["№ лицензии", "Организация", "Вид деятельности", "Статус", "Действует до"],
        stroki_tablitsy,
    )


async def pokazateli_zdorovya(
    kontekst: Context,
    subiekt: str = "",
    god: int = 0,
) -> str:
    """Получить показатели здоровья населения из открытых данных Минздрава.

    Аргументы:
        subiekt: Субъект РФ (пусто = вся Россия).
        god: Год данных.

    Возвращает:
        Показатели здоровья населения.
    """
    await kontekst.info(f"Запрос показателей здоровья: {subiekt or 'РФ'}, {god or 'последние'}...")
    dannye = await client.pokazateli_zdorovya(subiekt=subiekt, god=god)
    if not dannye:
        return (
            f"**Показатели здоровья населения**\n\n"
            f"Регион: {subiekt or 'Вся Россия'}\n\n"
            f"Данные доступны через открытые источники Минздрава:\n"
            f"https://data.minzdrav.gov.ru"
        )
    stroki_tablitsy = [
        (
            pokazatel.get("nazvanie", ""),
            str(pokazatel.get("znachenie", "")),
            pokazatel.get("ed_izm", ""),
            str(pokazatel.get("god", "")),
            pokazatel.get("subiekt", ""),
        )
        for pokazatel in dannye
    ]
    return tablitsa_v_markdown(
        ["Показатель", "Значение", "Ед. изм.", "Год", "Регион"],
        stroki_tablitsy,
    )


async def statistika_zabolevaniy(
    kontekst: Context,
    kod_mkb: str = "",
    subiekt: str = "",
    god: int = 0,
) -> str:
    """Получить статистику заболеваний по МКБ-10.

    Аргументы:
        kod_mkb: Код МКБ-10 (например, 'I00-I99' для болезней кровообращения).
        subiekt: Субъект РФ.
        god: Год данных.

    Возвращает:
        Статистика заболеваний.
    """
    await kontekst.info(
        f"Запрос статистики заболеваний: {kod_mkb or 'все'}, {god or 'последние'}..."
    )
    dannye = await client.statistika_zabolevaniy(kod_mkb=kod_mkb, subiekt=subiekt, god=god)
    if not dannye:
        zagolovok = "**Статистика заболеваний**\n\n"
        if kod_mkb:
            zagolovok += f"Код МКБ-10: {kod_mkb}\n"
        if subiekt:
            zagolovok += f"Регион: {subiekt}\n"
        zagolovok += (
            "\nДанные о заболеваемости доступны через:\n"
            "- Открытые данные Минздрава: https://data.minzdrav.gov.ru\n"
        )
        return zagolovok
    stroki_tablitsy = [
        (
            zapis.get("kod_mkb", ""),
            zapis.get("nazvanie", ""),
            str(zapis.get("chelovek_zabolelo", "")),
            str(zapis.get("letalnykh_sluchaev", "")),
            str(zapis.get("god", "")),
        )
        for zapis in dannye
    ]
    return tablitsa_v_markdown(
        ["МКБ-10", "Заболевание", "Заболевших", "Летальных", "Год"],
        stroki_tablitsy,
    )


async def spravochnik_mo(kontekst: Context) -> str:
    """Получить справочник типов медицинских организаций.

    Возвращает:
        Справочник типов МО.
    """
    await kontekst.info("Запрос справочника типов медицинских организаций...")
    tipy = client.poluchit_tipy_mo()
    stroki_tablitsy = [(tip["kod"], tip["nazvanie"]) for tip in tipy]
    zagolovok = "**Типы медицинских организаций**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Тип организации"], stroki_tablitsy)


async def spravochnik_spetsialnostey(kontekst: Context) -> str:
    """Получить справочник врачебных специальностей.

    Возвращает:
        Справочник специальностей.
    """
    await kontekst.info("Запрос справочника врачебных специальностей...")
    spetsialnosti = client.poluchit_spetsialnosti()
    stroki_tablitsy = [
        (spetsialnost["kod"], spetsialnost["nazvanie"]) for spetsialnost in spetsialnosti
    ]
    zagolovok = "**Врачебные специальности**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Специальность"], stroki_tablitsy)


async def spravochnik_mkb10(kontekst: Context) -> str:
    """Получить основные классы МКБ-10.

    Возвращает:
        Классы МКБ-10.
    """
    await kontekst.info("Запрос справочника МКБ-10...")
    mkb_klassy = client.poluchit_klassy_mkb10()
    stroki_tablitsy = [(klass["kod"], klass["nazvanie"]) for klass in mkb_klassy]
    zagolovok = "**Классы МКБ-10**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Класс заболеваний"], stroki_tablitsy)
