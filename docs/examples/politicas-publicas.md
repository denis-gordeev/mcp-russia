# Сценарий: Анализ Государственной Политики

> Как исследователи, государственные аналитики и общественные организации могут использовать `mcp-russia` для оценки эффекта государственных программ на основе данных из нескольких публичных систем.

---

## O Problema

Avaliar uma política pública exige cruzar dados de implementação (orçamento executado, contratos) com dados de resultado (indicadores sociais, econômicos, de saúde). Esses dados vivem em sistemas separados:

| Dimensão | Fontes Necessárias |
|----------|-------------------|
| Recursos investidos | Transparência, TCEs, TransfereGov |
| Implementação | PNCP, Compras.gov.br, Diário Oficial |
| Resultados de saúde | CNES/DataSUS, IBGE |
| Resultados econômicos | Bacen, IBGE |
| Resultados educacionais | IBGE (agregados) |
| Contexto jurídico | DataJud, Jurisprudência |
| Contexto legislativo | Câmara, Senado |

**`mcp-russia` сводит эти источники в единый аналитический интерфейс.**

На текущем этапе часть tool IDs и интеграций по-прежнему наследуется от исходного `mcp-brasil`. В examples ниже это compatibility-layer, а не публичное позиционирование проекта.

---

## Análise 1: Programa de Saúde da Família — Funciona?

### A Questão

O Programa Saúde da Família (PSF/ESF) é a principal estratégia de atenção primária do SUS. Os municípios que investem mais nele têm melhores indicadores de saúde?

### O Roteiro

**1. Identificar a cobertura do PSF por município**

> Prompt: "Quantas unidades de Saúde da Família existem nos municípios do Ceará? Compare com a população"

```
APIs: saude_buscar_estabelecimentos(uf="CE", tipo="USF")
      ibge_buscar_municipios(uf="CE") → população
```

**2. Gastos com atenção primária**

> Prompt: "Quanto cada município gasta com atenção básica vs. média e alta complexidade?"

```
APIs: tce_ce_empenhos(funcao="Saúde", subfuncao="Atenção Básica")
```

**3. Indicadores de resultado**

> Prompt: "Compare mortalidade infantil e expectativa de vida nos municípios com maior e menor cobertura de PSF"

```
API: ibge_consultar_agregado (indicadores de saúde por município)
```

**4. Transferências federais do SUS**

> Prompt: "Quanto o governo federal transferiu para cada município do CE via SUS em 2024?"

```
API: transparencia_transferencias(uf="CE", funcao="Saúde")
```

### O Cross-Reference

```
Cobertura de PSF (CNES)   +   Gasto per capita (TCE-CE)
         ↓                            ↓
Mortalidade infantil (IBGE) ←→ Transferências SUS (Transparência)
```

### O Que a Análise Revela

| Grupo | Cobertura PSF | Mortalidade Infantil | Gasto Saúde/capita |
|-------|--------------|---------------------|-------------------|
| Top 20% (mais cobertura) | > 90% | 12,3/1000 | R$ 890 |
| Médios 60% | 50-90% | 16,7/1000 | R$ 650 |
| Bottom 20% (menos cobertura) | < 50% | 21,4/1000 | R$ 480 |

**Correlação clara: mais cobertura de PSF → menor mortalidade infantil.**

---

## Análise 2: Emendas PIX — Impacto Real ou Clientelismo?

### A Questão

As emendas PIX (transferências especiais) chegaram a bilhões em 2024. Esses recursos melhoram a vida dos municípios ou servem apenas a interesses eleitorais?

### O Roteiro

**1. Mapear emendas PIX por município**

> Prompt: "Quais municípios mais receberam emendas PIX em 2024 no Brasil?"

```
API: transferegov_buscar_emendas(ano=2024)
```

**2. Calcular per capita e comparar com indicadores**

> Prompt: "Cruze o valor per capita das emendas com o IDH dos municípios"

```
APIs: transferegov_buscar_emendas + ibge_buscar_municipios + ibge_consultar_agregado
```

**3. Verificar destino dos recursos**

> Prompt: "Em que os municípios gastaram as emendas PIX? Houve licitação?"

```
APIs: tce_[estado]_empenhos + pncp_buscar_contratacoes
```

**4. Analisar o padrão de distribuição**

> Prompt: "Emendas PIX são mais direcionadas para municípios da base aliada do governo ou distribuídas proporcionalmente?"

```
APIs: transferegov_buscar_emendas + camara_buscar_deputados (partido) + tse_buscar_candidatos
```

### Achados Típicos

```
DISTRIBUIÇÃO DE EMENDAS PIX — 2024

Por IDH do município:
  IDH Muito Alto (>0,800):  R$ 45/capita
  IDH Alto (0,700-0,799):   R$ 78/capita
  IDH Médio (0,600-0,699):  R$ 123/capita
  IDH Baixo (<0,600):       R$ 89/capita

⚠️ Municípios de IDH médio recebem MAIS que municípios
   de IDH baixo — sugerindo critério político, não social.

Por alinhamento político:
  Base do governo:           R$ 112/capita
  Oposição:                  R$ 67/capita
  ⚠️ Diferença de 67% a favor da base aliada.
```

---

## Análise 3: Desmatamento vs. Multas — O Ciclo da Impunidade?

### A Questão

O Brasil aplica multas ambientais, mas elas são efetivamente pagas? Há relação entre o desmatamento e a execução das penalidades?

### O Roteiro

**1. Dados de desmatamento**

> Prompt: "Qual o desmatamento acumulado por estado na Amazônia Legal nos últimos 5 anos?"

```
API: inpe_desmatamento(bioma="amazonia")
```

**2. Multas e sanções**

> Prompt: "Quantas empresas foram sancionadas por desmatamento ilegal? As multas foram pagas?"

```
APIs: transparencia_sancoes + tcu_buscar_acordaos(assunto="desmatamento")
```

**3. Processos judiciais**

> Prompt: "Quantos processos sobre crimes ambientais foram julgados nos últimos 5 anos?"

```
APIs: datajud_buscar_processos(assunto="crime ambiental")
      jurisprudencia_buscar_stj(termo="desmatamento condenacao")
```

**4. Recursos hídricos impactados**

> Prompt: "Os níveis dos reservatórios nas regiões com mais desmatamento caíram?"

```
API: ana_monitorar_reservatorios
```

### O Cross-Reference

```
Desmatamento (INPE)
    ↓
Multas aplicadas (Transparência)    →  Multas pagas? (Transparência)
    ↓                                       ↓
Processos judiciais (DataJud)       →  Condenações (Jurisprudência)
    ↓
Impacto hídrico (ANA)
```

---

## Análise 4: Reforma Tributária — Projeção de Impacto por Estado

### A Questão

A reforma tributária muda a distribuição de receitas entre estados. Quais ganham e quais perdem?

### O Roteiro

**1. Receitas atuais por estado**

> Prompt: "Qual a arrecadação de ICMS por estado nos últimos 3 anos?"

```
APIs: ibge_consultar_agregado (receitas estaduais)
      tce_[estado]_receitas
```

**2. PIB por estado**

> Prompt: "Qual o PIB e PIB per capita de cada estado?"

```
API: ibge_consultar_agregado (PIB estadual)
```

**3. Impacto legislativo**

> Prompt: "Quais foram as votações sobre reforma tributária na Câmara e no Senado? Como cada bancada estadual votou?"

```
APIs: camara_votacoes_proposicao + senado_votacoes_materia
```

**4. Publicações regulamentadoras**

> Prompt: "Busque no Diário Oficial as regulamentações da reforma tributária publicadas até agora"

```
API: diario_oficial_buscar(termo="reforma tributaria regulamentacao")
```

---

## Análise 5: Compras Públicas — Eficiência e Competitividade

### A Questão

As licitações públicas são competitivas ou dominadas por poucos fornecedores?

### O Roteiro

**1. Dados de licitações**

> Prompt: "Quantas licitações foram realizadas pelo governo federal em 2024? Qual o valor total?"

```
APIs: pncp_buscar_contratacoes(ano=2024)
      dadosabertos_buscar_contratos(ano=2024)
```

**2. Concentração de mercado**

> Prompt: "Quais os 20 maiores fornecedores do governo federal? Qual % do total representam?"

```
API: transparencia_buscar_contratos (agrupado por fornecedor)
```

**3. Competitividade das licitações**

> Prompt: "Qual a média de propostas por licitação? Quantas tiveram apenas 1 proponente?"

```
APIs: pncp_buscar_contratacoes + dadosabertos_buscar_licitacoes
```

**4. Penalidades e irregularidades**

> Prompt: "Quantas empresas fornecedoras do governo estão na lista de inidôneos do TCU?"

```
API: tcu_buscar_licitantes_inidoneos
```

---

## Каркас Для Анализа Государственной Политики

`mcp-russia` позволяет выстроить системный сценарий исследования:

```
1. CONTEXTO LEGISLATIVO
   └── Câmara/Senado: qual lei criou a política?

2. RECURSOS (INPUT)
   └── Transparência/TCEs: quanto foi investido?

3. IMPLEMENTAÇÃO (PROCESS)
   └── PNCP/Compras.gov.br: como foi executado?
   └── Diário Oficial: quais regulamentações?

4. RESULTADOS (OUTPUT)
   └── IBGE/CNES/Bacen: quais indicadores mudaram?

5. ACCOUNTABILITY
   └── TCU: houve irregularidades?
   └── DataJud: houve processos?
   └── TSE: quem se beneficiou politicamente?
```

### Автоматизация Через `planejar_consulta`

> Prompt: "Хочу оценить влияние программы льготного лекарственного обеспечения на доступность медикаментов. Составь план запросов"

`mcp-russia` строит полный план исследования: набор инструментов, порядок вызовов и зависимости между шагами.

---

_Источники: API IBGE, Banco Central, Portal da Transparência, TCEs (9 штатов), PNCP, Compras.gov.br, TransfereGov, INPE, ANA, CNES/DataSUS, DataJud, Jurisprudência STF/STJ, Câmara, Senado, Diário Oficial, TSE. В текущей версии они сохраняются как legacy-источники исходного проекта и должны постепенно заменяться на российские аналоги._
