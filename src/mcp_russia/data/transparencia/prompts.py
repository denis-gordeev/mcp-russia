"""Prompts for the Transparência feature — analysis templates for LLMs.

NOTE: This is a legacy/compatibility layer within mcp-russia.
These Brazilian federal transparency analysis prompts are kept for backward
compatibility with the historical Portal da Transparência integration and are
NOT part of the target Russian data model.

Prompts provide reusable message templates that guide LLM interactions.
They appear in client UIs (e.g., Claude Desktop) as slash-commands.
"""

from __future__ import annotations


def auditoria_fornecedor(cpf_cnpj: str) -> str:
    """Генерирует полный аудит поставщика федерального правительства (legacy — Бразилия).

    Cria um template que orienta o LLM a consultar contratos, sanções
    e emendas relacionados a um fornecedor específico por CPF ou CNPJ.

    Args:
        cpf_cnpj: CPF ou CNPJ do fornecedor (ex: 12345678000190).
    """
    return (
        f"Проведи полный аудит поставщика {cpf_cnpj}.\n\n"
        "Контекст:\n"
        "- Репозиторий `mcp-russia` всё ещё находится в миграции.\n"
        "- Данные поступают из исторического бразильского integration-layer\n"
        "  (Portal da Transparência, Бразилия).\n\n"
        "Passos:\n"
        f"1. Use buscar_contratos(cpf_cnpj='{cpf_cnpj}') para listar "
        "todos os contratos federais deste fornecedor\n"
        f"2. Use buscar_sancoes(consulta='{cpf_cnpj}') para verificar "
        "se há sanções nas bases CEIS, CNEP, CEPIM, CEAF\n"
        "3. Se houver contratos, analise os valores e períodos\n\n"
        "Сформируй отчёт:\n"
        "- Резюме контрактов (количество, общая сумма, заказывающие органы)\n"
        "- Статус в реестрах санкций (чист или под санкциями)\n"
        "- При наличии санкций: тип, период и обоснование\n"
        "- Анализ рисков: есть ли у поставщика нарушения?\n\n"
        "Пометка: это legacy-бразильский источник в переходном контуре `mcp-russia`."
    )


def analise_despesas(mes_ano_inicio: str, mes_ano_fim: str, uf: str = "") -> str:
    """Генерирует анализ расходов федерального правительства за период (legacy — Бразилия).

    Cria um template que orienta o LLM a consultar e analisar
    despesas públicas, emendas e licitações em um período.

    Args:
        mes_ano_inicio: Mês/ano de início no formato MM/AAAA (ex: 01/2024).
        mes_ano_fim: Mês/ano de fim no formato MM/AAAA (ex: 12/2024).
        uf: UF para filtrar análise (opcional, ex: PI, SP).
    """
    filtro_uf = f" no estado {uf.upper()}" if uf else ""
    return (
        f"Проанализируй расходы федерального правительства за период "
        f"с {mes_ano_inicio} по {mes_ano_fim}{filtro_uf}.\n\n"
        "Контекст:\n"
        "- Данные поступают из исторического бразильского слоя Portal da Transparência.\n\n"
        "Passos:\n"
        f"1. Use consultar_despesas(mes_ano_inicio='{mes_ano_inicio}', "
        f"mes_ano_fim='{mes_ano_fim}') para obter os dados de despesas\n"
        f"2. Use buscar_emendas(ano={mes_ano_inicio.split('/')[1]}) "
        "para verificar emendas parlamentares no período\n"
        f"3. Use buscar_licitacoes(data_inicial='01/{mes_ano_inicio}', "
        f"data_final='28/{mes_ano_fim}') para licitações no período\n\n"
        "Сформируй отчёт:\n"
        "- Объём расходов за период\n"
        "- Основные бенефициары (топ-10 по сумме)\n"
        "- Распределение по ведомствам\n"
        "- Парламентские поправки: авторы и суммы\n"
        "- Открытые и завершённые тендеры за период\n"
        "- Наблюдения о концентрации ресурсов\n\n"
        "Пометка: это legacy-бразильский источник в переходном контуре `mcp-russia`."
    )


def verificacao_compliance(consulta: str) -> str:
    """Проверяет статус компании или лица в реестрах федеральных санкций (legacy — Бразилия).

    Cria um template de due diligence/compliance que consulta todas as
    bases de sanções (CEIS, CNEP, CEPIM, CEAF) simultaneamente.

    Args:
        consulta: CPF, CNPJ ou nome da pessoa/empresa a verificar.
    """
    return (
        f"Выполни проверку комплаенса для '{consulta}'.\n\n"
        "Контекст:\n"
        "- Данные поступают из исторического бразильского слоя Portal da Transparência.\n\n"
        "Passos:\n"
        f"1. Use buscar_sancoes(consulta='{consulta}') para consultar "
        "todas as 4 bases de sanções simultaneamente:\n"
        "   - CEIS: Cadastro de Empresas Inidôneas e Suspensas\n"
        "   - CNEP: Cadastro Nacional de Empresas Punidas (Lei Anticorrupção)\n"
        "   - CEPIM: Cadastro de Entidades Privadas sem Fins Lucrativos Impedidas\n"
        "   - CEAF: Cadastro de Expulsões da Administração Federal\n"
        f"2. Use buscar_contratos(cpf_cnpj='{consulta}') para verificar "
        "se possui contratos ativos com o governo\n\n"
        "Сформируй отчёт:\n"
        "- Статус в каждом реестре санкций (чист или есть запись)\n"
        "- При наличии санкций: тип, орган, период и обоснование\n"
        "- Действующие контракты с федеральным правительством (если есть)\n"
        "- Заключение комплаенса: допущен или не допущен к госзакупкам\n"
        "- Рекомендации по дополнительной проверке (если применимо)\n\n"
        "Пометка: это legacy-бразильский источник в переходном контуре `mcp-russia`."
    )
