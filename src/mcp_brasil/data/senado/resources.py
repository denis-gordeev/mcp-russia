"""Справочные resources для слоя Senado (legacy) — данные для контекста LLM.

NOTE: Это слой обратной совместимости (legacy) в рамках mcp-russia.
Данные бразильского Федерального Сената сохранены для обратной совместимости
и НЕ являются частью целевой российской модели данных.
"""

from __future__ import annotations

import json

from .constants import SENADO_API_BASE, TIPOS_MATERIA


def tipos_materia() -> str:
    """(legacy) Типы законодательных материалов Федерального Сената Бразилии с аббревиатурами и описаниями."""
    data = [
        {"sigla": sigla, "descricao": descricao}
        for sigla, descricao in sorted(TIPOS_MATERIA.items())
    ]
    return json.dumps(data, ensure_ascii=False)


def info_api() -> str:
    """(legacy) Общая информация об API открытых данных Федерального Сената Бразилии."""
    data = {
        "nome": "API открытых данных Федерального Сената Бразилии (legacy)",
        "url_base": SENADO_API_BASE,
        "autenticacao": "Не требует аутентификации",
        "documentacao": "https://legis.senado.leg.br/dadosabertos/docs",
        "formato": "JSON через заголовок Accept (application/json)",
        "observacoes": [
            "Ответы могут быть глубоко вложенными",
            "Один результат может прийти как dict вместо списка",
            "Наиболее распространённые типы материалов: PEC, PLS, PLC, MPV, PLP, PDL",
        ],
    }
    return json.dumps(data, ensure_ascii=False)


def comissoes_permanentes() -> str:
    """(legacy) Постоянные комиссии Федерального Сената Бразилии."""
    data = [
        {"sigla": "CAE", "nome": "Комиссия по экономическим вопросам"},
        {"sigla": "CAS", "nome": "Комиссия по социальным вопросам"},
        {"sigla": "CCJ", "nome": "Комиссия по Конституции, правосудию и гражданству"},
        {
            "sigla": "CCT",
            "nome": "Комиссия по науке, технологии, инновациям, связи и информатике",
        },
        {"sigla": "CDH", "nome": "Комиссия по правам человека и participatory законодательству"},
        {"sigla": "CDR", "nome": "Комиссия по региональному развитию и туризму"},
        {"sigla": "CE", "nome": "Комиссия по образованию, культуре и спорту"},
        {"sigla": "CI", "nome": "Комиссия по инфраструктурным услугам"},
        {"sigla": "CMA", "nome": "Комиссия по окружающей среде"},
        {"sigla": "CRA", "nome": "Комиссия по сельскому хозяйству и аграрной реформе"},
        {"sigla": "CRE", "nome": "Комиссия по международным отношениям и национальной обороне"},
        {"sigla": "CSF", "nome": "Комиссия Сената по будущему"},
        {
            "sigla": "CTFC",
            "nome": "Комиссия по прозрачности, управлению, контролю и защите потребителей",
        },
    ]
    return json.dumps(data, ensure_ascii=False)
