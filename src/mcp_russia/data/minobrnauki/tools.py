"""Инструменты модуля Минобрнауки."""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import formatirovat_chislo_ru, tablitsa_v_markdown

from . import client
from .constants import (
    FEDERALNYE_OKRUGA,
    FORMY_OBUCHENIYA,
    OTRASLI_NAUKI,
    STATUSY_AKKREDITATSII,
    TIPY_GRANTOV,
    TIPY_VUZOV,
    UROVNI_OBRAZOVANIYA,
)


async def spisok_tipov_vuzov(kontekst: Context) -> str:
    """Список типов высших учебных заведений.

    Возвращает:
        Список типов вузов (университет, академия, институт и т.д.).
    """
    stroki_tablitsy = [(tip["kod"], tip["nazvanie"]) for tip in TIPY_VUZOV]
    return tablitsa_v_markdown(["Код", "Тип вуза"], stroki_tablitsy)


async def spisok_form_obucheniya(kontekst: Context) -> str:
    """Список форм обучения.

    Возвращает:
        Список форм (очная, заочная, очно-заочная, дистанционная).
    """
    stroki_tablitsy = [(forma["kod"], forma["nazvanie"]) for forma in FORMY_OBUCHENIYA]
    return tablitsa_v_markdown(["Код", "Форма обучения"], stroki_tablitsy)


async def spisok_urovney_obrazovaniya(kontekst: Context) -> str:
    """Список уровней образования.

    Возвращает:
        Список уровней (бакалавриат, специалитет, магистратура и т.д.).
    """
    stroki_tablitsy = [(uroven["kod"], uroven["nazvanie"]) for uroven in UROVNI_OBRAZOVANIYA]
    return tablitsa_v_markdown(["Код", "Уровень образования"], stroki_tablitsy)


async def spisok_otrasley_nauki(kontekst: Context) -> str:
    """Список отраслей науки.

    Возвращает:
        Список отраслей (естественные, технические, гуманитарные и т.д.).
    """
    stroki_tablitsy = [(otrasl["kod"], otrasl["nazvanie"]) for otrasl in OTRASLI_NAUKI]
    return tablitsa_v_markdown(["Код", "Отрасль науки"], stroki_tablitsy)


async def spisok_tipov_grantov(kontekst: Context) -> str:
    """Список типов научных грантов.

    Возвращает:
        Список грантовых фондов и программ.
    """
    stroki_tablitsy = [(grant["kod"], grant["nazvanie"]) for grant in TIPY_GRANTOV]
    return tablitsa_v_markdown(["Код", "Тип гранта"], stroki_tablitsy)


async def spisok_statusov_akkreditatsii(kontekst: Context) -> str:
    """Список статусов аккредитации вузов.

    Возвращает:
        Список статусов (действует, приостановлена, отменена).
    """
    stroki_tablitsy = [
        (sostoyanie["kod"], sostoyanie["nazvanie"]) for sostoyanie in STATUSY_AKKREDITATSII
    ]
    return tablitsa_v_markdown(["Код", "Статус аккредитации"], stroki_tablitsy)


async def spisok_federalnyh_okrugov(kontekst: Context) -> str:
    """Список федеральных округов РФ.

    Возвращает:
        Список федеральных округов.
    """
    stroki_tablitsy = [(okrug["kod"], okrug["nazvanie"]) for okrug in FEDERALNYE_OKRUGA]
    return tablitsa_v_markdown(["Код", "Федеральный округ"], stroki_tablitsy)


async def info_vuza(kontekst: Context, nazvanie: str = "", inn: str = "") -> str:
    """Информация о высшем учебном заведении (аккредитация Рособрнадзора).

    Аргументы:
        nazvanie: Название вуза (напр. «МГУ», «МФТИ»).
        inn: ИНН вуза.

    Возвращает:
        Сведения о вузе (тип, город, регион, аккредитация).
    """
    await kontekst.info(f"Запрос информации о вузе «{nazvanie or inn}»...")
    if inn:
        dannye = await client.info_akkreditacii(inn)
    else:
        rezultaty = await client.poisk_akreditovannyh_vuzov(nazvanie=nazvanie)
        dannye = rezultaty[0] if rezultaty else None

    if not dannye:
        return f"Информация о вузе «{nazvanie or inn}» не найдена в реестре Рособрнадзора."
    stroki = [
        f"**{dannye.get('nazvanie', nazvanie or inn)}**",
        f"- ИНН: {dannye.get('inn', '')}",
        f"- Тип: {dannye.get('tip', '')}",
        f"- Город: {dannye.get('gorod', '')}",
        f"- Регион: {dannye.get('subiekt', '')}",
        f"- Аккредитация: {dannye.get('sostoyanie_akkreditatsii', '')}",
        f"- Дата аккредитации: {dannye.get('data_akkreditatsii', '')}",
        f"- Срок действия: {dannye.get('srok_deystviya', '')}",
        f"- № свидетельства: {dannye.get('nomer_svidetelstva', '')}",
        f"- Адрес: {dannye.get('adres', '')}",
        f"- Сайт: {dannye.get('sayt', '')}",
        f"- Источник: {dannye.get('istochnik', 'Рособрнадзор')}",
    ]
    return "\n".join(stroki)


async def programmy_vuza(kontekst: Context, vuz: str, uroven: str = "") -> str:
    """Образовательные программы вуза.

    Аргументы:
        vuz: Название вуза.
        uroven: Уровень образования (необязательно).

    Возвращает:
        Список программ с кодами направлений.
    """
    await kontekst.info(f"Запрос программ вуза «{vuz}»...")
    rezultaty = await client.poisk_akreditovannyh_vuzov(nazvanie=vuz)
    if not rezultaty:
        return f"Вуз «{vuz}» не найден в реестре Рособрнадзора."

    dannye = rezultaty[0]
    stroki = [
        f"**{dannye.get('nazvanie', vuz)}**",
        f"- Аккредитация: {dannye.get('sostoyanie_akkreditatsii', '')}",
        f"- № свидетельства: {dannye.get('nomer_svidetelstva', '')}",
        "",
        "Подробная информация об образовательных программах доступна на:",
        f"- {dannye.get('sayt', 'сайте вуза')}",
        "- Рособрнадзор: https://obrnadzor.gov.ru/ru/registry_accreditation",
    ]
    return "\n".join(stroki)


async def granty_i_isledovaniya(kontekst: Context, organizatsiya: str = "") -> str:
    """Научные гранты и исследования.

    Аргументы:
        organizatsiya: Организация-заявитель (необязательно).

    Возвращает:
        Список грантовых фондов и программ.
    """
    await kontekst.info("Запрос информации о грантах...")
    granty = await client.poluchit_granty(organizatsiya)
    if not granty:
        return "Гранты не найдены."
    stroki_tablitsy = []
    for grant in granty:
        summ = (
            formatirovat_chislo_ru(grant.get("summa_finansirovaniya", 0), 0)
            if grant.get("summa_finansirovaniya")
            else "—"
        )
        stroki_tablitsy.append(
            (
                grant.get("tip_granta", ""),
                grant.get("nazvanie", ""),
                grant.get("rukovoditel", ""),
                summ,
                grant.get("sostoyanie", ""),
            )
        )
    return tablitsa_v_markdown(
        ["Тип гранта", "Название", "Руководитель", "Сумма (₽)", "Статус"],
        stroki_tablitsy,
    )


async def reyting_vuzov(kontekst: Context, tip_reytinga: str = "", god: int = 2024) -> str:
    """Рейтинг высших учебных заведений.

    Аргументы:
        tip_reytinga: Тип рейтинга (необязательно).
        god: Год рейтинга.

    Возвращает:
        Таблица рейтинга вузов с баллами по категориям.
    """
    await kontekst.info(f"Запрос рейтинга вузов за {god} г....")
    reyting = await client.poluchit_reyting(tip_reytinga, god)
    if not reyting:
        return (
            f"Рейтинг вузов за {god} г. не получен.\n\n"
            f"Актуальные рейтинги доступны на:\n"
            f"- https://vuz.minobrnauki.gov.ru\n"
            f"- https://obrnadzor.gov.ru"
        )
    stroki_tablitsy = []
    for pozitsiya in reyting:
        stroki_tablitsy.append(
            (
                str(pozitsiya.get("mesto_v_reytinge", "")),
                pozitsiya.get("nazvanie", ""),
                formatirovat_chislo_ru(pozitsiya.get("ball", 0), 1)
                if pozitsiya.get("ball")
                else "—",
                pozitsiya.get("tip_reytinga", ""),
            )
        )
    return tablitsa_v_markdown(
        ["Место", "Вуз", "Балл", "Тип рейтинга"],
        stroki_tablitsy,
    )


async def aspirantura(kontekst: Context, organizatsiya: str = "") -> str:
    """Данные об аспирантах и докторантах.

    Аргументы:
        organizatsiya: Организация (необязательно).

    Возвращает:
        Сведения об аспирантах, направлениях и научных руководителях.
    """
    return (
        "**Данные об аспирантуре**\n\n"
        "Информация об аспирантах и докторантах доступна через:\n"
        "- ЕГИСУ науки: https://esu.minobrnauki.gov.ru\n"
        "- Рособрнадзор: https://obrnadzor.gov.ru\n"
        "- Мониторинг образования: https://vuz.minobrnauki.gov.ru\n\n"
        "Для получения данных по конкретной организации "
        "укажите ИНН через инструмент info_vuza."
    )


async def poisk_litsenziy(kontekst: Context, nazvanie: str = "", inn: str = "") -> str:
    """Поиск лицензий на образовательную деятельность.

    Аргументы:
        nazvanie: Название вуза (необязательно).
        inn: ИНН организации (необязательно).

    Возвращает:
        Список лицензий с номерами и статусами.
    """
    await kontekst.info("Запрос лицензий из реестра Рособрнадзора...")
    rezultaty = await client.poisk_litsenziy(nazvanie=nazvanie, inn=inn)
    if not rezultaty:
        return "Лицензии не найдены."
    stroki_tablitsy = []
    for rezultat in rezultaty:
        stroki_tablitsy.append(
            (
                rezultat.get("nomer_litsenzii", ""),
                rezultat.get("nazvanie", ""),
                rezultat.get("sostoyanie_litsenzii", ""),
                rezultat.get("srok_deystviya", ""),
            )
        )
    return tablitsa_v_markdown(
        ["№ лицензии", "Организация", "Статус", "Срок действия"],
        stroki_tablitsy,
    )
