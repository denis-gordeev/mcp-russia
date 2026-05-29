"""Constants for the PNCP (Portal Nacional de Contratações Públicas) feature.

API docs: https://pncp.gov.br/api/consulta/swagger-ui/index.html
OpenAPI spec: https://pncp.gov.br/api/consulta/v3/api-docs
"""

# API base URL
PNCP_API_BASE = "https://pncp.gov.br/api/consulta/v1"

# Endpoints (verified against OpenAPI spec)
CONTRATACOES_URL = f"{PNCP_API_BASE}/contratacoes/publicacao"
CONTRATOS_URL = f"{PNCP_API_BASE}/contratos"
ATAS_URL = f"{PNCP_API_BASE}/atas"
FORNECEDORES_URL = f"{PNCP_API_BASE}/fornecedores"
ORGAOS_URL = f"{PNCP_API_BASE}/orgaos"
# Note: /itens endpoint does NOT exist (returns 404). Removed.

# Paginação
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE_CONTRATACOES = 50  # max for /contratacoes/publicacao
MAX_PAGE_SIZE_CONTRATOS = 500  # max for /contratos and /atas

# Limite de período (dias)
MAX_DATE_RANGE_DAYS = 365

# Modalidades de contratação — códigos reais da API PNCP
# Fonte: https://pncp.gov.br/api/consulta/v1/modalidades
MODALIDADES: dict[int, str] = {
    1: "Leilão - Eletrônico",
    2: "Diálogo Competitivo",
    3: "Concurso",
    4: "Concorrência - Eletrônica",
    5: "Concorrência - Presencial",
    6: "Pregão - Eletrônico",
    7: "Pregão - Presencial",
    8: "Dispensa",
    9: "Inexigibilidade",
    10: "Manifestação de Interesse",
    11: "Pré-qualificação",
    12: "Credenciamento",
    13: "Leilão - Presencial",
    14: "Inaplicabilidade da Licitação",
    15: "Chamada Pública",
    16: "Concorrência - Eletrônica Internacional",
    17: "Concorrência - Presencial Internacional",
    18: "Pregão - Eletrônico Internacional",
    19: "Pregão - Presencial Internacional",
}

# Modos de disputa
MODOS_DISPUTA: dict[int, str] = {
    1: "Aberto",
    2: "Fechado",
    3: "Aberto-Fechado",
    4: "Dispensa Com Disputa",
    5: "Não se aplica",
}
