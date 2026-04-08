# Caso de Uso: Relatório Parlamentar (Votação + Emendas + Atividade)

> Как в `mcp-russia` собрать единый профиль парламентария: голосования, инициативы, расходы, трансферты и связанные источники в одном отчете. Отдельные названия tools и источников пока остаются legacy-совместимыми.

---

## Проблема

Чтобы оценить работу депутата или сенатора, обычно приходится вручную собирать сведения из нескольких систем:

| Dado | Fonte | До `mcp-russia` |
|------|-------|-------------------|
| Presenças e votações | Câmara/Senado | Navegar portal manualmente |
| Proposições apresentadas | Câmara/Senado | Buscar uma a uma |
| Despesas de gabinete | Câmara | Planilhas CSV |
| Emendas parlamentares | Transparência/TransfereGov | Portais separados |
| Financiamento de campanha | TSE | Outro portal |
| Processos judiciais | DataJud | Outro portal |

**С `mcp-russia`:** один сценарий может собрать сводный отчет и подсветить узкие места для дальнейшей проверки.

---

## Отчет по парламентарию

### Этап 1 — профиль и история

> Prompt: "Gere um perfil completo do deputado [Nome]: partido, estado, legislaturas, comissões e cargos"

Ferramentas:
- `camara_buscar_deputados(nome="...")` → ID
- `camara_detalhes_deputado(id=...)` → perfil completo

```
═══════════════════════════════════════════
  PERFIL PARLAMENTAR
═══════════════════════════════════════════

Nome: [Nome Completo]
Partido: [Sigla]-[UF]
Legislatura: 57ª (2023-2027)
Comissões:
  ├── Comissão de Finanças e Tributação (titular)
  ├── Comissão de Educação (suplente)
  └── CPI das Apostas Online (titular)
Mandatos anteriores: 2 (2015-2019, 2019-2023)
```

---

### Этап 2 — законодательная активность

> Prompt: "Quantas proposições o deputado [Nome] apresentou em 2024? Liste por tipo"

Ferramentas:
- `camara_buscar_proposicoes(autor="[Nome]", ano=2024)`

```
═══════════════════════════════════════════
  ATIVIDADE LEGISLATIVA — 2024
═══════════════════════════════════════════

Proposições apresentadas: 23
  ├── Projetos de Lei (PL):           8
  ├── Requerimentos:                  7
  ├── Indicações:                     4
  ├── Projetos de Decreto Leg.:       2
  └── Emendas a PL:                   2

Proposições aprovadas: 3 de 23 (13%)
Proposições arquivadas: 5
Proposições em tramitação: 15

Principais temas:
  1. Tributação (7 proposições)
  2. Educação (5 proposições)
  3. Tecnologia (4 proposições)
```

---

### Этап 3 — голосования

> Prompt: "Como o deputado votou nas principais matérias de 2024? Comparar com a orientação do partido e do governo"

Ferramentas:
- `camara_votacoes_deputado(id=..., ano=2024)`

```
═══════════════════════════════════════════
  VOTAÇÕES — 2024
═══════════════════════════════════════════

Total de votações nominais: 87
Presenças: 79 (90,8%)
Ausências: 8 (9,2%)

Alinhamento com o partido: 82% (65/79)
Alinhamento com o governo: 61% (48/79)
Votações em que divergiu do partido: 14

VOTAÇÕES MAIS RELEVANTES:

| Matéria                    | Voto | Partido | Governo |
|----------------------------|------|---------|---------|
| Reforma Tributária         | SIM  | SIM ✅   | SIM ✅   |
| Marco Legal da IA          | SIM  | SIM ✅   | SIM ✅   |
| Desoneração da Folha       | NÃO  | SIM ❌   | NÃO ✅   |
| Orçamento 2025             | SIM  | SIM ✅   | SIM ✅   |
| Marco Temporal Indígena    | SIM  | SIM ✅   | NÃO ❌   |
```

---

### Этап 4 — расходы

> Prompt: "Detalhe as despesas de gabinete do deputado em 2024. Quais os maiores gastos?"

Ferramentas:
- `camara_despesas_deputado(id=..., ano=2024)`

```
═══════════════════════════════════════════
  DESPESAS DE GABINETE — 2024
═══════════════════════════════════════════

Total gasto: R$ 312.456,78
Cota parlamentar mensal: R$ 44.632,46 (limite UF)
Utilização média: 58,3% da cota

Por categoria:
| Categoria                    | Valor         | % Total |
|------------------------------|---------------|---------|
| Divulgação de atividade      | R$ 89.234     | 28,6%   |
| Passagens aéreas             | R$ 67.891     | 21,7%   |
| Combustíveis e lubrificantes | R$ 45.672     | 14,6%   |
| Alimentação                  | R$ 38.456     | 12,3%   |
| Locação de veículos          | R$ 28.903     | 9,3%    |
| Consultoria/assessoria       | R$ 24.567     | 7,9%    |
| Outros                       | R$ 17.734     | 5,6%    |

Fornecedores mais recorrentes:
  1. [Empresa A] — R$ 67.891 (passagens)
  2. [Empresa B] — R$ 45.672 (combustível)
  3. [Empresa C] — R$ 38.456 (alimentação)
```

---

### Этап 5 — трансферты и распределение средств

> Prompt: "Quais emendas o deputado destinou em 2024? Para quais municípios e áreas?"

Ferramentas:
- `transparencia_emendas_parlamentares(autor="[Nome]", ano=2024)`
- `transferegov_buscar_emendas(autor="[Nome]", ano=2024)`

```
═══════════════════════════════════════════
  EMENDAS PARLAMENTARES — 2024
═══════════════════════════════════════════

Total destinado: R$ 25.380.000,00

Por tipo:
  ├── Emendas individuais:    R$ 18.000.000
  ├── Emendas de bancada:     R$  5.380.000
  └── Transferências especiais: R$  2.000.000

Top 5 муниципалитетов:
| Município        | UF | Valor          | Área      |
|------------------|----|----------------|-----------|
| [Cidade natal]   | SP | R$ 5.000.000   | Saúde     |
| [Município 2]    | SP | R$ 3.500.000   | Educação  |
| [Município 3]    | SP | R$ 3.000.000   | Infra.    |
| [Município 4]    | SP | R$ 2.500.000   | Saúde     |
| [Município 5]    | SP | R$ 2.000.000   | Cultura   |

Концентрация: 73% средств направлено в 5 муниципалитетов
Áreas: 45% Saúde, 25% Educação, 20% Infraestrutura, 10% Outros
```

---

### Этап 6 — электоральное финансирование

> Prompt: "Quem financiou a campanha do deputado em 2022? Compare os doadores com os municípios que recebem emendas"

Ferramentas:
- `tse_buscar_candidatos(nome="...", ano=2022)`
- `tse_receitas_candidato(id=...)`

```
═══════════════════════════════════════════
  FINANCIAMENTO DE CAMPANHA — 2022
═══════════════════════════════════════════

Total arrecadado: R$ 2.890.456,00

Por origem:
  ├── Fundo Eleitoral:     R$ 1.500.000 (51,9%)
  ├── Fundo Partidário:    R$   450.000 (15,6%)
  ├── Pessoas físicas:      R$   680.456 (23,5%)
  └── Recursos próprios:    R$   260.000 (9,0%)

Top 10 doadores PF:
| Doador              | Valor     | Profissão      |
|---------------------|-----------|----------------|
| [Nome 1]            | R$ 80.000 | Empresário     |
| [Nome 2]            | R$ 65.000 | Agropecuarista |
| ...                 | ...       | ...            |

⚠️ CROSS-REFERENCE:
[Nome 1] é sócio da [Empresa X] de [Município Y]
[Município Y] recebeu R$ 3.500.000 em emendas do deputado
```

---

### Сводный отчет

> Prompt: "Gere um relatório consolidado da atuação do deputado [Nome] em 2024"

`mcp-russia` объединяет все этапы через `planejar_consulta`:

```
═══════════════════════════════════════════════════════
  RELATÓRIO PARLAMENTAR CONSOLIDADO — 2024
  Dep. [Nome Completo] ([Partido]-[UF])
═══════════════════════════════════════════════════════

PRESENÇA:      79/87 votações (90,8%)
ALINHAMENTO:   Partido 82% | Governo 61%
PROPOSIÇÕES:   23 apresentadas | 3 aprovadas
DESPESAS:      R$ 312K (58% da cota)
TRANSFERÊNCIAS: R$ 25,4M (73% для 5 муниципалитетов)
CAMPANHA:      R$ 2,9M arrecadados (52% fundo eleitoral)

DESTAQUES POSITIVOS:
  ✅ Alta presença em plenário (91%)
  ✅ 3 projetos aprovados (acima da média)
  ✅ Despesas abaixo da cota parlamentar

PONTOS DE ATENÇÃO:
  ⚠️ Концентрация средств в небольшом числе муниципалитетов
  ⚠️ 14 votações divergentes do partido
  ⚠️ Cross-reference донор ↔ получатель средств

FONTES: Câmara dos Deputados, TSE, Portal da
Transparência, TransfereGov. Consulta em [data].
═══════════════════════════════════════════════════════
```

В текущем состоянии репозитория такой отчет стоит понимать как публичный workflow `mcp-russia` над унаследованным набором парламентских и электоральных интеграций. Это важно: продуктовая оболочка уже русскоязычная, но конкретные data-sources внутри еще мигрируют.

---

## Para o Senado

O mesmo relatório funciona para senadores, trocando as ferramentas:

| Dado | Câmara | Senado |
|------|--------|--------|
| Perfil | `camara_detalhes_deputado` | `senado_detalhes_senador` |
| Votações | `camara_votacoes_deputado` | `senado_votacoes_materia` |
| Proposições | `camara_buscar_proposicoes` | `senado_buscar_materias` |
| Despesas | `camara_despesas_deputado` | (via Transparência) |
| Comissões | `camara_membros_comissao` | `senado_composicao_comissao` |

O Senado tem **26 tools** — mais do que qualquer outra feature — com cobertura detalhada de matérias, emendas, agenda plenária e composição de comissões.

---

## Automatizando com `executar_lote`

Para gerar o relatório de múltiplos parlamentares de uma vez:

```json
[
  {"tool": "camara_detalhes_deputado", "args": {"id": 204554}},
  {"tool": "camara_detalhes_deputado", "args": {"id": 204555}},
  {"tool": "camara_detalhes_deputado", "args": {"id": 204556}},
  {"tool": "camara_despesas_deputado", "args": {"deputado_id": 204554, "ano": 2024}},
  {"tool": "camara_despesas_deputado", "args": {"deputado_id": 204555, "ano": 2024}},
  {"tool": "camara_despesas_deputado", "args": {"deputado_id": 204556, "ano": 2024}}
]
```

6 consultas em paralelo — perfil + despesas de 3 deputados numa única chamada.

---

_Источники: парламентские API, TSE, Portal da Transparencia, TransfereGov и другие legacy-компоненты исходного проекта._
