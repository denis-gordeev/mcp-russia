"""Tool functions for the DataJud (CNJ) feature.

Инструмент совместимости с API DataJud Национального совета юстиции Бразилии (CNJ).
Эти инструменты обеспечивают устаревший доступ к бразильским данным
в рамках mcp-russia.

Правила (ADR-001):
    - tools.py НИКОГДА не выполняет HTTP напрямую — делегирует client.py
    - Возвращает отформатированные строки для потребления LLM
"""

from __future__ import annotations

import contextlib

from mcp_russia._shared.formatting import markdown_table

from . import client
from .constants import DEFAULT_PAGE_SIZE


async def buscar_processos(
    query: str,
    tribunal: str = "tjsp",
    tamanho: int = DEFAULT_PAGE_SIZE,
) -> str:
    """(legacy) Поиск судебных процессов в публичном API DataJud (CNJ).

    Примечание: инструмент совместимости для бразильских судебных данных.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Поиск по свободному тексту: CPF, CNPJ, имя стороны, номер процесса
    или любой термин, связанный с процессом.

    Требуется переменная окружения DATAJUD_API_KEY.
    Регистрация: https://datajud.cnj.jus.br

    Args:
        query: Поисковый термин (CPF, CNPJ, имя, номер процесса).
        tribunal: Аббревиатура трибунала (напр.: tjsp, trf1, stj). По умолчанию: tjsp.
        tamanho: Максимальное количество результатов (1-100). По умолчанию: 10.

    Returns:
        Таблица с найденными процессами.
    """
    processos = await client.buscar_processos(query, tribunal, tamanho)
    if not processos:
        return f"Nenhum processo encontrado para '{query}' no {tribunal.upper()}."

    rows = [
        (
            (p.numero or "—")[:25],
            (p.classe or "—")[:30],
            (p.assunto or "—")[:30],
            (p.orgao_julgador or "—")[:25],
            (p.data_ajuizamento or "—")[:10],
        )
        for p in processos
    ]
    header = f"Processos encontrados no {tribunal.upper()} ({len(processos)} resultados):\n\n"
    return header + markdown_table(
        ["Número", "Classe", "Assunto", "Órgão Julgador", "Ajuizamento"], rows
    )


async def buscar_processo_por_numero(
    numero_processo: str,
    tribunal: str = "tjsp",
) -> str:
    """(legacy) Поиск конкретного процесса по унифицированному номеру (NPU).

    Примечание: инструмент совместимости для бразильских судебных данных.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Возвращает полные данные, включая стороны, темы и движения.

    Args:
        numero_processo: Номер процесса (свободный формат, напр.: 0001234-56.2024.8.26.0100).
        tribunal: Аббревиатура трибунала (напр.: tjsp, trf1, stj). По умолчанию: tjsp.

    Returns:
        Подробные данные процесса со сторонами и движениями.
    """
    detalhe = await client.buscar_processo_por_numero(numero_processo, tribunal)
    if detalhe is None:
        return f"Processo '{numero_processo}' não encontrado no {tribunal.upper()}."

    lines = [
        f"**Processo:** {detalhe.numero or '—'}",
        f"**Classe:** {detalhe.classe or '—'}",
        f"**Tribunal:** {detalhe.tribunal or tribunal.upper()}",
        f"**Órgão Julgador:** {detalhe.orgao_julgador or '—'}",
        f"**Ajuizamento:** {detalhe.data_ajuizamento or '—'}",
        f"**Última atualização:** {detalhe.data_ultima_atualizacao or '—'}",
        f"**Grau:** {detalhe.grau or '—'}",
    ]

    # Assuntos
    if detalhe.assuntos:
        assuntos = [a.nome or "—" for a in detalhe.assuntos]
        lines.append(f"\n**Assuntos:** {', '.join(assuntos)}")

    # Partes
    if detalhe.partes:
        lines.append("\n**Partes:**")
        for parte in detalhe.partes[:20]:
            lines.append(f"  - [{parte.polo or '—'}] {parte.nome or '—'}")

    # Movimentações (últimas 10)
    if detalhe.movimentacoes:
        lines.append(f"\n**Últimas movimentações** ({len(detalhe.movimentacoes)}):")
        for mov in detalhe.movimentacoes[:10]:
            data = (mov.data or "—")[:10]
            nome = mov.nome or "—"
            lines.append(f"  - {data}: {nome}")

    return "\n".join(lines)


async def buscar_processos_por_classe(
    classe: str,
    tribunal: str = "tjsp",
    tamanho: int = DEFAULT_PAGE_SIZE,
) -> str:
    """(legacy) Поиск процессов по процессуальному классу.

    Примечание: инструмент совместимости для бразильских судебных данных.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Примеры классов: Ação Civil Pública, Mandado de Segurança,
    Habeas Corpus, Execução Fiscal, Recurso Extraordinário.

    Args:
        classe: Название процессуального класса (напр.: Mandado de Segurança).
        tribunal: Аббревиатура трибунала. По умолчанию: tjsp.
        tamanho: Максимальное количество результатов (1-100). По умолчанию: 10.

    Returns:
        Таблица с процессами указанного класса.
    """
    processos = await client.buscar_processos_por_classe(classe, tribunal, tamanho)
    if not processos:
        return f"Nenhum processo da classe '{classe}' encontrado no {tribunal.upper()}."

    rows = [
        (
            (p.numero or "—")[:25],
            (p.assunto or "—")[:35],
            (p.orgao_julgador or "—")[:25],
            (p.data_ajuizamento or "—")[:10],
        )
        for p in processos
    ]
    header = f"Processos — {classe} — {tribunal.upper()} ({len(processos)} resultados):\n\n"
    return header + markdown_table(["Número", "Assunto", "Órgão Julgador", "Ajuizamento"], rows)


async def buscar_processos_por_assunto(
    assunto: str,
    tribunal: str = "tjsp",
    tamanho: int = DEFAULT_PAGE_SIZE,
) -> str:
    """(legacy) Поиск процессов по теме/предмету.

    Примечание: инструмент совместимости для бразильских судебных данных.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Примеры: Direito do Consumidor, Direito Ambiental, Dano Moral,
    Execução de Título Extrajudicial.

    Args:
        assunto: Тема или предмет процесса.
        tribunal: Аббревиатура трибунала. По умолчанию: tjsp.
        tamanho: Максимальное количество результатов (1-100). По умолчанию: 10.

    Returns:
        Таблица с процессами по указанной теме.
    """
    processos = await client.buscar_processos_por_assunto(assunto, tribunal, tamanho)
    if not processos:
        return f"Nenhum processo sobre '{assunto}' encontrado no {tribunal.upper()}."

    rows = [
        (
            (p.numero or "—")[:25],
            (p.classe or "—")[:25],
            (p.orgao_julgador or "—")[:25],
            (p.data_ajuizamento or "—")[:10],
        )
        for p in processos
    ]
    header = (
        f"Processos — assunto: {assunto} — {tribunal.upper()} ({len(processos)} resultados):\n\n"
    )
    return header + markdown_table(["Número", "Classe", "Órgão Julgador", "Ajuizamento"], rows)


async def buscar_processos_por_orgao(
    orgao_julgador: str,
    tribunal: str = "tjsp",
    tamanho: int = DEFAULT_PAGE_SIZE,
) -> str:
    """(legacy) Поиск процессов по судебному органу (суд, палата, коллегия).

    Примечание: инструмент совместимости для бразильских судебных данных.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Примеры: 1ª Vara Cível, 3ª Câmara de Direito Privado, 1ª Turma Recursal.

    Args:
        orgao_julgador: Название судебного органа.
        tribunal: Аббревиатура трибунала. По умолчанию: tjsp.
        tamanho: Максимальное количество результатов (1-100). По умолчанию: 10.

    Returns:
        Таблица с процессами указанного органа.
    """
    processos = await client.buscar_processos_por_orgao(orgao_julgador, tribunal, tamanho)
    if not processos:
        return f"Nenhum processo encontrado no órgão '{orgao_julgador}' do {tribunal.upper()}."

    rows = [
        (
            (p.numero or "—")[:25],
            (p.classe or "—")[:25],
            (p.assunto or "—")[:30],
            (p.data_ajuizamento or "—")[:10],
        )
        for p in processos
    ]
    header = (
        f"Processos — {orgao_julgador} — {tribunal.upper()} ({len(processos)} resultados):\n\n"
    )
    return header + markdown_table(["Número", "Classe", "Assunto", "Ajuizamento"], rows)


async def buscar_processos_avancado(
    tribunal: str = "tjsp",
    classe_codigo: int | None = None,
    orgao_codigo: int | None = None,
    tamanho: int = DEFAULT_PAGE_SIZE,
    search_after: str | None = None,
) -> str:
    """(legacy) Расширенный поиск процессов с фильтрацией по коду и пагинацией.

    Примечание: инструмент совместимости для бразильских судебных данных.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Позволяет комбинировать фильтры (процессуальный класс + судебный орган)
    и paginate большие результаты через search_after (курсор Elasticsearch).

    Используйте процессуальные классы из ресурса data://classes-processuais
    и коды органов из поля orgaoJulgador.codigo.

    Для пагинации: передайте значение search_after из предыдущего ответа.

    Args:
        tribunal: Аббревиатура трибунала (напр.: tjsp, trf1, tjdft). По умолчанию: tjsp.
        classe_codigo: Код процессуального класса (напр.: 1116 = Execução Fiscal).
        orgao_codigo: Код судебного органа (напр.: 13597).
        tamanho: Количество результатов на страницу (1-10000). По умолчанию: 10.
        search_after: Токен пагинации, возвращённый предыдущим запросом.

    Returns:
        Таблица с процессами и токеном для следующей страницы.
    """
    token: list[int] | None = None
    if search_after is not None:
        with contextlib.suppress(ValueError, TypeError):
            token = [int(search_after)]

    processos, next_token = await client.buscar_processos_avancado(
        tribunal=tribunal,
        classe_codigo=classe_codigo,
        orgao_codigo=orgao_codigo,
        tamanho=tamanho,
        search_after=token,
    )

    if not processos:
        return f"Nenhum processo encontrado no {tribunal.upper()} com os filtros informados."

    rows = [
        (
            (p.numero or "—")[:25],
            (p.classe or "—")[:30],
            (p.assunto or "—")[:30],
            (p.orgao_julgador or "—")[:25],
            (p.data_ajuizamento or "—")[:10],
        )
        for p in processos
    ]
    header = f"Processos — {tribunal.upper()} ({len(processos)} resultados):\n\n"
    table = markdown_table(["Número", "Classe", "Assunto", "Órgão Julgador", "Ajuizamento"], rows)

    pagination = ""
    if next_token:
        pagination = f'\n\n**Próxima página:** use search_after="{next_token[0]}"'

    return header + table + pagination


async def consultar_movimentacoes(
    numero_processo: str,
    tribunal: str = "tjsp",
) -> str:
    """(legacy) Запрос движений судебного процесса.

    Примечание: инструмент совместимости для бразильских судебных данных.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Возвращает историю движений (распоряжения, решения, слушания и т.д.).

    Args:
        numero_processo: Номер процесса (свободный формат).
        tribunal: Аббревиатура трибунала. По умолчанию: tjsp.

    Returns:
        Хронологический список движений.
    """
    movimentacoes = await client.consultar_movimentacoes(numero_processo, tribunal)
    if not movimentacoes:
        return (
            f"Nenhuma movimentação encontrada para o processo '{numero_processo}' "
            f"no {tribunal.upper()}."
        )

    rows = [
        (
            (m.data or "—")[:10],
            (m.nome or "—")[:40],
            (m.complemento or "—")[:40],
        )
        for m in movimentacoes
    ]
    header = (
        f"Movimentações do processo {numero_processo} — {tribunal.upper()} "
        f"({len(movimentacoes)} movimentações):\n\n"
    )
    return header + markdown_table(["Data", "Movimentação", "Complemento"], rows)
