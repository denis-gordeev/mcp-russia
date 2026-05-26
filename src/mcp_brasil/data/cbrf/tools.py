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
from .constants import MOEDAS_POR_PAIS


async def cursos_atuais(ctx: Context) -> str:
    """Получить официальные курсы основных валют ЦБ РФ на сегодня.

    Возвращает курсы: доллар США, евро, китайский юань,
    фунт стерлингов, японская иена, швейцарский франк.

    Returns:
        Таблица с курсами валют.
    """
    await ctx.info("Запрос курсов основных валют ЦБ РФ...")
    moedas = await client.buscar_moedas_principais()

    if not moedas:
        return "Не удалось получить курсы валют ЦБ РФ."

    rows = []
    for m in moedas:
        change = ""
        if m.valor_anterior is not None and m.valor_anterior > 0:
            diff = m.valor - m.valor_anterior
            sinal = "+" if diff >= 0 else ""
            pct = (diff / m.valor_anterior) * 100
            change = f"{sinal}{format_number_br(diff, 4)} ({sinal}{format_number_br(pct, 2)}%)"
        else:
            change = "—"

        rows.append(
            (
                m.codigo,
                m.nome,
                str(m.nominal),
                format_number_br(m.valor, 4),
                change,
            )
        )

    header = "**Официальные курсы валют ЦБ РФ**\n\n"
    return header + markdown_table(
        ["Код", "Валюта", "Номинал", "Курс (₽)", "Изменение"],
        rows,
    )


async def consultar_moeda(codigo: str, ctx: Context) -> str:
    """Получить курс одной конкретной валюты ЦБ РФ.

    Доступные коды: USD, EUR, CNY, GBP, JPY, CHF, KZT, BYN и др.
    Используйте listar_moedas() для полного списка.

    Args:
        codigo: Код валюты (например, 'USD', 'EUR', 'CNY').

    Returns:
        Подробная информация о курсе валюты.
    """
    await ctx.info(f"Запрос курса {codigo}...")
    moeda = await client.buscar_moeda(codigo)

    if not moeda:
        return (
            f"Валюта '{codigo}' не найдена в справочнике ЦБ РФ.\n\n"
            f"Попробуйте один из основных: USD, EUR, CNY, GBP, JPY, CHF"
        )

    lines = [
        f"**{moeda.nome}** ({moeda.codigo})",
        f"- Номинал: {moeda.nominal}",
        f"- Курс: {format_number_br(moeda.valor, 4)} ₽",
    ]

    if moeda.valor_anterior is not None:
        diff = moeda.valor - moeda.valor_anterior
        sinal = "+" if diff >= 0 else ""
        pct = (diff / moeda.valor_anterior) * 100 if moeda.valor_anterior else 0
        lines.append(f"- Предыдущий: {format_number_br(moeda.valor_anterior, 4)} ₽")
        pct_str = f"{sinal}{format_number_br(pct, 2)}%"
        diff_str = f"{sinal}{format_number_br(diff, 4)}"
        lines.append(f"- Изменение: {diff_str} ({pct_str})")

    if moeda.data:
        lines.append(f"- Дата: {moeda.data}")

    lines.append("- Источник: Центральный банк Российской Федерации")
    return "\n".join(lines)


async def listar_moedas(ctx: Context) -> str:
    """Получить полный список валют, доступных в справочнике ЦБ РФ.

    Returns:
        Список всех доступных валют с кодами и названиями.
    """
    await ctx.info("Запрос списка валют ЦБ РФ...")
    result = await client.buscar_todas_moedas()
    valute_data = result.get("Valute", {})

    rows = []
    for code, entry in sorted(valute_data.items()):
        name = entry.get("Name", code)
        nominal = entry.get("Nominal", 1)
        value = entry.get("Value", 0)
        valor_unit = value / nominal if nominal else value
        rows.append((code, name, str(nominal), format_number_br(valor_unit, 4)))

    header = f"**Справочник валют ЦБ РФ** — {len(rows)} валют\n\n"
    return header + markdown_table(
        ["Код", "Валюта", "Номинал", "Курс (₽)"],
        rows,
    )


async def converter_moeda(
    moeda: str,
    quantidade: float,
    ctx: Context,
) -> str:
    """Конвертировать сумму из иностранной валюты в рубли по курсу ЦБ РФ.

    Args:
        moeda: Код валюты (USD, EUR, CNY и т.д.).
        quantidade: Сумма в иностранной валюте.

    Returns:
        Результат конвертации.
    """
    await ctx.info(f"Конвертация {quantidade} {moeda} в рубли...")
    dados = await client.buscar_moeda(moeda)

    if not dados:
        return f"Валюта '{moeda}' не найдена в справочнике ЦБ РФ."

    rubles = dados.valor * quantidade

    lines = [
        "**Конвертация валюты**",
        f"- Сумма: {format_number_br(quantidade, 2)} {dados.codigo} ({dados.nome})",
        f"- Курс ЦБ РФ: {format_number_br(dados.valor, 4)} ₽ за 1 {dados.codigo}",
        f"- Номинал: {dados.nominal}",
        f"- **Результат: {format_number_br(rubles, 2)} ₽**",
    ]

    if dados.data:
        lines.append(f"- Дата курса: {dados.data}")

    return "\n".join(lines)


async def comparar_moedas(codigos: list[str] | None = None, ctx: Context | None = None) -> str:
    """Сравнить курсы нескольких валют ЦБ РФ.

    Args:
        codigos: Коды валют для сравнения (например, ['USD', 'EUR', 'CNY']).
                 По умолчанию сравниваются USD, EUR, CNY.

    Returns:
        Сравнительная таблица курсов.
    """
    if not codigos:
        codigos = ["USD", "EUR", "CNY"]

    if len(codigos) > 10:
        return "Можно сравнить не более 10 валют одновременно."

    if ctx is not None:
        await ctx.info(f"Сравнение {len(codigos)} валют...")
    moedas = await client.buscar_moedas_varios(codigos)

    if not moedas:
        return "Не удалось получить данные для указанных валют."

    rows = []
    for m in sorted(moedas, key=lambda x: x.codigo):
        change = "—"
        if m.valor_anterior is not None and m.valor_anterior > 0:
            diff = m.valor - m.valor_anterior
            pct = (diff / m.valor_anterior) * 100
            sinal = "+" if pct >= 0 else ""
            change = f"{sinal}{format_number_br(pct, 2)}%"
        rows.append((m.codigo, m.nome, format_number_br(m.valor, 4), change))

    header = "**Сравнение курсов валют ЦБ РФ**\n\n"
    return header + markdown_table(
        ["Код", "Валюта", "Курс (₽)", "Изменение"],
        rows,
    )


async def cursos_por_pais(ctx: Context) -> str:
    """Получить курсы валют для основных стран-партнёров России.

    Returns:
        Таблица с курсами валют по странам.
    """
    await ctx.info("Запрос курсов валют по странам...")
    moedas = await client.buscar_moedas_varios(list(MOEDAS_POR_PAIS.values()))

    if not moedas:
        return "Не удалось получить данные."

    rows = []
    for m in sorted(moedas, key=lambda x: x.codigo):
        pais = next((p for p, c in MOEDAS_POR_PAIS.items() if c == m.codigo), m.codigo)
        rows.append((pais, m.codigo, format_number_br(m.valor, 4)))

    header = "**Курсы валют основных стран-партнёров России**\n\n"
    return header + markdown_table(
        ["Страна", "Код", "Курс (₽)"],
        rows,
    )
