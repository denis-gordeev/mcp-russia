"""Tool functions for the Jurisprudência feature (STF, STJ, TST).

Инструмент совместимости с API судебных решений высших трибуналов Бразилии.
Эти инструменты обеспечивают устаревший доступ к бразильским данным
в рамках mcp-russia.

Правила (ADR-001):
    - tools.py НИКОГДА не выполняет HTTP напрямую — делегирует client.py
    - Возвращает отформатированные строки для потребления LLM
"""

from __future__ import annotations

from . import client
from .constants import DEFAULT_PAGE_SIZE


def _format_ementa(ementa: str | None, max_len: int = 300) -> str:
    """Truncate ementa for table display."""
    if not ementa:
        return "—"
    text = ementa.strip().replace("\n", " ")
    if len(text) > max_len:
        return text[:max_len] + "..."
    return text


async def buscar_jurisprudencia_stf(
    query: str,
    pagina: int = 1,
    tamanho: int = DEFAULT_PAGE_SIZE,
) -> str:
    """(legacy) Поиск судебной практики в Верховном федеральном трибунале Бразилии (STF).

    Примечание: инструмент совместимости для бразильских судебных данных.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Поиск решений STF по тезису, теме или юридическим терминам.
    Поддерживает операторы: E, OU, NÃO, кавычки для точного выражения,
    ~ для нечёткого поиска, $ для подстановочного знака.

    Примеры: "direito E privacidade", "súmula vinculante", "ADPF 153".

    Args:
        query: Поисковые термины (поддерживает логические операторы).
        pagina: Страница результатов (по умолчанию: 1).
        tamanho: Результаты на страницу (по умолчанию: 10).

    Returns:
        Список решений с тезисом, докладчиком и датой.
    """
    resultados = await client.buscar_stf(query, pagina, tamanho)
    if not resultados:
        return f"Nenhum acórdão do STF encontrado para '{query}'."

    lines = [f"**Jurisprudência STF** — '{query}' (página {pagina}):\n"]
    for i, r in enumerate(resultados, 1):
        lines.append(f"**{i}. {r.classe or ''} {r.numero_processo or ''}**")
        lines.append(f"   Relator: {r.relator or '—'}")
        lines.append(f"   Julgamento: {r.data_julgamento or '—'}")
        lines.append(f"   Órgão: {r.orgao_julgador or '—'}")
        lines.append(f"   Ementa: {_format_ementa(r.ementa)}")
        if r.url:
            lines.append(f"   Link: {r.url}")
        lines.append("")

    if len(resultados) >= tamanho:
        lines.append(f"> Use `pagina={pagina + 1}` para ver mais resultados.")

    return "\n".join(lines)


async def buscar_jurisprudencia_stj(
    query: str,
    pagina: int = 1,
    tamanho: int = DEFAULT_PAGE_SIZE,
) -> str:
    """(legacy) Поиск судебной практики в Высшем суде справедливости Бразилии (STJ).

    Примечание: инструмент совместимости для бразильских судебных данных.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Поиск решений STJ через систему SCON.
    Поддерживает операторы: e, ou, não, mesmo, com, PROX(N), ADJ(N),
    кавычки для точного выражения, $ для подстановочного знака.

    Примеры: "consumidor e dano moral", "recurso especial e FGTS".

    Args:
        query: Поисковые термины (поддерживает логические операторы).
        pagina: Страница результатов (по умолчанию: 1).
        tamanho: Результаты на страницу (по умолчанию: 10).

    Returns:
        Список решений с тезисом, докладчиком и датой.
    """
    resultados = await client.buscar_stj(query, pagina, tamanho)
    if not resultados:
        return f"Nenhum acórdão do STJ encontrado para '{query}'."

    lines = [f"**Jurisprudência STJ** — '{query}' (página {pagina}):\n"]
    for i, r in enumerate(resultados, 1):
        lines.append(f"**{i}. {r.classe or ''} {r.numero_processo or ''}**")
        lines.append(f"   Relator: {r.relator or '—'}")
        lines.append(f"   Julgamento: {r.data_julgamento or '—'}")
        lines.append(f"   Órgão: {r.orgao_julgador or '—'}")
        lines.append(f"   Ementa: {_format_ementa(r.ementa)}")
        if r.url:
            lines.append(f"   Link: {r.url}")
        lines.append("")

    if len(resultados) >= tamanho:
        lines.append(f"> Use `pagina={pagina + 1}` para ver mais resultados.")

    return "\n".join(lines)


async def buscar_jurisprudencia_tst(
    query: str,
    pagina: int = 1,
    tamanho: int = DEFAULT_PAGE_SIZE,
) -> str:
    """(legacy) Поиск судебной практики в Высшем трудовом трибунале Бразилии (TST).

    Примечание: инструмент совместимости для бразильских судебных данных.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Поиск решений TST по тезису или трудовым терминам.
    Поддерживает кавычки для точного выражения.

    Примеры: "horas extras", "dano moral trabalhista", "FGTS".

    Args:
        query: Поисковые термины.
        pagina: Страница результатов (по умолчанию: 1).
        tamanho: Результаты на страницу (по умолчанию: 10).

    Returns:
        Список решений с тезисом, докладчиком и датой.
    """
    resultados = await client.buscar_tst(query, pagina, tamanho)
    if not resultados:
        return f"Nenhum acórdão do TST encontrado para '{query}'."

    lines = [f"**Jurisprudência TST** — '{query}' (página {pagina}):\n"]
    for i, r in enumerate(resultados, 1):
        lines.append(f"**{i}. {r.classe or ''} {r.numero_processo or ''}**")
        lines.append(f"   Relator: {r.relator or '—'}")
        lines.append(f"   Julgamento: {r.data_julgamento or '—'}")
        lines.append(f"   Órgão: {r.orgao_julgador or '—'}")
        lines.append(f"   Ementa: {_format_ementa(r.ementa)}")
        if r.url:
            lines.append(f"   Link: {r.url}")
        lines.append("")

    if len(resultados) >= tamanho:
        lines.append(f"> Use `pagina={pagina + 1}` para ver mais resultados.")

    return "\n".join(lines)


async def buscar_sumulas(
    tribunal: str = "stf",
    query: str | None = None,
) -> str:
    """(legacy) Поиск сводных тезисов (сумул) высших трибуналов.

    Примечание: инструмент совместимости для бразильских судебных данных.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Поиск сумул STF (включая обязательные).

    Args:
        tribunal: Трибунал (stf). По умолчанию: stf.
        query: Фильтр по тексту сумулы (необязательно).

    Returns:
        Список сумул с номером и формулировкой.
    """
    if tribunal.lower() != "stf":
        return "Busca de súmulas atualmente disponível apenas para o STF."

    sumulas = await client.buscar_sumulas_stf(query)
    if not sumulas:
        msg = "Nenhuma súmula encontrada"
        if query:
            msg += f" para '{query}'"
        return msg + "."

    lines = [f"**Súmulas {tribunal.upper()}** ({len(sumulas)} resultados):\n"]
    for s in sumulas:
        vinc = " [VINCULANTE]" if s.vinculante else ""
        lines.append(f"**Súmula {s.numero or '?'}{vinc}**")
        lines.append(f"  {_format_ementa(s.enunciado, 500)}")
        if s.situacao:
            lines.append(f"  Situação: {s.situacao}")
        lines.append("")

    return "\n".join(lines)


async def buscar_repercussao_geral(
    query: str | None = None,
    tema: int | None = None,
) -> str:
    """(legacy) Поиск тем общей реперкуссии STF.

    Примечание: инструмент совместимости для бразильских судебных данных.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Общая реперкуссия — темы, которые STF признаёт значимыми
    и решение по которым применяется ко всем аналогичным делам.

    Args:
        query: Поиск по тексту темы (необязательно).
        tema: Номер конкретной темы (необязательно).

    Returns:
        Список тем с установленным тезисом и статусом.
    """
    temas = await client.buscar_repercussao_geral(query, tema)
    if not temas:
        msg = "Nenhum tema de repercussão geral encontrado"
        if query:
            msg += f" para '{query}'"
        if tema:
            msg += f" (tema {tema})"
        return msg + "."

    lines = [f"**Repercussão Geral STF** ({len(temas)} temas):\n"]
    for t in temas:
        lines.append(f"**Tema {t.numero_tema or '?'}:** {t.titulo or '—'}")
        lines.append(f"  Relator: {t.relator or '—'}")
        lines.append(f"  Leading case: {t.leading_case or '—'}")
        lines.append(f"  Situação: {t.situacao or '—'}")
        if t.tese:
            lines.append(f"  Tese: {_format_ementa(t.tese, 400)}")
        lines.append("")

    return "\n".join(lines)


async def buscar_informativos(
    tribunal: str = "stf",
    query: str | None = None,
) -> str:
    """(legacy) Поиск информационных бюллетеней судебной практики высших трибуналов.

    Примечание: инструмент совместимости для бразильских судебных данных.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Информативы — периодические резюме наиболее важных решений.
    В настоящее время поиск через решения с фильтром по информативу.

    Args:
        tribunal: Трибунал (stf, stj, tst). По умолчанию: stf.
        query: Поисковые термины (необязательно).

    Returns:
        Список релевантных решений информативов.
    """
    search = query or "informativo"
    tribunal_lower = tribunal.lower()

    if tribunal_lower == "stf":
        resultados = await client.buscar_stf(search)
    elif tribunal_lower == "stj":
        resultados = await client.buscar_stj(search)
    elif tribunal_lower == "tst":
        resultados = await client.buscar_tst(search)
    else:
        return f"Tribunal '{tribunal}' não suportado. Use: stf, stj ou tst."

    if not resultados:
        return f"Nenhum informativo encontrado no {tribunal.upper()}."

    lines = [f"**Informativos {tribunal.upper()}** ({len(resultados)} resultados):\n"]
    for i, r in enumerate(resultados, 1):
        lines.append(f"**{i}. {r.classe or ''} {r.numero_processo or ''}**")
        lines.append(f"   Relator: {r.relator or '—'}")
        lines.append(f"   Julgamento: {r.data_julgamento or '—'}")
        lines.append(f"   Ementa: {_format_ementa(r.ementa)}")
        lines.append("")

    return "\n".join(lines)
