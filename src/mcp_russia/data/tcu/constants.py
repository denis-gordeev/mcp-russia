"""Constants for the TCU feature."""

# ---------------------------------------------------------------------------
# Domain bases
# ---------------------------------------------------------------------------

DADOS_ABERTOS_BASE = "https://dados-abertos.apps.tcu.gov.br"
CONTAS_ORDS_BASE = "https://contas.tcu.gov.br/ords"
CERTIDOES_APF_BASE = "https://certidoes-apf.apps.tcu.gov.br"
DIVIDA_BASE = "https://divida.apps.tcu.gov.br"
CONTRATA_BASE = "https://contas.tcu.gov.br/contrata2RS"

# ---------------------------------------------------------------------------
# Endpoint URLs
# ---------------------------------------------------------------------------

ACORDAOS_URL = f"{DADOS_ABERTOS_BASE}/api/acordao/recupera-acordaos"
INABILITADOS_URL = f"{CONTAS_ORDS_BASE}/condenacao/consulta/inabilitados"
INIDONEOS_URL = f"{CONTAS_ORDS_BASE}/condenacao/consulta/inidoneos"
TIPOS_CERTIDOES_URL = f"{CERTIDOES_APF_BASE}/api/rest/publico/tipos-certidoes"
CERTIDOES_URL = f"{CERTIDOES_APF_BASE}/api/rest/publico/certidoes"
CALCULO_DEBITO_URL = f"{DIVIDA_BASE}/api/publico/calculadora/calcular-saldos-debito"
PEDIDOS_CONGRESSO_URL = f"{CONTAS_ORDS_BASE}/api/publica/scn/pedidos_congresso"
TERMOS_CONTRATUAIS_URL = f"{CONTRATA_BASE}/api/publico/termos-contratuais"
CADIRREG_URL = f"{DADOS_ABERTOS_BASE}/api/recuperapessoacadirreg"

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------

DEFAULT_LIMIT = 25
DEFAULT_QUANTIDADE_ACORDAOS = 20
