"""Справочные resources для слоя Transparência (legacy) — данные для контекста LLM.

Resources предоставляют данные только для чтения, которые LLM могут запрашивать для контекста.
Эти данные дают LLM знание доступных конечных точек и баз данных
без вызова инструментов.

NOTE: Это слой обратной совместимости (legacy) в рамках mcp-russia.
Данные бразильского портала прозрачности сохранены для обратной совместимости
и НЕ являются частью целевой российской модели данных.
"""

from __future__ import annotations

import json

from .constants import SANCOES_DATABASES, TRANSPARENCIA_API_BASE


def endpoints_disponiveis() -> str:
    """(legacy) Список всех доступных конечных точек API Портала прозрачности Бразилии."""
    data = [
        {
            "endpoint": "contratos",
            "descricao": "Федеральные контракты по CPF/CNPJ поставщика",
            "parametros": ["cpfCnpj", "pagina"],
        },
        {
            "endpoint": "despesas/recursos-recebidos",
            "descricao": "Расходы и полученные ресурсы по получателю и периоду",
            "parametros": ["mesAnoInicio", "mesAnoFim", "codigoFavorecido", "pagina"],
        },
        {
            "endpoint": "servidores",
            "descricao": "Федеральные государственные служащие по CPF или имени",
            "parametros": ["cpf", "nome", "pagina"],
        },
        {
            "endpoint": "licitacoes",
            "descricao": "Федеральные тендеры по органу и/или периоду",
            "parametros": ["codigoOrgao", "dataInicial", "dataFinal", "pagina"],
        },
        {
            "endpoint": "novo-bolsa-familia-por-municipio",
            "descricao": "Данные программы Novo Bolsa Família по муниципалитету",
            "parametros": ["mesAno", "codigoIbge", "pagina"],
        },
        {
            "endpoint": "novo-bolsa-familia-sacado-por-nis",
            "descricao": "Данные Novo Bolsa Família по NIS получателя",
            "parametros": ["mesAno", "nis", "pagina"],
        },
        {
            "endpoint": "emendas",
            "descricao": "Парламентские поправки по году и/или автору",
            "parametros": ["ano", "nomeAutor", "pagina"],
        },
        {
            "endpoint": "viagens-por-cpf",
            "descricao": "Служебные поездки по CPF служащего",
            "parametros": ["cpf", "pagina"],
        },
        {
            "endpoint": "ceis/cnep/cepim/ceaf",
            "descricao": "Санкции в федеральных базах (недобросовестные, наказанные, запрещённые, исключённые)",
            "parametros": ["codigoSancionado", "nomeSancionado", "pagina"],
        },
        {
            "endpoint": "convenios",
            "descricao": "Соглашения и добровольные трансферты",
            "parametros": ["codigoOrgao", "convenente", "pagina"],
        },
        {
            "endpoint": "cartoes",
            "descricao": "Корпоративная карта / фонд снабжения",
            "parametros": [
                "cpfPortador",
                "codigoOrgao",
                "mesExtratoInicio",
                "mesExtratoFim",
                "pagina",
            ],
        },
        {
            "endpoint": "pep",
            "descricao": "ПолитическиExposed лица (PEP)",
            "parametros": ["cpf", "nome", "pagina"],
        },
        {
            "endpoint": "acordos-leniencia",
            "descricao": "Соглашения о-lenienсe (антикоррупция)",
            "parametros": ["nomeEmpresa", "cnpj", "pagina"],
        },
        {
            "endpoint": "notas-fiscais",
            "descricao": "Электронные счета-фактуры",
            "parametros": ["cnpjEmitente", "dataEmissaoDe", "dataEmissaoAte", "pagina"],
        },
        {
            "endpoint": "beneficios-cidadao",
            "descricao": "Социальные пособия (BPC, пособие по безработице и т.д.)",
            "parametros": ["cpf", "nis", "mesAno", "pagina"],
        },
        {
            "endpoint": "pessoas-fisicas",
            "descricao": "Связи и пособия по CPF",
            "parametros": ["cpf", "pagina"],
        },
        {
            "endpoint": "pessoas-juridicas",
            "descricao": "Санкции и контракты по CNPJ",
            "parametros": ["cnpj", "pagina"],
        },
        {
            "endpoint": "contratos/id/{id}",
            "descricao": "Детали конкретного контракта",
            "parametros": ["id"],
        },
        {
            "endpoint": "servidores/{id}",
            "descricao": "Полные данные служащего с вознаграждением",
            "parametros": ["id"],
        },
    ]
    return json.dumps(data, ensure_ascii=False)


def bases_sancoes() -> str:
    """(legacy) 4 федеральные базы санкций с описанием и параметрами запроса."""
    data = [
        {
            "sigla": key.upper(),
            "nome": db["nome"],
            "url": db["url"],
            "parametro_cpf_cnpj": db["param_cpf_cnpj"],
            "parametro_nome": db["param_nome"],
        }
        for key, db in SANCOES_DATABASES.items()
    ]
    return json.dumps(data, ensure_ascii=False)


def categorias_beneficios() -> str:
    """(legacy) Типы социальных пособий, доступных для запроса."""
    data = [
        {"tipo": "BPC", "descricao": "Непрерывное пособие (LOAS)"},
        {"tipo": "seguro-desemprego", "descricao": "Пособие по безработице"},
        {"tipo": "abono-salarial", "descricao": "Зарплатный бонус PIS/PASEP"},
        {"tipo": "garantia-safra", "descricao": "Гарантия урожая"},
        {"tipo": "peti", "descricao": "Программа ликвидации детского труда"},
        {"tipo": "bolsa-familia", "descricao": "Novo Bolsa Família (выделенный endpoint)"},
    ]
    return json.dumps(data, ensure_ascii=False)


def info_api() -> str:
    """(legacy) Общая информация об API Портала прозрачности Бразилии."""
    data = {
        "nome": "API Портала прозрачности Федерального правительства Бразилии (legacy)",
        "url_base": TRANSPARENCIA_API_BASE,
        "autenticacao": {
            "tipo": "API Key",
            "header": "chave-api-dados",
            "cadastro": "https://portaldatransparencia.gov.br/api-de-dados/cadastrar-email",
        },
        "limites": {
            "horario_comercial": "90 запросов/минуту (06:00–23:59)",
            "horario_madrugada": "300 запросов/минуту (00:00–05:59)",
        },
        "paginacao": "Параметр 'pagina' (1-indexed, по умолчанию 15 элементов на страницу)",
        "formatos": "JSON",
    }
    return json.dumps(data, ensure_ascii=False)
