"""Tools for the ГИБДД/МВД feature.

All tool docstrings are in Russian with "(legacy — placeholder)" markers since
this is a placeholder module pending real API integration.
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import format_number_ru, markdown_table

from . import client
from .constants import (
    KategoriiVoditelskihUdostovereniy,
    RegionyRegistratsii,
    StatusyShtrafov,
    TipyDTP,
    TipyTransportnykhSredstv,
    VidyNarusheniy,
)


async def spisok_tipov_ts(ctx: Context) -> str:
    """Список типов транспортных средств. (legacy — placeholder)

    Returns:
        Список типов ТС (легковой, грузовой, автобус, мотоцикл и т.д.).
    """
    rows = [(t["code"], t["name"]) for t in TipyTransportnykhSredstv]
    return markdown_table(["Код", "Тип ТС"], rows)


async def spisok_kategoriyy_vu(ctx: Context) -> str:
    """Список категорий водительских удостоверений. (legacy — placeholder)

    Returns:
        Список категорий ВУ (A, B, C, D, M и т.д.).
    """
    rows = [(k["code"], k["name"]) for k in KategoriiVoditelskihUdostovereniy]
    return markdown_table(["Категория", "Описание"], rows)


async def spisok_vidov_narusheniy(ctx: Context) -> str:
    """Список видов нарушений ПДД. (legacy — placeholder)

    Returns:
        Список нарушений (скорость, красный свет, пешеходы и т.д.).
    """
    rows = [(n["code"], n["name"]) for n in VidyNarusheniy]
    return markdown_table(["Код", "Вид нарушения"], rows)


async def spisok_statusov_shtrafov(ctx: Context) -> str:
    """Список статусов штрафов ГИБДД. (legacy — placeholder)

    Returns:
        Список статусов (не оплачен, оплачен, передан приставам и т.д.).
    """
    rows = [(s["code"], s["name"]) for s in StatusyShtrafov]
    return markdown_table(["Код", "Статус штрафа"], rows)


async def spisok_tipov_dtp(ctx: Context) -> str:
    """Список типов ДТП. (legacy — placeholder)

    Returns:
        Список типов ДТП (столкновение, налёт на пешехода и т.д.).
    """
    rows = [(t["code"], t["name"]) for t in TipyDTP]
    return markdown_table(["Код", "Тип ДТП"], rows)


async def spisok_regionov_registratsii(ctx: Context) -> str:
    """Список основных регионов регистрации ТС. (legacy — placeholder)

    Returns:
        Список регионов с кодами.
    """
    rows = [(r["code"], r["name"]) for r in RegionyRegistratsii]
    return markdown_table(["Код региона", "Регион"], rows)


async def info_ts(ctx: Context, vin: str) -> str:
    """Проверка транспортного средства по VIN. (legacy — placeholder)

    Args:
        vin: VIN-номер транспортного средства (17 символов).

    Returns:
        Сведения о ТС (марка, модель, год, мощность, регистрации).
    """
    c = client.GibddClient()
    data = c.poluchit_info_ts(vin)
    if not data:
        return f"Информация по VIN {vin} не найдена (API integration pending)."
    lines = [
        f"**Транспортное средство** (VIN: {vin})",
        f"- Марка/модель: {data.get('marka_model', '')}",
        f"- Год выпуска: {data.get('god_vypuska', '')}",
        f"- Тип: {data.get('tip_ts', '')}",
        f"- Мощность: {data.get('moshchnost_ls', '')} л.с.",
        f"- Объём: {data.get('obiem_sm3', '')} см³",
    ]
    return "\n".join(lines)


async def info_vu(ctx: Context, nomer_vu: str) -> str:
    """Проверка водительского удостоверения. (legacy — placeholder)

    Args:
        nomer_vu: Серия и номер ВУ (10 цифр, без пробелов).

    Returns:
        Сведения о ВУ (категория, срок, статус, ограничения).
    """
    c = client.GibddClient()
    data = c.poluchit_info_vu(nomer_vu)
    if not data:
        return f"Информация по ВУ {nomer_vu} не найдена (API integration pending)."
    lines = [
        f"**Водительское удостоверение** (№ {nomer_vu})",
        f"- Категория: {data.get('kategoriya', '')}",
        f"- Дата выдачи: {data.get('data_vydachi', '')}",
        f"- Срок действия: {data.get('srok_deystviya', '')}",
        f"- Статус: {data.get('status', '')}",
    ]
    return "\n".join(lines)


async def shtrafy_po_ts(ctx: Context, gos_nomer: str) -> str:
    """Штрафы ГИБДД по госномеру транспортного средства. (legacy — placeholder)

    Args:
        gos_nomer: Государственный регистрационный номер ТС (напр. «А123АА77»).

    Returns:
        Список штрафов с суммами, статьями КоАП и статусами оплаты.
    """
    c = client.GibddClient()
    shtrafy = c.poluchit_shtrafy_po_ts(gos_nomer)
    if not shtrafy:
        return f"Штрафы по госномеру {gos_nomer} не найдены (API integration pending)."
    rows = []
    for s in shtrafy:
        rows.append(
            (
                s.get("postanovlenie_nomer", ""),
                s.get("data_narusheniya", ""),
                s.get("opisanie_narusheniya", ""),
                format_number_ru(s.get("summa_shtrafa", 0), 0),
                s.get("status_oplaty", ""),
            )
        )
    return markdown_table(
        ["Постановление", "Дата", "Нарушение", "Сумма (₽)", "Статус"],
        rows,
    )


async def shtrafy_po_vu(ctx: Context, nomer_vu: str) -> str:
    """Штрафы ГИБДД по номеру водительского удостоверения. (legacy — placeholder)

    Args:
        nomer_vu: Серия и номер ВУ (10 цифр).

    Returns:
        Список штрафов с суммами и статусами.
    """
    c = client.GibddClient()
    shtrafy = c.poluchit_shtrafy_po_vu(nomer_vu)
    if not shtrafy:
        return f"Штрафы по ВУ {nomer_vu} не найдены (API integration pending)."
    rows = []
    for s in shtrafy:
        rows.append(
            (
                s.get("postanovlenie_nomer", ""),
                s.get("data_narusheniya", ""),
                s.get("opisanie_narusheniya", ""),
                format_number_ru(s.get("summa_shtrafa", 0), 0),
                s.get("status_oplaty", ""),
            )
        )
    return markdown_table(
        ["Постановление", "Дата", "Нарушение", "Сумма (₽)", "Статус"],
        rows,
    )


async def statistika_dtp(ctx: Context, region: str, god: int = 2024) -> str:
    """Статистика ДТП по региону. (legacy — placeholder)

    Args:
        region: Название субъекта РФ.
        god: Год статистики.

    Returns:
        Статистика ДТП: количество, погибшие, раненые, пешеходы, дети.
    """
    c = client.GibddClient()
    data = c.poluchit_statistiku_dtp(region, god)
    if not data:
        return f"Статистика ДТП по региону «{region}» за {god} год не найдена (API integration pending)."
    lines = [
        f"**Статистика ДТП** — {region}, {god} г.",
        f"- Всего ДТП: {format_number_ru(data.get('kolichestvo_dtp', 0), 0)}",
        f"- Погибшие: {format_number_ru(data.get('pogibshie', 0), 0)}",
        f"- Раненые: {format_number_ru(data.get('ranennye', 0), 0)}",
        f"- ДТП с пешеходами: {format_number_ru(data.get('dtp_s_peshchodami', 0), 0)}",
        f"- ДТП с участием детей: {format_number_ru(data.get('dtp_s_detmi', 0), 0)}",
        f"- ДТП по вине нетрезвых: {format_number_ru(data.get('alco_gibdd', 0), 0)}",
    ]
    return "\n".join(lines)


async def istoriya_registraciy(ctx: Context, vin: str) -> str:
    """История регистрационных действий транспортного средства. (legacy — placeholder)

    Args:
        vin: VIN-номер транспортного средства (17 символов).

    Returns:
        Список регистрационных действий (постановка/снятие с учёта, смена собственника).
    """
    c = client.GibddClient()
    records = c.poluchit_istoriyu_registraciy(vin)
    if not records:
        return f"История регистраций по VIN {vin} не найдена (API integration pending)."
    rows = []
    for r in records:
        rows.append(
            (
                r.get("data_deystviya", ""),
                r.get("tip_deystviya", ""),
                r.get("region", ""),
            )
        )
    return markdown_table(["Дата", "Действие", "Регион"], rows)
