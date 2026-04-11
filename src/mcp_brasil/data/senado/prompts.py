"""Prompts for the Senado feature — analysis templates for LLMs.

NOTE: This is a legacy/compatibility layer within mcp-russia.
These Brazilian Senate legislative analysis prompts are kept for backward
compatibility with the historical Senado Federal integration and are NOT part
of the target Russian data model.
"""

from __future__ import annotations


def acompanhar_materia(sigla_tipo: str, numero: str, ano: str) -> str:
    """Генерирует полный обзор законодательного акта в Сенате (legacy — Бразилия).

    Cria um template que orienta o LLM a consultar dados da matéria,
    tramitação e votações no Senado Federal.

    Args:
        sigla_tipo: Tipo da matéria (ex: PEC, PLS, PLC, MPV).
        numero: Número da matéria.
        ano: Ano da matéria.
    """
    materia = f"{sigla_tipo} {numero}/{ano}"
    return (
        f"Подготовь полный обзор законодательного акта {materia}.\n\n"
        "Контекст:\n"
        "- Репозиторий `mcp-russia` всё ещё находится в миграции.\n"
        "- Данные поступают из исторического бразильского integration-layer\n"
        "  (Senado Federal, Бразилия).\n\n"
        "Passos:\n"
        f"1. Use buscar_materia(sigla_tipo='{sigla_tipo}', numero='{numero}', "
        f"ano='{ano}') para encontrar a matéria e obter o código\n"
        "2. Com o código, use detalhe_materia(codigo=CÓDIGO) "
        "para ver a ementa completa e autor\n"
        "3. Use consultar_tramitacao_materia(codigo=CÓDIGO) "
        "para ver o histórico de tramitação\n"
        "4. Use votos_materia(codigo=CÓDIGO) para verificar votações\n"
        "5. Use textos_materia(codigo=CÓDIGO) para obter links dos documentos\n\n"
        "Сформируй отчёт:\n"
        f"- Резюме {materia}: содержание, автор и текущий статус\n"
        "- История движения (ключевые события)\n"
        "- Результаты голосований (если есть)\n"
        "- Ссылки на тексты и официальные документы\n"
        "- Следующие этапы процедуры\n\n"
        "Пометка: это legacy-бразильский источник в переходном контуре `mcp-russia`."
    )


def perfil_senador(codigo: str) -> str:
    """Генерирует полный профиль сенатора (legacy — Бразилия).

    Cria um template com dados pessoais e votações do senador.

    Args:
        codigo: Código do senador na API do Senado.
    """
    return (
        f"Составь полный профиль сенатора, код {codigo}.\n\n"
        "Контекст:\n"
        "- Данные поступают из исторического бразильского слоя Senado Federal.\n\n"
        "Passos:\n"
        f"1. Use buscar_senador(codigo='{codigo}') "
        "para obter os dados básicos\n"
        f"2. Use votacoes_senador(codigo='{codigo}') "
        "para verificar as votações recentes\n\n"
        "Сформируй отчёт:\n"
        "- Данные сенатора: имя, партия, штат, срок полномочий\n"
        "- Последние голосования: позиция по ключевым актам\n"
        "- Паттерн голосований: соответствие правительству/оппозиции\n\n"
        "Пометка: это legacy-бразильский источник в переходном контуре `mcp-russia`."
    )


def analise_votacao_senado(codigo_sessao: str) -> str:
    """Генерирует детальный анализ голосования в Сенате (legacy — Бразилия).

    Cria um template que analisa o resultado e contexto de uma votação.

    Args:
        codigo_sessao: Código da sessão de votação.
    """
    return (
        f"Детально проанализируй голосование {codigo_sessao}.\n\n"
        "Контекст:\n"
        "- Данные поступают из исторического бразильского слоя Senado Federal.\n\n"
        "Passos:\n"
        f"1. Use detalhe_votacao(codigo_sessao='{codigo_sessao}') "
        "para obter o resultado e placar\n\n"
        "Сформируй отчёт:\n"
        "- Общий результат: принято или отклонено\n"
        "- Расклад голосов: За, Против, Воздержались\n"
        "- Рассмотренный акт и его контекст\n"
        "- Анализ: каково влияние этого голосования?\n\n"
        "Пометка: это legacy-бразильский источник в переходном контуре `mcp-russia`."
    )
