# Smart tools

Корневой сервер публикует 4 meta-tools, которые помогают находить нужные integrations, строить план запроса и выполнять несколько вызовов за один проход. Публично это часть `mcp-russia`, хотя внутри каталог пока включает legacy features исходного проекта.

## `spisok_funktsiy`

Показывает все активные features и статус авторизации.

```text
→ spisok_funktsiy()
← 27 активных features:
   ibge (9 tools) ✓
   bacen (9 tools) ✓
   transparencia (18 tools) ✓ (с ключом)
   ...
```

Это хороший первый шаг, когда модели нужно понять, какие API вообще доступны в текущем экземпляре сервера.

## `rekomendovat_instrumenty`

Принимает вопрос на естественном языке и предлагает 3-5 наиболее релевантных tools.

```text
→ rekomendovat_instrumenty("Какие крупнейшие расходы федерального бюджета доступны за 2024 год?")
← Рекомендация:
   1. transparencia_consultar_despesas
   2. transparencia_buscar_contratos
   3. tcu_buscar_acordaos
```

Как работает:

1. `build_catalog()` собирает markdown-каталог всех tools
2. Каталог и пользовательский вопрос отправляются в LLM
3. Модель возвращает краткий список tools с объяснением и примером использования

**Требует:** `ANTHROPIC_API_KEY`

## `splanirovat_zapros`

Строит структурированный план выполнения для запросов, где нужно несколько API, зависимые шаги или параллельные вызовы.

```text
→ splanirovat_zapros("Сравни расходы на здравоохранение в двух регионах за 3 года")
← План:
   Этап 1: получить данные по первому региону
   Этап 2: получить данные по второму региону
   Этап 3: добавить население и рассчитать per capita
```

Модель данных:

```python
class EtapaPlano(BaseModel):
    etapa: int
    descricao: str
    tool: str
    parametros: dict[str, str]
    depende_de: list[int]
    justificativa: str

class PlanoConsulta(BaseModel):
    consulta: str
    complexidade: str
    resumo: str
    etapas: list[EtapaPlano]
    observacoes: str
```

Типичные стратегии:

- `enriquecimento`: добавить контекст из другой feature
- `comparacao`: сопоставить одну и ту же метрику по разным регионам или источникам
- `contextualizacao`: подтянуть справочные, демографические или макроэкономические данные
- `paralelismo`: выполнить независимые шаги одновременно

**Требует:** `ANTHROPIC_API_KEY`

## `vypolnit_paket`

Выполняет до 10 tool calls за одну MCP-команду и снижает число round-trips между моделью и сервером.

```text
→ vypolnit_paket([
    {"tool": "bacen_indicadores_atuais", "params": {}},
    {"tool": "ibge_listar_estados", "params": {}},
    {"tool": "brasilapi_consultar_taxa", "params": {"sigla": "SELIC"}}
  ])
← [resultado1, resultado2, resultado3]
```

Как работает:

1. `build_dispatch(registry)` строит отображение `tool name -> async function`
2. `asyncio.gather()` выполняет вызовы параллельно
3. Результаты возвращаются в исходном порядке

**Лимит:** максимум 10 вызовов за одну команду

## Когда использовать

| Ситуация | Tool |
|----------|------|
| Нужно понять, что вообще доступно | `spisok_funktsiy` |
| Нужно быстро подобрать tool под вопрос | `rekomendovat_instrumenty` |
| Нужно разложить сложный запрос на этапы | `splanirovat_zapros` |
| Нужно получить несколько независимых ответов за один проход | `vypolnit_paket` |

## Рекомендуемый поток

```text
1. splanirovat_zapros("сложный вопрос")
2. vypolnit_paket([...независимые этапы...])
3. vypolnit_paket([...зависимые этапы...])
4. модель синтезирует итоговый ответ
```

## Tool Search (BM25)

Полный каталог слишком большой, чтобы всегда публиковать его целиком в LLM-контекст. Поэтому по умолчанию используется BM25-фильтрация:

- анализируется текущий диалог
- tools ранжируются по релевантности
- в контекст попадают только top-N совпадений
- meta-tools всегда остаются видимыми

Настройка управляется через `MCP_RUSSIA_TOOL_SEARCH`:

| Значение | Поведение |
|----------|-----------|
| `bm25` | Показать только релевантные tools |
| `none` | Показать весь каталог |
| `code_mode` | Экспериментальный программный discovery |
