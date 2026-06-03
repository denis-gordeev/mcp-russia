"""Prompts for the ГИБДД/МВД feature."""

from __future__ import annotations

import mcp.types as mt
from fastmcp.prompts import Message, PromptMessage, PromptResult


def analiz_transportnogo_sredstva() -> PromptResult:
    """Анализ транспортного средства по VIN.

    Используйте этот промпт для проверки транспортного средства перед покупкой.
    """
    return PromptResult(
        messages=[
            Message(
                PromptMessage(
                    role="user",
                    content=mt.TextContent(
                        type="text",
                        text=(
                            "Выполните проверку транспортного средства по VIN:\n\n"
                            "1. Получите основные сведения о ТС (марка, модель, год).\n"
                            "2. Проверьте историю регистрационных действий.\n"
                            "3. Проверьте ДТП с участием ТС.\n"
                            "4. Проверьте розыск и ограничения.\n"
                            "5. Оцените общую историю ТС и риски.\n\n"
                            "Используйте tools: info_ts, istoriya_registraciy."
                        ),
                    ),
                )
            )
        ]
    )


def analiz_voditelya() -> PromptResult:
    """Анализ водительского удостоверения.

    Используйте этот промпт для проверки статуса ВУ и наличия штрафов.
    """
    return PromptResult(
        messages=[
            Message(
                PromptMessage(
                    role="user",
                    content=mt.TextContent(
                        type="text",
                        text=(
                            "Выполните проверку водителя:\n\n"
                            "1. Проверьте действительность водительского удостоверения.\n"
                            "2. Получите сведения о категориях и ограничениях.\n"
                            "3. Проверьте наличие неоплаченных штрафов ГИБДД.\n"
                            "4. Оцените статус оплаты и наличие скидок.\n"
                            "5. Рекомендуйте действия по оплате или обжалованию.\n\n"
                            "Используйте tools: info_vu, shtrafy_po_vu, "
                            "spisok_statusov_shtrafov."
                        ),
                    ),
                )
            )
        ]
    )
