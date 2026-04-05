"""Переиспользуемые prompts для анализа политической рекламы через legacy-layer."""

from __future__ import annotations


def analise_candidato(nome_candidato: str, pagina_id: str = "") -> str:
    """Разбор рекламной стратегии кандидата или партии через Meta Ad Library.

    Формирует структурированный анализ затрат, охвата и коммуникационной тактики.

    Args:
        nome_candidato: Nome do candidato ou partido para analisar.
        pagina_id: ID da página do Facebook (opcional, melhora precisão).
    """
    instrucoes = (
        f"Подготовь разбор политической рекламы для '{nome_candidato}' "
        "по данным Meta Ad Library.\n\n"
        "Контекст:\n"
        "- В `mcp-russia` это пока переходный legacy-layer с бразильским покрытием.\n"
        "- Не подавай этот источник как окончательную российскую интеграцию.\n\n"
    )

    if pagina_id:
        instrucoes += (
            f"1. Use `buscar_anuncios_por_pagina` com o ID [{pagina_id}] "
            "para obter os anúncios da página\n"
        )
    else:
        instrucoes += (
            f"1. Use `buscar_anuncios_eleitorais` com o termo '{nome_candidato}' "
            "para encontrar anúncios relevantes\n"
        )

    instrucoes += (
        f"2. Use `analisar_demografia_anuncios` com '{nome_candidato}' para "
        "entender o público-alvo\n"
        "3. Сформируй анализ со следующими блоками:\n"
        "   - Quantidade de anúncios encontrados\n"
        "   - Faixa total de gastos\n"
        "   - Plataformas mais utilizadas (Facebook, Instagram, etc.)\n"
        "   - Perfil demográfico do público alcançado (idade e gênero)\n"
        "   - Estados com maior alcance\n"
        "   - Principais temas/mensagens dos anúncios\n"
        "   - Período de maior atividade\n"
        "4. Отдельно отметь, что анализ основан на legacy-бразильском покрытии внутри `mcp-russia`"
    )
    return instrucoes


def panorama_eleitoral(estado: str = "", periodo_inicio: str = "", periodo_fim: str = "") -> str:
    """Сводка по политической рекламе в штате или по Бразилии в целом.

    Дает обзор активности, крупных рекламодателей и тематических паттернов.

    Args:
        estado: Nome do estado para filtrar (ex: 'São Paulo'). Vazio = Brasil todo.
        periodo_inicio: Data de início no formato YYYY-mm-dd (opcional).
        periodo_fim: Data de fim no formato YYYY-mm-dd (opcional).
    """
    local = f"no estado de {estado}" if estado else "no Brasil"
    instrucoes = (
        f"Собери обзор политической рекламы {local}.\n\n"
        "Контекст:\n"
        "- Используется исторический бразильский dataset Meta Ad Library.\n"
        "- В итоговом тексте явно пометь это как compatibility-layer `mcp-russia`.\n\n"
    )

    if estado:
        instrucoes += f"1. Use `buscar_anuncios_por_regiao` com região ['{estado}'] "
    else:
        instrucoes += "1. Use `buscar_anuncios_eleitorais` com termos amplos "

    if periodo_inicio:
        instrucoes += f"filtrando a partir de {periodo_inicio} "
    if periodo_fim:
        instrucoes += f"até {periodo_fim} "

    instrucoes += (
        "para obter uma amostra de anúncios\n"
        "2. Analise os resultados e identifique:\n"
        "   - Páginas/candidatos com mais anúncios\n"
        "   - Temas e palavras-chave predominantes\n"
        "   - Faixas de gasto mais comuns\n"
        "   - Plataformas mais utilizadas\n"
        "3. Use `analisar_demografia_anuncios` para entender o perfil do público\n"
        "4. В финале дай executive summary со следующими пунктами:\n"
        "   - Visão geral da atividade publicitária política\n"
        "   - Top anunciantes por volume e gasto\n"
        "   - Principais temas abordados\n"
        "   - Tendências observadas no período"
    )
    return instrucoes


def comparar_candidatos(candidato_a: str, candidato_b: str) -> str:
    """Сравнение рекламных стратегий двух кандидатов или партий.

    Сопоставляет расходы, охват, аудитории и сообщения.

    Args:
        candidato_a: Nome do primeiro candidato ou partido.
        candidato_b: Nome do segundo candidato ou partido.
    """
    return (
        f"Сравни политическую рекламу '{candidato_a}' и '{candidato_b}'.\n\n"
        "Контекст:\n"
        "- Используй данные Meta Ad Library как legacy-бразильский слой внутри `mcp-russia`.\n"
        "- Не описывай этот сценарий как готовую российскую интеграцию.\n\n"
        f"1. Use `buscar_anuncios_eleitorais` com '{candidato_a}' (limit=50)\n"
        f"2. Use `buscar_anuncios_eleitorais` com '{candidato_b}' (limit=50)\n"
        f"3. Use `analisar_demografia_anuncios` para '{candidato_a}'\n"
        f"4. Use `analisar_demografia_anuncios` para '{candidato_b}'\n"
        "5. Сравни и представь:\n"
        "   - Quantidade de anúncios de cada um\n"
        "   - Comparação de gastos (faixas)\n"
        "   - Diferenças no público-alvo (idade, gênero)\n"
        "   - Diferenças na distribuição regional\n"
        "   - Plataformas preferidas por cada um\n"
        "   - Diferenças nos temas e tom das mensagens\n"
        "   - Qual tem maior alcance estimado\n"
        "6. Заверши выводом с ключевыми инсайтами и пометкой о переходном статусе источника"
    )
