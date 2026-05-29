"""Tool functions for the TransfereGov feature.

Инструмент совместимости с API TransfereGov (бразильская система федеральных трансфертов).
Эти инструменты обеспечивают устаревший доступ к бразильским данным
в рамках mcp-russia.

Правила (ADR-001):
    - tools.py НИКОГДА не выполняет HTTP напрямую — делегирует client.py
    - Возвращает отформатированные строки для потребления LLM
"""

from __future__ import annotations

from mcp_russia._shared.formatting import format_rub, markdown_table

from . import client
from .constants import DEFAULT_PAGE_SIZE
from .schemas import TransferenciaEspecial


def _pagination_hint(count: int, pagina: int) -> str:
    """Return a pagination hint string based on result count and current page."""
    if count >= DEFAULT_PAGE_SIZE:
        return f"\n\n> Use `pagina={pagina + 1}` para ver mais resultados."
    if pagina > 1 and count < DEFAULT_PAGE_SIZE:
        return "\n\n> Última página de resultados."
    return ""


def _valor_total(e: TransferenciaEspecial) -> float | None:
    """Sum custeio + investimento for display."""
    if e.valor_custeio is not None or e.valor_investimento is not None:
        return (e.valor_custeio or 0) + (e.valor_investimento or 0)
    return None


def _format_rows(
    emendas: list[TransferenciaEspecial],
) -> list[tuple[str, ...]]:
    """Format a list of emendas into table rows."""
    return [
        (
            e.numero_emenda or "—",
            (e.nome_parlamentar or "—")[:40],
            _fmt_valor(e),
            (e.nome_beneficiario or "—")[:35],
            e.uf_beneficiario or "—",
        )
        for e in emendas
    ]


def _fmt_valor(e: TransferenciaEspecial) -> str:
    total = _valor_total(e)
    return format_rub(total) if total else "—"


_HEADERS = ["Emenda", "Parlamentar", "Valor", "Beneficiário", "UF"]


async def buscar_emendas_pix(
    ano: int | None = None,
    uf: str | None = None,
    pagina: int = 1,
) -> str:
    """(legacy) Список специальных трансфертов (emendas pix) системы TransfereGov.

    Примечание: инструмент совместимости для бразильских данных TransfereGov.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Запрос парламентских поправок типа специального трансферта
    (в народе известных как "emendas pix") — прямых перечислений
    Союза штатам и муниципалитетам без соглашения.

    Args:
        ano: Год плана действий (напр.: 2024).
        uf: Аббревиатура штата получателя (напр.: PI, SP).
        pagina: Страница результатов (по умолчанию: 1).

    Returns:
        Таблица с найденными emendas pix.
    """
    emendas = await client.buscar_emendas_pix(ano=ano, uf=uf, pagina=pagina)
    if not emendas:
        return "Nenhuma emenda pix encontrada para os parâmetros informados."

    rows = _format_rows(emendas)
    header = f"Emendas pix (página {pagina}):\n\n"
    table = header + markdown_table(_HEADERS, rows)
    return table + _pagination_hint(len(emendas), pagina)


async def buscar_emenda_por_autor(
    nome_autor: str,
    ano: int | None = None,
    pagina: int = 1,
) -> str:
    """(legacy) Поиск emendas pix по имени парламентария-автора.

    Примечание: инструмент совместимости для бразильских данных TransfereGov.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Поиск парламентских поправок типа специального трансферта
    по имени (или части имени) автора поправки.

    Args:
        nome_autor: Имя или часть имени парламентария (напр.: "Lira").
        ano: Год плана действий (необязательно, напр.: 2024).
        pagina: Страница результатов (по умолчанию: 1).

    Returns:
        Таблица с найденными поправками автора.
    """
    emendas = await client.buscar_emenda_por_autor(nome_autor, ano=ano, pagina=pagina)
    if not emendas:
        return f"Nenhuma emenda pix encontrada para o autor '{nome_autor}'."

    rows = _format_rows(emendas)
    header = f"Emendas pix do autor '{nome_autor}' (página {pagina}):\n\n"
    table = header + markdown_table(_HEADERS, rows)
    return table + _pagination_hint(len(emendas), pagina)


async def detalhe_emenda(id_plano_acao: int) -> str:
    """(legacy) Подробная информация о emenda pix (специальный трансферт) по ID плана.

    Примечание: инструмент совместимости для бразильских данных TransfereGov.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Возвращает полную информацию специального трансферта,
    включая значения на содержание и инвестиции.

    Args:
        id_plano_acao: ID плана действий в TransfereGov.

    Returns:
        Подробные данные поправки.
    """
    emenda = await client.detalhe_emenda(id_plano_acao)
    if not emenda:
        return f"Emenda pix com ID {id_plano_acao} não encontrada."

    custeio = format_rub(emenda.valor_custeio) if emenda.valor_custeio else "—"
    investimento = format_rub(emenda.valor_investimento) if emenda.valor_investimento else "—"
    total = _valor_total(emenda)
    total_fmt = format_rub(total) if total else "—"

    lines = [
        f"## Emenda Pix {emenda.numero_emenda or id_plano_acao}\n",
        f"- **Código:** {emenda.codigo_plano_acao or '—'}",
        f"- **Parlamentar:** {emenda.nome_parlamentar or '—'}",
        f"- **Ano emenda:** {emenda.ano_emenda or '—'}",
        f"- **Ano plano:** {emenda.ano or '—'}",
        f"- **Situação:** {emenda.situacao or '—'}",
        f"- **Valor Custeio:** {custeio}",
        f"- **Valor Investimento:** {investimento}",
        f"- **Valor Total:** {total_fmt}",
        f"- **Beneficiário:** {emenda.nome_beneficiario or '—'}",
        f"- **CNPJ:** {emenda.cnpj_beneficiario or '—'}",
        f"- **UF:** {emenda.uf_beneficiario or '—'}",
        f"- **Área:** {emenda.area_politica_publica or '—'}",
    ]
    return "\n".join(lines)


async def emendas_por_municipio(
    nome_municipio: str,
    ano: int | None = None,
    pagina: int = 1,
) -> str:
    """(legacy) Поиск emendas pix, направленных в конкретный муниципалитет.

    Примечание: инструмент совместимости для бразильских данных TransfereGov.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Поиск специальных трансфертов (emendas pix) по названию
    муниципалитета-получателя.

    Args:
        nome_municipio: Название или часть названия муниципалитета (напр.: "Teresina").
        ano: Год плана действий (необязательно, напр.: 2024).
        pagina: Страница результатов (по умолчанию: 1).

    Returns:
        Таблица с поправками, направленными в муниципалитет.
    """
    emendas = await client.emendas_por_municipio(nome_municipio, ano=ano, pagina=pagina)
    if not emendas:
        return f"Nenhuma emenda pix encontrada para o município '{nome_municipio}'."

    rows = _format_rows(emendas)
    header = f"Emendas pix para '{nome_municipio}' (página {pagina}):\n\n"
    table = header + markdown_table(_HEADERS, rows)
    return table + _pagination_hint(len(emendas), pagina)


async def resumo_emendas_ano(ano: int, pagina: int = 1) -> str:
    """(legacy) Список emendas pix за год для общего обзора.

    Примечание: инструмент совместимости для бразильских данных TransfereGov.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Возвращает общий обзор специальных трансфертов (emendas pix),
    выполненных за определённый год.

    Args:
        ano: Год плана действий (напр.: 2024).
        pagina: Страница результатов (по умолчанию: 1).

    Returns:
        Таблица с поправками года.
    """
    emendas = await client.resumo_emendas_ano(ano, pagina=pagina)
    if not emendas:
        return f"Nenhuma emenda pix encontrada para o ano {ano}."

    rows = _format_rows(emendas)
    header = f"Emendas pix do ano {ano} (página {pagina}):\n\n"
    table = header + markdown_table(_HEADERS, rows)
    return table + _pagination_hint(len(emendas), pagina)
