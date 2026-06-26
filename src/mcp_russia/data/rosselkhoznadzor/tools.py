"""Инструменты модуля Россельхознадзор.

Правила (ADR-001):
    - tools.py НЕ делает HTTP-запросы напрямую — делегирует client.py
    - Возвращает форматированные строки для LLM
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import tablitsa_v_markdown

from . import client


async def spisok_vidov_nadzora(ctx: Context) -> str:
    """Получить список видов надзора Россельхознадзора."""
    await ctx.info("Запрос списка видов надзора...")
    vidy = client.poluchit_spisok_vidov_nadzora()
    rows = [(v["kod"], v["nazvanie"]) for v in vidy]
    header = "**Виды надзора Россельхознадзора**\n\n"
    return header + tablitsa_v_markdown(["Код", "Вид надзора"], rows)


async def spisok_kategoriy_proverok(ctx: Context) -> str:
    """Получить список категорий проверок."""
    await ctx.info("Запрос списка категорий проверок...")
    kategorii = client.poluchit_spisok_kategoriy_proverok()
    rows = [(k["kod"], k["nazvanie"]) for k in kategorii]
    header = "**Категории проверок Россельхознадзора**\n\n"
    return header + tablitsa_v_markdown(["Код", "Категория"], rows)


async def spisok_vidov_narusheniy(ctx: Context) -> str:
    """Получить список видов нарушений."""
    await ctx.info("Запрос списка видов нарушений...")
    vidy = client.poluchit_spisok_vidov_narusheniy()
    rows = [(v["kod"], v["nazvanie"]) for v in vidy]
    header = "**Виды нарушений Россельхознадзора**\n\n"
    return header + tablitsa_v_markdown(["Код", "Вид нарушений"], rows)


async def spisok_tipov_produktsii(ctx: Context) -> str:
    """Получить список типов поднадзорной продукции."""
    await ctx.info("Запрос списка типов продукции...")
    tipy = client.poluchit_spisok_tipov_produktsii()
    rows = [(t["kod"], t["nazvanie"]) for t in tipy]
    header = "**Типы поднадзорной продукции**\n\n"
    return header + tablitsa_v_markdown(["Код", "Тип продукции"], rows)


async def poisk_proverok(
    ctx: Context,
    subiekt: str = "",
    vid_nadzora: str = "",
    tip_proverki: str = "",
) -> str:
    """Поиск проверок Россельхознадзора.

    Аргументы:
        subiekt: Регион (необязательно).
        vid_nadzora: Вид надзора (необязательно).
        tip_proverki: Тип проверки (необязательно).

    Возвращает:
        Список проверок.
    """
    await ctx.info("Поиск проверок Россельхознадзора...")
    proverki = await client.poisk_proverok(
        subiekt=subiekt,
        vid_nadzora=vid_nadzora,
        tip_proverki=tip_proverki,
    )
    if not proverki:
        static = client.poluchit_statistiku_rskhn_staticheskie()
        if static:
            lines = [
                "**Статистика проверок Россельхознадзора (2023, резервные данные)**\n",
                f"- Всего проверок: {static['vsego_proverok']:,}",
                f"- Выявлено нарушений: {static['narusheniy_vyyavleno']:,}",
                f"- Наложено штрафов: {static['shtrafov_nalozheno']:,}",
                f"- Сумма штрафов: {static['summa_shtrafov_mlrd_rub']} млрд руб.\n",
                "| Вид надзора | Проверок | Нарушений |",
                "|-------------|----------|-----------|",
            ]
            for vid, data in static["po_vidam"].items():
                vid_name = (
                    vid.replace("veterinarnyy", "Ветеринарный")
                    .replace("fitosanitarnyy", "Фитосанитарный")
                    .replace("zemelnyy", "Земельный")
                    .replace("karantin_rasteniy", "Карантин растений")
                    .replace("pestitsidy", "Пестициды")
                )
                lines.append(f"| {vid_name} | {data['proverok']:,} | {data['narusheniy']:,} |")
            lines.append("\nАктуальные данные доступны на: https://fsvps.gov.ru/inspections")
            return "\n".join(lines)
        return "Проверки не найдены.\n\nАктуальные данные доступны на: https://fsvps.gov.ru"

    rows = [
        (
            p.get("nomer", ""),
            p.get("vid_nadzora", ""),
            p.get("data_provedeniya", ""),
            p.get("subiekt", "")[:30],
            p.get("status", ""),
            str(p.get("narusheniya", "")),
        )
        for p in proverki
    ]
    header = f"**Проверки Россельхознадзора** — найдено: {len(proverki)}\n\n"
    return header + tablitsa_v_markdown(
        ["№", "Вид надзора", "Дата", "Регион", "Статус", "Нарушений"],
        rows,
    )


async def poisk_karantinnykh_obektov(
    ctx: Context,
    subiekt: str = "",
    tip: str = "",
) -> str:
    """Поиск карантинных объектов.

    Аргументы:
        subiekt: Регион (необязательно).
        tip: Тип объекта (необязательно).

    Возвращает:
        Список карантинных объектов.
    """
    await ctx.info("Поиск карантинных объектов...")
    obekty = await client.poisk_karantinnykh_obektov(subiekt=subiekt, tip=tip)
    if not obekty:
        return (
            "Карантинные объекты не найдены.\n\n"
            "Актуальные данные доступны на: https://fsvps.gov.ru/quarantine"
        )
    rows = [
        (
            o.get("nazvanie", ""),
            o.get("tip", ""),
            o.get("subiekt", "")[:30],
            o.get("status_karantina", ""),
            o.get("data_vvedeniya", ""),
        )
        for o in obekty
    ]
    header = f"**Карантинные объекты** — найдено: {len(obekty)}\n\n"
    return header + tablitsa_v_markdown(
        ["Название", "Тип", "Регион", "Статус", "Дата введения"],
        rows,
    )


async def poisk_registratsiy_produktsii(
    ctx: Context,
    tip_produktsii: str = "",
    proizvoditel: str = "",
) -> str:
    """Поиск зарегистрированной продукции.

    Аргументы:
        tip_produktsii: Тип продукции (необязательно).
        proizvoditel: Производитель (необязательно).

    Возвращает:
        Список зарегистрированной продукции.
    """
    await ctx.info("Поиск зарегистрированной продукции...")
    registratsii = await client.poisk_registratsiy_produktsii(
        tip_produktsii=tip_produktsii,
        proizvoditel=proizvoditel,
    )
    if not registratsii:
        return (
            "Зарегистрированная продукция не найдена.\n\n"
            "Реестр доступен на: https://fsvps.gov.ru/registrations"
        )
    rows = [
        (
            r.get("nomer", ""),
            r.get("naimenovanie", "")[:40],
            r.get("proizvoditel", "")[:25],
            r.get("tip_produktsii", ""),
            r.get("sostoyanie", ""),
        )
        for r in registratsii
    ]
    header = f"**Зарегистрированная продукция** — найдено: {len(registratsii)}\n\n"
    return header + tablitsa_v_markdown(
        ["№", "Наименование", "Производитель", "Тип", "Статус"],
        rows,
    )


async def veterinarsnye_sertifikaty(
    ctx: Context,
    subiekt: str = "",
    tip_produktsii: str = "",
) -> str:
    """Поиск ветеринарных сертификатов.

    Аргументы:
        subiekt: Регион отправки (необязательно).
        tip_produktsii: Тип продукции (необязательно).

    Возвращает:
        Список ветеринарных сертификатов.
    """
    await ctx.info("Поиск ветеринарных сертификатов...")
    sertifikaty = await client.veterinarsnye_sertifikaty(
        subiekt=subiekt,
        tip_produktsii=tip_produktsii,
    )
    if not sertifikaty:
        return (
            "Ветеринарные сертификаты не найдены.\n\n"
            "ФГИС «Меркурий» доступна на: https://vgis.fsvps.ru"
        )
    rows = [
        (
            s.get("nomer", ""),
            s.get("tip_produktsii", ""),
            s.get("region_otpravki", "")[:30],
            s.get("data_oformleniya", ""),
            s.get("sostoyanie", ""),
        )
        for s in sertifikaty
    ]
    header = f"**Ветеринарные сертификаты** — найдено: {len(sertifikaty)}\n\n"
    return header + tablitsa_v_markdown(
        ["№", "Тип продукции", "Регион отправки", "Дата", "Статус"],
        rows,
    )


async def preduprezhdeniya_karantina(
    ctx: Context,
    subiekt: str = "",
) -> str:
    """Предупреждения о карантинных ограничениях.

    Аргументы:
        subiekt: Регион (необязательно).

    Возвращает:
        Список предупреждений.
    """
    await ctx.info("Запрос предупреждений о карантине...")
    preduprezhdeniya = await client.preduprezhdeniya_karantina(subiekt=subiekt)
    if not preduprezhdeniya:
        return (
            "Действующие карантинные ограничения не найдены.\n\n"
            "Мониторинг карантинов: https://fsvps.gov.ru/quarantine"
        )
    rows = [
        (
            p.get("nomer", ""),
            p.get("tip_karantina", ""),
            p.get("subiekt", "")[:30],
            p.get("opisanie", "")[:60],
            p.get("data_nachala", ""),
            p.get("data_okonchaniya", ""),
        )
        for p in preduprezhdeniya
    ]
    header = f"**Предупреждения о карантине** — активно: {len(preduprezhdeniya)}\n\n"
    return header + tablitsa_v_markdown(
        ["№", "Тип", "Регион", "Описание", "Начало", "Окончание"],
        rows,
    )
