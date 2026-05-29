"""Инструменты для работы с официальным вестником (Diário Oficial, legacy).

Примечание: это слой совместимости в рамках mcp-russia. Данные инструменты
предоставляют устаревший доступ к данным бразильских официальных вестников
(Querido Diário) и считаются переходными.

Правила (ADR-001):
    - tools.py НИКОГДА не выполняет HTTP напрямую — делегирует client.py
    - Возвращает отформатированные строки для потребления LLM
"""

from __future__ import annotations

import re

from fastmcp import Context

from mcp_russia._shared.formatting import markdown_table

from . import client

_HTML_TAG_RE = re.compile(r"<[^>]+>")


async def buscar_diarios(
    texto: str,
    ctx: Context,
    territorio_id: str | None = None,
    data_inicio: str | None = None,
    data_fim: str | None = None,
    pagina: int = 0,
) -> str:
    """(legacy) Поиск в муниципальных официальных вестниках по свободному тексту.

    Инструмент совместимости с Querido Diário (Бразилия).
    Полнотекстовый поиск в официальных вестниках 5000+ бразильских муниципалитетов.
    Полезно для поиска упоминаний компаний, лиц, контрактов, торгов,
    назначений, увольнений и административных актов.

    Args:
        texto: Поисковый запрос (название компании, CNPJ, имя, ключевое слово).
        territorio_id: Код IBGE муниципалитета (необязательно, напр.: 3550308 для Сан-Паулу).
        data_inicio: Дата начала в формате YYYY-MM-DD (необязательно).
        data_fim: Дата окончания в формате YYYY-MM-DD (необязательно).
        pagina: Страница результатов (0-indexed, по умолчанию 0).

    Returns:
        Список официальных вестников с релевантными фрагментами.
    """
    await ctx.info(f"Buscando diários oficiais para '{texto}'...")
    resultado = await client.buscar_diarios(
        querystring=texto,
        territory_id=territorio_id,
        since=data_inicio,
        until=data_fim,
        offset=pagina * 10,
    )
    await ctx.info(f"{resultado.total_gazettes} diários encontrados")

    if not resultado.gazettes:
        return f"Nenhum diário oficial encontrado para '{texto}'."

    lines = [f"**Total:** {resultado.total_gazettes} diários encontrados\n"]
    for i, d in enumerate(resultado.gazettes[:10], 1):
        lines.append(f"### {i}. {d.territory_name or 'N/A'}/{d.state_code or '??'}")
        lines.append(f"**Data:** {d.date or 'N/A'} | **Edição:** {d.edition_number or 'N/A'}")
        if d.is_extra_edition:
            lines.append("**Edição Extra**")
        if d.excerpts:
            excerpt = _HTML_TAG_RE.sub("", d.excerpts[0])[:500]
            lines.append(f"\n> {excerpt}...")
        if d.txt_url:
            lines.append(f"\n[Texto completo]({d.txt_url})")
        lines.append("")

    if resultado.total_gazettes > 10:
        lines.append(
            f"\n*Mostrando 10 de {resultado.total_gazettes}. "
            f"Use pagina={pagina + 1} para mais resultados.*"
        )
    return "\n".join(lines)


async def buscar_trechos(
    territorio_id: str,
    texto: str,
    ctx: Context,
    data_inicio: str | None = None,
    data_fim: str | None = None,
    pagina: int = 0,
) -> str:
    """(legacy) Поиск конкретных фрагментов в официальных вестниках муниципалитета.

    Инструмент совместимости с Querido Diário (Бразилия).
    Возвращает отдельные выдержки (вырезки) из официальных вестников
    конкретного муниципалитета. В отличие от buscar_diarios, который возвращает
    целые выпуски, этот инструмент возвращает изолированные фрагменты с контекстом.

    Используйте buscar_cidades() для получения кода IBGE муниципалитета (territorio_id).

    Args:
        territorio_id: Код IBGE муниципалитета (напр.: 3550308 для Сан-Паулу).
        texto: Поисковый запрос (имя, CNPJ, ключевое слово).
        data_inicio: Дата начала в формате YYYY-MM-DD (необязательно).
        data_fim: Дата окончания в формате YYYY-MM-DD (необязательно).
        pagina: Страница результатов (0-indexed, по умолчанию 0).

    Returns:
        Список найденных фрагментов с датой и содержанием.
    """
    await ctx.info(f"Buscando trechos para '{texto}' no território {territorio_id}...")
    resultado = await client.buscar_trechos(
        territory_id=territorio_id,
        querystring=texto,
        since=data_inicio,
        until=data_fim,
        offset=pagina * 10,
    )
    await ctx.info(f"{resultado.total_excerpts} trechos encontrados")

    if not resultado.excerpts:
        return f"Nenhum trecho encontrado para '{texto}' no território {territorio_id}."

    lines = [f"**Total:** {resultado.total_excerpts} trechos encontrados\n"]
    for i, e in enumerate(resultado.excerpts[:10], 1):
        lines.append(f"### {i}. {e.territory_name or 'N/A'}/{e.state_code or '??'}")
        lines.append(f"**Data:** {e.date or 'N/A'} | **Edição:** {e.edition_number or 'N/A'}")
        if e.is_extra_edition:
            lines.append("**Edição Extra**")
        if e.subheadline:
            lines.append(f"**Seção:** {e.subheadline}")
        if e.excerpt:
            excerpt = _HTML_TAG_RE.sub("", e.excerpt)[:500]
            lines.append(f"\n> {excerpt}...")
        if e.txt_url:
            lines.append(f"\n[Texto completo]({e.txt_url})")
        lines.append("")

    if resultado.total_excerpts > 10:
        lines.append(
            f"\n*Mostrando 10 de {resultado.total_excerpts}. "
            f"Use pagina={pagina + 1} para mais resultados.*"
        )
    return "\n".join(lines)


async def buscar_cidades(nome: str, ctx: Context) -> str:
    """(legacy) Поиск муниципалитетов, доступных в Querido Diário, по названию.

    Инструмент совместимости с Querido Diário (Бразилия).
    Возвращает коды IBGE, необходимые для фильтрации поисков по территории.

    Args:
        nome: Название (или часть названия) города.

    Returns:
        Список найденных городов с кодом IBGE.
    """
    await ctx.info(f"Buscando cidades '{nome}'...")
    cidades = await client.buscar_cidades(nome)
    await ctx.info(f"{len(cidades)} cidades encontradas")

    if not cidades:
        return f"Nenhuma cidade encontrada para '{nome}'."

    rows = [(c.territory_id, c.territory_name, c.state_code) for c in cidades]
    return markdown_table(["Código IBGE", "Cidade", "UF"], rows)


async def listar_territorios(ctx: Context) -> str:
    """(legacy) Список всех муниципалитетов с официальными вестниками в Querido Diário.

    Инструмент совместимости с Querido Diário (Бразилия).
    Возвращает полный список территорий, доступных для поиска.
    Используйте возвращённый код IBGE для фильтрации поисков в buscar_diarios.

    Returns:
        Список доступных муниципалитетов с кодом IBGE и штатом.
    """
    await ctx.info("Listando territórios disponíveis...")
    cidades = await client.listar_cidades()
    await ctx.info(f"{len(cidades)} territórios disponíveis")

    rows = [(c.territory_id, c.territory_name, c.state_code) for c in cidades]
    header = f"**{len(cidades)} municípios** com diários oficiais disponíveis:\n\n"
    return header + markdown_table(["Código IBGE", "Cidade", "UF"], rows[:100])
