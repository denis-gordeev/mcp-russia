"""Инструменты модуля МЧС России.

Правила (ADR-001):
    - tools.py НЕ делает HTTP-запросы напрямую — делегирует client.py
    - Возвращает форматированные строки для LLM
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import tablitsa_v_markdown

from . import client


async def spisok_vidov_chs(ctx: Context) -> str:
    """Получить список видов чрезвычайных ситуаций."""
    await ctx.info("Запрос списка видов ЧС...")
    vidy = client.poluchit_spisok_vidov_chs()
    rows = [(v["kod"], v["nazvanie"]) for v in vidy]
    header = "**Виды чрезвычайных ситуаций**\n\n"
    return header + tablitsa_v_markdown(["Код", "Вид ЧС"], rows)


async def spisok_klassov_chs(ctx: Context) -> str:
    """Получить список классов чрезвычайных ситуаций."""
    await ctx.info("Запрос списка классов ЧС...")
    klassy = client.poluchit_spisok_klassov_chs()
    rows = [(k["kod"], k["nazvanie"]) for k in klassy]
    header = "**Классы чрезвычайных ситуаций**\n\n"
    return header + tablitsa_v_markdown(["Код", "Класс ЧС"], rows)


async def spisok_vidov_pojarov(ctx: Context) -> str:
    """Получить список видов пожаров."""
    await ctx.info("Запрос списка видов пожаров...")
    vidy = client.poluchit_spisok_vidov_pozharov()
    rows = [(v["kod"], v["nazvanie"]) for v in vidy]
    header = "**Виды пожаров**\n\n"
    return header + tablitsa_v_markdown(["Код", "Вид пожара"], rows)


async def spisok_tipov_opasnosti(ctx: Context) -> str:
    """Получить список типов опасностей."""
    await ctx.info("Запрос списка типов опасностей...")
    tipy = client.poluchit_spisok_tipov_opasnosti()
    rows = [(t["kod"], t["nazvanie"]) for t in tipy]
    header = "**Типы опасностей для предупреждений МЧС**\n\n"
    return header + tablitsa_v_markdown(["Код", "Тип опасности"], rows)


async def statistika_pojarov(
    ctx: Context,
    region: str = "",
    god: int = 0,
    vid_pozhara: str = "",
) -> str:
    """Статистика пожаров с данными из МЧС России.

    Аргументы:
        region: Субъект РФ или федеральный округ (необязательно).
        god: Год (необязательно).
        vid_pozhara: Вид пожара (необязательно).

    Возвращает:
        Статистика пожаров.
    """
    await ctx.info("Запрос статистики пожаров...")
    pojarov_data = await client.statistika_pojarov(
        region=region,
        god=god,
        vid_pozhara=vid_pozhara,
    )
    if not pojarov_data:
        static = client.poluchit_statistiku_pozharov_staticheskie()
        if static:
            lines = [
                "**Статистика пожаров в РФ (2023, резервные данные)**\n",
                f"- Всего пожаров: {static['vsego_pojarov']:,}",
                f"- Погибших: {static['pogibshikh']:,}",
                f"- Пострадавших: {static['postradavshikh']:,}",
                f"- Ущерб: {static['usherb_mlrd_rub']} млрд руб.\n",
                "| ФО | Пожаров | Погибших |",
                "|----|---------|----------|",
            ]
            for fo_code, fo_data in static["po_fo"].items():
                fo_name = (
                    fo_code.replace("tcentralnyy", "Центральный")
                    .replace("severo-zapadnyy", "Северо-Западный")
                    .replace("yuzhnyy", "Южный")
                    .replace("privolzhskiy", "Приволжский")
                    .replace("uralskiy", "Уральский")
                    .replace("sibirskiy", "Сибирский")
                    .replace("dalnevostochnyy", "Дальневосточный")
                )
                lines.append(f"| {fo_name} | {fo_data['pojarov']:,} | {fo_data['pogibshikh']:,} |")
            lines.append("\nАктуальные данные доступны на: https://mchs.gov.ru/monitoring")
            return "\n".join(lines)
        return (
            "Статистика пожаров не найдена.\n\n"
            "Актуальные данные доступны на: https://fires.ru и https://mchs.gov.ru"
        )

    rows = [
        (
            p.get("nomer", ""),
            p.get("data", ""),
            p.get("region", "")[:30],
            p.get("vid_pozhara", ""),
            str(p.get("pogibshikh", "")),
            str(p.get("postradavshikh", "")),
        )
        for p in pojarov_data
    ]
    header = f"**Статистика пожаров** — найдено: {len(pojarov_data)}\n\n"
    return header + tablitsa_v_markdown(
        ["№", "Дата", "Регион", "Вид", "Погибших", "Пострадавших"],
        rows,
    )


async def poisk_chs(
    ctx: Context,
    region: str = "",
    vid_chs: str = "",
    klass_chs: str = "",
) -> str:
    """Поиск чрезвычайных ситуаций.

    Аргументы:
        region: Регион (необязательно).
        vid_chs: Вид ЧС (необязательно).
        klass_chs: Класс ЧС (необязательно).

    Возвращает:
        Список чрезвычайных ситуаций.
    """
    await ctx.info("Поиск чрезвычайных ситуаций...")
    chs_data = await client.poisk_chs(
        region=region,
        vid_chs=vid_chs,
        klass_chs=klass_chs,
    )
    if not chs_data:
        filters = []
        if region:
            filters.append(f"регион: {region}")
        if vid_chs:
            filters.append(f"вид: {vid_chs}")
        if klass_chs:
            filters.append(f"класс: {klass_chs}")
        filter_text = f" ({', '.join(filters)})" if filters else ""
        return (
            f"Чрезвычайные ситуации{filter_text} не найдены.\n\n"
            f"Мониторинг ЧС доступен на: https://mchs.gov.ru/monitoring"
        )
    rows = [
        (
            c.get("nomer", ""),
            c.get("vid_chs", ""),
            c.get("klass_chs", ""),
            c.get("data_vozniknoveniya", ""),
            c.get("region", "")[:30],
            str(c.get("pogibshikh", "")),
            str(c.get("postradavshikh", "")),
        )
        for c in chs_data
    ]
    header = f"**Чрезвычайные ситуации** — найдено: {len(chs_data)}\n\n"
    return header + tablitsa_v_markdown(
        ["№", "Вид", "Класс", "Дата", "Регион", "Погибших", "Пострадавших"],
        rows,
    )


async def radiatsionnyy_monitoring(
    ctx: Context,
    region: str = "",
) -> str:
    """Данные радиационного мониторинга МЧС России.

    Аргументы:
        region: Регион (необязательно).

    Возвращает:
        Данные радиационного мониторинга.
    """
    await ctx.info("Запрос данных радиационного мониторинга...")
    monitoring_data = await client.radiatsionnyy_monitoring(region=region)
    if not monitoring_data:
        return (
            "Данные радиационного мониторинга не найдены.\n\n"
            "Актуальные данные доступны на: https://mchs.gov.ru/monitoring/radiation"
        )
    rows = [
        (
            m.get("stantsiya", ""),
            m.get("region", "")[:30],
            str(m.get("uroven_radiatsii", "")),
            m.get("edinitsa", ""),
            str(m.get("norma", "")),
            m.get("data_izmereniya", ""),
        )
        for m in monitoring_data
    ]
    header = f"**Радиационный мониторинг** — станций: {len(monitoring_data)}\n\n"
    return header + tablitsa_v_markdown(
        ["Станция", "Регион", "Уровень", "Ед.", "Норма", "Дата"],
        rows,
    )


async def gidrologicheskaya_obstanovka(
    ctx: Context,
    region: str = "",
) -> str:
    """Данные гидрологической обстановки МЧС России.

    Аргументы:
        region: Регион (необязательно).

    Возвращает:
        Данные гидрологической обстановки.
    """
    await ctx.info("Запрос данных гидрологической обстановки...")
    gidro_data = await client.gidrologicheskaya_obstanovka(region=region)
    if not gidro_data:
        return (
            "Данные гидрологической обстановки не найдены.\n\n"
            "Актуальные данные доступны на: https://mchs.gov.ru/monitoring/hydro"
        )
    rows = [
        (
            g.get("reka", ""),
            g.get("punkt_nablyudeniya", "")[:30],
            str(g.get("uroven_vody", "")),
            str(g.get("opasnyy_uroven", "")) if g.get("opasnyy_uroven") else "—",
            g.get("tendentsiya", ""),
            g.get("data_izmereniya", ""),
        )
        for g in gidro_data
    ]
    header = f"**Гидрологическая обстановка** — пунктов: {len(gidro_data)}\n\n"
    return header + tablitsa_v_markdown(
        ["Река", "Пункт", "Уровень (см)", "Опасный (см)", "Тенденция", "Дата"],
        rows,
    )


async def preduprezhdeniya_chs(
    ctx: Context,
    region: str = "",
    tip_opasnosti: str = "",
) -> str:
    """Предупреждения о чрезвычайных ситуациях.

    Аргументы:
        region: Регион (необязательно).
        tip_opasnosti: Тип опасности (необязательно).

    Возвращает:
        Список предупреждений о ЧС.
    """
    await ctx.info("Запрос предупреждений о ЧС...")
    preduprezhdeniya = await client.preduprezhdeniya_chs(
        region=region,
        tip_opasnosti=tip_opasnosti,
    )
    if not preduprezhdeniya:
        return (
            "Действующие предупреждения о ЧС не найдены.\n\n"
            "Мониторинг предупреждений: https://mchs.gov.ru/monitoring"
        )
    rows = [
        (
            p.get("nomer", ""),
            p.get("tip_opasnosti", ""),
            p.get("region", "")[:30],
            p.get("opisanie", "")[:60],
            p.get("data_nachala", ""),
            p.get("data_okonchaniya", ""),
        )
        for p in preduprezhdeniya
    ]
    header = f"**Предупреждения о ЧС** — активно: {len(preduprezhdeniya)}\n\n"
    return header + tablitsa_v_markdown(
        ["№", "Тип опасности", "Регион", "Описание", "Начало", "Окончание"],
        rows,
    )
