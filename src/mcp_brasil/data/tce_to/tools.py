"""Tool functions for the TCE-TO feature.

Инструмент совместимости с API Счётного трибунала штата Токантинс (TCE-TO) Бразилии.
Эти инструменты обеспечивают устаревший доступ к бразильским данным
в рамках mcp-russia.

Правила (ADR-001):
    - tools.py НИКОГДА не выполняет HTTP напрямую — делегирует client.py
    - Возвращает отформатированные строки для потребления LLM
    - Использует Context для структурированного логирования и отчёта о прогрессе
"""

from __future__ import annotations

from fastmcp import Context

from . import client


async def buscar_pessoas_to(
    ctx: Context,
    nome: str | None = None,
    codigo: str | None = None,
) -> str:
    """(legacy) Поиск лиц с процессами в TCE-TO.

    Примечание: инструмент совместимости для бразильских данных TCE-TO.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Поиск по названию или CPF (частичный) в системе e-Contas.
    Возвращает найденных лиц и связанные с ними процессы.
    Необходим хотя бы один фильтр (nome или codigo).

    Args:
        ctx: Контекст MCP.
        nome: Название лица (частичный поиск).
        codigo: CPF (частичный поиск).

    Returns:
        Список лиц со связанными процессами.
    """
    await ctx.info("Buscando pessoas no TCE-TO...")
    pessoas = await client.buscar_pessoas(nome=nome, codigo=codigo)

    if not pessoas:
        return "Nenhuma pessoa encontrada no TCE-TO."

    lines: list[str] = [f"**{len(pessoas)} pessoas encontradas:**\n"]
    for p in pessoas[:10]:
        n_procs = len(p.processos) if p.processos else 0
        lines.append(f"### {p.nome or '—'} (CPF: `{p.codigo or '—'}`)")
        lines.append(f"- **{n_procs} processos**")
        if p.processos:
            for proc in p.processos[:5]:
                lines.append(
                    f"  - `{proc.numero_ano}` — {proc.assunto or '—'} "
                    f"({proc.entidade_origem_municipio or '—'})"
                )
            if len(p.processos) > 5:
                lines.append(f"  - *... e mais {len(p.processos) - 5} processos*")
        lines.append("")

    if len(pessoas) > 10:
        lines.append(f"*Mostrando 10 de {len(pessoas)} pessoas.*")
    return "\n".join(lines)


async def consultar_processo_to(
    ctx: Context,
    numero: int,
    ano: int,
) -> str:
    """(legacy) Запрос подробностей процесса в TCE-TO.

    Примечание: инструмент совместимости для бразильских данных TCE-TO.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Возвращает информацию о процессе: тема, орган-источник,
    текущий департамент, дополнение и распределение.

    Args:
        ctx: Контекст MCP.
        numero: Номер процесса.
        ano: Год процесса.

    Returns:
        Подробные данные процесса.
    """
    await ctx.info(f"Consultando processo {numero}/{ano} no TCE-TO...")
    proc = await client.consultar_processo(numero=numero, ano=ano)

    if not proc:
        return f"Processo {numero}/{ano} não encontrado no TCE-TO."

    lines = [
        f"### Processo {proc.numero_ano or f'{numero}/{ano}'}",
        f"- **Assunto:** {proc.assunto or '—'}",
        f"- **Classe:** {proc.classe_assunto or '—'}",
        f"- **Entidade:** {proc.entidade_origem or '—'}",
        f"- **Município:** {proc.entidade_origem_municipio or '—'}",
        f"- **CNPJ:** {proc.entidade_origem_cnpj or '—'}",
        f"- **Entrada:** {proc.data_entrada or '—'}",
        f"- **Departamento atual:** {proc.departamento_atual or '—'}",
        f"- **Distribuição:** {proc.distribuicao or '—'}",
    ]
    if proc.complemento:
        lines.append(f"- **Complemento:** {proc.complemento[:300]}")
    return "\n".join(lines)


async def listar_pautas_to(
    ctx: Context,
    tamanho: int = 10,
) -> str:
    """(legacy) Список повесток заседаний TCE-TO.

    Примечание: инструмент совместимости для бразильских данных TCE-TO.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Возвращает самые свежие повестки (ординарные, виртуальные,
    видеоконференции) палат и пленума TCE-TO.

    Args:
        ctx: Контекст MCP.
        tamanho: Количество возвращаемых повесток (по умолчанию: 10).

    Returns:
        Список повесток с датой, типом и источником.
    """
    await ctx.info("Buscando pautas de sessões do TCE-TO...")
    pautas = await client.listar_pautas(tamanho=tamanho)

    if not pautas:
        return "Nenhuma pauta encontrada no TCE-TO."

    lines: list[str] = [f"**{len(pautas)} pautas de sessão:**\n"]
    for p in pautas:
        lines.append(f"- **{p.data or '—'}** {p.hora or ''} — {p.tipo or '—'}")
        lines.append(f"  Origem: {p.origem or '—'}")
        if p.url:
            lines.append(f"  [Ver pauta]({p.url})")

    return "\n".join(lines)
