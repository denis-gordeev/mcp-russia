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
    stroki_tablitsy = [(v["kod"], v["nazvanie"]) for v in vidy]
    zagolovok = "**Виды чрезвычайных ситуаций**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Вид ЧС"], stroki_tablitsy)


async def spisok_klassov_chs(ctx: Context) -> str:
    """Получить список классов чрезвычайных ситуаций."""
    await ctx.info("Запрос списка классов ЧС...")
    klassy = client.poluchit_spisok_klassov_chs()
    stroki_tablitsy = [(k["kod"], k["nazvanie"]) for k in klassy]
    zagolovok = "**Классы чрезвычайных ситуаций**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Класс ЧС"], stroki_tablitsy)


async def spisok_vidov_pojarov(ctx: Context) -> str:
    """Получить список видов пожаров."""
    await ctx.info("Запрос списка видов пожаров...")
    vidy = client.poluchit_spisok_vidov_pozharov()
    stroki_tablitsy = [(v["kod"], v["nazvanie"]) for v in vidy]
    zagolovok = "**Виды пожаров**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Вид пожара"], stroki_tablitsy)


async def spisok_tipov_opasnosti(ctx: Context) -> str:
    """Получить список типов опасностей."""
    await ctx.info("Запрос списка типов опасностей...")
    tipy = client.poluchit_spisok_tipov_opasnosti()
    stroki_tablitsy = [(t["kod"], t["nazvanie"]) for t in tipy]
    zagolovok = "**Типы опасностей для предупреждений МЧС**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Тип опасности"], stroki_tablitsy)


async def statistika_pojarov(
    ctx: Context,
    subiekt: str = "",
    god: int = 0,
    vid_pozhara: str = "",
) -> str:
    """Статистика пожаров с данными из МЧС России.

    Аргументы:
        subiekt: Субъект РФ или федеральный округ (необязательно).
        god: Год (необязательно).
        vid_pozhara: Вид пожара (необязательно).

    Возвращает:
        Статистика пожаров.
    """
    await ctx.info("Запрос статистики пожаров...")
    pojarov_data = await client.statistika_pojarov(
        subiekt=subiekt,
        god=god,
        vid_pozhara=vid_pozhara,
    )
    if not pojarov_data:
        static = client.poluchit_statistiku_pozharov_staticheskie()
        if static:
            stroki = [
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
                stroki.append(
                    f"| {fo_name} | {fo_data['pojarov']:,} | {fo_data['pogibshikh']:,} |"
                )
            stroki.append("\nАктуальные данные доступны на: https://mchs.gov.ru/monitoring")
            return "\n".join(stroki)
        return (
            "Статистика пожаров не найдена.\n\n"
            "Актуальные данные доступны на: https://fires.ru и https://mchs.gov.ru"
        )

    stroki_tablitsy = [
        (
            p.get("nomer", ""),
            p.get("data", ""),
            p.get("subiekt", "")[:30],
            p.get("vid_pozhara", ""),
            str(p.get("pogibshikh", "")),
            str(p.get("postradavshikh", "")),
        )
        for p in pojarov_data
    ]
    zagolovok = f"**Статистика пожаров** — найдено: {len(pojarov_data)}\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["№", "Дата", "Регион", "Вид", "Погибших", "Пострадавших"],
        stroki_tablitsy,
    )


async def poisk_chs(
    ctx: Context,
    subiekt: str = "",
    vid_chs: str = "",
    klass_chs: str = "",
) -> str:
    """Поиск чрезвычайных ситуаций.

    Аргументы:
        subiekt: Регион (необязательно).
        vid_chs: Вид ЧС (необязательно).
        klass_chs: Класс ЧС (необязательно).

    Возвращает:
        Список чрезвычайных ситуаций.
    """
    await ctx.info("Поиск чрезвычайных ситуаций...")
    chs_data = await client.poisk_chs(
        subiekt=subiekt,
        vid_chs=vid_chs,
        klass_chs=klass_chs,
    )
    if not chs_data:
        filtry = []
        if subiekt:
            filtry.append(f"регион: {subiekt}")
        if vid_chs:
            filtry.append(f"вид: {vid_chs}")
        if klass_chs:
            filtry.append(f"класс: {klass_chs}")
        tekst_filtra = f" ({', '.join(filtry)})" if filtry else ""
        return (
            f"Чрезвычайные ситуации{tekst_filtra} не найдены.\n\n"
            f"Мониторинг ЧС доступен на: https://mchs.gov.ru/monitoring"
        )
    stroki_tablitsy = [
        (
            c.get("nomer", ""),
            c.get("vid_chs", ""),
            c.get("klass_chs", ""),
            c.get("data_vozniknoveniya", ""),
            c.get("subiekt", "")[:30],
            str(c.get("pogibshikh", "")),
            str(c.get("postradavshikh", "")),
        )
        for c in chs_data
    ]
    zagolovok = f"**Чрезвычайные ситуации** — найдено: {len(chs_data)}\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["№", "Вид", "Класс", "Дата", "Регион", "Погибших", "Пострадавших"],
        stroki_tablitsy,
    )


async def radiatsionnyy_monitoring(
    ctx: Context,
    subiekt: str = "",
) -> str:
    """Данные радиационного мониторинга МЧС России.

    Аргументы:
        subiekt: Регион (необязательно).

    Возвращает:
        Данные радиационного мониторинга.
    """
    await ctx.info("Запрос данных радиационного мониторинга...")
    monitoring_data = await client.radiatsionnyy_monitoring(subiekt=subiekt)
    if not monitoring_data:
        return (
            "Данные радиационного мониторинга не найдены.\n\n"
            "Актуальные данные доступны на: https://mchs.gov.ru/monitoring/radiation"
        )
    stroki_tablitsy = [
        (
            m.get("stantsiya", ""),
            m.get("subiekt", "")[:30],
            str(m.get("uroven_radiatsii", "")),
            m.get("edinitsa", ""),
            str(m.get("norma", "")),
            m.get("data_izmereniya", ""),
        )
        for m in monitoring_data
    ]
    zagolovok = f"**Радиационный мониторинг** — станций: {len(monitoring_data)}\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["Станция", "Регион", "Уровень", "Ед.", "Норма", "Дата"],
        stroki_tablitsy,
    )


async def gidrologicheskaya_obstanovka(
    ctx: Context,
    subiekt: str = "",
) -> str:
    """Данные гидрологической обстановки МЧС России.

    Аргументы:
        subiekt: Регион (необязательно).

    Возвращает:
        Данные гидрологической обстановки.
    """
    await ctx.info("Запрос данных гидрологической обстановки...")
    gidro_data = await client.gidrologicheskaya_obstanovka(subiekt=subiekt)
    if not gidro_data:
        return (
            "Данные гидрологической обстановки не найдены.\n\n"
            "Актуальные данные доступны на: https://mchs.gov.ru/monitoring/hydro"
        )
    stroki_tablitsy = [
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
    zagolovok = f"**Гидрологическая обстановка** — пунктов: {len(gidro_data)}\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["Река", "Пункт", "Уровень (см)", "Опасный (см)", "Тенденция", "Дата"],
        stroki_tablitsy,
    )


async def preduprezhdeniya_chs(
    ctx: Context,
    subiekt: str = "",
    tip_opasnosti: str = "",
) -> str:
    """Предупреждения о чрезвычайных ситуациях.

    Аргументы:
        subiekt: Регион (необязательно).
        tip_opasnosti: Тип опасности (необязательно).

    Возвращает:
        Список предупреждений о ЧС.
    """
    await ctx.info("Запрос предупреждений о ЧС...")
    preduprezhdeniya = await client.preduprezhdeniya_chs(
        subiekt=subiekt,
        tip_opasnosti=tip_opasnosti,
    )
    if not preduprezhdeniya:
        return (
            "Действующие предупреждения о ЧС не найдены.\n\n"
            "Мониторинг предупреждений: https://mchs.gov.ru/monitoring"
        )
    stroki_tablitsy = [
        (
            p.get("nomer", ""),
            p.get("tip_opasnosti", ""),
            p.get("subiekt", "")[:30],
            p.get("opisanie", "")[:60],
            p.get("data_nachala", ""),
            p.get("data_okonchaniya", ""),
        )
        for p in preduprezhdeniya
    ]
    zagolovok = f"**Предупреждения о ЧС** — активно: {len(preduprezhdeniya)}\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["№", "Тип опасности", "Регион", "Описание", "Начало", "Окончание"],
        stroki_tablitsy,
    )
