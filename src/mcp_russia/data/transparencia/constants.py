"""Constants for the Transparência feature."""

# Pagination
DEFAULT_PAGE_SIZE = 15

# API base URL
TRANSPARENCIA_API_BASE = "https://api.portaldatransparencia.gov.br/api-de-dados"

# Auth
AUTH_HEADER_NAME = "chave-api-dados"
AUTH_ENV_VAR = "TRANSPARENCIA_API_KEY"

# Endpoints
CONTRATOS_URL = f"{TRANSPARENCIA_API_BASE}/contratos/cpf-cnpj"
DESPESAS_URL = f"{TRANSPARENCIA_API_BASE}/despesas/recursos-recebidos"
SERVIDORES_URL = f"{TRANSPARENCIA_API_BASE}/servidores"
LICITACOES_URL = f"{TRANSPARENCIA_API_BASE}/licitacoes"
BOLSA_FAMILIA_MUNICIPIO_URL = f"{TRANSPARENCIA_API_BASE}/novo-bolsa-familia-por-municipio"
BOLSA_FAMILIA_NIS_URL = f"{TRANSPARENCIA_API_BASE}/novo-bolsa-familia-sacado-por-nis"
EMENDAS_URL = f"{TRANSPARENCIA_API_BASE}/emendas"
VIAGENS_URL = f"{TRANSPARENCIA_API_BASE}/viagens-por-cpf"
CONVENIOS_URL = f"{TRANSPARENCIA_API_BASE}/convenios"
CARTOES_URL = f"{TRANSPARENCIA_API_BASE}/cartoes"
PEP_URL = f"{TRANSPARENCIA_API_BASE}/peps"
ACORDOS_LENIENCIA_URL = f"{TRANSPARENCIA_API_BASE}/acordos-leniencia"
NOTAS_FISCAIS_URL = f"{TRANSPARENCIA_API_BASE}/notas-fiscais"
BENEFICIOS_CIDADAO_URL = f"{TRANSPARENCIA_API_BASE}/beneficios-cidadao"
PESSOAS_FISICAS_URL = f"{TRANSPARENCIA_API_BASE}/pessoas-fisicas"
PESSOAS_JURIDICAS_URL = f"{TRANSPARENCIA_API_BASE}/pessoas-juridicas"
CONTRATO_DETALHE_URL = f"{TRANSPARENCIA_API_BASE}/contratos/id"
SERVIDOR_DETALHE_URL = f"{TRANSPARENCIA_API_BASE}/servidores"

# Sanções — cada base tem endpoint e nome de parâmetro diferentes
SANCOES_DATABASES: dict[str, dict[str, str]] = {
    "ceis": {
        "url": f"{TRANSPARENCIA_API_BASE}/ceis",
        "param_cpf_cnpj": "codigoSancionado",
        "param_nome": "nomeSancionado",
        "nome": "CEIS (Empresas Inidôneas e Suspensas)",
    },
    "cnep": {
        "url": f"{TRANSPARENCIA_API_BASE}/cnep",
        "param_cpf_cnpj": "codigoSancionado",
        "param_nome": "nomeSancionado",
        "nome": "CNEP (Empresas Punidas)",
    },
    "cepim": {
        "url": f"{TRANSPARENCIA_API_BASE}/cepim",
        "param_cpf_cnpj": "cnpjSancionado",
        "param_nome": "nomeSancionado",
        "nome": "CEPIM (Entidades Privadas sem Fins Lucrativos Impedidas)",
    },
    "ceaf": {
        "url": f"{TRANSPARENCIA_API_BASE}/ceaf",
        "param_cpf_cnpj": "cpfSancionado",
        "param_nome": "nomeSancionado",
        "nome": "CEAF (Expulsões da Administração Federal)",
    },
}
