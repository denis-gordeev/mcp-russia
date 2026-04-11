"""Prompts for the Camara feature — analysis templates for LLMs.

NOTE: This is a legacy/compatibility layer within mcp-russia.
These Brazilian legislative analysis prompts are kept for backward compatibility
with the historical Camara dos Deputados integration and are NOT part of the
target Russian data model.
"""

from __future__ import annotations


def acompanhar_proposicao(sigla_tipo: str, numero: int, ano: int) -> str:
    """Генерирует обзор законодательного предложения (legacy — Бразилия).

    Cria um template que orienta o LLM a consultar dados da proposição,
    tramitação e votações na Câmara dos Deputados.

    Args:
        sigla_tipo: Tipo da proposição (ex: PL, PEC, MPV).
        numero: Número da proposição.
        ano: Ano da proposição.
    """
    prop = f"{sigla_tipo} {numero}/{ano}"
    return (
        f"Подготовь полный обзор законодательного предложения {prop}.\n\n"
        "Контекст:\n"
        "- Репозиторий `mcp-russia` всё ещё находится в миграции.\n"
        "- Данные ниже поступают из исторического бразильского integration-layer\n"
        "  (Câmara dos Deputados, Бразилия).\n\n"
        "Passos:\n"
        f"1. Use buscar_proposicao(sigla_tipo='{sigla_tipo}', numero={numero}, "
        f"ano={ano}) para encontrar a proposição\n"
        "2. Com o ID da proposição, use consultar_tramitacao(proposicao_id=ID) "
        "para ver o histórico de tramitação\n"
        "3. Use buscar_votacao(proposicao_id=ID) para verificar se houve votações\n"
        "4. Se houver votação, use votos_nominais(votacao_id=ID) "
        "para ver como cada deputado votou\n\n"
        "Сформируй отчёт:\n"
        f"- Резюме {prop}: содержание и текущий статус\n"
        "- История движения (ключевые события)\n"
        "- Результаты голосований (если есть)\n"
        "- Расклад по партиям (при поимённом голосовании)\n"
        "- Следующие этапы процедуры\n\n"
        "Пометка: это legacy-бразильский источник в переходном контуре `mcp-russia`."
    )


def perfil_deputado(deputado_id: int) -> str:
    """Генерирует полный профиль федерального депутата (legacy — Бразилия).

    Cria um template com dados pessoais, votações e despesas do deputado.

    Args:
        deputado_id: ID do deputado na API da Câmara.
    """
    return (
        f"Составь полный профиль депутата ID {deputado_id}.\n\n"
        "Контекст:\n"
        "- Данные поступают из исторического бразильского слоя Câmara dos Deputados.\n\n"
        "Passos:\n"
        f"1. Use buscar_deputado(deputado_id={deputado_id}) "
        "para obter os dados básicos\n"
        f"2. Use despesas_deputado(deputado_id={deputado_id}) "
        "para verificar os gastos de cota parlamentar\n\n"
        "Сформируй отчёт:\n"
        "- Данные депутата: имя, партия, штат, легислатура\n"
        "- Расходы парламентской квоты: итого, основные категории\n"
        "- Основные поставщики услуг\n"
        "- Анализ расходов: соответствуют ли среднему уровню?\n\n"
        "Пометка: это legacy-бразильский источник в переходном контуре `mcp-russia`."
    )


def analise_votacao(votacao_id: str) -> str:
    """Генерирует детальный анализ голосования в Палате депутатов (legacy — Бразилия).

    Cria um template que analisa os votos nominais por partido e região.

    Args:
        votacao_id: ID da votação na API da Câmara.
    """
    return (
        f"Детально проанализируй голосование {votacao_id}.\n\n"
        "Контекст:\n"
        "- Данные поступают из исторического бразильского слоя Câmara dos Deputados.\n\n"
        "Passos:\n"
        f"1. Use votos_nominais(votacao_id='{votacao_id}') "
        "para obter todos os votos individuais\n\n"
        "Сформируй отчёт:\n"
        "- Общий результат: принято или отклонено, голоса За/Против/Воздержались\n"
        "- Анализ по партиям: как голосовала каждая партия (% За vs Против)\n"
        "- Анализ по регионам: как голосовал каждый штат/регион\n"
        "- Особые случаи: депутаты, проголосовавшие против своей партии\n"
        "- Правительственный блок vs оппозиция: поведение каждого блока\n\n"
        "Пометка: это legacy-бразильский источник в переходном контуре `mcp-russia`."
    )
