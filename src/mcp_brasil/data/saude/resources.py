"""Resources for the Saúde feature — legacy compatibility layer for Brazilian health data.

NOTE: This is a legacy/compatibility layer within mcp-russia.
Brazilian CNES/DataSUS reference datasets are kept for backward compatibility
with the historical health integration and are NOT part of the target Russian data model.
"""

from __future__ import annotations

import json

# UF codes used by CNES/DataSUS for filtering
_UFS_CNES = [
    {"codigo": "11", "sigla": "RO", "nome": "Rondônia"},
    {"codigo": "12", "sigla": "AC", "nome": "Acre"},
    {"codigo": "13", "sigla": "AM", "nome": "Amazonas"},
    {"codigo": "14", "sigla": "RR", "nome": "Roraima"},
    {"codigo": "15", "sigla": "PA", "nome": "Pará"},
    {"codigo": "16", "sigla": "AP", "nome": "Amapá"},
    {"codigo": "17", "sigla": "TO", "nome": "Tocantins"},
    {"codigo": "21", "sigla": "MA", "nome": "Maranhão"},
    {"codigo": "22", "sigla": "PI", "nome": "Piauí"},
    {"codigo": "23", "sigla": "CE", "nome": "Ceará"},
    {"codigo": "24", "sigla": "RN", "nome": "Rio Grande do Norte"},
    {"codigo": "25", "sigla": "PB", "nome": "Paraíba"},
    {"codigo": "26", "sigla": "PE", "nome": "Pernambuco"},
    {"codigo": "27", "sigla": "AL", "nome": "Alagoas"},
    {"codigo": "28", "sigla": "SE", "nome": "Sergipe"},
    {"codigo": "29", "sigla": "BA", "nome": "Bahia"},
    {"codigo": "31", "sigla": "MG", "nome": "Minas Gerais"},
    {"codigo": "32", "sigla": "ES", "nome": "Espírito Santo"},
    {"codigo": "33", "sigla": "RJ", "nome": "Rio de Janeiro"},
    {"codigo": "35", "sigla": "SP", "nome": "São Paulo"},
    {"codigo": "41", "sigla": "PR", "nome": "Paraná"},
    {"codigo": "42", "sigla": "SC", "nome": "Santa Catarina"},
    {"codigo": "43", "sigla": "RS", "nome": "Rio Grande do Sul"},
    {"codigo": "50", "sigla": "MS", "nome": "Mato Grosso do Sul"},
    {"codigo": "51", "sigla": "MT", "nome": "Mato Grosso"},
    {"codigo": "52", "sigla": "GO", "nome": "Goiás"},
    {"codigo": "53", "sigla": "DF", "nome": "Distrito Federal"},
]


def codigos_uf_cnes() -> str:
    """Códigos IBGE de UF usados para filtrar dados no CNES/DataSUS."""
    return json.dumps(_UFS_CNES, ensure_ascii=False)
