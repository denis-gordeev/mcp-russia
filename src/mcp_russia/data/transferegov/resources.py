"""Resources для TransfereGov — уровень обратной совместимости для бразильских данных о трансфертах.

NOTE: Это уровень обратной совместимости (legacy) в рамках mcp-russia.
Бразильские справочные данные TransfereGov сохраняются для обратной совместимости
с исторической интеграцией и НЕ входят в целевую российскую модель данных.
"""

from __future__ import annotations

import json


def info_api() -> str:
    """Информация об API TransfereGov и инструкции по использованию (legacy, Бразилия)."""
    data = {
        "nome": "API TransfereGov (PostgREST) — Бразилия (legacy)",
        "url_base": "https://api.transferegov.gestao.gov.br",
        "autenticacao": "Отсутствует (публичное API)",
        "formato": "JSON array (без обёртки)",
        "paginacao": "limit/offset через query params",
        "filtros": {
            "descricao": "PostgREST: column=operator.value",
            "operadores": ["eq", "neq", "gt", "lt", "gte", "lte", "like", "ilike", "in"],
            "exemplos": [
                "ano_plano_acao=eq.2024",
                "nome_parlamentar_emenda_plano_acao=ilike.*nome*",
                "uf_beneficiario_plano_acao=eq.PI",
            ],
        },
        "endpoint_principal": "/transferenciasespeciais/plano_acao_especial",
        "colunas_principais": [
            "id_plano_acao",
            "ano_plano_acao",
            "numero_emenda_parlamentar_plano_acao",
            "nome_parlamentar_emenda_plano_acao",
            "valor_custeio_plano_acao",
            "valor_investimento_plano_acao",
            "nome_beneficiario_plano_acao",
            "uf_beneficiario_plano_acao",
            "situacao_plano_acao",
        ],
    }
    return json.dumps(data, ensure_ascii=False)
