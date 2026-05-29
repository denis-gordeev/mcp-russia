"""Tool functions for the Anuncios Eleitorais feature.

Инструмент совместимости с API библиотеки рекламных объявлений Meta Бразилии.
Эти инструменты обеспечивают устаревший доступ к бразильским данным
в рамках mcp-russia.

Правила (ADR-001):
    - tools.py НИКОГДА не выполняет HTTP напрямую — делегирует client.py
    - Возвращает отформатированные строки для потребления LLM
    - Использует Context для структурированного логирования и отчёта о прогрессе
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import markdown_table

from . import client
from .constants import BUSCA_FRASE_EXATA
from .schemas import AnuncioEleitoral


def _formatar_anuncio(ad: AnuncioEleitoral) -> str:
    """Format a single ad for LLM consumption."""
    lines: list[str] = []
    lines.append(f"### {ad.page_name or 'Página desconhecida'} (ID: {ad.id})")

    if ad.bylines:
        lines.append(f"**Financiado por:** {ad.bylines}")

    if ad.ad_delivery_start_time:
        periodo = f"**Período:** {ad.ad_delivery_start_time}"
        if ad.ad_delivery_stop_time:
            periodo += f" até {ad.ad_delivery_stop_time}"
        else:
            periodo += " (em veiculação)"
        lines.append(periodo)

    if ad.ad_creative_bodies:
        texto = ad.ad_creative_bodies[0]
        if len(texto) > 300:
            texto = texto[:300] + "..."
        lines.append(f"**Texto:** {texto}")

    if ad.spend:
        gasto = ""
        if ad.spend.lower_bound and ad.spend.upper_bound:
            gasto = f"{ad.spend.lower_bound} - {ad.spend.upper_bound}"
        elif ad.spend.lower_bound:
            gasto = f"> {ad.spend.lower_bound}"
        if gasto and ad.currency:
            lines.append(f"**Gasto:** {gasto} {ad.currency}")

    if ad.impressions:
        imp = ""
        if ad.impressions.lower_bound and ad.impressions.upper_bound:
            imp = f"{ad.impressions.lower_bound} - {ad.impressions.upper_bound}"
        elif ad.impressions.lower_bound:
            imp = f"> {ad.impressions.lower_bound}"
        if imp:
            lines.append(f"**Impressões:** {imp}")

    if ad.br_total_reach:
        lines.append(f"**Alcance Brasil:** {ad.br_total_reach:,}".replace(",", "."))

    if ad.publisher_platforms:
        lines.append(f"**Plataformas:** {', '.join(ad.publisher_platforms)}")

    if ad.ad_snapshot_url:
        lines.append(f"**Visualizar:** {ad.ad_snapshot_url}")

    return "\n".join(lines)


def _formatar_lista_anuncios(anuncios: list[AnuncioEleitoral], total: int | None = None) -> str:
    """Format a list of ads for LLM consumption."""
    if not anuncios:
        return "Nenhum anúncio encontrado para os critérios informados."

    lines: list[str] = []
    if total is not None:
        lines.append(f"**{total} anúncio(s) retornado(s)**\n")
    else:
        lines.append(f"**{len(anuncios)} anúncio(s) retornado(s)**\n")

    for ad in anuncios:
        lines.append(_formatar_anuncio(ad))
        lines.append("")

    return "\n".join(lines)


async def buscar_anuncios_eleitorais(
    search_terms: str,
    ctx: Context,
    ad_active_status: str | None = None,
    ad_delivery_date_min: str | None = None,
    ad_delivery_date_max: str | None = None,
    media_type: str | None = None,
    publisher_platforms: list[str] | None = None,
    search_type: str | None = None,
    limit: int = 25,
) -> str:
    """(legacy) Поиск избирательных и политических рекламных объявлений в Бразилии.

    Примечание: инструмент совместимости для бразильских данных о рекламе Meta.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Поиск в библиотеке рекламных объявлений Meta по объявлениям на социальные темы,
    выборы или политику, которые содержат указанные термины и охватывают аудиторию в Бразилии.

    Args:
        search_terms: Поисковые термины (макс. 100 символов). Пробел между словами = AND.
            Пример: 'educação saúde' ищет объявления с обоими словами.
        ad_active_status: Статус объявления (ACTIVE, INACTIVE, ALL). По умолчанию: ACTIVE.
        ad_delivery_date_min: Минимальная дата размещения в формате YYYY-mm-dd.
        ad_delivery_date_max: Максимальная дата размещения в формате YYYY-mm-dd.
        media_type: Тип медиа (ALL, IMAGE, MEME, VIDEO, NONE).
        publisher_platforms: Платформы (напр.: ['FACEBOOK', 'INSTAGRAM']).
        search_type: Тип поиска. KEYWORD_UNORDERED (по умолчанию) — слова в любом порядке,
            KEYWORD_EXACT_PHRASE — точная фраза.
        limit: Максимальное количество результатов (1-500). По умолчанию: 25.

    Returns:
        Форматированный список избирательных объявлений с данными о расходах и охвате.
    """
    await ctx.info(f"Buscando anúncios eleitorais: '{search_terms}'...")
    kwargs: dict[str, object] = {
        "search_terms": search_terms,
        "ad_active_status": ad_active_status,
        "ad_delivery_date_min": ad_delivery_date_min,
        "ad_delivery_date_max": ad_delivery_date_max,
        "media_type": media_type,
        "publisher_platforms": publisher_platforms,
        "limit": limit,
    }
    if search_type is not None:
        kwargs["search_type"] = search_type
    resposta = await client.buscar_anuncios(**kwargs)  # type: ignore[arg-type]
    return _formatar_lista_anuncios(resposta.data)


async def buscar_anuncios_por_pagina(
    search_page_ids: list[str],
    ctx: Context,
    ad_active_status: str | None = None,
    ad_delivery_date_min: str | None = None,
    ad_delivery_date_max: str | None = None,
    limit: int = 25,
) -> str:
    """(legacy) Поиск избирательных объявлений конкретных страниц Facebook.

    Примечание: инструмент совместимости для бразильских данных о рекламе Meta.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Используйте этот инструмент для просмотра всех политических объявлений
    конкретного кандидата, партии или организации по ID страницы Facebook.

    Args:
        search_page_ids: Список ID страниц Facebook (макс. 10).
            Пример: ['123456789', '987654321'].
        ad_active_status: Статус объявления (ACTIVE, INACTIVE, ALL). По умолчанию: ACTIVE.
        ad_delivery_date_min: Минимальная дата размещения (YYYY-mm-dd).
        ad_delivery_date_max: Максимальная дата размещения (YYYY-mm-dd).
        limit: Максимальное количество результатов (1-500). По умолчанию: 25.

    Returns:
        Форматированный список объявлений страницы(страниц) с данными о расходах и охвате.
    """
    await ctx.info(f"Buscando anúncios das páginas: {', '.join(search_page_ids)}...")
    resposta = await client.buscar_anuncios(
        search_page_ids=search_page_ids,
        ad_active_status=ad_active_status,
        ad_delivery_date_min=ad_delivery_date_min,
        ad_delivery_date_max=ad_delivery_date_max,
        limit=limit,
    )
    return _formatar_lista_anuncios(resposta.data)


async def buscar_anuncios_por_financiador(
    bylines: list[str],
    ctx: Context,
    search_terms: str = "",
    ad_active_status: str | None = None,
    ad_delivery_date_min: str | None = None,
    ad_delivery_date_max: str | None = None,
    limit: int = 25,
) -> str:
    """(legacy) Поиск избирательных объявлений по имени спонсора (кто оплатил).

    Примечание: инструмент совместимости для бразильских данных о рекламе Meta.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Фильтрация объя по полю 'Pago por' (byline). Имя должно быть
    полным текстом, отображаемым в дисклеймере объявления.

    Args:
        bylines: Имена спонсоров. Должен быть точный текст дисклеймера.
            Пример: ['Partido X', 'Candidato Y para Prefeito'].
        search_terms: Дополнительные поисковые термины (необязательно).
        ad_active_status: Статус объявления (ACTIVE, INACTIVE, ALL). По умолчанию: ACTIVE.
        ad_delivery_date_min: Минимальная дата размещения (YYYY-mm-dd).
        ad_delivery_date_max: Максимальная дата размещения (YYYY-mm-dd).
        limit: Максимальное количество результатов (1-500). По умолчанию: 25.

    Returns:
        Форматированный список объявлений спонсора(спонсоров).
    """
    await ctx.info(f"Buscando anúncios financiados por: {', '.join(bylines)}...")
    resposta = await client.buscar_anuncios(
        search_terms=search_terms,
        bylines=bylines,
        ad_active_status=ad_active_status,
        ad_delivery_date_min=ad_delivery_date_min,
        ad_delivery_date_max=ad_delivery_date_max,
        limit=limit,
    )
    return _formatar_lista_anuncios(resposta.data)


async def buscar_anuncios_por_regiao(
    regiao: str,
    ctx: Context,
    search_terms: str = "",
    ad_active_status: str | None = None,
    ad_delivery_date_min: str | None = None,
    ad_delivery_date_max: str | None = None,
    limit: int = 50,
) -> str:
    """(legacy) Поиск избирательных объявлений с охватом в регионе/штате Бразилии.

    Примечание: инструмент совместимости для бразильских данных о рекламе Meta.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Поиск политических объявлений с фильтрацией по указанному региону.
    Фильтрация выполняется после поиска через поле delivery_by_region ответа,
    так как API не поддерживает прямую фильтрацию по региону.

    Args:
        regiao: Название бразильского штата (напр.: 'Piauí', 'São Paulo').
            Используйте полное название штата, не аббревиатуру.
        search_terms: Дополнительные поисковые термины (необязательно). Если пусто,
            автоматически ищет по названию региона.
        ad_active_status: Статус объявления (ACTIVE, INACTIVE, ALL). По умолчанию: ACTIVE.
        ad_delivery_date_min: Минимальная дата размещения (YYYY-mm-dd).
        ad_delivery_date_max: Максимальная дата размещения (YYYY-mm-dd).
        limit: Количество результатов для поиска перед фильтрацией (1-500). По умолчанию: 50.

    Returns:
        Форматированный список объявлений с охватом в регионе.
    """
    termo = search_terms or regiao
    await ctx.info(f"Buscando anúncios com alcance em {regiao}...")
    resposta = await client.buscar_anuncios(
        search_terms=termo,
        ad_active_status=ad_active_status,
        ad_delivery_date_min=ad_delivery_date_min,
        ad_delivery_date_max=ad_delivery_date_max,
        limit=limit,
    )

    # Filtrar pós-busca: anúncios com alcance na região
    regiao_lower = regiao.lower()
    filtrados = []
    for ad in resposta.data:
        # Check delivery_by_region
        if ad.delivery_by_region:
            for r in ad.delivery_by_region:
                if r.region and regiao_lower in r.region.lower():
                    filtrados.append(ad)
                    break
        # Check target_locations
        if ad.target_locations:
            for loc in ad.target_locations:
                if loc.name and regiao_lower in loc.name.lower():
                    filtrados.append(ad)
                    break
        # Check ad text mentions
        texto = " ".join(ad.ad_creative_bodies or []).lower()
        if regiao_lower in texto and ad not in filtrados:
            filtrados.append(ad)

    return _formatar_lista_anuncios(filtrados)


async def analisar_demografia_anuncios(
    search_terms: str,
    ctx: Context,
    search_page_ids: list[str] | None = None,
    ad_delivery_date_min: str | None = None,
    ad_delivery_date_max: str | None = None,
    limit: int = 25,
) -> str:
    """(legacy) Анализ демографического и регионального распредения избирательных объявлений.

    Примечание: инструмент совместимости для бразильских данных о рекламе Meta.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Возвращает данные о возрасте, поле и регионе охвата политических объявлений.
    Полезно для понимания целевой аудитории кампаний.

    Args:
        search_terms: Поисковые термины для фильтрации объявлений.
        search_page_ids: ID страниц для фильтрации (необязательно).
        ad_delivery_date_min: Минимальная дата размещения (YYYY-mm-dd).
        ad_delivery_date_max: Максимальная дата размещения (YYYY-mm-dd).
        limit: Максимальное количество объявлений для анализа (1-500). По умолчанию: 25.

    Returns:
        Форматированный демографический и региональный анализ.
    """
    await ctx.info(f"Analisando demografia dos anúncios: '{search_terms}'...")
    resposta = await client.buscar_anuncios(
        search_terms=search_terms,
        search_page_ids=search_page_ids,
        ad_delivery_date_min=ad_delivery_date_min,
        ad_delivery_date_max=ad_delivery_date_max,
        limit=limit,
    )

    if not resposta.data:
        return "Nenhum anúncio encontrado para análise demográfica."

    lines: list[str] = [f"## Análise demográfica — {len(resposta.data)} anúncio(s)\n"]

    # Aggregate demographics
    demo_totals: dict[str, float] = {}
    region_totals: dict[str, float] = {}
    count_with_demo = 0
    count_with_region = 0

    for ad in resposta.data:
        if ad.demographic_distribution:
            count_with_demo += 1
            for d in ad.demographic_distribution:
                key = f"{d.age or '?'} / {d.gender or '?'}"
                pct = float(d.percentage) if d.percentage else 0.0
                demo_totals[key] = demo_totals.get(key, 0.0) + pct

        if ad.delivery_by_region:
            count_with_region += 1
            for r in ad.delivery_by_region:
                region = r.region or "Desconhecida"
                pct = float(r.percentage) if r.percentage else 0.0
                region_totals[region] = region_totals.get(region, 0.0) + pct

    # Format demographics
    if demo_totals and count_with_demo > 0:
        lines.append("### Distribuição por idade e gênero (média)\n")
        rows = []
        for key in sorted(demo_totals.keys()):
            avg = demo_totals[key] / count_with_demo * 100
            parts = key.split(" / ")
            rows.append((parts[0], parts[1], f"{avg:.1f}%"))
        lines.append(markdown_table(["Idade", "Gênero", "Alcance médio"], rows))
        lines.append("")

    # Format regions
    if region_totals and count_with_region > 0:
        lines.append("### Distribuição por região (média)\n")
        sorted_regions = sorted(region_totals.items(), key=lambda x: x[1], reverse=True)
        region_rows: list[tuple[str, str]] = []
        for region, total in sorted_regions[:15]:
            avg = total / count_with_region * 100
            region_rows.append((region, f"{avg:.1f}%"))
        lines.append(markdown_table(["Região", "Alcance médio"], region_rows))
        lines.append("")

    if not demo_totals and not region_totals:
        lines.append("Dados demográficos e regionais não disponíveis para estes anúncios.")

    return "\n".join(lines)


async def buscar_anuncios_frase_exata(
    frase: str,
    ctx: Context,
    ad_active_status: str | None = None,
    ad_delivery_date_min: str | None = None,
    ad_delivery_date_max: str | None = None,
    limit: int = 25,
) -> str:
    """(legacy) Поиск избирательных объявлений по точной фразе в Бразилии.

    Примечание: инструмент совместимости для бразильских данных о рекламе Meta.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    В отличие от стандартного поиска (который обрабатывает каждое слово отдельно),
    этот инструмент ищет полную фразу точно так, как она указана.
    Для поиска нескольких фраз разделите их запятой.

    Args:
        frase: Точная фраза для поиска. Для нескольких фраз разделите запятой.
            Пример: 'governo federal' или 'saúde pública,educação básica'.
        ad_active_status: Статус объявления (ACTIVE, INACTIVE, ALL). По умолчанию: ACTIVE.
        ad_delivery_date_min: Минимальная дата размещения (YYYY-mm-dd).
        ad_delivery_date_max: Максимальная дата размещения (YYYY-mm-dd).
        limit: Максимальное количество результатов (1-500). По умолчанию: 25.

    Returns:
        Форматированный список избирательных объявлений, содержащих точную фразу.
    """
    await ctx.info(f"Buscando anúncios com frase exata: '{frase}'...")
    resposta = await client.buscar_anuncios(
        search_terms=frase,
        search_type=BUSCA_FRASE_EXATA,
        ad_active_status=ad_active_status,
        ad_delivery_date_min=ad_delivery_date_min,
        ad_delivery_date_max=ad_delivery_date_max,
        limit=limit,
    )
    return _formatar_lista_anuncios(resposta.data)
