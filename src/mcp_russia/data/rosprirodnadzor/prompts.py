"""Prompts for the Росприроднадзор feature."""

from __future__ import annotations

from fastmcp import Context


async def analiz_ekologicheskoy_proverki(context: str, ctx: Context) -> str:
    """Анализ экологической проверки Росприроднадзора.

    Args:
        context: Контекст запроса (например, "анализ проверки № 123").

    Returns:
        Prompt template for environmental inspection analysis.
    """
    return (
        f"Выполни анализ экологической проверки Росприроднадзора.\n\n"
        f"Контекст: {context}\n\n"
        f"Инструкция:\n"
        f"1. Получи данные о проверке через info_proverki()\n"
        f"2. Проанализируй вид надзора и выявленные нарушения\n"
        f"3. Изучи статус проверки\n"
        f"4. Оцени возможные экологические риски\n"
        f"5. Дай краткую характеристику результатов проверки\n\n"
        f"Важно: обращай внимание на вид надзора и количество выявленных нарушений."
    )


async def obzor_nedropolzovaniya(ctx: Context) -> str:
    """Обзор лицензий на пользование недрами.

    Returns:
        Prompt template for subsoil use overview.
    """
    return (
        "Подготовь обзор лицензий на пользование недрами.\n\n"
        "Инструкция:\n"
        "1. Получи список лицензий через poisk_litsenziy_nedra()\n"
        "2. Проанализируй виды лицензий и территории\n"
        "3. Отметь основных держателей лицензий\n"
        "4. Оцени сроки действия лицензий\n"
        "5. Оформи как аналитическую справку\n\n"
        "Важно: указывай территории и виды полезных ископаемых."
    )
