# Caso de Uso: Cientista Político — Comportamento Legislativo, Coalizões e Poder

> Публичный сценарий для `mcp-russia`: как исследователи политических институтов могут изучать поименные голосования, коалиции, дисциплину фракций, распределение трансфертов и электоральное финансирование на основе официальных API. Часть внутренних feature-имен ниже пока сохранена в legacy-совместимом виде.

---

## Почему `mcp-russia` полезен для политического анализа

Для политической науки в русскоязычном контуре главная проблема обычно одна и та же: данные о парламентской активности, финансировании, трансфертах и судебных спорах лежат в разрозненных системах, где без ручной выгрузки и чистки быстро не обойтись. `mcp-russia` собирает такой исследовательский контур в единую точку входа, а текущие бразильские интеграции выступают как переходный compatibility-layer:

| Base | Feature | Relevância |
|------|---------|-----------|
| **Câmara dos Deputados** | `camara` (10 tools) | Votações nominais, proposições, comissões, despesas |
| **Senado Federal** | `senado` (26 tools) | Votações, matérias, composição de comissões, agenda |
| **TSE** | `tse` (15 tools) | Электоральное финансирование, кандидаты, результаты |
| **Portal da Transparência** | `transparencia` (18 tools) | Трансферты, выплаты, контракты |
| **TransfereGov** | `transferegov` (5 tools) | Специальные трансферты и иные межбюджетные перечисления |
| **Diário Oficial** | `diario_oficial` (4 tools) | Publicações, nomeações, regulamentações |
| **DataJud** | `datajud` (7 tools) | Processos, judicialização da política |

**Итого: 85 tools, полезных для сравнительного институционального анализа уже сейчас.**

---

## Estudo 1: Índice de Fidelidade Partidária

### A Pergunta de Pesquisa

Каков уровень фракционной дисциплины в парламенте? Какие объединения голосуют наиболее слаженно, а какие депутаты чаще других расходятся с линией своей политической силы?

### Metodologia

**1. Coletar todas as votações nominais do período**

> Prompt: "Liste todas as votações nominais na Câmara em 2024 com os votos individuais de cada deputado"

```
APIs: camara_listar_votacoes(ano=2024)
      camara_votos_votacao(votacao_id=...) → para cada votação
```

Usando `executar_lote` para paralelizar a coleta:

```json
[
  {"tool": "camara_votos_votacao", "args": {"votacao_id": "2024-001"}},
  {"tool": "camara_votos_votacao", "args": {"votacao_id": "2024-002"}},
  {"tool": "camara_votos_votacao", "args": {"votacao_id": "2024-003"}}
]
```

**2. Construir a matriz de votação**

O LLM estrutura os dados em formato deputado × votação:

```
MATRIZ DE VOTAÇÃO — Câmara 2024 (amostra)

                    Vot.001  Vot.002  Vot.003  ...  Vot.087
Dep. A (PT-SP)       SIM      SIM      NÃO          SIM
Dep. B (PT-RJ)       SIM      SIM      SIM          SIM
Dep. C (PL-MG)       NÃO      NÃO      SIM          NÃO
Dep. D (PL-SP)       NÃO      ABS      SIM          NÃO
Dep. E (MDB-GO)      SIM      NÃO      SIM          SIM
...
```

**3. Calcular fidelidade por partido**

Para cada deputado, comparar seu voto com a posição majoritária do partido:

```
ÍNDICE DE FIDELIDADE PARTIDÁRIA — 2024

Partido    Deputados   Votações   Fidelidade   Desvio Padrão
────────────────────────────────────────────────────────────
PT            68          87        94,2%          4,1%
PL            92          87        91,8%          6,3%
UNIÃO         59          87        82,5%         11,2%
MDB           44          87        79,3%         13,8%
PP            50          87        85,1%          9,7%
PSD           45          87        83,7%         10,4%
PSOL          12          87        97,8%          2,1%
NOVO           4          87        96,5%          3,3%

Mais coesos: PSOL (97,8%), NOVO (96,5%), PT (94,2%)
Menos coesos: MDB (79,3%), UNIÃO (82,5%), PSD (83,7%)
```

**4. Identificar os "rebeldes"**

> Prompt: "Quais deputados mais votaram contra a orientação de seus partidos em 2024?"

```
TOP 10 DEPUTADOS "REBELDES" — 2024

Deputado              Partido   Fidelidade   Divergências
──────────────────────────────────────────────────────────
[Nome 1]              MDB-XX      52%         42 de 87
[Nome 2]              UNIÃO-XX    58%         37 de 87
[Nome 3]              PP-XX       61%         34 de 87
...
```

---

## Estudo 2: Análise de Coalizão — Governo vs. Oposição

### A Pergunta de Pesquisa

Каков реальный размер проправительственной коалиции? Сохраняется ли она от голосования к голосованию или разваливается на отдельных темах?

### Metodologia

**1. Mapear a orientação do governo em cada votação**

> Prompt: "Em cada votação nominal de 2024, qual foi a orientação do líder do governo? Compare com o resultado"

```
API: camara_votacoes_proposicao → inclui orientação do governo
```

**2. Calcular taxa de governismo por partido**

```
TAXA DE GOVERNISMO POR PARTIDO — 2024

Partido    Tipo        Governismo   Quando diverge
──────────────────────────────────────────────────────────
PT         Base         98,1%       Quase nunca
PSD        Base         87,3%       Temas fiscais
MDB        Base         82,5%       Costumes, segurança
PP         Base         84,9%       Temas tributários
UNIÃO      Base         76,2%       Varia muito por tema
PL         Oposição     18,3%       Pauta econômica às vezes
NOVO       Oposição     12,7%       Quase nunca
PSOL       Oposição*    71,4%       Segurança, defesa
──────────────────────────────────────────────────────────
* PSOL: oposição formal mas vota com governo em pautas sociais
```

**3. Analisar coalizão por tema**

> Prompt: "A base governista é maior ou menor em votações sobre economia vs. costumes vs. segurança?"

```
TAMANHO DA COALIZÃO POR TEMA — 2024

Tema                    Votos com governo   % da Câmara
──────────────────────────────────────────────────────────
Orçamento/fiscal         312 de 513          60,8%
Saúde/educação           378 de 513          73,7%
Tributação               298 de 513          58,1%
Segurança/defesa         267 de 513          52,0%
Costumes                 241 de 513          47,0%  ⚠️
Meio ambiente            289 de 513          56,3%
──────────────────────────────────────────────────────────

Achado: A coalizão se fragmenta em pautas de costumes
(aborto, drogas, armas) onde partidos do "centrão"
votam com a oposição conservadora.
```

---

## Estudo 3: Emendas Como Instrumento de Poder — Análise Distributiva

### A Pergunta de Pesquisa

Распределяются ли парламентские трансферты по социальным критериям или решающую роль играют политические связи и электоральные интересы?

### Metodologia

**1. Coletar todas as emendas individuais**

> Prompt: "Liste todas as emendas parlamentares individuais executadas em 2024, com autor, valor, município e área"

```
APIs: transparencia_emendas_parlamentares(ano=2024)
      transferegov_buscar_emendas(ano=2024)
```

**2. Classificar autores por posição política**

> Prompt: "Para cada deputado que destinou emendas, identifique partido e se é governo ou oposição"

```
APIs: camara_buscar_deputados → partido e bancada
```

**3. Cruzar com indicadores sociais dos municípios**

> Prompt: "Para cada município que recebeu emendas, qual o IDH, taxa de pobreza e população?"

```
APIs: ibge_buscar_municipios + ibge_consultar_agregado
```

**4. Modelo distributivo**

```
DISTRIBUIÇÃO DE EMENDAS — ANÁLISE MULTIVARIADA 2024

                            Emenda média/capita
Variável                    Coeficiente    Sig.
──────────────────────────────────────────────────
IDH do município             -0,23         **
População (log)              -0,41         ***
Autor é da base gov.         +0,38         ***
Município é reduto eleitoral +0,52         ***
Estado do autor              +0,67         ***
Ano eleitoral                +0,19         *
──────────────────────────────────────────────────
R² = 0,47

Interpretação:
• Municípios menores recebem mais per capita (pop -)
• Municípios do próprio estado do deputado recebem mais
• Base aliada recebe 38% mais que oposição
• Reduto eleitoral é o fator mais forte (+52%)
• IDH tem efeito negativo — municípios mais pobres
  recebem um pouco mais, mas efeito é fraco vs. político
```

**5. Проверить географическую концентрацию**

> Prompt: "Quais municípios mais receberam emendas per capita? São redutos eleitorais de quais deputados?"

```
APIs: transferegov_buscar_emendas
      tse_buscar_candidatos + tse_resultados_eleicao
```

```
TOP 10 MUNICÍPIOS — EMENDAS PER CAPITA 2024

Município         UF   Pop.     Emendas/cap   Dep. que enviou    Votação do dep. aqui (2022)
──────────────────────────────────────────────────────────────────────────────────────────────
[Cidade A]        PI   8.200    R$ 2.340      Dep. X (PP-PI)     78% dos votos ← reduto
[Cidade B]        CE   5.100    R$ 1.890      Dep. Y (MDB-CE)    82% dos votos ← reduto
[Cidade C]        MA   12.300   R$ 1.567      Dep. Z (PL-MA)     71% dos votos ← reduto
...
──────────────────────────────────────────────────────────────────────────────────────────────

Correlação: emendas/capita × votação do deputado no município = +0,61
```

Даже в этом примере `mcp-russia` следует читать как публичную исследовательскую оболочку: конкретные calls к `tse_*`, `transferegov_*` и другим legacy tools пока отражают текущее состояние исходного data-layer, а не финальную российскую модель данных.

---

## Estudo 4: Judicialização da Política

### A Pergunta de Pesquisa

Com que frequência leis aprovadas pelo Congresso são contestadas judicialmente? Quais partidos mais judicializam?

### Metodologia

**1. Listar leis aprovadas no período**

> Prompt: "Quantas leis ordinárias e complementares foram aprovadas em 2023-2024?"

```
APIs: camara_buscar_proposicoes(tipo="PL", situacao="Transformado em Lei")
      senado_buscar_materias(tipo="PLC", situacao="Aprovado")
```

**2. Buscar ADIs contra essas leis**

> Prompt: "Quantas Ações Diretas de Inconstitucionalidade foram ajuizadas contra leis de 2023-2024?"

```
APIs: datajud_buscar_processos(classe="ADI", periodo="2023-2024")
      jurisprudencia_buscar_stf(termo="inconstitucionalidade lei 2024")
```

**3. Classificar por requerente**

```
JUDICIALIZAÇÃO DE LEIS — 2023-2024

Requerente                      ADIs    % Total
──────────────────────────────────────────────
Partidos de oposição              23      38%
Partidos da base                   5       8%
Governadores                      12      20%
Procuradoria-Geral                 8      13%
Entidades de classe                7      12%
Confederações sindicais            5       8%
──────────────────────────────────────────────
Total                             60     100%

Temas mais judicializados:
  1. Tributação (18 ADIs)
  2. Direitos fundamentais (12 ADIs)
  3. Competência federativa (10 ADIs)
  4. Orçamento/fiscal (8 ADIs)
```

**4. Taxa de sucesso**

> Prompt: "Das ADIs ajuizadas, quantas obtiveram liminar ou foram julgadas procedentes?"

```
APIs: jurisprudencia_buscar_stf(termo="ADI procedente 2024")
      datajud_movimentacoes_processo(id=...)
```

---

## Estudo 5: Poder de Agenda — Quem Controla a Pauta?

### A Pergunta de Pesquisa

Quem define o que é votado e quando? A pauta do plenário reflete as prioridades do presidente da Casa, do governo ou das comissões?

### Metodologia

**1. Coletar a agenda do plenário**

> Prompt: "Quais matérias foram pautadas para votação no Senado em cada semana de 2024?"

```
API: senado_agenda_plenario(ano=2024)
```

**2. Classificar por origem e prioridade**

> Prompt: "Para cada matéria votada, identifique: quem propôs, qual comissão relatou, se é urgência do governo"

```
APIs: senado_detalhes_materia(codigo=...)
      senado_tramitacao_materia(codigo=...)
```

**3. Analisar tempo de tramitação**

```
TEMPO DE TRAMITAÇÃO — SENADO 2024

Origem da matéria          Mediana (dias)   Máximo
──────────────────────────────────────────────────
Governo (urgência const.)       45            120
Governo (regime normal)        180            540
Senador da base                210            720
Senador da oposição            380          1.200+
Câmara (revisão)               90            365
──────────────────────────────────────────────────

Achado: Matérias do governo com urgência constitucional
tramitam 8x mais rápido que projetos da oposição.
```

**4. Medir o "poder de gaveta"**

> Prompt: "Quantas proposições foram apresentadas vs. quantas chegaram a votação em plenário?"

```
FUNIL LEGISLATIVO — SENADO 2024

Apresentadas:                    432  (100%)
Distribuídas a comissão:         398   (92%)
Relatório aprovado em comissão:  112   (26%)
Pautadas no plenário:             67   (16%)
Votadas:                          54   (13%)
Aprovadas:                        41    (9%)
──────────────────────────────────────────────
87% das proposições NUNCA chegam ao plenário.
O relator e o presidente da comissão decidem
o destino de 74% dos projetos.
```

---

## Estudo 6: Carreiras Políticas e Financiamento

### A Pergunta de Pesquisa

Existe correlação entre o volume de financiamento e o sucesso eleitoral? Candidatos mais financiados vencem mais?

### Metodologia

**1. Coletar dados de candidaturas e receitas**

> Prompt: "Para todos os candidatos a deputado federal em SP em 2022, liste: votos recebidos, total arrecadado e se foi eleito"

```
APIs: tse_buscar_candidatos(cargo="deputado federal", uf="SP", ano=2022)
      tse_receitas_candidato(id=...) → para cada candidato
      tse_resultados_eleicao(...) → votos e resultado
```

**2. Construir o modelo**

```
FINANCIAMENTO vs. ELEIÇÃO — Dep. Federal SP 2022

                        Eleitos     Não-eleitos   Razão
──────────────────────────────────────────────────────────
Arrecadação média       R$ 2,8M     R$ 340K       8,2x
Mediana arrecadação     R$ 2,1M     R$ 120K      17,5x
% fundo eleitoral       62%          31%          2,0x
% pessoas físicas       24%          45%          0,5x
Nº de doadores PF       89           23           3,9x
──────────────────────────────────────────────────────────

Correlação financiamento × votos: +0,72 (forte)
Correlação fundo eleitoral × eleição: +0,58 (moderada)

Achado: O acesso ao fundo eleitoral é o preditor mais
forte de sucesso — mais do que ideologia, experiência
prévia ou popularidade medida por pesquisas.
```

**3. Analisar a concentração do fundo**

> Prompt: "Como o fundo eleitoral foi distribuído entre os partidos? E dentro de cada partido, entre candidatos?"

```
CONCENTRAÇÃO DO FUNDO ELEITORAL — 2022

Distribuição entre partidos:
  Top 5 partidos: 68% do total
  Bottom 15 partidos: 8% do total
  Gini entre partidos: 0,62

Distribuição DENTRO dos partidos (média):
  10% dos candidatos recebem 55% dos recursos
  50% dos candidatos recebem 12% dos recursos
  Gini intra-partidário: 0,71

Achado: A concentração DENTRO dos partidos é maior
que ENTRE partidos — a direção partidária escolhe
quem vai ser eleito ao direcionar os recursos.
```

---

## Ferramentas Para o Cientista Político

### `planejar_consulta` — Design de Pesquisa Assistido

> Prompt: "Quero estudar o efeito das emendas parlamentares na votação dos deputados a favor do governo. Planeje as consultas necessárias"

Retorna um plano com todas as variáveis, fontes e ordem de coleta.

### `executar_lote` — Coleta de Dados em Escala

Para coletar votações de todos os 513 deputados:

```json
[
  {"tool": "camara_votacoes_deputado", "args": {"id": 204554}},
  {"tool": "camara_votacoes_deputado", "args": {"id": 204555}},
  {"tool": "camara_votacoes_deputado", "args": {"id": 204556}}
]
```

Até 25 consultas por lote, múltiplos lotes em sequência = cobertura total.

### `recomendar_tools` — Descoberta de Dados

> Prompt: "Какие данные о законодательном поведении уже доступны в `mcp-russia`?"

Retorna as ferramentas mais relevantes com descrição de cada uma.

---

## Variáveis Disponíveis Para Modelos

### Variável Dependente — Comportamento do Parlamentar

| Variável | Fonte | Tool |
|----------|-------|------|
| Voto nominal (sim/não/abs) | Câmara | `camara_votos_votacao` |
| Voto nominal | Senado | `senado_votos_votacao` |
| Proposições apresentadas | Câmara | `camara_buscar_proposicoes` |
| Proposições apresentadas | Senado | `senado_buscar_materias` |
| Despesas de gabinete | Câmara | `camara_despesas_deputado` |

### Variáveis Independentes — Político

| Variável | Fonte | Tool |
|----------|-------|------|
| Partido e bancada | Câmara/Senado | `camara_detalhes_deputado` |
| Receitas de campanha | TSE | `tse_receitas_candidato` |
| Doadores (PF e PJ) | TSE | `tse_receitas_candidato` |
| Votação recebida | TSE | `tse_resultados_eleicao` |
| Emendas destinadas | Transparência | `transparencia_emendas_parlamentares` |
| Emendas PIX | TransfereGov | `transferegov_buscar_emendas` |

### Variáveis Independentes — Contexto

| Variável | Fonte | Tool |
|----------|-------|------|
| IDH do município | IBGE | `ibge_consultar_agregado` |
| População | IBGE | `ibge_buscar_municipios` |
| PIB per capita | IBGE | `ibge_consultar_agregado` |
| Indicadores econômicos | Bacen | `bacen_indicadores_atuais` |
| Processos judiciais | DataJud | `datajud_buscar_processos` |

### Variáveis de Resultado — Políticas Públicas

| Variável | Fonte | Tool |
|----------|-------|------|
| Gastos municipais por área | TCEs | `tce_[estado]_despesas` |
| Contratos celebrados | PNCP | `pncp_buscar_contratacoes` |
| Infraestrutura de saúde | CNES | `saude_buscar_estabelecimentos` |
| Indicadores ambientais | INPE | `inpe_focos_queimadas` |
| Indicadores hídricos | ANA | `ana_monitorar_reservatorios` |

---

## Limitações e Cuidados Metodológicos

### O Que os Dados Permitem

- Análise descritiva de comportamento legislativo
- Correlações entre financiamento e votação
- Mapeamento de coalizões e fidelidade
- Análise distributiva de emendas
- Séries temporais de indicadores

### O Que os Dados NÃO Permitem (Sozinhos)

- **Causalidade:** Correlação entre doação e voto não prova compra de voto
- **Motivação:** Dados não revelam por que um deputado votou de certa forma
- **Completude:** Nem toda interação política é registrada em APIs
- **Tempo real:** Algumas APIs têm atraso de atualização (dias a meses)

### Boas Práticas

1. **Sempre cite a API de origem** com data da consulta
2. **Use múltiplas fontes** para triangulação
3. **Distinga correlação de causalidade** na análise
4. **Considere variáveis omitidas** — lobby presencial, relações pessoais, pressão da mídia
5. **Verifique outliers** — dados faltantes podem distorcer estatísticas

---

_Источники: парламентские API, электоральные данные, Portal da Transparencia, TransfereGov, DataJud, судебная практика, IBGE, Banco Central и другие legacy-интеграции исходного проекта._

_Примечание: коэффициенты и результаты в примере иллюстративные. Для реального исследования запускайте tools на живых данных и отдельно фиксируйте, какие сущности пока используются как compatibility-слой, а какие уже перенесены в русскоязычное позиционирование `mcp-russia`._
