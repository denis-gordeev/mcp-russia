"""Промпты модуля Минобрнауки."""

from __future__ import annotations

import mcp.types as mt
from fastmcp.prompts import Message, PromptMessage, PromptResult


def analiz_vuza() -> PromptResult:
    """Анализ высшего учебного заведения.

    Используйте этот промпт для комплексного анализа вуза.
    """
    return PromptResult(
        messages=[
            Message(
                PromptMessage(
                    role="user",
                    content=mt.TextContent(
                        type="text",
                        text=(
                            "Выполните анализ высшего учебного заведения:\n\n"
                            "1. Получите основные сведения о вузе.\n"
                            "2. Проверьте статус аккредитации.\n"
                            "3. Изучите образовательные программы.\n"
                            "4. Оцените позицию в рейтингах.\n"
                            "5. Проверьте научную деятельность и гранты.\n\n"
                            "Используйте tools: info_vuza, programmy_vuza, "
                            "reyting_vuzov, granty_i_isledovaniya."
                        ),
                    ),
                )
            )
        ]
    )


def obzor_nauchnyh_grantov() -> PromptResult:
    """Обзор научных грантов и возможностей финансирования.

    Используйте этот промпт для поиска грантов и анализа финансирования.
    """
    return PromptResult(
        messages=[
            Message(
                PromptMessage(
                    role="user",
                    content=mt.TextContent(
                        type="text",
                        text=(
                            "Подготовьте обзор научных грантов:\n\n"
                            "1. Перечислите типы доступных грантов.\n"
                            "2. Для каждого типа укажите фонд и условия.\n"
                            "3. Проверьте текущие конкурсы.\n"
                            "4. Сравните размеры финансирования.\n"
                            "5. Дайте рекомендации по выбору фонда.\n\n"
                            "Используйте tools: spisok_tipov_grantov, "
                            "granty_i_isledovaniya, spisok_otrasley_nauki."
                        ),
                    ),
                )
            )
        ]
    )
