"""Промпты модуля ЕИС Закупок."""

from __future__ import annotations

from fastmcp import Context


async def analiz_zakupki(context: str, ctx: Context) -> str:
    """Анализ конкретной закупки в ЕИС.

    Args:
        context: Контекст запроса (номер закупки или описание).

    Returns:
        Prompt template for procurement analysis.
    """
    return (
        f"Выполни анализ закупки в ЕИС.\n\n"
        f"Контекст: {context}\n\n"
        f"Инструкция:\n"
        f"1. Найди закупку через poisk_zakupok() или info_zakupki()\n"
        f"2. Определи закон (44-ФЗ или 223-ФЗ), способ определения поставщика\n"
        f"3. Проанализируй заказчика (info_zakazchika по ИНН)\n"
        f"4. Проверь начальную цену и сравни с рыночными\n"
        f"5. Оформи как аналитическую справку по закупке\n\n"
        f"Важно: обращай внимание на признаки ограничения конкуренции."
    )


async def obzor_zakupok(context: str, ctx: Context) -> str:
    """Обзор закупочной активности организации.

    Args:
        context: Контекст запроса (ИНН или название организации).

    Returns:
        Prompt template for procurement overview.
    """
    return (
        f"Подготовь обзор закупочной активности организации.\n\n"
        f"Контекст: {context}\n\n"
        f"Инструкция:\n"
        f"1. Определи организацию как заказчика или поставщика (по ИНН)\n"
        f"2. Получи info_zakazchika() или info_postavshchika()\n"
        f"3. Проанализируй объём и структуру закупок\n"
        f"4. Отметь ключевых контрагентов\n"
        f"5. Оформи как аналитический обзор\n\n"
        f"Важно: используй только данные из открытых источников ЕИС."
    )
