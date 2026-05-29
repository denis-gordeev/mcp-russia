"""Constants for the Saúde feature."""

CNES_API_BASE = "https://apidadosabertos.saude.gov.br/cnes"

ESTABELECIMENTOS_URL = f"{CNES_API_BASE}/estabelecimentos"
PROFISSIONAIS_URL = f"{CNES_API_BASE}/profissionais"
TIPOS_URL = f"{CNES_API_BASE}/tipodeestabelecimento"
LEITOS_URL = f"{CNES_API_BASE}/leitos"

DEFAULT_LIMIT = 20
MAX_LIMIT = 100
