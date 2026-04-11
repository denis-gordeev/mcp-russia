"""Tool functions for the Dados Abertos Compras.gov.br feature.

Инструмент совместимости с API открытых данных Compras.gov.br Бразилии.
Эти инструменты обеспечивают устаревший доступ к бразильским данным
в рамках mcp-russia.

Правила (ADR-001):
    - tools.py НИКОГДА не выполняет HTTP напрямую — делегирует client.py
    - Возвращает отформатированные строки для потребления LLM
"""

from __future__ import annotations

from fastmcp import Context

from mcp_brasil._shared.formatting import format_brl

from . import client


async def buscar_licitacoes(
    data_publicacao_inicial: str,
    data_publicacao_final: str,
    ctx: Context,
    uasg: int | None = None,
    modalidade: int | None = None,
    pagina: int = 1,
) -> str:
    """(legacy) Поиск закупок в устаревшей системе SIASG/ComprasNet (до 2020).

    Примечание: инструмент совместимости для бразильских данных госзакупок.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Поиск федеральных закупок по периоду публикации. Исторические данные
    SIASG (Интегрированная система управления услугами).

    Args:
        data_publicacao_inicial: Начальная дата публикации YYYY-MM-DD (обязательно).
        data_publicacao_final: Конечная дата публикации YYYY-MM-DD (обязательно).
        uasg: Код UASG органа (необязательно).
        modalidade: Код модальности (1=Приглашение, 2=Запрос цен,
            3=Конкурс, 5=Аукцион, 6=Отказ, 7=Необязательность).
        pagina: Страница результатов (по умолчанию 1).

    Returns:
        Список найденных закупок с объектом, стоимостью и статусом.
    """
    await ctx.info(
        f"Buscando licitações de {data_publicacao_inicial} a {data_publicacao_final}..."
    )
    resultado = await client.buscar_licitacoes(
        data_publicacao_inicial=data_publicacao_inicial,
        data_publicacao_final=data_publicacao_final,
        uasg=uasg,
        modalidade=modalidade,
        pagina=pagina,
    )
    await ctx.info(f"{resultado.total} licitações encontradas")

    if not resultado.licitacoes:
        return "Nenhuma licitação encontrada no período informado."

    lines = [f"**Total:** {resultado.total} licitações\n"]
    for i, lic in enumerate(resultado.licitacoes, 1):
        val_est = format_brl(lic.valor_estimado_total) if lic.valor_estimado_total else "N/A"
        val_hom = format_brl(lic.valor_homologado_total) if lic.valor_homologado_total else "N/A"
        lines.extend(
            [
                f"### {i}. {lic.objeto or 'Sem descrição'}",
                f"**UASG:** {lic.uasg or 'N/A'} | **Modalidade:** {lic.nome_modalidade or 'N/A'}",
                f"**Situação:** {lic.situacao_aviso or 'N/A'}",
                f"**Valor estimado:** {val_est} | **Homologado:** {val_hom}",
                f"**Publicação:** {lic.data_publicacao or 'N/A'}",
                f"**Itens:** {lic.numero_itens or 'N/A'}",
                "",
            ]
        )

    if resultado.total > len(resultado.licitacoes):
        lines.append(f"*Use pagina={pagina + 1} para mais resultados.*")
    return "\n".join(lines)


async def buscar_pregoes(
    data_edital_inicial: str,
    data_edital_final: str,
    ctx: Context,
    co_uasg: int | None = None,
    pagina: int = 1,
) -> str:
    """(legacy) Поиск электронных аукционов в SIASG/ComprasNet.

    Примечание: инструмент совместимости для бразильских данных госзакупок.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Аукционы — наиболее используемая модальность для приобретения товаров
    и услуг федеральным правительством.

    Args:
        data_edital_inicial: Начальная дата извещения YYYY-MM-DD (обязательно).
        data_edital_final: Конечная дата извещения YYYY-MM-DD (обязательно).
        co_uasg: Код UASG органа (необязательно).
        pagina: Страница результатов (по умолчанию 1).

    Returns:
        Список найденных аукционов.
    """
    await ctx.info(f"Buscando pregões de {data_edital_inicial} a {data_edital_final}...")
    resultado = await client.buscar_pregoes(
        data_edital_inicial=data_edital_inicial,
        data_edital_final=data_edital_final,
        co_uasg=co_uasg,
        pagina=pagina,
    )
    await ctx.info(f"{resultado.total} pregões encontrados")

    if not resultado.licitacoes:
        return "Nenhum pregão encontrado no período informado."

    lines = [f"**Total:** {resultado.total} pregões\n"]
    for i, lic in enumerate(resultado.licitacoes, 1):
        val_est = format_brl(lic.valor_estimado_total) if lic.valor_estimado_total else "N/A"
        val_hom = format_brl(lic.valor_homologado_total) if lic.valor_homologado_total else "N/A"
        lines.extend(
            [
                f"### {i}. {lic.objeto or 'Sem descrição'}",
                f"**UASG:** {lic.uasg or 'N/A'} | **Tipo:** {lic.tipo_pregao or 'N/A'}",
                f"**Situação:** {lic.situacao_aviso or 'N/A'}",
                f"**Valor estimado:** {val_est} | **Homologado:** {val_hom}",
                f"**Publicação:** {lic.data_publicacao or 'N/A'}",
                "",
            ]
        )

    if resultado.total > len(resultado.licitacoes):
        lines.append(f"*Use pagina={pagina + 1} para mais resultados.*")
    return "\n".join(lines)


async def buscar_dispensas(
    ano_aviso: int,
    ctx: Context,
    co_uasg: int | None = None,
    pagina: int = 1,
) -> str:
    """(legacy) Поиск закупок без торгов (отказы и необязательности).

    Примечание: инструмент совместимости для бразильских данных госзакупок.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Отказы — закупки, осуществляемые без конкурентных процедур, согласно
    законодательным положениям (ст. 24 Закона 8.666/93 или ст. 75 Закона 14.133/2021).

    Args:
        ano_aviso: Год извещения об отказе (обязательно, напр.: 2020).
        co_uasg: Код UASG органа (необязательно).
        pagina: Страница результатов (по умолчанию 1).

    Returns:
        Список найденных закупок без торгов.
    """
    await ctx.info(f"Buscando dispensas do ano {ano_aviso}...")
    resultado = await client.buscar_dispensas(
        ano_aviso=ano_aviso,
        co_uasg=co_uasg,
        pagina=pagina,
    )
    await ctx.info(f"{resultado.total} dispensas encontradas")

    if not resultado.licitacoes:
        return f"Nenhuma dispensa encontrada para o ano {ano_aviso}."

    lines = [f"**Total:** {resultado.total} dispensas\n"]
    for i, lic in enumerate(resultado.licitacoes, 1):
        val_est = format_brl(lic.valor_estimado_total) if lic.valor_estimado_total else "N/A"
        lines.extend(
            [
                f"### {i}. {lic.objeto or 'Sem descrição'}",
                f"**UASG:** {lic.uasg or 'N/A'} | **Modalidade:** {lic.nome_modalidade or 'N/A'}",
                f"**Valor estimado:** {val_est}",
                f"**Publicação:** {lic.data_publicacao or 'N/A'}",
                "",
            ]
        )

    if resultado.total > len(resultado.licitacoes):
        lines.append(f"*Use pagina={pagina + 1} para mais resultados.*")
    return "\n".join(lines)


async def buscar_contratos(
    data_vigencia_inicial_min: str,
    data_vigencia_inicial_max: str,
    ctx: Context,
    codigo_orgao: str | None = None,
    ni_fornecedor: str | None = None,
    pagina: int = 1,
) -> str:
    """(legacy) Поиск контрактов в Compras.gov.br (Открытые данные).

    Примечание: инструмент совместимости для бразильских данных госзакупок.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Запрос федеральных контрактов по периоду действия. Включает полные
    данные: орган, поставщик, объект, стоимость и срок.

    Args:
        data_vigencia_inicial_min: Минимальное начало действия YYYY-MM-DD (обязательно).
        data_vigencia_inicial_max: Максимальное начало действия YYYY-MM-DD (обязательно).
        codigo_orgao: Код органа (необязательно).
        ni_fornecedor: CNPJ/CPF поставщика (необязательно).
        pagina: Страница результатов (по умолчанию 1).

    Returns:
        Список найденных контрактов.
    """
    await ctx.info("Buscando contratos...")
    resultado = await client.buscar_contratos(
        data_vigencia_inicial_min=data_vigencia_inicial_min,
        data_vigencia_inicial_max=data_vigencia_inicial_max,
        codigo_orgao=codigo_orgao,
        ni_fornecedor=ni_fornecedor,
        pagina=pagina,
    )
    await ctx.info(f"{resultado.total} contratos encontrados")

    if not resultado.contratos:
        return "Nenhum contrato encontrado no período informado."

    lines = [f"**Total:** {resultado.total} contratos\n"]
    for i, c in enumerate(resultado.contratos, 1):
        valor = format_brl(c.valor_global) if c.valor_global else "N/A"
        lines.extend(
            [
                f"### {i}. {c.objeto or 'Sem descrição'}",
                f"**Órgão:** {c.nome_orgao or 'N/A'}",
                f"**Fornecedor:** {c.nome_fornecedor or 'N/A'} ({c.ni_fornecedor or 'N/A'})",
                f"**Contrato nº:** {c.numero_contrato or 'N/A'}",
                f"**Modalidade:** {c.nome_modalidade_compra or 'N/A'}"
                f" | **Tipo:** {c.nome_tipo or 'N/A'}",
                f"**Valor global:** {valor}",
                f"**Vigência:** {c.data_vigencia_inicial or 'N/A'}"
                f" a {c.data_vigencia_final or 'N/A'}",
                "",
            ]
        )

    if resultado.total > len(resultado.contratos):
        lines.append(f"*Use pagina={pagina + 1} para mais resultados.*")
    return "\n".join(lines)


async def consultar_fornecedor(
    ctx: Context,
    cnpj: str | None = None,
    cpf: str | None = None,
    pagina: int = 1,
) -> str:
    """(legacy) Запрос поставщиков, зарегистрированных в Compras.gov.br.

    Примечание: инструмент совместимости для бразильских данных госзакупок.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Поиск данных поставщиков, участвующих в федеральных закупках.
    Необходим хотя бы один фильтр (CNPJ или CPF).

    Args:
        cnpj: CNPJ поставщика (необязательно).
        cpf: CPF поставщика-физлица (необязательно).
        pagina: Страница результатов (по умолчанию 1).

    Returns:
        Данные найденного поставщика.
    """
    if not any([cnpj, cpf]):
        return "Informe pelo menos um filtro: cnpj ou cpf."

    desc = cnpj or cpf or "fornecedor"
    await ctx.info(f"Consultando fornecedor {desc}...")
    resultado = await client.consultar_fornecedor(cnpj=cnpj, cpf=cpf, pagina=pagina)
    await ctx.info(f"{resultado.total} fornecedor(es) encontrado(s)")

    if not resultado.fornecedores:
        return f"Nenhum fornecedor encontrado para {desc}."

    lines: list[str] = []
    for f in resultado.fornecedores:
        ident = f.cnpj or f.cpf or "N/A"
        lines.extend(
            [
                f"**{f.nome_razao_social or 'N/A'}**",
                f"**CNPJ/CPF:** {ident}",
                f"**Local:** {f.nome_municipio or 'N/A'}/{f.uf_sigla or 'N/A'}",
                f"**Porte:** {f.porte_empresa_nome or 'N/A'}",
                f"**CNAE:** {f.nome_cnae or 'N/A'}",
                f"**Ativo:** {'Sim' if f.ativo else 'Não'}"
                f" | **Habilitado:** {'Sim' if f.habilitado_licitar else 'Não'}",
                "",
            ]
        )
    return "\n".join(lines)


async def buscar_material_catmat(
    ctx: Context,
    descricao: str | None = None,
    codigo_grupo: int | None = None,
    codigo_classe: int | None = None,
    pagina: int = 1,
) -> str:
    """(legacy) Поиск позиций в каталоге CATMAT (материалы федерального правительства).

    Примечание: инструмент совместимости для бразильских данных госзакупок.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    CATMAT — Каталог материалов, используемый федеральным правительством
    для классификации и стандартизации приобретения материалов (товаров).

    Args:
        descricao: Описание материала (необязательно).
        codigo_grupo: Код группы CATMAT (необязательно, напр.: 70=ТИК, 65=Здравоохранение).
        codigo_classe: Код класса CATMAT (необязательно).
        pagina: Страница результатов (по умолчанию 1).

    Returns:
        Список найденных материалов каталога.
    """
    if not any([descricao, codigo_grupo, codigo_classe]):
        return "Informe pelo menos um filtro: descricao, codigo_grupo ou codigo_classe."

    desc = descricao or f"grupo {codigo_grupo}" if codigo_grupo else "material"
    await ctx.info(f"Buscando material CATMAT '{desc}'...")
    resultado = await client.buscar_material(
        descricao=descricao,
        codigo_grupo=codigo_grupo,
        codigo_classe=codigo_classe,
        pagina=pagina,
    )
    await ctx.info(f"{resultado.total} materiais encontrados")

    if not resultado.itens:
        return f"Nenhum material encontrado para '{desc}'."

    lines = [f"**Total:** {resultado.total} materiais\n"]
    for i, item in enumerate(resultado.itens, 1):
        status = "Ativo" if item.status_item else "Inativo"
        lines.extend(
            [
                f"### {i}. {item.descricao_item or 'Sem descrição'}",
                f"**Código:** {item.codigo_item or 'N/A'}",
                f"**Grupo:** {item.codigo_grupo or 'N/A'}"
                f" | **Classe:** {item.codigo_classe or 'N/A'}"
                f" | **PDM:** {item.codigo_pdm or 'N/A'}",
                f"**Status:** {status}",
                "",
            ]
        )

    if resultado.total > len(resultado.itens):
        lines.append(f"*Use pagina={pagina + 1} para mais resultados.*")
    return "\n".join(lines)


async def buscar_servico_catser(
    ctx: Context,
    codigo_servico: int | None = None,
    codigo_grupo: int | None = None,
    pagina: int = 1,
) -> str:
    """(legacy) Поиск позиций в каталоге CATSER (услуги федерального правительства).

    Примечание: инструмент совместимости для бразильских данных госзакупок.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    CATSER — Каталог услуг, используемый федеральным правительством
    для классификации и стандартизации привлечения услуг.

    Args:
        codigo_servico: Код услуги CATSER (необязательно).
        codigo_grupo: Код группы CATSER (необязательно).
        pagina: Страница результатов (по умолчанию 1).

    Returns:
        Список найденных услуг каталога.
    """
    if not any([codigo_servico, codigo_grupo]):
        return "Informe pelo menos um filtro: codigo_servico ou codigo_grupo."

    await ctx.info("Buscando serviço CATSER...")
    resultado = await client.buscar_servico(
        codigo_servico=codigo_servico,
        codigo_grupo=codigo_grupo,
        pagina=pagina,
    )
    await ctx.info(f"{resultado.total} serviços encontrados")

    if not resultado.itens:
        return "Nenhum serviço encontrado."

    lines = [f"**Total:** {resultado.total} serviços\n"]
    for i, item in enumerate(resultado.itens, 1):
        status = "Ativo" if item.status_servico else "Inativo"
        lines.extend(
            [
                f"### {i}. {item.nome_servico or 'Sem descrição'}",
                f"**Código:** {item.codigo_servico or 'N/A'}",
                f"**Grupo:** {item.codigo_grupo or 'N/A'}"
                f" | **Classe:** {item.codigo_classe or 'N/A'}",
                f"**Status:** {status}",
                "",
            ]
        )

    if resultado.total > len(resultado.itens):
        lines.append(f"*Use pagina={pagina + 1} para mais resultados.*")
    return "\n".join(lines)


async def buscar_uasg(
    ctx: Context,
    codigo_uasg: str | None = None,
    sigla_uf: str | None = None,
    pagina: int = 1,
) -> str:
    """(legacy) Поиск UASG (Административные единицы обслуживания).

    Примечание: инструмент совместимости для бразильских данных госзакупок.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    UASG — единицы федерального правительства, осуществляющие закупки.
    Используйте этот инструмент для обнаружения кода UASG органа и фильтрации запросов.

    Args:
        codigo_uasg: Код UASG (необязательно).
        sigla_uf: Аббревиатура штата (напр.: SP, RJ, DF) (необязательно).
        pagina: Страница результатов (по умолчанию 1).

    Returns:
        Список найденных UASG.
    """
    if not any([codigo_uasg, sigla_uf]):
        return "Informe pelo menos um filtro: codigo_uasg ou sigla_uf."

    desc = codigo_uasg or sigla_uf or "UASG"
    await ctx.info(f"Buscando UASG '{desc}'...")
    resultado = await client.buscar_uasg(
        codigo_uasg=codigo_uasg,
        sigla_uf=sigla_uf,
        pagina=pagina,
    )
    await ctx.info(f"{resultado.total} UASGs encontradas")

    if not resultado.uasgs:
        return f"Nenhuma UASG encontrada para '{desc}'."

    lines = [f"**Total:** {resultado.total} UASGs\n"]
    for i, u in enumerate(resultado.uasgs, 1):
        lines.extend(
            [
                f"### {i}. {u.nome_uasg or 'N/A'}",
                f"**Código:** {u.codigo_uasg or 'N/A'}",
                f"**CNPJ:** {u.cnpj_cpf_orgao or 'N/A'}",
                f"**Local:** {u.nome_municipio or 'N/A'}/{u.sigla_uf or 'N/A'}",
                f"**SISG:** {'Sim' if u.uso_sisg else 'Não'}",
                "",
            ]
        )

    if resultado.total > len(resultado.uasgs):
        lines.append(f"*Use pagina={pagina + 1} para mais resultados.*")
    return "\n".join(lines)
