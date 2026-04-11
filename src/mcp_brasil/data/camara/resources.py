"""Справочные resources для слоя совместимости Câmara (legacy).

NOTE: Это слой обратной совместимости (legacy/compatibility layer) в рамках mcp-russia.
Данные бразильского парламента сохранены для обратной совместимости
с исторической интеграцией Câmara dos Deputados и НЕ являются частью целевой российской модели данных.
"""

from __future__ import annotations

import json

from .constants import CAMARA_API_BASE


def tipos_proposicao() -> str:
    """(legacy) Типы законодательных предложений Палаты депутатов Бразилии."""
    data = [
        {"sigla": "PL", "nome": "Projeto de Lei", "descricao": "Федеральный обычный закон"},
        {
            "sigla": "PLP",
            "nome": "Projeto de Lei Complementar",
            "descricao": "Регламентирует положения Конституции",
        },
        {
            "sigla": "PEC",
            "nome": "Proposta de Emenda à Constituição",
            "descricao": "Вносит изменения в Федеральную Конституцию",
        },
        {
            "sigla": "MPV",
            "nome": "Medida Provisória",
            "descricao": "Издаётся Президентом, имеет немедленную силу закона",
        },
        {
            "sigla": "PDL",
            "nome": "Projeto de Decreto Legislativo",
            "descricao": "Вопросы исключительной компетенции Конгресса",
        },
        {
            "sigla": "PRC",
            "nome": "Projeto de Resolução da Câmara",
            "descricao": "Регулирует внутренние вопросы Палаты",
        },
        {
            "sigla": "REQ",
            "nome": "Requerimento",
            "descricao": "Различные запросы (CPI, слушания и т.д.)",
        },
        {"sigla": "INC", "nome": "Indicação", "descricao": "Предложение другому органу власти"},
    ]
    return json.dumps(data, ensure_ascii=False)


def legislaturas_recentes() -> str:
    """(legacy) Последние законодательные сроки Палаты депутатов Бразилии."""
    data = [
        {
            "id": 57,
            "inicio": "2023-02-01",
            "fim": "2027-01-31",
            "descricao": "57-й законодательный срок (2023–2027) — текущий",
        },
        {
            "id": 56,
            "inicio": "2019-02-01",
            "fim": "2023-01-31",
            "descricao": "56-й законодательный срок (2019–2023)",
        },
        {
            "id": 55,
            "inicio": "2015-02-01",
            "fim": "2019-01-31",
            "descricao": "55-й законодательный срок (2015–2019)",
        },
        {
            "id": 54,
            "inicio": "2011-02-01",
            "fim": "2015-01-31",
            "descricao": "54-й законодательный срок (2011–2015)",
        },
    ]
    return json.dumps(data, ensure_ascii=False)


def info_api() -> str:
    """(legacy) Общая информация об API открытых данных Палаты депутатов Бразилии."""
    data = {
        "nome": "API открытых данных Палаты депутатов Бразилии (legacy)",
        "url_base": CAMARA_API_BASE,
        "autenticacao": "Не требует аутентификации",
        "documentacao": "https://dadosabertos.camara.leg.br/swagger/api.html",
        "formato": "JSON (обёртка с полями 'dados' и 'links')",
        "paginacao": "Параметры 'pagina' и 'itens' (по умолчанию: 15 элементов на страницу)",
        "filtros_comuns": {
            "deputados": ["nome", "siglaPartido", "siglaUf", "idLegislatura"],
            "proposicoes": ["siglaTipo", "numero", "ano", "keywords"],
            "votacoes": ["dataInicio", "dataFim"],
            "eventos": ["dataInicio", "dataFim"],
        },
    }
    return json.dumps(data, ensure_ascii=False)
