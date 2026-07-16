"""Инструменты модуля ЦИК РФ.

Инструменты для работы с данными Центральной избирательной комиссии РФ.
Источник: ЦИК РФ / ГАС «Выборы» (vybory.izbirkom.ru)

Правила (ADR-001):
    - tools.py НЕ выполняет HTTP-запросы напрямую — делегирует client.py
    - Возвращает отформатированные строки для потребления LLM
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import formatirovat_chislo_ru, tablitsa_v_markdown

from . import client

_ISTOCHNIK = "ЦИК РФ / ГАС «Выборы» (vybory.izbirkom.ru)"


async def tipy_vyborov(kontekst: Context) -> str:
    """Получить список типов выборов в РФ.

    Включает: выборы Президента, Госдумы, губернаторов,
    муниципальные выборы, референдумы.

    Возвращает:
        Таблица с типами выборов.
    """
    await kontekst.info("Запрос типов выборов ЦИК РФ...")
    tipy = await client.tipy_vyborov()

    stroki_tablitsy = [(str(tip.kod), tip.nazvanie) for tip in tipy]
    zagolovok = "**Типы выборов в РФ**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Тип выборов"], stroki_tablitsy)


async def subyekty_rf(kontekst: Context) -> str:
    """Получить справочник субъектов Российской Федерации.

    Включает все 89 субъектов РФ (85 + 4 новых).

    Возвращает:
        Таблица с субъектами РФ.
    """
    await kontekst.info("Запрос справочника субъектов РФ...")
    subyekty = await client.subyekty_rf()

    stroki_tablitsy = [(subiekt.kod, subiekt.nazvanie) for subiekt in subyekty]
    zagolovok = f"**Субъекты Российской Федерации** — {len(stroki_tablitsy)} субъектов\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Субъект РФ"], stroki_tablitsy)


async def dolzhnosti_federal(kontekst: Context) -> str:
    """Получить список федеральных избирательных должностей.

    Включает: Президент РФ, депутат Госдумы (фед. округ),
    депутат Госдумы (одномандатный округ).

    Возвращает:
        Таблица с должностями.
    """
    await kontekst.info("Запрос федеральных избирательных должностей...")
    dolzhnosti = await client.dolzhnosti_federal()

    stroki_tablitsy = [
        (str(dolzhnost.kod), dolzhnost.nazvanie, dolzhnost.uroven) for dolzhnost in dolzhnosti
    ]
    zagolovok = "**Федеральные избирательные должности**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Должность", "Уровень"], stroki_tablitsy)


async def partii_rf(kontekst: Context) -> str:
    """Получить справочник основных политических партий РФ.

    Возвращает:
        Таблица с партиями.
    """
    await kontekst.info("Запрос справочника партий РФ...")
    partii = await client.partii_rf()

    stroki_tablitsy = [
        (partiya.kratkoe_nazvanie, partiya.nazvanie, partiya.tsvet) for partiya in partii
    ]
    zagolovok = f"**Политические партии РФ** — {len(stroki_tablitsy)} партий\n\n"
    return zagolovok + tablitsa_v_markdown(["Краткое", "Наименование", "Цвет"], stroki_tablitsy)


async def gody_vyborov(kontekst: Context) -> str:
    """Получить список годов основных федеральных выборов.

    Возвращает:
        Список годов выборов.
    """
    await kontekst.info("Запрос годов выборов...")
    gody = await client.gody_vyborov()

    stroki = ["**Годы федеральных выборов в РФ**\n"]
    for god in gody:
        stroki.append(f"- {god}")
    return "\n".join(stroki)


async def spisok_vyborov(
    kontekst: Context,
    god: int | None = None,
    tip: int | None = None,
    subiekt: int | None = None,
) -> str:
    """Получить список выборов из ГАС «Выборы».

    Аргументы:
        god: Год выборов (необязательно).
        tip: Код типа выборов (необязательно).
        subiekt: Номер региона (необязательно).

    Возвращает:
        Таблица с выборами.
    """
    await kontekst.info("Запрос списка выборов...")
    vybory = await client.spisok_vyborov(god=god, tip=tip, subiekt=subiekt)

    if not vybory:
        return "Выборы не найдены. Уточните параметры запроса."

    stroki_tablitsy = [
        (
            vybory_item.get("nazvanie", ""),
            str(vybory_item.get("god", "")),
            vybory_item.get("data", ""),
            vybory_item.get("klyuch", ""),
        )
        for vybory_item in vybory
    ]
    zagolovok = f"**Найдено выборов: {len(vybory)}**\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["Наименование", "Год", "Дата", "Ключ"], stroki_tablitsy
    )


async def poisk_kandidata(fio: str, kontekst: Context, god: int | None = None) -> str:
    """Поиск кандидата по ФИО в базе ЦИК РФ.

    Аргументы:
        fio: Фамилия, имя или отчество кандидата.
        god: Год выборов (необязательно).

    Возвращает:
        Результаты поиска.
    """
    await kontekst.info(f"Поиск кандидата: '{fio}'...")
    kandidaty = await client.poisk_kandidata(fio, god=god)

    if not kandidaty:
        return f"Кандидат '{fio}' не найден в базе ЦИК РФ.\n\nИсточник: {_ISTOCHNIK}"

    stroki_tablitsy = [
        (
            kandidat.identifikator,
            kandidat.fio,
            kandidat.partia,
            kandidat.dolzhnost,
            kandidat.sostoyanie,
        )
        for kandidat in kandidaty
    ]
    zagolovok = f"**Найдено кандидатов: {len(kandidaty)}**\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["ID", "ФИО", "Партия", "Должность", "Статус"],
        stroki_tablitsy,
    )


async def kandidat_podrobno(
    kandidat_identifikator: str, kontekst: Context, god: int | None = None
) -> str:
    """Получить подробную информацию о кандидате.

    Включает: биографические данные, партийность,
    место работы, декларации о доходах и имуществе.

    Аргументы:
        kandidat_identifikator: ID кандидата в базе ЦИК.
        god: Год выборов (необязательно).

    Возвращает:
        Подробная карточка кандидата.
    """
    await kontekst.info(f"Запрос подробной информации о кандидате {kandidat_identifikator}...")
    kandidat = await client.kandidat_podrobno(kandidat_identifikator, god=god)

    if not kandidat:
        return (
            f"Кандидат с ID '{kandidat_identifikator}' не найден.\n\n"
            "Используйте poisk_kandidata() для поиска по ФИО."
        )

    stroki = [
        f"**{kandidat.fio}**",
        f"- ID: {kandidat.identifikator}",
        f"- Партия: {kandidat.partia or 'Самовыдвижение'}",
        f"- Должность: {kandidat.dolzhnost}",
        f"- Регион: {kandidat.subiekt or 'Не указан'}",
        f"- Статус: {kandidat.sostoyanie}",
    ]

    if kandidat.data_rozhdeniya:
        stroki.append(f"- Дата рождения: {kandidat.data_rozhdeniya}")
    if kandidat.obrazovanie:
        stroki.append(f"- Образование: {kandidat.obrazovanie}")
    if kandidat.mesto_raboty:
        stroki.append(f"- Место работы: {kandidat.mesto_raboty}")
    if kandidat.dolzhnost_rabota:
        stroki.append(f"- Должность: {kandidat.dolzhnost_rabota}")
    if kandidat.dokhod:
        stroki.append(f"- Доход: {kandidat.dokhod}")

    stroki.append(f"- Источник: {_ISTOCHNIK}")
    return "\n".join(stroki)


async def rezultaty_vyborov(
    kontekst: Context,
    god: int,
    tip: int | None = None,
    subiekt: str | None = None,
) -> str:
    """Получить результаты выборов.

    Аргументы:
        god: Год выборов.
        tip: Код типа выборов (необязательно).
        subiekt: Код субъекта РФ (необязательно).

    Возвращает:
        Таблица с результатами кандидатов.
    """
    await kontekst.info(f"Запрос результатов выборов {god}...")
    rezultaty = await client.rezultaty_vyborov(god, tip=tip, subiekt=subiekt)

    if not rezultaty:
        return f"Результаты выборов {god} года недоступны.\n\nИсточник: {_ISTOCHNIK}"

    stroki_tablitsy = [
        (
            rezultat.fio,
            rezultat.partia,
            formatirovat_chislo_ru(rezultat.golosov, 0),
            f"{formatirovat_chislo_ru(rezultat.procent, 2)}%",
            "✓" if rezultat.izbrann else "",
        )
        for rezultat in rezultaty
    ]
    zagolovok = f"**Результаты выборов {god} года**\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["Кандидат", "Партия", "Голоса", "%", "Избран"],
        stroki_tablitsy,
    )


async def yavka_i_itogi(
    kontekst: Context,
    god: int,
    tip: int | None = None,
    subiekt: str | None = None,
) -> str:
    """Получить данные о явке и итогах выборов.

    Аргументы:
        god: Год выборов.
        tip: Код типа выборов (необязательно).
        subiekt: Код субъекта РФ (необязательно).

    Возвращает:
        Сводка по явке и итогам.
    """
    await kontekst.info(f"Запрос явки и итогов выборов {god}...")
    itogi = await client.yavka_i_itogi(god, tip=tip, subiekt=subiekt)

    stroki = [
        f"**Итоги выборов {god} года**",
    ]
    if itogi.get("nazvanie"):
        stroki.append(f"- Выборы: {itogi['nazvanie']}")
    if itogi.get("data"):
        stroki.append(f"- Дата: {itogi['data']}")

    stroki.extend(
        [
            f"- Всего избирателей: {formatirovat_chislo_ru(itogi.get('vseh_izbirateley', 0), 0)}",
            f"- Проголосовало: {formatirovat_chislo_ru(itogi.get('progalosovalo', 0), 0)}",
            f"- Явка: {formatirovat_chislo_ru(itogi.get('yavka_procent', 0), 2)}%",
            f"- Действительных бюллетеней: {formatirovat_chislo_ru(itogi.get('deystvitelnykh_byulleteney', 0), 0)}",
            f"- Недействительных бюллетеней: {formatirovat_chislo_ru(itogi.get('nedeystvitelnykh_byulleteney', 0), 0)}",
            f"- Источник: {_ISTOCHNIK}",
        ]
    )
    return "\n".join(stroki)
