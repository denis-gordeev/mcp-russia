"""Инструменты модуля Россельхознадзор.

Правила (ADR-001):
    - tools.py НЕ делает HTTP-запросы напрямую — делегирует client.py
    - Возвращает форматированные строки для LLM
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import tablitsa_v_markdown

from . import client


async def spisok_vidov_nadzora(kontekst: Context) -> str:
    """Получить список видов надзора Россельхознадзора."""
    await kontekst.info("Запрос списка видов надзора...")
    vidy = client.poluchit_spisok_vidov_nadzora()
    stroki_tablitsy = [(vid["kod"], vid["nazvanie"]) for vid in vidy]
    zagolovok = "**Виды надзора Россельхознадзора**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Вид надзора"], stroki_tablitsy)


async def spisok_kategoriy_proverok(kontekst: Context) -> str:
    """Получить список категорий проверок."""
    await kontekst.info("Запрос списка категорий проверок...")
    kategorii = client.poluchit_spisok_kategoriy_proverok()
    stroki_tablitsy = [(kategoriya["kod"], kategoriya["nazvanie"]) for kategoriya in kategorii]
    zagolovok = "**Категории проверок Россельхознадзора**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Категория"], stroki_tablitsy)


async def spisok_vidov_narusheniy(kontekst: Context) -> str:
    """Получить список видов нарушений."""
    await kontekst.info("Запрос списка видов нарушений...")
    vidy = client.poluchit_spisok_vidov_narusheniy()
    stroki_tablitsy = [(vid["kod"], vid["nazvanie"]) for vid in vidy]
    zagolovok = "**Виды нарушений Россельхознадзора**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Вид нарушений"], stroki_tablitsy)


async def spisok_tipov_produktsii(kontekst: Context) -> str:
    """Получить список типов поднадзорной продукции."""
    await kontekst.info("Запрос списка типов продукции...")
    tipy = client.poluchit_spisok_tipov_produktsii()
    stroki_tablitsy = [(tip["kod"], tip["nazvanie"]) for tip in tipy]
    zagolovok = "**Типы поднадзорной продукции**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Тип продукции"], stroki_tablitsy)


async def poisk_proverok(
    kontekst: Context,
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
    await kontekst.info("Поиск проверок Россельхознадзора...")
    proverki = await client.poisk_proverok(
        subiekt=subiekt,
        vid_nadzora=vid_nadzora,
        tip_proverki=tip_proverki,
    )
    if not proverki:
        statika = client.poluchit_statistiku_rskhn_staticheskie()
        if statika:
            stroki = [
                "**Статистика проверок Россельхознадзора (2023, резервные данные)**\n",
                f"- Всего проверок: {statika['vsego_proverok']:,}",
                f"- Выявлено нарушений: {statika['narusheniy_vyyavleno']:,}",
                f"- Наложено штрафов: {statika['shtrafov_nalozheno']:,}",
                f"- Сумма штрафов: {statika['summa_shtrafov_mlrd_rub']} млрд руб.\n",
                "| Вид надзора | Проверок | Нарушений |",
                "|-------------|----------|-----------|",
            ]
            for vid, dannye in statika["po_vidam"].items():
                vid_nazvanie = (
                    vid.replace("veterinarnyy", "Ветеринарный")
                    .replace("fitosanitarnyy", "Фитосанитарный")
                    .replace("zemelnyy", "Земельный")
                    .replace("karantin_rasteniy", "Карантин растений")
                    .replace("pestitsidy", "Пестициды")
                )
                stroki.append(
                    f"| {vid_nazvanie} | {dannye['proverok']:,} | {dannye['narusheniy']:,} |"
                )
            stroki.append("\nАктуальные данные доступны на: https://fsvps.gov.ru/inspections")
            return "\n".join(stroki)
        return "Проверки не найдены.\n\nАктуальные данные доступны на: https://fsvps.gov.ru"

    stroki_tablitsy = [
        (
            proverka.get("nomer", ""),
            proverka.get("vid_nadzora", ""),
            proverka.get("data_provedeniya", ""),
            proverka.get("subiekt", "")[:30],
            proverka.get("sostoyanie", ""),
            str(proverka.get("narusheniya", "")),
        )
        for proverka in proverki
    ]
    zagolovok = f"**Проверки Россельхознадзора** — найдено: {len(proverki)}\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["№", "Вид надзора", "Дата", "Регион", "Статус", "Нарушений"],
        stroki_tablitsy,
    )


async def poisk_karantinnykh_obektov(
    kontekst: Context,
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
    await kontekst.info("Поиск карантинных объектов...")
    obekty = await client.poisk_karantinnykh_obektov(subiekt=subiekt, tip=tip)
    if not obekty:
        return (
            "Карантинные объекты не найдены.\n\n"
            "Актуальные данные доступны на: https://fsvps.gov.ru/quarantine"
        )
    stroki_tablitsy = [
        (
            obiekt.get("nazvanie", ""),
            obiekt.get("tip", ""),
            obiekt.get("subiekt", "")[:30],
            obiekt.get("status_karantina", ""),
            obiekt.get("data_vvedeniya", ""),
        )
        for obiekt in obekty
    ]
    zagolovok = f"**Карантинные объекты** — найдено: {len(obekty)}\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["Название", "Тип", "Регион", "Статус", "Дата введения"],
        stroki_tablitsy,
    )


async def poisk_registratsiy_produktsii(
    kontekst: Context,
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
    await kontekst.info("Поиск зарегистрированной продукции...")
    registratsii = await client.poisk_registratsiy_produktsii(
        tip_produktsii=tip_produktsii,
        proizvoditel=proizvoditel,
    )
    if not registratsii:
        return (
            "Зарегистрированная продукция не найдена.\n\n"
            "Реестр доступен на: https://fsvps.gov.ru/registrations"
        )
    stroki_tablitsy = [
        (
            registratsiya.get("nomer", ""),
            registratsiya.get("naimenovanie", "")[:40],
            registratsiya.get("proizvoditel", "")[:25],
            registratsiya.get("tip_produktsii", ""),
            registratsiya.get("sostoyanie", ""),
        )
        for registratsiya in registratsii
    ]
    zagolovok = f"**Зарегистрированная продукция** — найдено: {len(registratsii)}\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["№", "Наименование", "Производитель", "Тип", "Статус"],
        stroki_tablitsy,
    )


async def veterinarsnye_sertifikaty(
    kontekst: Context,
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
    await kontekst.info("Поиск ветеринарных сертификатов...")
    sertifikaty = await client.veterinarsnye_sertifikaty(
        subiekt=subiekt,
        tip_produktsii=tip_produktsii,
    )
    if not sertifikaty:
        return (
            "Ветеринарные сертификаты не найдены.\n\n"
            "ФГИС «Меркурий» доступна на: https://vgis.fsvps.ru"
        )
    stroki_tablitsy = [
        (
            sertifikat.get("nomer", ""),
            sertifikat.get("tip_produktsii", ""),
            sertifikat.get("region_otpravki", "")[:30],
            sertifikat.get("data_oformleniya", ""),
            sertifikat.get("sostoyanie", ""),
        )
        for sertifikat in sertifikaty
    ]
    zagolovok = f"**Ветеринарные сертификаты** — найдено: {len(sertifikaty)}\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["№", "Тип продукции", "Регион отправки", "Дата", "Статус"],
        stroki_tablitsy,
    )


async def preduprezhdeniya_karantina(
    kontekst: Context,
    subiekt: str = "",
) -> str:
    """Предупреждения о карантинных ограничениях.

    Аргументы:
        subiekt: Регион (необязательно).

    Возвращает:
        Список предупреждений.
    """
    await kontekst.info("Запрос предупреждений о карантине...")
    preduprezhdeniya = await client.preduprezhdeniya_karantina(subiekt=subiekt)
    if not preduprezhdeniya:
        return (
            "Действующие карантинные ограничения не найдены.\n\n"
            "Мониторинг карантинов: https://fsvps.gov.ru/quarantine"
        )
    stroki_tablitsy = [
        (
            preduprezhdenie.get("nomer", ""),
            preduprezhdenie.get("tip_karantina", ""),
            preduprezhdenie.get("subiekt", "")[:30],
            preduprezhdenie.get("opisanie", "")[:60],
            preduprezhdenie.get("data_nachala", ""),
            preduprezhdenie.get("data_okonchaniya", ""),
        )
        for preduprezhdenie in preduprezhdeniya
    ]
    zagolovok = f"**Предупреждения о карантине** — активно: {len(preduprezhdeniya)}\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["№", "Тип", "Регион", "Описание", "Начало", "Окончание"],
        stroki_tablitsy,
    )
