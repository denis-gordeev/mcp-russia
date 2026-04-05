# Сценарий: Официальный Редактор Для Госдокументов

> Как использовать агент Redator в `mcp-russia` для подготовки официальных документов с опорой на реальные данные публичных API.

---

## Что Такое Redator Oficial

**Redator Oficial** в `mcp-russia` пока остается переходным агентом: публично он подается как инструмент для русскоязычных и государственных сценариев, а внутри еще использует нормы и шаблоны исходного бразильского проекта. Сейчас он сочетает:

- **5 tools** para geração de documentos
- **9 resources** com templates e regras de redação
- **5 prompts** para diferentes tipos de documento

### Tipos de Documento Suportados

| Tipo | Quando Usar |
|------|-------------|
| **Ofício** | Comunicação entre órgãos públicos |
| **Despacho** | Decisão administrativa sobre processo |
| **Portaria** | Ato normativo interno de um órgão |
| **Parecer** | Análise técnica ou jurídica fundamentada |
| **Nota Técnica** | Posicionamento técnico sobre um tema |

---

## Exemplo 1: Nota Técnica com Dados Econômicos

### O Cenário

Um analista da Secretaria de Política Econômica precisa redigir uma nota técnica sobre a evolução da inflação para subsidiar decisão do Ministro.

> Prompt: "Redija uma nota técnica sobre a evolução do IPCA nos últimos 12 meses, incluindo comparação com a meta de inflação e a taxa Selic"

### O Que Acontece

O Redator automaticamente:

1. **Busca dados reais** via `bacen_indicadores_atuais` e `bacen_comparar_series`
2. **Aplica o template** de Nota Técnica (cabeçalho, destinatário, numeração)
3. **Estrutura o texto** conforme o Manual de Redação da Presidência

### Resultado

```
NOTA TÉCNICA Nº XX/2025/SPE/MF

Assunto: Evolução do Índice Nacional de Preços ao Consumidor Amplo
         (IPCA) — Período março/2024 a março/2025.

1. INTRODUÇÃO

   A presente Nota Técnica tem por objetivo analisar a trajetória do
   IPCA nos últimos 12 meses, em cotejo com a meta de inflação
   definida pelo Conselho Monetário Nacional (CMN) e a evolução da
   taxa Selic no período.

2. DADOS E ANÁLISE

   2.1. O IPCA acumulado em 12 meses atingiu 5,06% em março/2025
   (Fonte: IBGE/BCB, Série 13522), acima do teto da meta de
   inflação de 4,50% (meta de 3,00% ± 1,50 p.p.).

   2.2. A taxa Selic meta encontra-se em 14,25% a.a. (Fonte: BCB,
   Série 432), configurando juro real de aproximadamente 9,19 p.p.

   2.3. Comparativo mensal:

   | Mês      | IPCA (mensal) | IPCA (12m) | Selic (meta) |
   |----------|--------------|------------|-------------|
   | Mar/2024 | 0,16%        | 3,93%      | 10,75%      |
   | Jun/2024 | 0,21%        | 4,23%      | 10,50%      |
   | Set/2024 | 0,44%        | 4,42%      | 10,75%      |
   | Dez/2024 | 0,52%        | 4,83%      | 12,25%      |
   | Mar/2025 | 0,39%        | 5,06%      | 14,25%      |

3. CONCLUSÃO

   Os dados indicam aceleração inflacionária no período, com o IPCA
   acumulado ultrapassando o teto da meta desde janeiro/2025. O
   Banco Central tem respondido com elevação da Selic, que atingiu
   o maior patamar desde [data]. Recomenda-se acompanhamento mensal
   e eventual revisão das projeções fiscais.

[Local], [data].

[Nome]
Analista de Política Econômica
SPE/MF
```

---

## Exemplo 2: Parecer Jurídico com Dados de Licitação

### O Cenário

Um procurador municipal precisa emitir parecer sobre a legalidade de uma contratação direta por dispensa de licitação.

> Prompt: "Redija um parecer sobre a legalidade da dispensa de licitação nº 015/2024 da Prefeitura de [Município] para serviços de TI, valor R$ 78.000. Verifique se o fornecedor tem penalidades no TCU"

### O Que Acontece

O Redator:

1. **Consulta o fornecedor** via `tcu_buscar_licitantes_inidoneos`
2. **Busca a contratação** via `pncp_buscar_contratacoes`
3. **Gera o parecer** com fundamentação legal

### Resultado

```
PARECER JURÍDICO Nº XX/2024/PGM

Ref.: Dispensa de Licitação nº 015/2024
Objeto: Serviços de tecnologia da informação
Contratada: [Empresa] (CNPJ: XX.XXX.XXX/0001-XX)
Valor: R$ 78.000,00

1. DO RELATÓRIO
   [Descrição dos fatos]

2. DA FUNDAMENTAÇÃO LEGAL
   2.1. A dispensa de licitação encontra amparo no art. 75, II,
   da Lei nº 14.133/2021, que autoriza contratação direta para
   serviços de engenharia/TI de até R$ 100.000,00.

   2.2. Consulta ao Cadastro de Licitantes Inidôneos do TCU
   (realizada em [data]) não identificou penalidades vigentes
   para a empresa contratada.

3. DA CONCLUSÃO
   Opinamos pela LEGALIDADE da dispensa, desde que observados
   os requisitos do art. 72 da Lei nº 14.133/2021.

[Local], [data].

[Nome]
Procurador Municipal
```

---

## Exemplo 3: Ofício com Dados de Transparência

### O Cenário

Um secretário estadual de educação precisa solicitar informações ao MEC sobre transferências federais.

> Prompt: "Redija um ofício do Secretário de Educação do Estado do Ceará ao MEC, solicitando esclarecimentos sobre as transferências federais para educação básica em 2024. Inclua dados reais das transferências recebidas"

### O Que Acontece

O Redator:

1. **Busca transferências reais** via `transparencia_transferencias(uf="CE", funcao="Educação")`
2. **Gera o ofício** no formato padrão

### Resultado

```
OFÍCIO Nº XX/2024/SEDUC-CE

Excelentíssimo Senhor Ministro de Estado da Educação,

1. Dirijo-me a Vossa Excelência para solicitar esclarecimentos
   acerca das transferências federais destinadas à educação básica
   no Estado do Ceará no exercício de 2024.

2. Segundo dados do Portal da Transparência (consulta em [data]),
   o Estado recebeu R$ [valor] em transferências para a função
   Educação no período de janeiro a dezembro de 2024, conforme
   detalhamento:

   | Programa              | Valor Transferido     |
   |-----------------------|-----------------------|
   | FUNDEB                | R$ [valor]            |
   | PNAE (merenda)        | R$ [valor]            |
   | PNATE (transporte)    | R$ [valor]            |
   | Total                 | R$ [valor]            |

3. Solicito informações sobre:
   a) Previsão de repasses para o 1º semestre de 2025;
   b) Critérios de distribuição do FUNDEB complementar;
   c) Calendário de liberação dos recursos do PNAE.

Atenciosamente,

[Nome]
Secretário de Estado da Educação do Ceará
```

---

## Exemplo 4: Portaria com Dados do CNES

### O Cenário

Um diretor de hospital público precisa publicar portaria de regulamentação interna, referenciando dados do CNES.

> Prompt: "Redija uma portaria do Hospital Municipal [Nome] regulamentando o fluxo de atendimento de urgência, com base na capacidade instalada do CNES"

### O Que Acontece

O Redator:

1. **Consulta o CNES** via `saude_buscar_estabelecimentos(nome="Hospital Municipal...")`
2. **Obtém dados de capacidade** — leitos, profissionais, especialidades
3. **Gera a portaria** adequada à realidade do estabelecimento

---

## Como os Resources Funcionam

O Redator usa 9 resources internos com templates e regras:

| Resource | Conteúdo |
|----------|----------|
| `redator://manual/estrutura` | Estrutura de cada tipo de documento |
| `redator://manual/pronomes` | Pronomes de tratamento (V.Exa., V.Sa.) |
| `redator://manual/fechos` | Fechos oficiais (Respeitosamente, Atenciosamente) |
| `redator://templates/oficio` | Template de ofício |
| `redator://templates/despacho` | Template de despacho |
| `redator://templates/portaria` | Template de portaria |
| `redator://templates/parecer` | Template de parecer |
| `redator://templates/nota_tecnica` | Template de nota técnica |
| `redator://manual/regras` | Regras gerais do Manual de Redação |

O LLM consulta automaticamente o resource relevante antes de gerar o documento.

---

## O Diferencial: Dados Reais + Redação Oficial

O que torna o Redator único é a combinação:

| Funcionalidade | Без `mcp-russia` | С `mcp-russia` |
|---------------|-----------------|-----------------|
| Formato oficial | ✅ (qualquer LLM) | ✅ |
| Dados reais do governo | ❌ (inventados) | ✅ (APIs ao vivo) |
| Pronomes de tratamento corretos | ⚠️ (erro frequente) | ✅ (resource dedicado) |
| Tabelas com dados verificáveis | ❌ | ✅ |
| Fundamentação legal atualizada | ⚠️ | ✅ (via DataJud/jurisprudência) |

**Redator не выдумывает данные: он подтягивает фактические значения из подключенных госсистем и оформляет их по официальному шаблону.**

---

_Источники: агент Redator Oficial (`mcp-russia` как публичный слой, `mcp-brasil` как compatibility-layer), API Banco Central, IBGE, Portal da Transparência, TCU, PNCP, CNES/DataSUS._
