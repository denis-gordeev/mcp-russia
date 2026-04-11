"""Tool functions for the ANA feature.

Инструмент совместимости с API Национального агентства водных ресурсов Бразилии (ANA).
Эти инструменты обеспечивают устаревший доступ к бразильским данным
в рамках mcp-russia.

Правила (ADR-001):
    - tools.py НИКОГДА не выполняет HTTP напрямую — делегирует client.py
    - Возвращает отформатированные строки для потребления LLM
"""

from __future__ import annotations

from fastmcp import Context

from mcp_brasil._shared.formatting import format_number_br, markdown_table

from . import client


async def buscar_estacoes(
    ctx: Context,
    codigo_estacao: str | None = None,
    codigo_rio: str | None = None,
    codigo_bacia: str | None = None,
    codigo_sub_bacia: str | None = None,
    nome_estacao: str | None = None,
    tipo_estacao: int | None = None,
) -> str:
    """(legacy) Поиск гидрологических станций ANA в системе Hidroweb.

    Примечание: инструмент совместимости для бразильских данных ANA.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Позволяет искать флювиометрические и плювиометрические станции
    по коду, названию, реке, бассейну или суббассейну.

    Args:
        codigo_estacao: Код станции (напр.: "60435000").
        codigo_rio: Код реки для фильтрации.
        codigo_bacia: Код гидрологического бассейна.
        codigo_sub_bacia: Код суббассейна.
        nome_estacao: Название станции (частичный поиск).
        tipo_estacao: Тип станции (1=Флювиометрическая, 2=Плювиометрическая).

    Returns:
        Таблица с найденными станциями.
    """
    await ctx.info("Buscando estações hidrológicas na ANA...")
    estacoes = await client.buscar_estacoes(
        codigo_estacao=codigo_estacao,
        codigo_rio=codigo_rio,
        codigo_bacia=codigo_bacia,
        codigo_sub_bacia=codigo_sub_bacia,
        nome_estacao=nome_estacao,
        tipo_estacao=tipo_estacao,
    )

    if not estacoes:
        return "Nenhuma estação encontrada para os filtros informados."

    await ctx.info(f"{len(estacoes)} estação(ões) encontrada(s)")

    rows = [
        (
            e.codigo_estacao,
            e.nome_estacao,
            e.nome_rio or "—",
            e.municipio or "—",
            e.estado or "—",
            e.tipo_estacao or "—",
        )
        for e in estacoes
    ]
    header = f"Estações hidrológicas ANA ({len(estacoes)} encontradas):\n\n"
    return header + markdown_table(["Código", "Nome", "Rio", "Município", "UF", "Tipo"], rows)


async def consultar_telemetria(
    ctx: Context,
    codigo_estacao: str,
    data_inicio: str | None = None,
    data_fim: str | None = None,
) -> str:
    """(legacy) Запрос телеметрических данных гидрологической станции ANA.

    Примечание: инструмент совместимости для бразильских данных ANA.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Возвращает показания уровня воды, расхода и осадков (дождя) станции.
    Данные собираются автоматически датчиками в реальном времени.

    Args:
        codigo_estacao: Код станции (напр.: "60435000").
        data_inicio: Начальная дата в формате dd/MM/yyyy (необязательно).
        data_fim: Конечная дата в формате dd/MM/yyyy (необязательно).

    Returns:
        Таблица с телеметрическими данными.
    """
    await ctx.info(f"Consultando telemetria da estação {codigo_estacao}...")
    dados = await client.consultar_telemetria(
        codigo_estacao=codigo_estacao,
        data_inicio=data_inicio,
        data_fim=data_fim,
    )

    if not dados:
        return f"Nenhum dado telemétrico encontrado para a estação {codigo_estacao}."

    await ctx.info(f"{len(dados)} leitura(s) encontrada(s)")

    rows = [
        (
            d.data_hora,
            format_number_br(d.nivel, 2) if d.nivel is not None else "—",
            format_number_br(d.vazao, 1) if d.vazao is not None else "—",
            format_number_br(d.chuva, 1) if d.chuva is not None else "—",
        )
        for d in dados
    ]
    header = f"Telemetria da estação {codigo_estacao} ({len(dados)} leituras):\n\n"
    return header + markdown_table(["Data/Hora", "Nível (cm)", "Vazão (m³/s)", "Chuva (mm)"], rows)


async def monitorar_reservatorios(
    ctx: Context,
    codigo_reservatorio: str | None = None,
    data_inicio: str | None = None,
    data_fim: str | None = None,
) -> str:
    """(legacy) Мониторинг водохранилищ системы SAR Национального агентства водных ресурсов.

    Примечание: инструмент совместимости для бразильских данных ANA.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Возвращает данные о полезном объёме, отметке, притоке и сбросе
    основных водохранилищ Бразилии. Полезно для мониторинга
    гидрологической ситуации и уровня водохранилищ ГЭС.

    Args:
        codigo_reservatorio: Код водохранилища (необязательно).
        data_inicio: Начальная дата в формате dd/MM/yyyy (необязательно).
        data_fim: Конечная дата в формате dd/MM/yyyy (необязательно).

    Returns:
        Таблица с данными водохранилищ.
    """
    await ctx.info("Consultando dados de reservatórios no SAR/ANA...")
    reservatorios = await client.monitorar_reservatorios(
        codigo_reservatorio=codigo_reservatorio,
        data_inicio=data_inicio,
        data_fim=data_fim,
    )

    if not reservatorios:
        return "Nenhum dado de reservatório encontrado para os filtros informados."

    await ctx.info(f"{len(reservatorios)} registro(s) de reservatório(s) encontrado(s)")

    rows = [
        (
            r.nome_reservatorio,
            r.rio or "—",
            r.estado or "—",
            r.data or "—",
            f"{format_number_br(r.volume_util, 1)}%" if r.volume_util is not None else "—",
            format_number_br(r.vazao_afluente, 1) if r.vazao_afluente is not None else "—",
            format_number_br(r.vazao_defluente, 1) if r.vazao_defluente is not None else "—",
        )
        for r in reservatorios
    ]
    header = f"Reservatórios SAR/ANA ({len(reservatorios)} registros):\n\n"
    return header + markdown_table(
        ["Reservatório", "Rio", "UF", "Data", "Vol. Útil", "Afluente (m³/s)", "Defluente (m³/s)"],
        rows,
    )
