# Análise Legislativa Cruzada: O Caminho de um Projeto de Lei

> Публичный сценарий для `mcp-russia`: кросс-анализ законодательного процесса по открытым парламентским, судебным и официальным источникам. Внутренние имена некоторых features пока могут оставаться legacy-совместимыми.

---

## O Que Este Exemplo Demonstra

Как проследить полный путь законопроекта: от внесения в парламент до публикации в официальных источниках, сопоставляя данные из **5 разных API**, чтобы понять, кто выступил инициатором, как проходили голосования, кто финансировал участников кампании и привел ли акт к судебным спорам.

---

## APIs Utilizadas

| API | Feature | O Que Forneceu |
|-----|---------|----------------|
| **Câmara dos Deputados** | `camara` | Proposições, autores, votações, tramitação |
| **Senado Federal** | `senado` | Matérias, votações, relatores, emendas |
| **Diário Oficial** | `diario_oficial` | Publicação da lei, regulamentações, portarias |
| **DataJud/CNJ** | `datajud` | Processos judiciais sobre a lei (ADIs, mandados) |
| **TSE** | `tse` | Financiamento de campanha dos votantes |
| **Jurisprudência** | `jurisprudencia` | Decisões do STF/STJ sobre a constitucionalidade |

---

## Caso: O Marco Legal da Inteligência Artificial

### O Cenário

В российской и русскоязычной повестке регулирование искусственного интеллекта обсуждается одновременно на уровне законопроектов, подзаконных актов и судебной практики. Как собрать это в единую аналитическую картину?

---

### Etapa 1: Encontrar os Projetos na Câmara

> Prompt: "Busque todos os projetos de lei sobre inteligência artificial que tramitaram na Câmara em 2024"

Ferramentas:
- `camara_buscar_proposicoes(tema="inteligencia artificial", ano=2024)`

Resultado esperado:

| PL | Autor | Partido | Situação |
|----|-------|---------|----------|
| PL 2338/2023 | Sen. Rodrigo Pacheco | PSD-MG | Em tramitação |
| PL 21/2020 | Dep. Eduardo Bismarck | PDT-CE | Aprovado Câmara |
| PL 5051/2019 | Sen. Styvenson Valentim | Podemos-RN | Arquivado |
| PL 872/2021 | Sen. Veneziano Vital do Rêgo | MDB-PB | Apensado |

> Prompt: "Detalhe o PL 2338/2023 — quem é o autor, qual a ementa e em que fase está"

Ferramentas:
- `camara_detalhes_proposicao(id=...)` — texto e ementa
- `camara_tramitacao_proposicao(id=...)` — histórico de tramitação

---

### Etapa 2: Votação na Câmara

> Prompt: "Como foi a votação do PL sobre IA na Câmara? Qual foi o placar por partido?"

Ferramentas:
- `camara_votacoes_proposicao(id=...)` — resultado da votação
- `camara_votos_votacao(votacao_id=...)` — voto de cada deputado

Resultado esperado:

| Partido | Sim | Não | Abstenção |
|---------|-----|-----|-----------|
| PL | 89 | 2 | 1 |
| PT | 65 | 0 | 3 |
| UNIÃO | 51 | 5 | 0 |
| MDB | 39 | 3 | 1 |
| PSD | 35 | 1 | 0 |
| ... | | | |
| **Total** | **401** | **23** | **12** |

---

### Etapa 3: Tramitação no Senado

> Prompt: "O PL sobre IA já chegou no Senado? Quem é o relator? Que emendas foram apresentadas?"

Ferramentas:
- `senado_buscar_materias(tipo="PL", tema="inteligencia artificial")`
- `senado_detalhes_materia(codigo=...)` — relator, comissão
- `senado_emendas_materia(codigo=...)` — emendas apresentadas
- `senado_tramitacao_materia(codigo=...)` — histórico no Senado

Resultado esperado:

```
Matéria: PL 2338/2023 — Marco Legal da IA
Relator: Sen. [Nome] ([Partido]-[UF])
Comissão: CTIA (Comissão Temporária sobre IA)
Status: Aprovado com substitutivo
Emendas: 52 apresentadas, 18 acatadas
```

---

### Etapa 4: Votação no Senado

> Prompt: "Como os senadores votaram o Marco Legal da IA? Compare com a votação na Câmara"

Ferramentas:
- `senado_votacoes_materia(codigo=...)` — resultado
- `senado_votos_votacao(codigo_sessao=...)` — voto nominal

Resultado esperado:

| | Câmara | Senado |
|--|--------|--------|
| **Sim** | 401 (92%) | 64 (79%) |
| **Não** | 23 (5%) | 12 (15%) |
| **Abstenção** | 12 (3%) | 5 (6%) |
| **Resultado** | Aprovado | Aprovado com emendas |

**Когда верхняя палата меняет текст, законопроект возвращается на повторное рассмотрение.** Такой цикл удобно отслеживать в одном сценарии вместо ручного обхода нескольких порталов.

---

### Etapa 5: Publicação no Diário Oficial

> Prompt: "A lei de IA já foi publicada no Diário Oficial? Busque a publicação"

Ferramentas:
- `diario_oficial_buscar(termo="inteligencia artificial", tipo="lei")`

Querido Diario агрегирует муниципальные и региональные официальные публикации. Для федеральных актов поиск помогает увидеть не только публикацию в центральном источнике, но и локальные акты применения или имплементации.

---

### Etapa 6: Contestações Judiciais

> Prompt: "Alguém entrou com ação judicial contra a lei de IA? Busque ADIs no STF"

Ferramentas:
- `datajud_buscar_processos(assunto="inteligencia artificial", tribunal="STF")`
- `jurisprudencia_buscar_stf(termo="inteligencia artificial regulamentacao")`

Resultado esperado:

| Processo | Tipo | Requerente | Status |
|----------|------|-----------|--------|
| ADI 7654 | Ação Direta de Inconstitucionalidade | Partido X | Em julgamento |
| MC 12345 | Mandado de Segurança | Associação Y | Indeferido |

> Prompt: "Qual o entendimento do STF sobre regulamentação de tecnologia? Há precedentes?"

Ferramentas:
- `jurisprudencia_buscar_stf(termo="regulamentacao tecnologia")`
- `jurisprudencia_buscar_stj(termo="inteligencia artificial responsabilidade")`

---

### Etapa 7: Quem Financiou os Votantes?

> Prompt: "Os deputados que votaram contra o Marco da IA receberam doações de empresas de tecnologia?"

Ferramentas:
- `camara_votos_votacao(votacao_id=...)` — lista dos que votaram "Não"
- `executar_lote` para buscar financiamento de cada um no TSE:

```json
[
  {"tool": "tse_buscar_candidatos", "args": {"nome": "Deputado 1", "ano": 2022}},
  {"tool": "tse_buscar_candidatos", "args": {"nome": "Deputado 2", "ano": 2022}},
  {"tool": "tse_buscar_candidatos", "args": {"nome": "Deputado 3", "ano": 2022}}
]
```

Depois, para cada candidato encontrado:
- `tse_receitas_candidato(id=...)` — doadores e valores

### O Cross-Reference Completo

```
PL apresentado (Câmara)
    ↓
Votação na Câmara (Câmara) → Quem votou? (Câmara)
    ↓                              ↓
Tramitação no Senado (Senado)   Quem financiou? (TSE)
    ↓                              ↓
Votação no Senado (Senado)     Doadores têm contratos? (Transparência)
    ↓
Publicação (Diário Oficial)
    ↓
Contestação judicial (DataJud/STF)
    ↓
Jurisprudência (STF/STJ/TST)
```

**Несколько API и один связный аналитический контур.**

---

## Caso 2: Monitoramento Legislativo Contínuo

### Para Organizações e Jornalistas

> Prompt: "Liste todas as proposições sobre mineração em terras indígenas que tiveram movimentação na última semana"

Ferramentas:
- `camara_buscar_proposicoes(tema="mineracao terras indigenas", tramitacao_recente=True)`
- `senado_buscar_materias(assunto="mineracao terras indigenas")`

> Prompt: "Quais proposições sobre reforma tributária estão pautadas para votação esta semana?"

Ferramentas:
- `senado_agenda_plenario` — pauta do Senado
- `camara_buscar_proposicoes(situacao="Pauta")` — pauta da Câmara

---

## Caso 3: Comparando Versões — Câmara vs. Senado

### O Cenário

O Senado altera significativamente um projeto vindo da Câmara. Quais artigos mudaram?

> Prompt: "Compare a versão aprovada na Câmara do PL [X] com o substitutivo do Senado. Quais os principais pontos de divergência?"

Ferramentas:
- `camara_detalhes_proposicao(id=...)` — texto da Câmara
- `senado_texto_materia(codigo=...)` — texto do Senado
- `senado_emendas_materia(codigo=...)` — emendas que alteraram o texto

LLM может сопоставить редакции и выделить содержательные расхождения без ручной вычитки больших массивов текста.

---

## Caso 4: Agenda do Plenário e Análise Preditiva

> Prompt: "O que está pautado para votação no Senado esta semana? Para cada matéria, como as bancadas tendem a votar com base em votações similares?"

Ferramentas:
- `senado_agenda_plenario` — pauta da semana
- `senado_votacoes_materia` — histórico de votações similares
- `senado_composicao_comissao` — quem é relator de cada matéria

### Análise Preditiva

O LLM pode cruzar:
1. **Tema da matéria** (ex: ambiental)
2. **Histórico de votação por partido** em temas similares
3. **Posição do relator** e da comissão
4. **Governo vs. oposição** na composição atual

Para gerar uma estimativa de como a votação pode se desenrolar.

---

## Usando `planejar_consulta` Para Análise Completa

> Prompt: "Faça uma análise completa do PL 2338/2023 sobre IA: tramitação, votações, autores, financiamento dos votantes e processos judiciais"

Публично этот сценарий относится к `mcp-russia`, даже если внутри отдельные tool IDs и модули еще используют исторические namespaced-алиасы.

A meta-tool gera:

```
Plano de Execução:
═══════════════════

Etapa 1 — Identificação:
  ├── camara_buscar_proposicoes(numero=2338, ano=2023)
  └── senado_buscar_materias(numero=2338, ano=2023)

Etapa 2 — Detalhamento (paralelo):
  ├── camara_detalhes_proposicao(id=...)
  ├── camara_tramitacao_proposicao(id=...)
  ├── senado_detalhes_materia(codigo=...)
  └── senado_tramitacao_materia(codigo=...)

Etapa 3 — Votações (paralelo):
  ├── camara_votacoes_proposicao(id=...)
  └── senado_votacoes_materia(codigo=...)

Etapa 4 — Financiamento (paralelo, lote):
  └── executar_lote([tse_receitas para cada votante-chave])

Etapa 5 — Judicial:
  ├── datajud_buscar_processos(assunto="PL 2338")
  └── jurisprudencia_buscar_stf(termo="inteligencia artificial")

Etapa 6 — Publicação:
  └── diario_oficial_buscar(termo="Lei [número]")
```

---

## O Poder da Análise Cruzada

Ключевая ценность `mcp-russia` не в доступе к каждой API по отдельности, а в том, чтобы **сшивать их между собой**:

| Pergunta | APIs Necessárias |
|----------|-----------------|
| "Quem propôs e quem financiou o autor?" | Câmara + TSE |
| "Quem votou a favor e quem financiou os votantes?" | Câmara/Senado + TSE |
| "A lei foi publicada e está sendo cumprida?" | Diário Oficial + DataJud |
| "Há contestação judicial?" | DataJud + Jurisprudência |
| "Os doadores dos votantes se beneficiam da lei?" | TSE + Transparência + PNCP |
| "Qual a repercussão nos municípios?" | Diário Oficial (municipal) |

**Ни на один из этих вопросов нельзя полноценно ответить одной API.** Практическая ценность возникает именно на стыке источников.

---

## Como Verificar Você Mesmo

| Dado | Fonte | URL |
|------|-------|-----|
| Proposições e votações | Câmara | dadosabertos.camara.leg.br |
| Matérias e votações | Senado | legis.senado.leg.br |
| Diários oficiais | Querido Diário | queridodiario.ok.org.br |
| Processos judiciais | DataJud/CNJ | datajud-wiki.cnj.jus.br |
| Jurisprudência STF | STF | portal.stf.jus.br |
| Jurisprudência STJ | STJ | scon.stj.jus.br |
| Financiamento eleitoral | TSE | divulgacandcontas.tse.jus.br |
| Contratos federais | Transparência | portaldatransparencia.gov.br |
| Licitações | PNCP | pncp.gov.br |

---

_Fontes de dados: API da Câmara dos Deputados, API do Senado Federal, API do Querido Diário, API do DataJud/CNJ, Jurisprudência STF/STJ/TST, API do TSE, API do Portal da Transparência, API do PNCP._

_Nota: Valores e cenários ilustrativos para demonstrar as capacidades do `mcp-russia` в его текущем переходном состоянии. Используйте tools для получения актуальных данных и учитывайте, что часть внутренних названий пока остается legacy-совместимой._
