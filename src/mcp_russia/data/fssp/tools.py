"""Инструменты модуля ФССП."""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import tablitsa_v_markdown

from . import client
from .constants import (
    KODY_REGIONOV_FSSP,
    KategoriiDolzhnikov,
    Ogranicheniya,
    OsnovaniyaVozbuzhdeniya,
    StatusyProizvodstva,
    VidyIspolnitelnyhProizvodstv,
)

_ATTRIBUTION = "\n\n_Источник: ФССП России (fssp.gov.ru)_"


async def spisok_vidov_proizvodstv(ctx: Context) -> str:
    """Список видов исполнительных производств.

    Возвращает:
        Список видов (имущественные, неимущественные, штрафы и т.д.).
    """
    rows = [(v["kod"], v["nazvanie"]) for v in VidyIspolnitelnyhProizvodstv]
    return tablitsa_v_markdown(["Код", "Вид производства"], rows) + _ATTRIBUTION


async def spisok_statusov_proizvodstva(ctx: Context) -> str:
    """Список статусов исполнительного производства.

    Возвращает:
        Список статусов (возбуждено, в производстве, окончено и т.д.).
    """
    rows = [(s["kod"], s["nazvanie"]) for s in StatusyProizvodstva]
    return tablitsa_v_markdown(["Код", "Статус"], rows) + _ATTRIBUTION


async def spisok_ogranicheniy(ctx: Context) -> str:
    """Список видов ограничений, налагаемых судебными приставами.

    Возвращает:
        Список ограничений (выезд, управление транспортом, арест счетов и т.д.).
    """
    rows = [(o["kod"], o["nazvanie"]) for o in Ogranicheniya]
    return tablitsa_v_markdown(["Код", "Ограничение"], rows) + _ATTRIBUTION


async def spisok_kategoriy_dolzhnikov(ctx: Context) -> str:
    """Список категорий должников.

    Возвращает:
        Список категорий (физлицо, юрлицо, ИП).
    """
    rows = [(k["kod"], k["nazvanie"]) for k in KategoriiDolzhnikov]
    return tablitsa_v_markdown(["Код", "Категория"], rows) + _ATTRIBUTION


async def spisok_osnovaniy_vozbuzhdeniya(ctx: Context) -> str:
    """Список оснований возбуждения исполнительного производства.

    Возвращает:
        Список оснований (судебный акт, постановление ГИБДД и т.д.).
    """
    rows = [(o["kod"], o["nazvanie"]) for o in OsnovaniyaVozbuzhdeniya]
    return tablitsa_v_markdown(["Код", "Основание"], rows) + _ATTRIBUTION


async def spisok_regionov(ctx: Context) -> str:
    """Список кодов регионов для поиска в Банке данных ФССП.

    Возвращает:
        Список регионов и их кодов.
    """
    rows = [
        (str(code), name) for name, code in sorted(KODY_REGIONOV_FSSP.items(), key=lambda x: x[1])
    ]
    return tablitsa_v_markdown(["Код", "Регион"], rows) + _ATTRIBUTION


async def info_proizvodstva(ctx: Context, nomer: str) -> str:
    """Подробная информация об исполнительном производстве.

    Аргументы:
        nomer: Номер исполнительного производства
            (напр.: «12345/23/77001-ИП»).

    Возвращает:
        Сведения о производстве (должник, взыскатель, сумма, статус).
    """
    result = await client.info_proizvodstva(nomer)
    if not result:
        return f"Исполнительное производство № {nomer} не найдено." + _ATTRIBUTION

    lines = [
        f"**Исполнительное производство** № {result.get('nomer', nomer)}",
        f"- Должник: {result.get('dolzhnik', '')}",
        f"- Дата возбуждения: {result.get('data_vozbuzhdeniya', '')}",
        f"- Предмет исполнения: {result.get('subject', '')}",
        f"- Сума взыскания: {result.get('summa', '')}",
        f"- Отдел судебных приставов: {result.get('otdel_pristavov', '')}",
        f"- Судебный пристав: {result.get('pristav', '')}",
        f"- Дата окончания: {result.get('ip_end', '') or 'в производстве'}",
        f"- Основание: {result.get('osnovanie', '')}",
        f"- Регион: {result.get('subiekt_rf', '')}",
    ]
    return "\n".join(lines) + _ATTRIBUTION


async def poisk_dolzhnika(
    ctx: Context,
    fio: str,
    data_rozhdeniya: str = "",
    subiekt: str = "",
) -> str:
    """Поиск исполнительных производств по должнику.

    Аргументы:
        fio: ФИО должника или название организации.
        data_rozhdeniya: Дата рождения (необязательно, напр.: «01.01.1990»).
        subiekt: Код региона (необязательно, напр.: «77» — Москва).

    Возвращает:
        Список исполнительных производств с суммами и статусами.
    """
    results = await client.poisk_proizvodstv(fio, data_rozhdeniya, subiekt)
    if not results:
        return f"Исполнительные производства по «{fio}» не найдены." + _ATTRIBUTION

    rows = [
        (
            r.get("nomer", ""),
            r.get("dolzhnik", ""),
            r.get("subiekt", ""),
            r.get("summa", ""),
            r.get("otdel_pristavov", ""),
            r.get("okonchanie_ip", "") or "в производстве",
        )
        for r in results
    ]
    return (
        tablitsa_v_markdown(
            ["Номер", "Должник", "Предмет", "Сумма", "Отдел", "Статус"],
            rows,
        )
        + _ATTRIBUTION
    )


async def ogranicheniya_dolzhnika(
    ctx: Context,
    fio: str,
    data_rozhdeniya: str = "",
) -> str:
    """Ограничения, наложенные на должника.

    Аргументы:
        fio: ФИО должника или название организации.
        data_rozhdeniya: Дата рождения (необязательно, напр.: «01.01.1990»).

    Возвращает:
        Список ограничений (запрет на выезд, арест счетов и т.д.).
    """
    results = await client.ogranicheniya_dolzhnika(fio, data_rozhdeniya)
    if not results:
        return f"Ограничения по «{fio}» не найдены." + _ATTRIBUTION

    rows = [
        (
            r.get("nomer", ""),
            r.get("dolzhnik", ""),
            r.get("subiekt", ""),
            r.get("okonchanie_ip", "") or "действует",
        )
        for r in results
    ]
    return (
        tablitsa_v_markdown(
            ["Номер ИП", "Должник", "Ограничение", "Статус"],
            rows,
        )
        + _ATTRIBUTION
    )


async def rozysk_dolzhnika(ctx: Context, fio: str) -> str:
    """Сведения о розыске должника или имущества.

    Аргументы:
        fio: ФИО разыскиваемого лица.

    Возвращает:
        Сведения о розыске (тип, основание, кто объявил).
    """
    results = await client.rozysk_dolzhnika(fio)
    if not results:
        return f"Сведения о розыске по «{fio}» не найдены." + _ATTRIBUTION

    rows = [
        (
            r.get("nomer", ""),
            r.get("dolzhnik", ""),
            r.get("subiekt", ""),
            r.get("otdel_pristavov", ""),
        )
        for r in results
    ]
    return (
        tablitsa_v_markdown(
            ["Номер ИП", "Должник", "Предмет розыска", "Отдел"],
            rows,
        )
        + _ATTRIBUTION
    )
