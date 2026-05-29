"""Инструменты для работы с BrasilAPI (слой совместимости, legacy).

Примечание: это слой совместимости в рамках mcp-russia. Данные инструменты
предоставляют справочные данные по Бразилии и считаются переходными.

Правила (ADR-001):
    - tools.py НИКОГДА не выполняет HTTP напрямую — делегирует client.py
    - Возвращает отформатированные строки для потребления LLM
    - Использует Context для структурированного логирования и отчёта о прогрессе
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import (
    format_number_ru,
    format_rub,
    markdown_table,
    truncate_list,
)

from . import client
from .constants import TAXAS_CONHECIDAS, TIPOS_VEICULO


async def consultar_cep(cep: str, ctx: Context) -> str:
    """Поиск адреса по бразильскому почтовому индексу CEP (legacy).

    Примечание: это инструмент совместимости для бразильских данных CEP.
    Возвращает улицу, район, город и штат.
    Принимает CEP с дефисом или без (например: 01001-000 или 01001000).

    Args:
        cep: CEP из 8 цифр (например: 01001000 или 01001-000).

    Returns:
        Данные адреса, соответствующего CEP.
    """
    await ctx.info(f"Consultando CEP {cep}...")
    endereco = await client.consultar_cep(cep)
    lines = [
        f"**CEP:** {endereco.cep}",
        f"**Logradouro:** {endereco.street or 'N/A'}",
        f"**Bairro:** {endereco.neighborhood or 'N/A'}",
        f"**Cidade:** {endereco.city}",
        f"**UF:** {endereco.state}",
    ]
    return "\n".join(lines)


async def consultar_cnpj(cnpj: str, ctx: Context) -> str:
    """Поиск регистрационных данных компании по бразильскому номеру CNPJ (legacy).

    Примечание: инструмент совместимости для бразильских данных CNPJ.
    Возвращает юридическое наименование, коммерческое название, статус регистрации,
    адрес, вид экономической деятельности (CNAE) и уставный капитал.
    Принимает CNPJ с форматированием или без.

    Args:
        cnpj: CNPJ из 14 цифр (например: 00000000000191 или 00.000.000/0001-91).

    Returns:
        Регистрационные данные компании.
    """
    await ctx.info(f"Consultando CNPJ {cnpj}...")
    emp = await client.consultar_cnpj(cnpj)
    capital = format_rub(emp.capital_social) if emp.capital_social else "N/A"
    lines = [
        f"**CNPJ:** {emp.cnpj}",
        f"**Razão Social:** {emp.razao_social or 'N/A'}",
        f"**Nome Fantasia:** {emp.nome_fantasia or 'N/A'}",
        f"**Situação:** {emp.descricao_situacao_cadastral or 'N/A'}",
        f"**Porte:** {emp.porte or 'N/A'}",
        f"**Natureza Jurídica:** {emp.natureza_juridica or 'N/A'}",
        f"**CNAE:** {emp.cnae_fiscal} — {emp.cnae_fiscal_descricao or 'N/A'}",
        f"**Endereço:** {emp.logradouro or ''}, {emp.numero or ''} "
        f"{emp.complemento or ''} — {emp.bairro or ''}",
        f"**Cidade/UF:** {emp.municipio or 'N/A'}/{emp.uf or 'N/A'} — CEP {emp.cep or 'N/A'}",
        f"**Telefone:** {emp.ddd_telefone_1 or 'N/A'}",
        f"**Email:** {emp.email or 'N/A'}",
        f"**Capital Social:** {capital}",
    ]
    return "\n".join(lines)


async def consultar_ddd(ddd: str, ctx: Context) -> str:
    """Поиск городов и штата по бразильскому телефонному коду DDD (legacy).

    Примечание: инструмент совместимости для бразильских данных DDD.
    Полезно для определения географического положения по телефонному номеру.

    Args:
        ddd: Код DDD из 2 цифр (например: 11, 21, 61).

    Returns:
        Штат и список городов кода DDD.
    """
    await ctx.info(f"Consultando DDD {ddd}...")
    info = await client.consultar_ddd(ddd)
    header = f"**DDD {ddd}** — Estado: {info.state}\n\n"
    header += f"**Cidades ({len(info.cities)}):**\n\n"
    return header + truncate_list(sorted(info.cities), max_items=50)


async def listar_bancos(ctx: Context) -> str:
    """Список всех бразильских банков, зарегистрированных в Центральном банке (legacy).

    Примечание: инструмент совместимости для бразильских банковских данных.
    Возвращает код, название и ISPB каждого банка.
    Полезно для идентификации банков по коду или поиска банковской информации.

    Returns:
        Таблица со всеми бразильскими банками.
    """
    await ctx.info("Buscando lista de bancos...")
    bancos = await client.listar_bancos()
    await ctx.info(f"{len(bancos)} bancos encontrados")
    rows = [
        (str(b.code or "—"), b.name or "N/A", b.ispb or "N/A")
        for b in bancos
        if b.code is not None
    ]
    rows.sort(key=lambda r: int(r[0]) if r[0] != "—" else 99999)
    return markdown_table(["Código", "Nome", "ISPB"], rows)


async def consultar_banco(codigo: int, ctx: Context) -> str:
    """Поиск данных конкретного банка по коду (legacy).

    Примечание: инструмент совместимости для бразильских банковских данных.

    Args:
        codigo: Код банка (например: 1 — Banco do Brasil, 341 — Itaú).

    Returns:
        Полные данные банка.
    """
    await ctx.info(f"Consultando banco {codigo}...")
    banco = await client.consultar_banco(codigo)
    lines = [
        f"**Código:** {banco.code}",
        f"**Nome:** {banco.name or 'N/A'}",
        f"**Nome Completo:** {banco.fullName or 'N/A'}",
        f"**ISPB:** {banco.ispb or 'N/A'}",
    ]
    return "\n".join(lines)


async def listar_moedas(ctx: Context) -> str:
    """Список всех валют, доступных для запроса курсов (legacy).

    Примечание: инструмент совместимости для бразильских валютных данных.
    Возвращает символ и название каждой валюты для использования в consultar_cotacao.

    Returns:
        Таблица с доступными валютами.
    """
    await ctx.info("Buscando moedas disponíveis...")
    moedas = await client.listar_moedas()
    await ctx.info(f"{len(moedas)} moedas encontradas")
    rows = [(m.simbolo, m.nome_formatado, m.tipo_moeda or "—") for m in moedas]
    return markdown_table(["Símbolo", "Nome", "Tipo"], rows)


async def consultar_cotacao(moeda: str, data: str, ctx: Context) -> str:
    """Поиск курса валюты по отношению к бразильскому реалу (BRL) на определённую дату (legacy).

    Примечание: инструмент совместимости для бразильских валютных данных.
    Используйте listar_moedas для просмотра доступных валют.
    Данные доступны с 28.11.1984. Невозможно запросить будущие даты.

    Args:
        moeda: Символ валюты (например: USD, EUR, GBP).
        data: Дата в формате YYYY-MM-DD (например: 2024-01-15).

    Returns:
        Курс покупки и продажи валюты.
    """
    await ctx.info(f"Consultando cotação {moeda} em {data}...")
    cotacao = await client.consultar_cotacao(moeda, data)
    compra = format_number_ru(cotacao.valor_compra, 4) if cotacao.valor_compra else "N/A"
    venda = format_number_ru(cotacao.valor_venda, 4) if cotacao.valor_venda else "N/A"
    lines = [
        f"**Moeda:** {cotacao.moeda}",
        f"**Data:** {cotacao.data}",
        f"**Compra:** {compra} ₽",
        f"**Venda:** {venda} ₽",
    ]
    return "\n".join(lines)


async def consultar_feriados(ano: int, ctx: Context) -> str:
    """Список всех национальных праздников Бразилии за год (legacy).

    Примечание: инструмент совместимости для бразильских данных.
    Возвращает дату, название и тип каждого праздника.

    Args:
        ano: Год из 4 цифр (например: 2024, 2025).

    Returns:
        Таблица с национальными праздниками Бразилии за год.
    """
    await ctx.info(f"Consultando feriados de {ano}...")
    feriados = await client.consultar_feriados(ano)
    await ctx.info(f"{len(feriados)} feriados encontrados")
    rows = [(f.date, f.name, f.type) for f in feriados]
    return markdown_table(["Data", "Feriado", "Tipo"], rows)


async def consultar_taxa(sigla: str, ctx: Context) -> str:
    """Поиск ставки или индекса бразильской экономики (legacy).

    Примечание: инструмент совместимости для бразильских экономических данных.
    Доступные ставки: SELIC, CDI, IPCA, TR, INPC, IGP-M и другие.

    Args:
        sigla: Аббревиатура ставки (например: SELIC, CDI, IPCA).

    Returns:
        Название и текущее значение ставки.
    """
    await ctx.info(f"Consultando taxa {sigla.upper()}...")
    taxa = await client.consultar_taxa(sigla)
    valor = format_number_ru(taxa.valor, 2) if taxa.valor is not None else "N/A"
    desc = TAXAS_CONHECIDAS.get(sigla.upper(), "")
    lines = [
        f"**Taxa:** {taxa.nome}",
        f"**Valor:** {valor}%",
    ]
    if desc:
        lines.append(f"**Descrição:** {desc}")
    return "\n".join(lines)


async def listar_tabelas_fipe(ctx: Context) -> str:
    """Список доступных справочных таблиц FIPE (legacy).

    Примечание: инструмент совместимости для бразильских данных об автомобилях.
    Самая свежая таблица находится первой в списке.
    Используйте код таблицы в listar_marcas_fipe для фильтрации по периоду.

    Returns:
        Список справочных таблиц FIPE с кодом и месяцем.
    """
    await ctx.info("Buscando tabelas FIPE...")
    tabelas = await client.listar_tabelas_fipe()
    await ctx.info(f"{len(tabelas)} tabelas encontradas")
    rows = [(str(t.codigo), t.mes) for t in tabelas]
    return markdown_table(["Código", "Mês/Ano"], rows[:24])


async def listar_marcas_fipe(tipo_veiculo: str, ctx: Context) -> str:
    """Список марок автомобилей в таблице FIPE по типу (legacy).

    Примечание: инструмент совместимости для бразильских данных об автомобилях.

    Args:
        tipo_veiculo: Тип транспортного средства: carros, caminhoes или motos.

    Returns:
        Список марок с названием и кодом для поиска автомобилей.
    """
    if tipo_veiculo not in TIPOS_VEICULO:
        return f"Tipo inválido: {tipo_veiculo}. Use: {', '.join(sorted(TIPOS_VEICULO))}"
    await ctx.info(f"Buscando marcas FIPE ({tipo_veiculo})...")
    marcas = await client.listar_marcas_fipe(tipo_veiculo)
    await ctx.info(f"{len(marcas)} marcas encontradas")
    rows = [(m.valor, m.nome) for m in marcas]
    return markdown_table(["Código", "Marca"], rows)


async def buscar_veiculos_fipe(tipo_veiculo: str, codigo_marca: str, ctx: Context) -> str:
    """Поиск моделей автомобилей в таблице FIPE по типу и марке (legacy).

    Примечание: инструмент совместимости для бразильских данных об автомобилях.
    Используйте listar_marcas_fipe для получения кода марки.

    Args:
        tipo_veiculo: Тип транспортного средства: carros, caminhoes или motos.
        codigo_marca: Код марки (полученный из listar_marcas_fipe).

    Returns:
        Список моделей с ценой FIPE.
    """
    if tipo_veiculo not in TIPOS_VEICULO:
        return f"Tipo inválido: {tipo_veiculo}. Use: {', '.join(sorted(TIPOS_VEICULO))}"
    await ctx.info(f"Buscando veículos FIPE ({tipo_veiculo}, marca {codigo_marca})...")
    veiculos = await client.buscar_veiculos_fipe(tipo_veiculo, codigo_marca)
    await ctx.info(f"{len(veiculos)} veículos encontrados")
    rows = [(v.codigo_fipe or "—", v.modelo or v.valor, v.valor) for v in veiculos]
    return markdown_table(["Código FIPE", "Modelo", "Valor"], rows[:50])


async def consultar_isbn(isbn: str, ctx: Context) -> str:
    """Поиск данных книги по ISBN (legacy).

    Примечание: инструмент совместимости для бразильских библиографических данных.
    Поиск по нескольким источникам: CBL, Google Books, Mercado Editorial, Open Library.

    Args:
        isbn: ISBN-10 или ISBN-13 (с дефисами или без).

    Returns:
        Данные книги (название, автор, издательство, год, страницы).
    """
    await ctx.info(f"Consultando ISBN {isbn}...")
    livro = await client.consultar_isbn(isbn)
    autores = ", ".join(livro.authors) if livro.authors else "N/A"
    lines = [
        f"**ISBN:** {livro.isbn or isbn}",
        f"**Título:** {livro.title or 'N/A'}",
    ]
    if livro.subtitle:
        lines.append(f"**Subtítulo:** {livro.subtitle}")
    lines.extend(
        [
            f"**Autor(es):** {autores}",
            f"**Editora:** {livro.publisher or 'N/A'}",
            f"**Ano:** {livro.year or 'N/A'}",
            f"**Páginas:** {livro.page_count or 'N/A'}",
        ]
    )
    if livro.subjects:
        lines.append(f"**Assuntos:** {', '.join(livro.subjects)}")
    return "\n".join(lines)


async def buscar_ncm(busca: str, ctx: Context) -> str:
    """Поиск кодов NCM (Общая номенклатура Меркосур) по описанию или коду (legacy).

    Примечание: инструмент совместимости для бразильских таможенных данных.
    NCM — это код, используемый для классификации товаров во внешней торговле
    и при оформлении электронных счетов-фактур.

    Args:
        busca: Текст для поиска (описание товара или частичный код NCM).

    Returns:
        Список найденных кодов NCM.
    """
    await ctx.info(f"Buscando NCM '{busca}'...")
    itens = await client.buscar_ncm(busca)
    await ctx.info(f"{len(itens)} NCMs encontrados")
    if not itens:
        return f"Nenhum NCM encontrado para '{busca}'."
    rows = [(n.codigo, n.descricao) for n in itens]
    return markdown_table(["Código", "Descrição"], rows[:30])


async def consultar_pix_participantes(ctx: Context) -> str:
    """Список всех организаций — участников платёжной системы PIX (legacy).

    Примечание: инструмент совместимости для бразильских платёжных данных.
    Возвращает ISPB, название и тип участия каждой организации.

    Returns:
        Таблица с участниками системы PIX.
    """
    await ctx.info("Buscando participantes do PIX...")
    participantes = await client.listar_pix_participantes()
    await ctx.info(f"{len(participantes)} participantes encontrados")
    rows = [
        (p.ispb or "—", p.nome_reduzido or p.nome or "N/A", p.tipo_participacao or "—")
        for p in participantes
    ]
    return markdown_table(["ISPB", "Nome", "Tipo"], rows[:50])


async def consultar_registro_br(dominio: str, ctx: Context) -> str:
    """Проверка доступности домена .br в Registro.br (legacy).

    Примечание: инструмент совместимости для бразильских доменных данных.

    Args:
        dominio: Имя домена (например: meusite.com.br).

    Returns:
        Статус доступности домена.
    """
    await ctx.info(f"Consultando domínio {dominio}...")
    info = await client.consultar_registro_br(dominio)
    status_map = {
        0: "Disponível para registro",
        1: "Disponível com processo de liberação",
        2: "Registrado",
        3: "Indisponível",
        4: "Processo de registro em andamento",
        5: "Domínio em processo de liberação (aguardando)",
    }
    code = info.status_code if info.status_code is not None else -1
    status_desc = status_map.get(code, info.status or "Desconhecido")
    lines = [
        f"**Domínio:** {info.fqdn or dominio}",
        f"**Status:** {status_desc}",
    ]
    if info.expires_at:
        lines.append(f"**Expira em:** {info.expires_at}")
    if info.hosts:
        lines.append(f"**DNS:** {', '.join(info.hosts)}")
    return "\n".join(lines)
