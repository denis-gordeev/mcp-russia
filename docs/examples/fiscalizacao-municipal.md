# Fiscalização Municipal: Onde Vai o Dinheiro da Sua Cidade

> Пример показывает, как в `mcp-russia` можно собирать муниципальную картину из открытых государственных API. Источники и feature-имена ниже частично остаются в legacy-совместимом виде, унаследованном от исходного проекта.

---

## O Que Este Exemplo Demonstra

Как использовать `mcp-russia` для муниципального контроля расходов, сопоставляя данные **9 региональных контрольно-счетных источников** с Portal da Transparencia, PNCP (федеральные закупки) и IBGE (демография). Сценарий по-прежнему опирается на бразильские API как на переходный data-layer, но публичное описание проекта уже русскоязычное.

---

## APIs Utilizadas

| API | Feature | O Que Forneceu |
|-----|---------|----------------|
| **TCE-SP** | `tce_sp` | Despesas e receitas de 645 municípios paulistas |
| **TCE-RJ** | `tce_rj` | Licitações, contratos, obras, penalidades |
| **TCE-RS** | `tce_rs` | Educação, saúde, gestão fiscal (LRF) |
| **TCE-PE** | `tce_pe` | Licitações, contratos, despesas, fornecedores |
| **TCE-CE** | `tce_ce` | Licitações, contratos, empenhos |
| **TCE-SC** | `tce_sc` | Municípios e unidades gestoras |
| **TCE-RN** | `tce_rn` | Jurisdicionados, licitações, contratos |
| **TCE-PI** | `tce_pi` | Prefeituras, despesas, receitas |
| **TCE-TO** | `tce_to` | Processos, pautas de sessões |
| **Portal da Transparência** | `transparencia` | Transferências federais para municípios |
| **PNCP** | `pncp` | Licitações e contratações públicas |
| **TransfereGov** | `transferegov` | Emendas parlamentares PIX |
| **IBGE** | `ibge` | População municipal, dados demográficos |
| **Compras.gov.br** | `dadosabertos` | Contratos e atas de registro de preços |

---

## Caso 1: Comparando Gastos com Educação Per Capita Entre Municípios

### O Cenário

Dois municípios vizinhos no interior de São Paulo com população similar têm resultados educacionais muito diferentes. A fiscalização começa pela comparação dos gastos.

### Passo a Passo

**1. Identificar os municípios e suas populações**

> Prompt: "Qual a população dos municípios de Araraquara e Franca em São Paulo?"

Ferramentas:
- `ibge_buscar_municipios(uf="SP")` — lista municípios
- `ibge_consultar_agregado(...)` — dados populacionais

**2. Buscar despesas com educação nos dois municípios**

> Prompt: "Compare os gastos com educação de Araraquara e Franca nos últimos 3 anos"

Ferramentas:
- `tce_sp_despesas(municipio="Araraquara", funcao="Educação", ano=2024)`
- `tce_sp_despesas(municipio="Franca", funcao="Educação", ano=2024)`

Usando `executar_lote` para paralelizar:

```json
[
  {"tool": "tce_sp_despesas", "args": {"municipio": "Araraquara", "funcao": "Educação", "ano": 2024}},
  {"tool": "tce_sp_despesas", "args": {"municipio": "Franca", "funcao": "Educação", "ano": 2024}},
  {"tool": "tce_sp_despesas", "args": {"municipio": "Araraquara", "funcao": "Educação", "ano": 2023}},
  {"tool": "tce_sp_despesas", "args": {"municipio": "Franca", "funcao": "Educação", "ano": 2023}}
]
```

**3. Calcular gasto per capita**

Com os dados de população (IBGE) e despesas (TCE-SP), o cálculo é direto:

| Município | População | Gasto Educação | Per Capita |
|-----------|-----------|---------------|-----------|
| Araraquara | 238.000 | R$ 285M | R$ 1.197 |
| Franca | 355.000 | R$ 320M | R$ 901 |
| **Diferença** | | | **+33%** |

**4. Verificar transferências federais**

> Prompt: "Quais transferências federais Araraquara e Franca receberam para educação em 2024?"

Ferramentas:
- `transparencia_transferencias` — transferências por município
- `transferegov_buscar_emendas` — emendas parlamentares destinadas

---

## Caso 2: Identificando Fornecedores Suspeitos em Licitações

### O Cenário

Um município do Rio de Janeiro contrata repetidamente o mesmo fornecedor para serviços diferentes, sempre abaixo do limite de dispensa de licitação.

### Passo a Passo

**1. Buscar contratos do município**

> Prompt: "Liste todos os contratos da Prefeitura de [Município] no último ano"

Ferramentas:
- `tce_rj_contratos(municipio="...", ano=2024)` — contratos pelo TCE-RJ
- `pncp_buscar_contratacoes(orgao="...", ano=2024)` — via PNCP

**2. Agrupar por fornecedor**

> Prompt: "Quais fornecedores mais receberam contratos dessa prefeitura? Algum aparece em múltiplas categorias?"

O LLM agrupa os resultados e identifica padrões:

```
Fornecedor: Empresa ABC Ltda (CNPJ: XX.XXX.XXX/0001-XX)
  ├── Contrato 001/2024 - Material de escritório   R$ 78.000 (dispensa)
  ├── Contrato 015/2024 - Serviço de limpeza       R$ 79.500 (dispensa)
  ├── Contrato 023/2024 - Manutenção predial        R$ 79.900 (dispensa)
  └── Total: R$ 237.400 em 3 contratos por dispensa
      ⚠️ Limite de dispensa: R$ 80.000 por contrato
```

**3. Verificar se o fornecedor tem penalidades**

> Prompt: "A Empresa ABC Ltda está na lista de licitantes inidôneos do TCU?"

Ferramentas:
- `tcu_buscar_licitantes_inidoneos(nome="Empresa ABC")`
- `tce_rj_penalidades(fornecedor="Empresa ABC")`

**4. Buscar obras relacionadas**

> Prompt: "A prefeitura tem obras em andamento? Qual o status de cada uma?"

Ferramentas:
- `tce_rj_obras(municipio="...")` — obras registradas no TCE-RJ

---

## Caso 3: Gestão Fiscal — Quais Municípios Estão em Risco?

### O Cenário

O TCE-RS publica indicadores de gestão fiscal (Lei de Responsabilidade Fiscal) para todos os municípios gaúchos. Quais estão no limite?

### Passo a Passo

> Prompt: "Quais municípios do Rio Grande do Sul estão no limite da Lei de Responsabilidade Fiscal para gastos com pessoal?"

Ferramentas:
- `tce_rs_gestao_fiscal` — indicadores LRF por município
- `tce_rs_educacao` — gastos com educação (mínimo constitucional 25%)
- `tce_rs_saude` — gastos com saúde (mínimo constitucional 15%)

### Resultado Esperado

| Município | Gasto Pessoal/RCL | Limite | Status |
|-----------|-------------------|--------|--------|
| [Município A] | 58,3% | 60% | ⚠️ Limite prudencial |
| [Município B] | 54,1% | 60% | ✅ OK |
| [Município C] | 61,2% | 60% | ❌ Acima do limite |

> Prompt: "Os municípios que ultrapassaram o limite de pessoal também cumprem o mínimo de 25% em educação?"

**Cross-reference:** Municípios que gastam demais com pessoal frequentemente descumprem os mínimos constitucionais em educação e saúde — porque não sobra orçamento.

---

## Caso 4: Rastreando Emendas PIX — De Brasília ao Seu Município

### O Cenário

As "emendas PIX" (transferências especiais) são recursos enviados diretamente por parlamentares a municípios, sem necessidade de convênio ou prestação de contas detalhada. Para onde estão indo?

### Passo a Passo

**1. Buscar emendas por estado**

> Prompt: "Quais municípios do Ceará mais receberam emendas PIX em 2024?"

Ferramentas:
- `transferegov_buscar_emendas(uf="CE", ano=2024)`

**2. Cruzar com dados populacionais**

> Prompt: "Calcule o valor per capita das emendas PIX para cada município do Ceará"

Ferramentas:
- `ibge_buscar_municipios(uf="CE")` — população
- Cross-reference com os valores do TransfereGov

**3. Identificar quem enviou as emendas**

> Prompt: "Quais deputados e senadores destinaram emendas para [Município]?"

Ferramentas:
- `transparencia_emendas_parlamentares(municipio="...")`

**4. Verificar gastos do município**

> Prompt: "O município aplicou as emendas em quê? Houve licitação?"

Ferramentas:
- `tce_ce_empenhos(municipio="...")` — como foi gasto
- `tce_ce_licitacoes(municipio="...")` — se houve licitação
- `pncp_buscar_contratacoes(municipio="...")` — contratações registradas

### A Cadeia Completa

```
Deputado destina emenda PIX (TransfereGov)
        ↓
Município recebe o recurso (Transparência)
        ↓
Prefeitura realiza despesa (TCE-CE)
        ↓
Verifica se houve licitação (PNCP + TCE-CE)
        ↓
Compara com necessidades reais (IBGE + Saúde/CNES)
```

---

## Comparação Entre Estados: O Poder dos 9 TCEs

В текущем compatibility-слое `mcp-russia` связывает **9 Tribunais de Contas Estaduais**. Это позволяет строить сквозные сравнения между регионами:

> Prompt: "Compare os gastos per capita com saúde dos municípios-capital de SP, RJ, RS, SC, PE, CE, RN, PI e TO"

Usando `executar_lote`:

```json
[
  {"tool": "tce_sp_despesas", "args": {"municipio": "São Paulo", "funcao": "Saúde"}},
  {"tool": "tce_rj_contratos", "args": {"municipio": "Rio de Janeiro", "tipo": "saude"}},
  {"tool": "tce_rs_saude", "args": {"municipio": "Porto Alegre"}},
  {"tool": "tce_sc_unidades_gestoras", "args": {"municipio": "Florianópolis"}},
  {"tool": "tce_pe_despesas", "args": {"municipio": "Recife", "funcao": "saude"}},
  {"tool": "tce_ce_empenhos", "args": {"municipio": "Fortaleza", "funcao": "saude"}},
  {"tool": "tce_rn_contratos", "args": {"municipio": "Natal"}},
  {"tool": "tce_pi_despesas", "args": {"municipio": "Teresina", "funcao": "saude"}},
  {"tool": "tce_to_processos", "args": {"municipio": "Palmas"}}
]
```

9 APIs consultadas em paralelo, uma chamada.

---

## O Que os Dados Mostram vs. O Que Não Mostram

### O Que Mostram
- Quanto cada município gasta por área
- Com quem contrata e por quanto
- Se cumpre os mínimos constitucionais
- De onde vêm os recursos (transferências, emendas, receita própria)
- Se há fornecedores com penalidades

### O Que Não Mostram
- Se o dinheiro foi bem aplicado (qualidade do gasto)
- Se houve superfaturamento (requer auditoria técnica)
- Se o prefeito agiu de má-fé (requer investigação)
- Se os dados estão completos (nem todo município alimenta os sistemas)

**Os dados públicos são o primeiro passo da fiscalização — não o último.**

---

## Como Verificar Você Mesmo

| Dado | Fonte | URL |
|------|-------|-----|
| Despesas/receitas SP | TCE-SP | transparencia.tce.sp.gov.br |
| Contratos/obras RJ | TCE-RJ | portal.tce.rj.gov.br |
| Gestão fiscal RS | TCE-RS | portal.tce.rs.gov.br |
| Licitações/contratos PE | TCE-PE | sistemas.tce.pe.gov.br |
| Empenhos CE | TCE-CE | api.tce.ce.gov.br |
| Licitações federais | PNCP | pncp.gov.br |
| Emendas PIX | TransfereGov | transferegov.sistema.gov.br |
| Transferências | Transparência | portaldatransparencia.gov.br |
| População | IBGE | servicodados.ibge.gov.br |

---

_Fontes de dados: APIs dos TCEs (SP, RJ, RS, SC, PE, CE, RN, PI, TO), API do Portal da Transparência, API do PNCP, API do TransfereGov, API do IBGE._

_Примечание: значения в примере иллюстративные и нужны, чтобы показать сценарий работы `mcp-russia`. Для актуальных выводов запускайте tools против живых источников; полнота данных зависит от региона, периода и состояния legacy-интеграций._
