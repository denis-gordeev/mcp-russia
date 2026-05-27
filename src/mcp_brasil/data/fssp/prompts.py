"""Prompts for the ФССП feature.

All prompts are in Russian with "(legacy — placeholder)" markers since
this is a placeholder module pending real API integration.
"""

from __future__ import annotations

import mcp.types as mt
from fastmcp.prompts import Message, PromptMessage, PromptResult


def analiz_dolzhnika() -> PromptResult:
    """Анализ задолженности должника. (legacy — placeholder)

    Используйте этот промпт для анализа исполнительных производств.
    """
    return PromptResult(
        messages=[
            Message(
                PromptMessage(
                    role="user",
                    content=mt.TextContent(
                        type="text",
                        text=(
                            "Выполните анализ задолженности:\n\n"
                            "1. Найдите все исполнительные производства по должнику.\n"
                            "2. Определите общую сумму задолженности.\n"
                            "3. Проверьте наличие ограничений (запрет на выезд и т.д.).\n"
                            "4. Уточните статус каждого производства.\n"
                            "5. Оцените риски и возможные действия.\n\n"
                            "Используйте tools: poisk_dolzhnika, ogranicheniya_dolzhnika, "
                            "info_proizvodstva, spisok_statusov_proizvodstva."
                        ),
                    ),
                )
            )
        ]
    )


def obzor_ispolnitelnogo_proizvodstva() -> PromptResult:
    """Обзор исполнительного производства по номеру. (legacy — placeholder)

    Используйте этот промпт для получения сведений о производстве.
    """
    return PromptResult(
        messages=[
            Message(
                PromptMessage(
                    role="user",
                    content=mt.TextContent(
                        type="text",
                        text=(
                            "Подготовьте обзор исполнительного производства:\n\n"
                            "1. Получите сведения о производстве по номеру.\n"
                            "2. Определите стороны (должник, взыскатель).\n"
                            "3. Уточните сумму взыскания и остаток долга.\n"
                            "4. Проверьте статус и основание возбуждения.\n"
                            "5. Определите отдел судебных приставов.\n\n"
                            "Используйте tools: info_proizvodstva, "
                            "spisok_vidov_proizvodstv, "
                            "spisok_osnovaniy_vozbuzhdeniya."
                        ),
                    ),
                )
            )
        ]
    )
