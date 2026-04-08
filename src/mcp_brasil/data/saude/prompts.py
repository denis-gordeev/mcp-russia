"""Prompts for the Saúde feature — analysis templates for LLMs.

Prompts provide reusable message templates that guide LLM interactions.
They appear in client UIs (e.g., Claude Desktop) as slash-commands.
"""

from __future__ import annotations


def analise_rede_saude(codigo_municipio: str) -> str:
    """Gera uma análise сети здравоохранения по legacy-данным Бразилии.

    Cria um template de análise que orienta o LLM a consultar dados
    de estabelecimentos, profissionais e leitos hospitalares do município.

    Args:
        codigo_municipio: Código IBGE do município (ex: "355030" para São Paulo).
    """
    return (
        f"Сделай разбор сети здравоохранения муниципалитета {codigo_municipio} "
        "по данным CNES/DataSUS.\n"
        "Это legacy-источник Бразилии внутри mcp-russia: используй его как "
        "справочный compatibility-layer и явно помечай географические ограничения.\n\n"
        "Passos:\n"
        f"1. Use buscar_estabelecimentos(codigo_municipio='{codigo_municipio}') "
        "para listar os estabelecimentos de saúde\n"
        "2. Use listar_tipos_estabelecimento() para entender os tipos disponíveis\n"
        f"3. Use buscar_profissionais(codigo_municipio='{codigo_municipio}') "
        "para ver os profissionais atuantes\n"
        f"4. Use consultar_leitos(codigo_municipio='{codigo_municipio}') "
        "para analisar a capacidade de leitos\n\n"
        "Apresente:\n"
        "- Quantidade e tipos de estabelecimentos\n"
        "- Distribuição de profissionais por especialidade\n"
        "- Capacidade de leitos (existentes vs SUS)\n"
        "- Avaliação geral da cobertura de saúde no município\n"
        "- Nota de escopo: análise baseada em dados CNES/DataSUS do Brasil"
    )
