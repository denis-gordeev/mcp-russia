# Caso de Uso: Журналист-расследователь

> Как журналист-расследователь может использовать `mcp-russia`, чтобы быстро сопоставлять открытые данные и находить подозрительные связи в закупках, финансировании и судебных делах.

---

## Проблема

Расследовательская журналистика в России и русскоязычном пространстве опирается на данные, разбросанные по десяткам государственных и публичных порталов. Чтобы проверить траты чиновника, депутата или муниципального подрядчика, репортеру обычно приходится вручную просматривать:

- порталы прозрачности и бюджетной отчетности (контракты, расходы, трансферты);
- избирательные и парламентские данные (финансирование кампаний, голосования, инициативы);
- контрольные и аудиторские источники (предписания, нарушения, санкции);
- региональные и муниципальные порталы закупок;
- судебные базы и официальные публикации.

**У каждого источника свой формат, ограничения и способ поиска.** На ручное сопоставление этих баз уходят дни и недели. `mcp-russia` сводит их к единому набору tools и позволяет быстро собрать проверяемую цепочку фактов.

---

## Расследование 1: «Кто выигрывает от бюджетных трансфертов?»

### Задача

Проследить путь межбюджетного трансферта или депутатского финансирования: от политического решения до подрядчика, который осваивает деньги на месте.

### Сценарий запросов

**1. Найти распределение средств**

> Prompt: "Покажи все трансферты и депутатские средства, связанные с [ФИО/регион] в 2024 году, с суммами и муниципалитетами назначения"

```
APIs: transparencia_emendas_parlamentares + transferegov_buscar_emendas
```

**2. Определить конечных получателей**

> Prompt: "Для каждого муниципалитета, получившего средства, покажи контракты и подрядчиков, которые могли быть профинансированы этими деньгами"

```
APIs: tce_[estado]_contratos + pncp_buscar_contratacoes
```

**3. Проверить политические связи бенефициаров**

> Prompt: "Есть ли у этих компаний или их владельцев политические пожертвования, связи с кампанией или пересечения с публичными реестрами?"

```
APIs: электоральные/парламентские источники + `brasilapi_consultar_cnpj` как legacy-слой для корпоративных данных
```

**4. Проверить историю нарушений**

> Prompt: "Есть ли у этих компаний санкции, претензии контрольных органов или судебные дела?"

```
APIs: tcu_buscar_licitantes_inidoneos + datajud_buscar_processos
```

### Что получает журналист

```
ДОКУМЕНТАЛЬНАЯ ЦЕПОЧКА:

Deputado X (PL-SP)
├── Emenda R$ 5M → Município Y/SP (TransfereGov)
│   ├── Contrato R$ 4,8M → Empresa ABC Ltda (TCE-SP)
│   │   ├── Владельцы: João da Silva, Maria Santos (legacy BrasilAPI)
│   │   └── João da Silva фигурирует в данных о финансировании кампании Dep. X
│   └── Dispensa de licitação - valor abaixo de R$ 5M (PNCP)
│
├── Emenda R$ 3M → Município Z/SP (TransfereGov)
│   ├── Contrato R$ 2,9M → Empresa DEF Ltda (TCE-SP)
│   │   └── Совпадает адрес с Empresa ABC (legacy BrasilAPI)
│   └── Empresa DEF уже упоминалась в материалах контрольного органа
│
└── Emenda R$ 2M → Município W/SP (TransfereGov)
    └── Контракт не найден ⚠️ Нужно разбирать движение средств дальше
```

**Каждое звено этой цепочки можно подтвердить ссылкой на источник.** На выходе у редакции есть даты, суммы, идентификаторы контрактов и юридические сущности, пригодные для публикации и фактчека.

---

## Расследование 2: «Мертвые души в ведомстве»

### Задача

Выявить сотрудников или подрядчиков, которые числятся в выплатных ведомостях, но их фактическая работа вызывает сомнения.

### Сценарий запросов

**1. Buscar servidores de um órgão**

> Prompt: "Покажи сотрудников или исполнителей [ведомства] с наибольшими выплатами в 2024 году"

```
API: transparencia_servidores(orgao="...")
```

**2. Cruzar com outros vínculos**

> Prompt: "Есть ли у этих людей параллельные назначения, контракты или связи с выборными должностями?"

```
APIs: transparencia_servidores + camara_buscar_deputados + senado_buscar_senadores
```

**3. Verificar se há processos judiciais**

> Prompt: "Есть ли у этих людей судебные дела по коррупции, злоупотреблениям или конфликту интересов?"

```
APIs: datajud_buscar_processos(assunto="improbidade")
```

**4. Buscar no Diário Oficial**

> Prompt: "Найди официальные публикации о назначении, переводе или увольнении этих людей"

```
API: diario_oficial_buscar(termo="[nome do servidor]")
```

---

## Расследование 3: «Закупки под своего поставщика»

### Задача

Найти закупки, где регулярно побеждает одна и та же компания, что может указывать на заранее заданный результат.

### O Roteiro de Consultas

**1. Buscar licitações de um município**

> Prompt: "Покажи все закупки администрации [муниципалитета] за последние 2 года"

```
APIs: tce_[estado]_licitacoes + pncp_buscar_contratacoes
```

**2. Agrupar por vencedor**

> Prompt: "Quais empresas venceram mais licitações? Alguma venceu em múltiplas categorias diferentes?"

LLM автоматически группирует победителей и показывает концентрацию:

```
КОНЦЕНТРАЦИЯ ПОБЕДИТЕЛЕЙ:

Empresa GHI Ltda:
  ├── Pregão 001/2023 - Material escolar      R$ 890K   ✅ venceu
  ├── Pregão 015/2023 - Material de limpeza   R$ 650K   ✅ venceu
  ├── Pregão 023/2024 - Combustíveis          R$ 1,2M   ✅ venceu
  ├── Pregão 031/2024 - Alimentação escolar   R$ 780K   ✅ venceu
  └── Total: 4 de 4 licitações = 100% de aproveitamento
      ⚠️ Один поставщик одновременно продает канцтовары, топливо и продукты?
```

**3. Verificar se houve impugnação**

> Prompt: "Оспаривались ли эти закупки в суде или у контрольных органов?"

```
APIs: tcu_buscar_acordaos(assunto="licitação [município]") + datajud_buscar_processos
```

**4. Checar vínculos entre empresa e gestores**

> Prompt: "Проверь регистрационные данные победителя и покажи владельцев"

```
API: brasilapi_consultar_cnpj(cnpj="...")
```

---

## Расследование 4: «Сбой в системе здравоохранения»

### Задача

Проверить состояние здравоохранения в муниципалитете: инфраструктуру, кадры, расходы и соответствие нормативам.

### Сценарий запросов

**1. Infraestrutura de saúde**

> Prompt: "Сколько больниц, поликлиник и коек есть в [муниципалитете]?"

```
API: saude_buscar_estabelecimentos(municipio="...", tipo="hospital")
```

**2. Gastos com saúde**

> Prompt: "Сколько местный бюджет потратил на здравоохранение в 2024 году и выполнены ли нормативы?"

```
APIs: tce_[estado]_despesas(funcao="Saúde") + tce_[estado]_receitas
```

**3. Transferências federais**

> Prompt: "Сколько муниципалитет получил целевых межбюджетных трансфертов на здравоохранение?"

```
API: transparencia_transferencias(municipio="...", funcao="Saúde")
```

**4. Comparar com municípios vizinhos**

> Prompt: "Сравни расходы на здравоохранение на душу населения в [муниципалитете] и пяти соседних муниципалитетах"

```
APIs: ibge_buscar_municipios + tce_[estado]_despesas (em lote)
```

**5. Verificar óbitos e causas**

> Prompt: "Есть ли показатели предотвратимой смертности и других проблемных исходов по этому муниципалитету?"

```
API: ibge_consultar_agregado(agregado=...) — indicadores de saúde
```

---

## Инструменты журналиста в `mcp-russia`

### `planejar_consulta` — цифровой редакторский план

> Prompt: "Хочу проверить возможные нарушения в администрации [муниципалитета]. Составь план расследования"

A ferramenta retorna um plano estruturado:

```
План расследования: администрация [муниципалитета]
═══════════════════════════════════════════════

1. PANORAMA FISCAL
   ├── tce_[estado]_despesas → gastos por função
   ├── tce_[estado]_receitas → arrecadação
   └── Цель: проверить бюджетные лимиты и аномалии

2. LICITAÇÕES E CONTRATOS
   ├── tce_[estado]_licitacoes → processos licitatórios
   ├── pncp_buscar_contratacoes → contratações federais
   └── Цель: выявить концентрацию поставщиков

3. EMENDAS E TRANSFERÊNCIAS
   ├── transferegov_buscar_emendas → специальные и иные трансферты
   ├── transparencia_transferencias → repasses federais
   └── Цель: проследить маршрут денег

4. VERIFICAÇÃO DE IRREGULARIDADES
   ├── tcu_buscar_acordaos → decisões do TCU
   ├── tcu_buscar_licitantes_inidoneos → lista suja
   └── datajud_buscar_processos → processos judiciais
```

### `executar_lote` — параллельная проверка

Uma única chamada dispara consultas em múltiplas APIs simultaneamente:

```json
[
  {"tool": "tce_sp_despesas", "args": {"municipio": "São Paulo", "ano": 2024}},
  {"tool": "transparencia_contratos", "args": {"orgao": "Prefeitura SP"}},
  {"tool": "pncp_buscar_contratacoes", "args": {"orgao": "São Paulo"}},
  {"tool": "tcu_buscar_acordaos", "args": {"entidade": "Prefeitura São Paulo"}}
]
```

4 источника, 1 вызов, вся первичка собирается параллельно.

### `recomendar_tools` — когда непонятно, с чего начать

> Prompt: "Хочу проверить закупочные манипуляции. Какие инструменты лучше использовать?"

```
API: recomendar_tools(query="fraudes em licitações municipais")
```

Возвращает подходящие tools и объясняет, в какой последовательности их лучше запускать.

---

## Чеклист для журналистского расследования

| Etapa | O Que Verificar | APIs |
|-------|----------------|------|
| 1. Financiamento | Quem doou para a campanha | TSE |
| 2. Votações | Como votou e em favor de quem | Câmara/Senado |
| 3. Трансферты | Куда ушли средства | Transparência/TransfereGov |
| 4. Contratos | Quem recebeu os contratos | TCE/PNCP/Transparência |
| 5. Связи | Доноры/контакты совпадают с подрядчиками? | электоральные данные + legacy BrasilAPI + TCE |
| 6. Antecedentes | Empresa/pessoa na lista suja? | TCU + DataJud |
| 7. Publicações | O que foi publicado oficialmente | Diário Oficial |
| 8. Jurisprudência | Há processos ou condenações? | DataJud + STF/STJ |

`mcp-russia` полезен здесь не как «готовый вывод», а как слой оркестрации между источниками. Публикуется только то, что подтверждается первичными данными.

---

_Источники: парламентские API, электоральные данные, порталы прозрачности, TCU и TCE, PNCP, судебные базы, Diário Oficial, IBGE, CNES/DataSUS, TransfereGov и сохраненные legacy-интеграции вроде BrasilAPI._
