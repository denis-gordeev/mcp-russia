"""Tool functions for the CBRF (Central Bank of Russia) feature.

Tools for accessing CBR exchange rates, key rate, and economic indicators.

Rules (ADR-001):
    - tools.py NEVER makes HTTP directly — delegates to client.py
    - Returns formatted strings for LLM consumption
"""

from __future__ import annotations

from fastmcp import Context

from mcp_brasil._shared.formatting import format_number_br, markdown_table

from . import client
from .constants import VALYUTY_PO_STRANAM


async def tekushchie_kursy(ctx: Context) -> str:
    """Получить официальные курсы основных валют ЦБ РФ на сегодня.

    Возвращает курсы: доллар США, евро, китайский юань,
    фунт стерлингов, японская иена, швейцарский франк.

    Returns:
        Таблица с курсами валют.
    """
    await ctx.info("Запрос курсов основных валют ЦБ РФ...")
    valyuty = await client.poluchit_osnovnye_valyuty()

    if not valyuty:
        return "Не удалось получить курсы валют ЦБ РФ."

    rows = []
    for m in valyuty:
        change = ""
        if m.predydushchee_znachenie is not None and m.predydushchee_znachenie > 0:
            diff = m.znachenie - m.predydushchee_znachenie
            znak = "+" if diff >= 0 else ""
            pct = (diff / m.predydushchee_znachenie) * 100
            change = f"{znak}{format_number_br(diff, 4)} ({znak}{format_number_br(pct, 2)}%)"
        else:
            change = "—"

        rows.append(
            (
                m.kod,
                m.nazvanie,
                str(m.nominal),
                format_number_br(m.znachenie, 4),
                change,
            )
        )

    header = "**Официальные курсы валют ЦБ РФ**\n\n"
    return header + markdown_table(
        ["Код", "Валюта", "Номинал", "Курс (₽)", "Изменение"],
        rows,
    )


async def uznat_kurs_valyuty(kod: str, ctx: Context) -> str:
    """Получить курс одной конкретной валюты ЦБ РФ.

    Доступные коды: USD, EUR, CNY, GBP, JPY, CHF, KZT, BYN и др.
    Используйте spisok_valyut() для полного списка.

    Args:
        kod: Код валюты (например, 'USD', 'EUR', 'CNY').

    Returns:
        Подробная информация о курсе валюты.
    """
    await ctx.info(f"Запрос курса {kod}...")
    valyuta = await client.poluchit_valyutu(kod)

    if not valyuta:
        return (
            f"Валюта '{kod}' не найдена в справочнике ЦБ РФ.\n\n"
            f"Попробуйте один из основных: USD, EUR, CNY, GBP, JPY, CHF"
        )

    lines = [
        f"**{valyuta.nazvanie}** ({valyuta.kod})",
        f"- Номинал: {valyuta.nominal}",
        f"- Курс: {format_number_br(valyuta.znachenie, 4)} ₽",
    ]

    if valyuta.predydushchee_znachenie is not None:
        diff = valyuta.znachenie - valyuta.predydushchee_znachenie
        znak = "+" if diff >= 0 else ""
        prev = valyuta.predydushchee_znachenie
        pct = (diff / prev) * 100 if prev else 0
        lines.append(f"- Предыдущий: {format_number_br(valyuta.predydushchee_znachenie, 4)} ₽")
        pct_str = f"{znak}{format_number_br(pct, 2)}%"
        diff_str = f"{znak}{format_number_br(diff, 4)}"
        lines.append(f"- Изменение: {diff_str} ({pct_str})")

    if valyuta.data:
        lines.append(f"- Дата: {valyuta.data}")

    lines.append("- Источник: Центральный банк Российской Федерации")
    return "\n".join(lines)


async def spisok_valyut(ctx: Context) -> str:
    """Получить полный список валют, доступных в справочнике ЦБ РФ.

    Returns:
        Список всех доступных валют с кодами и названиями.
    """
    await ctx.info("Запрос списка валют ЦБ РФ...")
    result = await client.poluchit_vse_valyuty()
    valute_data = result.get("Valute", {})

    rows = []
    for code, entry in sorted(valute_data.items()):
        name = entry.get("Name", code)
        nominal = entry.get("Nominal", 1)
        value = entry.get("Value", 0)
        znachenie_za_edinitsu = value / nominal if nominal else value
        rows.append((code, name, str(nominal), format_number_br(znachenie_za_edinitsu, 4)))

    header = f"**Справочник валют ЦБ РФ** — {len(rows)} валют\n\n"
    return header + markdown_table(
        ["Код", "Валюта", "Номинал", "Курс (₽)"],
        rows,
    )


async def konvertirovat_valyutu(
    valyuta: str,
    kolichestvo: float,
    ctx: Context,
) -> str:
    """Конвертировать сумму из иностранной валюты в рубли по курсу ЦБ РФ.

    Args:
        valyuta: Код валюты (USD, EUR, CNY и т.д.).
        kolichestvo: Сумма в иностранной валюте.

    Returns:
        Результат конвертации.
    """
    await ctx.info(f"Конвертация {kolichestvo} {valyuta} в рубли...")
    dannye = await client.poluchit_valyutu(valyuta)

    if not dannye:
        return f"Валюта '{valyuta}' не найдена в справочнике ЦБ РФ."

    rubles = dannye.znachenie * kolichestvo

    lines = [
        "**Конвертация валюты**",
        f"- Сумма: {format_number_br(kolichestvo, 2)} {dannye.kod} ({dannye.nazvanie})",
        f"- Курс ЦБ РФ: {format_number_br(dannye.znachenie, 4)} ₽ за 1 {dannye.kod}",
        f"- Номинал: {dannye.nominal}",
        f"- **Результат: {format_number_br(rubles, 2)} ₽**",
    ]

    if dannye.data:
        lines.append(f"- Дата курса: {dannye.data}")

    return "\n".join(lines)


async def sravnit_valyuty(kody: list[str] | None = None, ctx: Context | None = None) -> str:
    """Сравнить курсы нескольких валют ЦБ РФ.

    Args:
        kody: Коды валют для сравнения (например, ['USD', 'EUR', 'CNY']).
              По умолчанию сравниваются USD, EUR, CNY.

    Returns:
        Сравнительная таблица курсов.
    """
    if not kody:
        kody = ["USD", "EUR", "CNY"]

    if len(kody) > 10:
        return "Можно сравнить не более 10 валют одновременно."

    if ctx is not None:
        await ctx.info(f"Сравнение {len(kody)} валют...")
    valyuty = await client.poluchit_valyuty_spisok(kody)

    if not valyuty:
        return "Не удалось получить данные для указанных валют."

    rows = []
    for m in sorted(valyuty, key=lambda x: x.kod):
        change = "—"
        if m.predydushchee_znachenie is not None and m.predydushchee_znachenie > 0:
            diff = m.znachenie - m.predydushchee_znachenie
            pct = (diff / m.predydushchee_znachenie) * 100
            znak = "+" if pct >= 0 else ""
            change = f"{znak}{format_number_br(pct, 2)}%"
        rows.append((m.kod, m.nazvanie, format_number_br(m.znachenie, 4), change))

    header = "**Сравнение курсов валют ЦБ РФ**\n\n"
    return header + markdown_table(
        ["Код", "Валюта", "Курс (₽)", "Изменение"],
        rows,
    )


async def kursy_po_stranam(ctx: Context) -> str:
    """Получить курсы валют для основных стран-партнёров России.

    Returns:
        Таблица с курсами валют по странам.
    """
    await ctx.info("Запрос курсов валют по странам...")
    valyuty = await client.poluchit_valyuty_spisok(list(VALYUTY_PO_STRANAM.values()))

    if not valyuty:
        return "Не удалось получить данные."

    rows = []
    for m in sorted(valyuty, key=lambda x: x.kod):
        strana = next((p for p, c in VALYUTY_PO_STRANAM.items() if c == m.kod), m.kod)
        rows.append((strana, m.kod, format_number_br(m.znachenie, 4)))

    header = "**Курсы валют основных стран-партнёров России**\n\n"
    return header + markdown_table(
        ["Страна", "Код", "Курс (₽)"],
        rows,
    )
