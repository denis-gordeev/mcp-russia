"""Промпты модуля ФНС."""

from __future__ import annotations

import mcp.types as mt
from fastmcp.prompts import Message, PromptMessage, PromptResult


def analiz_nalogoplatelshchika() -> PromptResult:
    """Анализ налогоплательщика по ИНН.

    Используйте этот промпт для анализа организации или ИП по ИНН.
    """
    return PromptResult(
        messages=[
            Message(
                PromptMessage(
                    role="user",
                    content=mt.TextContent(
                        type="text",
                        text=(
                            "Выполните анализ налогоплательщика по ИНН:\n\n"
                            "1. Получите сведения из ЕГРЮЛ/ЕГРИП.\n"
                            "2. Проверьте статус организации (действующая/ликвидирована).\n"
                            "3. Определите режим налогообложения.\n"
                            "4. Проверьте наличие налоговых проверок.\n"
                            "5. Оцените налоговую нагрузку и задолженность.\n\n"
                            "Используйте tools: info_organizatsii, info_ip, "
                            "proverki_organizatsii, nalogovye_nachisleniya."
                        ),
                    ),
                )
            )
        ]
    )


def obzor_rezhimov_nalogooblozheniya() -> PromptResult:
    """Обзор режимов налогообложения для бизнеса.

    Используйте этот промпт для выбора оптимального режима налогообложения.
    """
    return PromptResult(
        messages=[
            Message(
                PromptMessage(
                    role="user",
                    content=mt.TextContent(
                        type="text",
                        text=(
                            "Подготовьте обзор режимов налогообложения:\n\n"
                            "1. Перечислите все доступные режимы.\n"
                            "2. Для каждого режима укажите ставки и условия применения.\n"
                            "3. Сравните налоговую нагрузку по режимам.\n"
                            "4. Укажите ограничения по видам деятельности.\n"
                            "5. Дайте рекомендации по выбору режима.\n\n"
                            "Используйте tools: spisok_nalogovyh_rezhimov, "
                            "spisok_vidov_nalogov, "
                            "spisok_kategoriy_nalogoplatelshchikov."
                        ),
                    ),
                )
            )
        ]
    )
