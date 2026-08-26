"""Инструменты модуля МЧС России.

Правила (CONTRIBUTING.md):
    - tools.py НЕ делает HTTP-запросы напрямую — делегирует client.py
    - Возвращает форматированные строки для LLM
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import tablitsa_v_markdown

from . import client


async def spisok_vidov_chs(kontekst: Context) -> str:
    """Получить список видов чрезвычайных ситуаций."""
    await kontekst.info("Запрос списка видов ЧС...")
    vidy = client.poluchit_spisok_vidov_chs()
    stroki_tablitsy = [(vid["kod"], vid["nazvanie"]) for vid in vidy]
    zagolovok = "**Виды чрезвычайных ситуаций**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Вид ЧС"], stroki_tablitsy)


async def spisok_klassov_chs(kontekst: Context) -> str:
    """Получить список классов чрезвычайных ситуаций."""
    await kontekst.info("Запрос списка классов ЧС...")
    klassy = client.poluchit_spisok_klassov_chs()
    stroki_tablitsy = [(klass["kod"], klass["nazvanie"]) for klass in klassy]
    zagolovok = "**Классы чрезвычайных ситуаций**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Класс ЧС"], stroki_tablitsy)


async def spisok_vidov_pojarov(kontekst: Context) -> str:
    """Получить список видов пожаров."""
    await kontekst.info("Запрос списка видов пожаров...")
    vidy = client.poluchit_spisok_vidov_pozharov()
    stroki_tablitsy = [(vid["kod"], vid["nazvanie"]) for vid in vidy]
    zagolovok = "**Виды пожаров**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Вид пожара"], stroki_tablitsy)


async def spisok_tipov_opasnosti(kontekst: Context) -> str:
    """Получить список типов опасностей."""
    await kontekst.info("Запрос списка типов опасностей...")
    tipy = client.poluchit_spisok_tipov_opasnosti()
    stroki_tablitsy = [(tip["kod"], tip["nazvanie"]) for tip in tipy]
    zagolovok = "**Типы опасностей для предупреждений МЧС**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Тип опасности"], stroki_tablitsy)


async def statistika_pojarov(
    kontekst: Context,
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
    await kontekst.info("Запрос статистики пожаров...")
    pojarov_dannye = await client.statistika_pojarov(
        subiekt=subiekt,
        god=god,
        vid_pozhara=vid_pozhara,
    )
    if not pojarov_dannye:
        statika = client.poluchit_statistiku_pozharov_staticheskie()
        if statika:
            stroki = [
                "**Статистика пожаров в РФ (2023, резервные данные)**\n",
                f"- Всего пожаров: {statika['vsego_pojarov']:,}",
                f"- Погибших: {statika['pogibshikh']:,}",
                f"- Пострадавших: {statika['postradavshikh']:,}",
                f"- Ущерб: {statika['usherb_mlrd_rub']} млрд руб.\n",
                "| ФО | Пожаров | Погибших |",
                "|----|---------|----------|",
            ]
            for fo_kod, fo_dannye in statika["po_fo"].items():
                fo_nazvanie = (
                    fo_kod.replace("ЦФО", "Центральный")
                    .replace("СЗФО", "Северо-Западный")
                    .replace("ЮФО", "Южный")
                    .replace("ПФО", "Приволжский")
                    .replace("УФО", "Уральский")
                    .replace("СФО", "Сибирский")
                    .replace("ДФО", "Дальневосточный")
                )
                stroki.append(
                    f"| {fo_nazvanie} | {fo_dannye['pojarov']:,} | {fo_dannye['pogibshikh']:,} |"
                )
            stroki.append("\nАктуальные данные доступны на: https://mchs.gov.ru/monitoring")
            return "\n".join(stroki)
        return (
            "Статистика пожаров не найдена.\n\n"
            "Актуальные данные доступны на: https://fires.ru и https://mchs.gov.ru"
        )

    stroki_tablitsy = [
        (
            pozhar.get("nomer", ""),
            pozhar.get("data", ""),
            pozhar.get("subiekt", "")[:30],
            pozhar.get("vid_pozhara", ""),
            str(pozhar.get("pogibshikh", "")),
            str(pozhar.get("postradavshikh", "")),
        )
        for pozhar in pojarov_dannye
    ]
    zagolovok = f"**Статистика пожаров** — найдено: {len(pojarov_dannye)}\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["№", "Дата", "Регион", "Вид", "Погибших", "Пострадавших"],
        stroki_tablitsy,
    )


async def poisk_chs(
    kontekst: Context,
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
    await kontekst.info("Поиск чрезвычайных ситуаций...")
    chs_dannye = await client.poisk_chs(
        subiekt=subiekt,
        vid_chs=vid_chs,
        klass_chs=klass_chs,
    )
    if not chs_dannye:
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
            chs.get("nomer", ""),
            chs.get("vid_chs", ""),
            chs.get("klass_chs", ""),
            chs.get("data_vozniknoveniya", ""),
            chs.get("subiekt", "")[:30],
            str(chs.get("pogibshikh", "")),
            str(chs.get("postradavshikh", "")),
        )
        for chs in chs_dannye
    ]
    zagolovok = f"**Чрезвычайные ситуации** — найдено: {len(chs_dannye)}\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["№", "Вид", "Класс", "Дата", "Регион", "Погибших", "Пострадавших"],
        stroki_tablitsy,
    )


async def radiatsionnyy_monitoring(
    kontekst: Context,
    subiekt: str = "",
) -> str:
    """Данные радиационного мониторинга МЧС России.

    Аргументы:
        subiekt: Регион (необязательно).

    Возвращает:
        Данные радиационного мониторинга.
    """
    await kontekst.info("Запрос данных радиационного мониторинга...")
    monitoring_dannye = await client.radiatsionnyy_monitoring(subiekt=subiekt)
    if not monitoring_dannye:
        return (
            "Данные радиационного мониторинга не найдены.\n\n"
            "Актуальные данные доступны на: https://mchs.gov.ru/monitoring/radiation"
        )
    stroki_tablitsy = [
        (
            monitoring.get("stantsiya", ""),
            monitoring.get("subiekt", "")[:30],
            str(monitoring.get("uroven_radiatsii", "")),
            monitoring.get("edinitsa_izmereniya", ""),
            str(monitoring.get("norma", "")),
            monitoring.get("data_izmereniya", ""),
        )
        for monitoring in monitoring_dannye
    ]
    zagolovok = f"**Радиационный мониторинг** — станций: {len(monitoring_dannye)}\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["Станция", "Регион", "Уровень", "Ед.", "Норма", "Дата"],
        stroki_tablitsy,
    )


async def gidrologicheskaya_obstanovka(
    kontekst: Context,
    subiekt: str = "",
) -> str:
    """Данные гидрологической обстановки МЧС России.

    Аргументы:
        subiekt: Регион (необязательно).

    Возвращает:
        Данные гидрологической обстановки.
    """
    await kontekst.info("Запрос данных гидрологической обстановки...")
    gidro_dannye = await client.gidrologicheskaya_obstanovka(subiekt=subiekt)
    if not gidro_dannye:
        return (
            "Данные гидрологической обстановки не найдены.\n\n"
            "Актуальные данные доступны на: https://mchs.gov.ru/monitoring/hydro"
        )
    stroki_tablitsy = [
        (
            gidro.get("reka", ""),
            gidro.get("punkt_nablyudeniya", "")[:30],
            str(gidro.get("uroven_vody", "")),
            str(gidro.get("opasnyy_uroven", "")) if gidro.get("opasnyy_uroven") else "—",
            gidro.get("tendentsiya", ""),
            gidro.get("data_izmereniya", ""),
        )
        for gidro in gidro_dannye
    ]
    zagolovok = f"**Гидрологическая обстановка** — пунктов: {len(gidro_dannye)}\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["Река", "Пункт", "Уровень (см)", "Опасный (см)", "Тенденция", "Дата"],
        stroki_tablitsy,
    )


async def preduprezhdeniya_chs(
    kontekst: Context,
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
    await kontekst.info("Запрос предупреждений о ЧС...")
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
            preduprezhdenie.get("nomer", ""),
            preduprezhdenie.get("tip_opasnosti", ""),
            preduprezhdenie.get("subiekt", "")[:30],
            preduprezhdenie.get("opisanie", "")[:60],
            preduprezhdenie.get("data_nachala", ""),
            preduprezhdenie.get("data_okonchaniya", ""),
        )
        for preduprezhdenie in preduprezhdeniya
    ]
    zagolovok = f"**Предупреждения о ЧС** — активно: {len(preduprezhdeniya)}\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["№", "Тип опасности", "Регион", "Описание", "Начало", "Окончание"],
        stroki_tablitsy,
    )
