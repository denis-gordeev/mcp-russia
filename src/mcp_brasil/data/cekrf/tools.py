"""Инструменты модуля ЦИК РФ.

Инструменты для работы с данными Центральной избирательной комиссии РФ.

Правила (ADR-001):
    - tools.py НЕ выполняет HTTP-запросы напрямую — делегирует client.py
    - Возвращает отформатированные строки для потребления LLM
"""

from __future__ import annotations

from fastmcp import Context

from mcp_brasil._shared.formatting import format_number_br, markdown_table

from . import client


async def tipy_vyborov(ctx: Context) -> str:
    """Получить список типов выборов в РФ.

    Включает: выборы Президента, Госдумы, губернаторов,
    муниципальные выборы, референдумы.

    Returns:
        Таблица с типами выборов.
    """
    await ctx.info("Запрос типов выборов ЦИК РФ...")
    tipy = await client.tipy_vyborov()

    rows = [(str(t.code), t.name) for t in tipy]
    header = "**Типы выборов в РФ**\n\n"
    return header + markdown_table(["Код", "Тип выборов"], rows)


async def subyekty_rf(ctx: Context) -> str:
    """Получить справочник субъектов Российской Федерации.

    Включает все 89 субъектов РФ (85 + 4 новых).

    Returns:
        Таблица с субъектами РФ.
    """
    await ctx.info("Запрос справочника субъектов РФ...")
    subyekty = await client.subyekty_rf()

    rows = [(s.code, s.name) for s in subyekty]
    header = f"**Субъекты Российской Федерации** — {len(rows)} субъектов\n\n"
    return header + markdown_table(["Код", "Субъект РФ"], rows)


async def dolzhnosti_federal(ctx: Context) -> str:
    """Получить список федеральных избирательных должностей.

    Включает: Президент РФ, депутат Госдумы (фед. округ),
    депутат Госдумы (одномандатный округ).

    Returns:
        Таблица с должностями.
    """
    await ctx.info("Запрос федеральных избирательных должностей...")
    dolzhnosti = await client.dolzhnosti_federal()

    rows = [(str(d.code), d.name, d.level) for d in dolzhnosti]
    header = "**Федеральные избирательные должности**\n\n"
    return header + markdown_table(["Код", "Должность", "Уровень"], rows)


async def partii_rf(ctx: Context) -> str:
    """Получить справочник основных политических партий РФ.

    Returns:
        Таблица с партиями.
    """
    await ctx.info("Запрос справочника партий РФ...")
    partii = await client.partii_rf()

    rows = [(p.short_name, p.name, p.color) for p in partii]
    header = f"**Политические партии РФ** — {len(rows)} партий\n\n"
    return header + markdown_table(["Краткое", "Наименование", "Цвет"], rows)


async def gody_vyborov(ctx: Context) -> str:
    """Получить список годов основных федеральных выборов.

    Returns:
        Список годов выборов.
    """
    await ctx.info("Запрос годов выборов...")
    gody = await client.gody_vyborov()

    lines = ["**Годы федеральных выборов в РФ**\n"]
    for god in gody:
        lines.append(f"- {god}")
    return "\n".join(lines)


async def poisk_kandidata(fio: str, ctx: Context, god: int | None = None) -> str:
    """Поиск кандидата по ФИО в базе ЦИК РФ.

    Args:
        fio: Фамилия, имя или отчество кандидата.
        god: Год выборов (необязательно).

    Returns:
        Результаты поиска.
    """
    await ctx.info(f"Поиск кандида: '{fio}'...")
    kandidaty = await client.poisk_kandidata(fio, god=god)

    if not kandidaty:
        return (
            f"Кандидат '{fio}' не найден в базе ЦИК РФ.\n\n"
            "Примечание: для полноценного поиска используйте ГАС «Выборы»: "
            "https://vybory.izbirkom.ru"
        )

    rows = [
        (k.id, k.fio, k.partia, k.dolzhnost, k.status)
        for k in kandidaty
    ]
    header = f"**Найдено кандидатов: {len(kandidaty)}**\n\n"
    return header + markdown_table(
        ["ID", "ФИО", "Партия", "Должность", "Статус"],
        rows,
    )


async def kandidat_podrobno(kandidat_id: str, ctx: Context, god: int | None = None) -> str:
    """Получить подробную информацию о кандидате.

    Включает: биографические данные, партийность,
    место работы, декларации о доходах и имуществе.

    Args:
        kandidat_id: ID кандидата в базе ЦИК.
        god: Год выборов (необязательно).

    Returns:
        Подробная карточка кандидата.
    """
    await ctx.info(f"Запрос подробной информации о кандидате {kandidat_id}...")
    kandidat = await client.kandidat_podrobno(kandidat_id, god=god)

    if not kandidat:
        return (
            f"Кандидат с ID '{kandidat_id}' не найден.\n\n"
            "Используйте poisk_kandidata() для поиска по ФИО."
        )

    lines = [
        f"**{kandidat.fio}**",
        f"- ID: {kandidat.id}",
        f"- Партия: {kandidat.partia or 'Самовыдвижение'}",
        f"- Должность: {kandidat.dolzhnost}",
        f"- Регион: {kandidat.region or 'Не указан'}",
        f"- Статус: {kandidat.status}",
    ]

    if kandidat.data_rozhdeniya:
        lines.append(f"- Дата рождения: {kandidat.data_rozhdeniya}")
    if kandidat.obrazovanie:
        lines.append(f"- Образование: {kandidat.obrazovanie}")
    if kandidat.mesto_raboty:
        lines.append(f"- Место работы: {kandidat.mesto_raboty}")
    if kandidat.dolzhnost_rabota:
        lines.append(f"- Должность: {kandidat.dolzhnost_rabota}")
    if kandidat.dokhod:
        lines.append(f"- Доход: {kandidat.dokhod}")

    lines.append("- Источник: Центральная избирательная комиссия РФ")
    return "\n".join(lines)


async def rezultaty_vyborov(
    ctx: Context,
    god: int,
    tip: int | None = None,
    region: str | None = None,
) -> str:
    """Получить результаты выборов.

    Args:
        god: Год выборов.
        tip: Код типа выборов (необязательно).
        region: Код субъекта РФ (необязательно).

    Returns:
        Таблица с результатами кандидатов.
    """
    await ctx.info(f"Запрос результатов выборов {god}...")
    rezultaty = await client.rezultaty_vyborov(god, tip=tip, region=region)

    if not rezultaty:
        return (
            f"Результаты выборов {god} года недоступны.\n\n"
            "Для получения результатов используйте ГАС «Выборы»: "
            "https://vybory.izbirkom.ru"
        )

    rows = [
        (
            r.fio,
            r.partia,
            format_number_br(r.golosov, 0),
            f"{format_number_br(r.procent, 2)}%",
            "✓" if r.izbrann else "",
        )
        for r in rezultaty
    ]
    header = f"**Результаты выборов {god} года**\n\n"
    return header + markdown_table(
        ["Кандидат", "Партия", "Голоса", "%", "Избран"],
        rows,
    )


async def yavka_i_itogi(
    ctx: Context,
    god: int,
    tip: int | None = None,
    region: str | None = None,
) -> str:
    """Получить данные о явке и итогах выборов.

    Args:
        god: Год выборов.
        tip: Код типа выборов (необязательно).
        region: Код субъекта РФ (необязательно).

    Returns:
        Сводка по явке и итогам.
    """
    await ctx.info(f"Запрос явки и итогов выборов {god}...")
    itogi = await client.yavka_i_itogi(god, tip=tip, region=region)

    lines = [
        f"**Итоги выборов {god} года**",
        f"- Всего избирателей: {format_number_br(itogi.get('vseh_izbirateley', 0), 0)}",
        f"- Проголосовало: {format_number_br(itogi.get('progalosovalo', 0), 0)}",
        f"- Явка: {format_number_br(itogi.get('yavka_procent', 0), 2)}%",
        "- Источник: ЦИК РФ / ГАС «Выборы»",
    ]
    return "\n".join(lines)
