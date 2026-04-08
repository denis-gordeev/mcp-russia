"""Prompts for the DataJud feature — analysis templates for LLMs."""

from __future__ import annotations


def analise_processo(numero_processo: str, tribunal: str = "tjsp") -> str:
    """Gera uma análise completa de um processo judicial.

    Orienta o LLM a consultar dados do processo, partes e movimentações.

    Args:
        numero_processo: Número do processo (NPU).
        tribunal: Sigla do tribunal (ex: tjsp, trf1, stj).
    """
    return (
        f"Сделай полный разбор процесса {numero_processo} "
        f"в {tribunal.upper()} по данным DataJud.\n"
        "Это переходный бразильский судебный источник внутри mcp-russia, "
        "поэтому не смешивай его с российскими судебными системами и явно "
        "обозначай юрисдикцию.\n\n"
        "Passos:\n"
        f"1. Use buscar_processo_por_numero(numero_processo='{numero_processo}', "
        f"tribunal='{tribunal}') para obter detalhes\n"
        f"2. Use consultar_movimentacoes(numero_processo='{numero_processo}', "
        f"tribunal='{tribunal}') para o histórico\n\n"
        "Apresente:\n"
        "- Resumo: classe, assunto, órgão julgador\n"
        "- Partes envolvidas (polo ativo e passivo)\n"
        "- Cronologia das movimentações relevantes\n"
        "- Situação atual do processo\n"
        "- Observações sobre prazos ou próximos passos\n"
        "- Nota de escopo: вывод относится к бразильской системе tribunais"
    )


def pesquisa_juridica(tema: str, tribunal: str = "tjsp") -> str:
    """Gera uma pesquisa jurídica sobre um tema.

    Orienta o LLM a buscar processos relacionados a um tema específico.

    Args:
        tema: Tema jurídico para pesquisar.
        tribunal: Sigla do tribunal. Default: tjsp.
    """
    return (
        f"Сделай юридический обзор по теме '{tema}' "
        f"в {tribunal.upper()} на основе DataJud.\n"
        "Считай DataJud legacy-источником Бразилии в составе mcp-russia "
        "и помечай это в финальном ответе.\n\n"
        "Passos:\n"
        f"1. Use buscar_processos(query='{tema}', tribunal='{tribunal}') "
        "para encontrar processos relevantes\n"
        f"2. Use buscar_processos_por_assunto(assunto='{tema}', "
        f"tribunal='{tribunal}') para filtrar por assunto\n"
        "3. Para processos relevantes, use buscar_processo_por_numero() "
        "para obter detalhes\n\n"
        "Apresente:\n"
        "- Quantos processos foram encontrados\n"
        "- Principais classes processuais usadas\n"
        "- Órgãos julgadores mais frequentes\n"
        "- Resumo dos processos mais relevantes\n"
        "- Tendências observadas (se houver)\n"
        "- Ограничения переноса: результаты относятся к бразильской судебной практике"
    )
