# Caso de Uso: Jornalista — Produção de Matérias com Dados

> Как использовать `mcp-russia` для подготовки, обогащения и проверки журналистских материалов на основе официальных и публичных API. Ниже часть источников и tool IDs все еще указана в legacy-виде, но публичный сценарий уже описывает русскоязычный продуктовый слой.

---

## O Diferencial

В отличие от сценария [jornalista investigativo](./jornalista-investigativo.md), здесь фокус не на выявлении нарушений, а на **повседневной data-driven журналистике**: быстро собрать проверяемые цифры, сравнить регионы или муниципалитеты и получить основу для публикации без ручного обхода десятка порталов.

---

## Matéria 1: "Quanto Custa um Deputado?"

### A Pauta

Сравнить представительские и аппаратные расходы парламентариев: кто тратит больше всего, кто экономит и какие категории расходов доминируют.

### A Apuração

**1. Ranking de despesas**

> Prompt: "Liste os 10 deputados que mais gastaram com a cota parlamentar em 2024"

```
API: camara_despesas_deputado (executar_lote para Top 10)
```

**2. Comparação por partido**

> Prompt: "Qual a média de gastos de gabinete por partido? Qual partido gasta mais per capita?"

```
APIs: camara_buscar_deputados (todos) + camara_despesas_deputado (em lote)
```

**3. Detalhamento das categorias**

> Prompt: "Quanto a Câmara gasta no total com passagens aéreas, alimentação e combustível?"

O LLM agrega os dados e produz:

```
GASTOS DA CÂMARA — COTA PARLAMENTAR 2024

Total gasto por 513 deputados: R$ 187.456.789

| Categoria                | Total          | Média/Dep.   |
|--------------------------|----------------|-------------|
| Divulgação               | R$ 52,3M      | R$ 101.945  |
| Passagens aéreas         | R$ 41,2M      | R$ 80.311   |
| Combustíveis             | R$ 28,9M      | R$ 56.335   |
| Alimentação              | R$ 22,1M      | R$ 43.079   |
| Locação de veículos      | R$ 18,4M      | R$ 35.867   |
| Consultorias             | R$ 14,6M      | R$ 28.460   |
| Outros                   | R$ 9,9M       | R$ 19.298   |

Deputados que NÃO usaram a cota: 3 de 513
Deputados que usaram > 90% da cota: 47 de 513
```

### O Lead da Matéria

> "Os 513 deputados federais gastaram R$ 187,4 milhões com a cota parlamentar em 2024 — uma média de R$ 365 mil por parlamentar. Passagens aéreas e combustíveis representam 37% do total. O deputado [Nome] liderou o ranking com R$ [valor], enquanto [Nome] foi o mais econômico com R$ [valor]."

**Cada número é verificável na API da Câmara.**

---

## Matéria 2: "Mapa da Desigualdade: Saúde Pública por Estado"

### A Pauta

Сравнить инфраструктуру здравоохранения между регионами: койки, кадры, расходы и итоговые показатели.

### A Apuração

**1. Infraestrutura por estado**

> Prompt: "Compare o número de leitos hospitalares per capita em todos os estados brasileiros"

```
APIs: saude_buscar_estabelecimentos (por UF) + ibge_listar_estados (população)
```

**2. Gastos com saúde**

> Prompt: "Quanto cada estado gasta com saúde per capita?"

```
APIs: tce_[estado]_despesas + ibge_consultar_agregado (população)
```

**3. Indicadores de resultado**

> Prompt: "Qual a expectativa de vida em cada estado? Qual a mortalidade infantil?"

```
API: ibge_consultar_agregado (indicadores demográficos)
```

### O Infográfico

```
MAPA DA SAÚDE PÚBLICA — 2024

                Leitos/1000hab   Gasto/capita   Exp. Vida
  DF  ████████░     3,2          R$ 1.890      78,1 anos
  SP  ███████░░     2,8          R$ 1.567      77,8 anos
  SC  ████████░     3,1          R$ 1.423      79,2 anos
  ...
  MA  ███░░░░░░     1,1          R$   678      71,4 anos
  PA  ██░░░░░░░     0,9          R$   591      72,1 anos

  Diferença DF vs MA: 2,9x leitos | 2,8x gastos | 6,7 anos de vida
```

---

## Matéria 3: "Selic em Alta: O Impacto no Bolso do Brasileiro"

### A Pauta

Показать, как изменение ключевой ставки и инфляции влияет на повседневные расходы домохозяйств и стоимость кредита.

### A Apuração

**1. Série histórica da Selic**

> Prompt: "Mostre a evolução da Selic nos últimos 5 anos e compare com a inflação"

```
APIs: bacen_comparar_series(codigos=[432, 433], ultimos=60)
```

**2. Impacto no crédito**

> Prompt: "Qual o custo de um financiamento de R$ 300 mil com a Selic atual vs. a de 2 anos atrás?"

```
API: bacen_consultar_serie (séries de crédito)
```

**3. Comparação internacional**

> Prompt: "Qual a taxa de juros real do Brasil comparada a outros países?"

O LLM calcula: Selic (14,25%) - IPCA (5,06%) = **Juro real de 9,19%**

```
JUROS REAIS — COMPARATIVO INTERNACIONAL

  🇧🇷 Brasil      ██████████████████░   9,19%
  🇲🇽 México      █████████░░░░░░░░░░   5,2%
  🇮🇳 Índia       ███████░░░░░░░░░░░░   3,1%
  🇺🇸 EUA         ████░░░░░░░░░░░░░░░   1,8%
  🇪🇺 Zona Euro   ███░░░░░░░░░░░░░░░░   1,2%
  🇯🇵 Japão       █░░░░░░░░░░░░░░░░░░  -0,1%
```

### O lead da matéria

> "При ключевой ставке 14,25% и инфляции 5,06% реальная ставка достигает 9,19%. Кредит на R$ 300 тыс., который в 2021 году обходился в R$ 1.580 в месяц, теперь стоит около R$ 2.890. Источник: данные центрального банка и официальной статистики."

---

## Matéria 4: "Queimadas Recordes: Os Números do INPE"

### A Pauta

Покрыть сезон природных пожаров и связанных климатических рисков на основе официальных данных наблюдения.

### A Apuração

**1. Focos de queimada**

> Prompt: "Quantos focos de queimada o INPE registrou na Amazônia em 2024? Compare com os 5 anos anteriores"

```
API: inpe_focos_queimadas(bioma="amazonia", ano=2024)
```

**2. Desmatamento**

> Prompt: "Qual o desmatamento acumulado na Amazônia nos últimos 12 meses?"

```
API: inpe_desmatamento(bioma="amazonia")
```

**3. Recursos hídricos**

> Prompt: "Qual o nível dos reservatórios nas regiões com mais queimadas?"

```
API: ana_monitorar_reservatorios
```

**4. Publicações oficiais**

> Prompt: "Busque publicações no Diário Oficial sobre decretos de emergência ambiental em 2024"

```
API: diario_oficial_buscar(termo="emergencia ambiental queimadas")
```

---

## Matéria 5: "Eleições 2026: O Dinheiro da Pré-Campanha"

### A Pauta

Отслеживать финансирование предвыборной активности и ранние финансовые сигналы кампаний.

### A Apuração

> Prompt: "Liste os pré-candidatos ao governo de SP que já têm prestação de contas registrada no TSE"

```
APIs: tse_buscar_candidatos(cargo="governador", uf="SP", ano=2026)
      tse_receitas_candidato (para cada candidato)
      tse_despesas_candidato (para cada candidato)
```

> Prompt: "Quem são os maiores doadores de campanhas a governador em todo o Brasil?"

```
API: tse_buscar_candidatos + tse_receitas_candidato (em lote)
```

---

## Dicas Para Jornalistas

### 1. Sempre cite a fonte

```
"Segundo dados da API do Banco Central (série SGS 432,
consulta em 23/03/2025), a taxa Selic..."
```

### 2. Use `executar_lote` para comparações

Quando a matéria precisa comparar múltiplos estados/municípios, uma única chamada resolve:

```json
[
  {"tool": "ibge_buscar_municipios", "args": {"uf": "SP"}},
  {"tool": "ibge_buscar_municipios", "args": {"uf": "RJ"}},
  {"tool": "ibge_buscar_municipios", "args": {"uf": "MG"}}
]
```

### 3. Use `planejar_consulta` para matérias complexas

> Prompt: "Preciso fazer uma matéria sobre o impacto das emendas PIX nos municípios do Nordeste. Planeje as consultas"

A ferramenta retorna o roteiro de apuração completo.

### 4. Dados + Redator = Matéria pronta

Комбинируйте data-tools с агентом Redator, если нужен черновик служебной записки, справки, explainer-текста или структурированного приложения к публикации.

Пока `mcp-russia` находится в миграции, такие сценарии полезно читать как редакционный workflow поверх текущего набора legacy-интеграций: продукт уже русскоязычный, а часть конкретных источников еще требует содержательной замены на российские аналоги.

---

_Источники: Banco Central, IBGE, парламентские и электоральные API, порталы прозрачности, экологические и отраслевые источники, Diário Oficial и другие сохраненные legacy-интеграции._
