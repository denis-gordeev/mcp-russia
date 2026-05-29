"""Tool functions for IBGE feature.

Ported from mcp-dadosbr/lib/tools/government.ts executeIBGE().
Extended with nomes, agregados, and pesquisas tools.

Rules (ADR-001):
    - tools.py NEVER makes HTTP directly — delegates to client.py
    - Returns formatted strings for LLM consumption
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import format_number_ru, markdown_table, truncate_list

from . import client
from .constants import AGREGADOS_POPULARES, MALHAS_URL


async def listar_estados(ctx: Context) -> str:
    """Список всех 27 бразильских штатов с аббревиатурой, названием и регионом. (legacy)

    Запрос географических данных IBGE (Бразильский институт географии и статистики).
    Эти инструменты обеспечивают устаревший доступ к бразильским
    справочным данным в рамках mcp-russia.
    Полезно для получения аббревиатур штатов, названий штатов и их регионов.

    Returns:
        Таблица со всеми бразильскими штатами.
    """
    await ctx.info("Buscando estados brasileiros...")
    estados = await client.listar_estados()
    await ctx.info(f"{len(estados)} estados encontrados")
    rows = [(e.sigla, e.nome, e.regiao.nome) for e in estados]
    return markdown_table(["UF", "Nome", "Região"], rows)


async def buscar_municipios(uf: str, ctx: Context) -> str:
    """Поиск всех муниципалитетов штата по его аббревиатуре. (legacy)

    Возвращает список муниципалитетов с кодом IBGE и названием.
    Эти инструменты обеспечивают устаревший доступ к бразильским
    справочным данным в рамках mcp-russia.
    В Бразилии ~5570 муниципалитетов, распределённых по 27 штатам.

    Args:
        uf: Аббревиатура штата из 2 букв (напр.: SP, RJ, PI, BA).

    Returns:
        Список муниципалитетов штата.
    """
    await ctx.info(f"Buscando municípios de {uf.upper()}...")
    municipios = await client.listar_municipios(uf)
    await ctx.info(f"{len(municipios)} municípios encontrados")
    items = [f"{m.id} — {m.nome}" for m in municipios]
    header = f"Municípios de {uf.upper()} ({len(municipios)} encontrados):\n\n"
    return header + truncate_list(items, max_items=100)


async def listar_regioes(ctx: Context) -> str:
    """Список 5 макрорегионов Бразилии. (legacy)

    Регионы: Norte (Север), Nordeste (Северо-Восток), Centro-Oeste (Центрально-Западный),
    Sudeste (Юго-Восток), Sul (Юг).
    Эти инструменты обеспечивают устаревший доступ к бразильским
    справочным данным в рамках mcp-russia.

    Returns:
        Таблица с бразильскими регионами.
    """
    await ctx.info("Buscando regiões brasileiras...")
    regioes = await client.listar_regioes()
    rows = [(r.sigla, r.nome) for r in regioes]
    return markdown_table(["Sigla", "Região"], rows)


async def consultar_nome(nome: str, ctx: Context) -> str:
    """Запрос частоты встречаемости имени по десятилетиям в Бразилии. (legacy)

    Данные демографической переписи IBGE (Бразильский институт географии и статистики).
    Эти инструменты обеспечивают устаревший доступ к бразильским
    справочным данным в рамках mcp-russia.
    Показывает, сколько людей было зарегистрировано с этим именем в каждый 10-летний период
    (с 1930 по 2010 год).

    Args:
        nome: Имя для запроса (напр.: João, Maria, Pedro).

    Returns:
        Динамика частоты встречаемости имени по десятилетиям.
    """
    await ctx.info(f"Consultando frequência do nome '{nome}'...")
    resultados = await client.consultar_nome(nome)
    if not resultados:
        return f"Nome '{nome}' não encontrado nos dados do IBGE."

    lines: list[str] = []
    for item in resultados:
        lines.append(f"Nome: {item.nome}")
        if item.sexo:
            lines.append(f"Sexo: {item.sexo}")
        rows = [(r.periodo, f"{r.frequencia:,}".replace(",", ".")) for r in item.res]
        lines.append(markdown_table(["Período", "Frequência"], rows))
        lines.append("")

    return "\n".join(lines)


async def ranking_nomes(
    ctx: Context, localidade: str | None = None, sexo: str | None = None
) -> str:
    """Рейтинг самых популярных имён в Бразилии. (legacy)

    Данные демографической переписи IBGE (Бразильский институт географии и статистики).
    Эти инструменты обеспечивают устаревший доступ к бразильским
    справочным данным в рамках mcp-russia.
    Возможна фильтрация по штату или муниципалитету (с использованием кода IBGE) и по полу.

    Args:
        localidade: Код IBGE штата или муниципалитета (необязательно).
                    Напр.: "33" для RJ, "3550308" для Сан-Паулу.
        sexo: Фильтр по полу: "M" — мужской, "F" — женский (необязательно).

    Returns:
        Рейтинг самых часто встречающихся имён.
    """
    await ctx.info("Buscando ranking de nomes...")
    resultados = await client.ranking_nomes(localidade=localidade, sexo=sexo)
    if not resultados:
        return "Nenhum resultado encontrado para o ranking de nomes."

    lines: list[str] = []
    for item in resultados:
        rows = [(str(r.ranking), r.nome, f"{r.frequencia:,}".replace(",", ".")) for r in item.res]
        lines.append(markdown_table(["#", "Nome", "Frequência"], rows))

    return "\n".join(lines)


async def consultar_agregado(
    ctx: Context,
    indicador: str = "",
    agregado_id: int = 0,
    variavel_id: int = 0,
    nivel: str = "estado",
    localidade: str = "all",
    periodos: str = "-6",
) -> str:
    """Запрос агрегированных данных исследований IBGE. (legacy)

    Эти инструменты обеспечивают устаревший доступ к бразильским
    справочным данным в рамках mcp-russia.
    Позволяет получать такие показатели, как население, ВВП, ВВП на душу населения
    и площадь территории по штатам, муниципалитетам или регионам.

    Для общих показателей используйте параметр 'indicador':
    - "populacao": предполагаемая численность населения
    - "pib": валовой внутренний продукт (ВВП)
    - "pib_per_capita": ВВП на душу населения (только национальный уровень)
    - "area_territorial": площадь территории в км²

    Для других агрегатов укажите agregado_id и variavel_id напрямую.
    Используйте инструмент listar_pesquisas() для поиска доступных идентификаторов.

    Args:
        indicador: Сокращение для общих показателей
            (populacao, pib, pib_per_capita, area_territorial).
        agregado_id: ID агрегата IBGE (используется, если indicador не указан).
        variavel_id: ID переменной внутри агрегата.
        nivel: Территориальный уровень: pais, regiao, estado, municipio.
        localidade: Код IBGE или "all" для всех.
        periodos: Периоды для запроса ("-6" для последних 6, "2020|2021" и т.д.).

    Returns:
        Таблица с агрегированными данными.
    """
    if indicador and indicador in AGREGADOS_POPULARES:
        info = AGREGADOS_POPULARES[indicador]
        agregado_id = int(info["id"])
        variavel_id = int(info["variavel"])
        # PIB per capita (tabela 6784) só está disponível em nível nacional (N1)
        if indicador == "pib_per_capita" and nivel != "pais":
            nivel = "pais"
            localidade = "all"
            await ctx.warning(
                "PIB per capita só está disponível em nível nacional. Ajustando para nível 'pais'."
            )

    if not agregado_id or not variavel_id:
        indicadores_disponiveis = ", ".join(AGREGADOS_POPULARES.keys())
        return f"Informe 'indicador' ({indicadores_disponiveis}) ou 'agregado_id' + 'variavel_id'."

    await ctx.info(f"Consultando agregado {agregado_id}, variável {variavel_id}...")
    resultados = await client.consultar_agregado(
        agregado_id=agregado_id,
        variavel_id=variavel_id,
        nivel=nivel,
        localidade=localidade,
        periodos=periodos,
    )

    if not resultados:
        return "Nenhum dado encontrado para os parâmetros informados."

    rows = [(r.localidade_nome, r.valor or "—") for r in resultados]
    titulo = ""
    if indicador and indicador in AGREGADOS_POPULARES:
        titulo = f"{AGREGADOS_POPULARES[indicador]['descricao']}\n\n"

    return titulo + markdown_table(["Localidade", "Valor"], rows)


async def listar_pesquisas(ctx: Context) -> str:
    """Список доступных исследований и агрегатов IBGE. (legacy)

    Эти инструменты обеспечивают устаревший доступ к бразильским
    справочным данным в рамках mcp-russia.
    Возвращает идентификаторы исследований и агрегатов, которые можно использовать
    с инструментом consultar_agregado(). Полезно для обнаружения доступных
    статистических данных.

    Returns:
        Список исследований с их агрегатами.
    """
    await ctx.info("Listando pesquisas disponíveis no IBGE...")
    pesquisas = await client.listar_pesquisas()
    if not pesquisas:
        return "Nenhuma pesquisa encontrada."

    lines: list[str] = []
    for p in pesquisas[:30]:
        lines.append(f"**{p.get('id', '')}** — {p.get('nome', '')}")
        for ag in p.get("agregados", [])[:3]:
            lines.append(f"  - Agregado {ag.get('id', '')}: {ag.get('nome', '')}")

    if len(pesquisas) > 30:
        lines.append(f"\n... e mais {len(pesquisas) - 30} pesquisas.")

    return "\n".join(lines)


async def obter_malha(codigo: str, ctx: Context) -> str:
    """Получение географических метаданных региона Бразилии. (legacy)

    Эти инструменты обеспечивают устаревший доступ к бразильским
    справочным данным в рамках mcp-russia.
    Возвращает центроид, площадь территории, ограничивающий прямоугольник и URL для скачивания
    GeoJSON-файла географической основы. Принимает код IBGE штата, муниципалитета или региона.

    Args:
        codigo: Код IBGE региона (напр.: "35" для SP, "3550308" для
                Сан-Паулу, "3" для региона Sudeste, "BR" для Бразилии).

    Returns:
        Географические метаданные региона.
    """
    await ctx.info(f"Buscando metadados geográficos para {codigo}...")
    meta = await client.buscar_malha_metadados(codigo)

    lines = [
        f"**Malha {meta.id}** — {meta.nivel_geografico}",
        f"- Centroide: {meta.centroide_lat:.4f}, {meta.centroide_lon:.4f}",
    ]

    if meta.area_km2:
        lines.append(f"- Área: {format_number_ru(meta.area_km2, 2)} km²")

    if meta.bbox_min_lon is not None:
        lines.append(
            f"- Bounding box: ({meta.bbox_min_lat:.4f}, {meta.bbox_min_lon:.4f}) "
            f"a ({meta.bbox_max_lat:.4f}, {meta.bbox_max_lon:.4f})"
        )

    geojson_url = f"{MALHAS_URL}/{codigo}?formato=application/vnd.geo+json&resolucao=5"
    lines.append(f"- GeoJSON (baixa resolução): {geojson_url}")

    return "\n".join(lines)


async def buscar_cnae(ctx: Context, codigo: str | None = None) -> str:
    """Поиск информации CNAE (Национальная классификация экономических деятельностей). (legacy)

    Эти инструменты обеспечивают устаревший доступ к бразильским
    справочным данным в рамках mcp-russia.
    Если указан код, возвращает полную иерархию подкласса
    (секция -> раздел -> группа -> класс -> подкласс) со списком деятельностей.
    Без кода перечисляет все 21 секцию CNAE.

    Полезно для классификации предприятий и понимания экономических деятельностей.

    Args:
        codigo: Код подкласса CNAE (напр.: "6201501" для разработки
                программного обеспечения, "9430800" для защиты прав). Необязательно.

    Returns:
        Иерархия CNAE или список секций.
    """
    if not codigo:
        await ctx.info("Listando seções CNAE...")
        secoes = await client.listar_cnae_secoes()
        rows = [(s.id, s.descricao.title()) for s in secoes]
        return "**Seções CNAE (21 categorias)**\n\n" + markdown_table(["Seção", "Descrição"], rows)

    await ctx.info(f"Buscando CNAE {codigo}...")
    cnae = await client.buscar_cnae_subclasse(codigo)

    lines = [
        f"**CNAE {cnae.id}** — {cnae.descricao.title()}",
        "",
        "**Hierarquia:**",
        f"- Seção {cnae.secao_id}: {cnae.secao_descricao.title()}",
        f"  - Divisão {cnae.divisao_id}: {cnae.divisao_descricao.title()}",
        f"    - Grupo {cnae.grupo_id}: {cnae.grupo_descricao.title()}",
        f"      - Classe {cnae.classe_id}: {cnae.classe_descricao.title()}",
    ]

    if cnae.atividades:
        lines.append("")
        lines.append(f"**Atividades ({len(cnae.atividades)}):**")
        for a in cnae.atividades[:15]:
            lines.append(f"- {a.strip().title()}")
        if len(cnae.atividades) > 15:
            lines.append(f"... e mais {len(cnae.atividades) - 15} atividades.")

    return "\n".join(lines)
