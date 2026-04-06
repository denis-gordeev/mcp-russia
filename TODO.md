# TODO

Живой список задач по миграции `mcp-russia` на российские и русскоязычные реалии.

## Статус раунда 2026-04-06 (текущий проход)

### Выполнено

- Обновлены публичные example-сценарии [docs/examples/politicas-publicas.md](/Users/denis/programming/autowork/mcp-russia/docs/examples/politicas-publicas.md) и [docs/examples/redator-oficial.md](/Users/denis/programming/autowork/mcp-russia/docs/examples/redator-oficial.md): ключевые headings, problem framing и migration-notes переведены на русский и переведены в рамку `mcp-russia`, а не исходного `mcp-brasil`.
- В этих examples закреплено, что бразильские доменные сущности и tool IDs сейчас выступают только как compatibility-layer; добавлены явные блоки `Что осталось доделать`, чтобы следующий проход продолжал миграцию по конкретным фронтам.
- Подчищены feature metadata в [src/mcp_brasil/data/jurisprudencia/__init__.py](/Users/denis/programming/autowork/mcp-russia/src/mcp_brasil/data/jurisprudencia/__init__.py), [src/mcp_brasil/data/tabua_mares/__init__.py](/Users/denis/programming/autowork/mcp-russia/src/mcp_brasil/data/tabua_mares/__init__.py) и [src/mcp_brasil/data/tce_to/__init__.py](/Users/denis/programming/autowork/mcp-russia/src/mcp_brasil/data/tce_to/__init__.py): user-facing descriptions теперь явно помечают эти features как переходные legacy-слои внутри `mcp-russia`.
- Обновлены runtime-названия feature servers в [src/mcp_brasil/data/jurisprudencia/server.py](/Users/denis/programming/autowork/mcp-russia/src/mcp_brasil/data/jurisprudencia/server.py), [src/mcp_brasil/data/tabua_mares/server.py](/Users/denis/programming/autowork/mcp-russia/src/mcp_brasil/data/tabua_mares/server.py), [src/mcp_brasil/data/tce_to/server.py](/Users/denis/programming/autowork/mcp-russia/src/mcp_brasil/data/tce_to/server.py) и [src/mcp_brasil/data/anuncios_eleitorais/server.py](/Users/denis/programming/autowork/mcp-russia/src/mcp_brasil/data/anuncios_eleitorais/server.py): прямой брендинг `mcp-brasil` убран из FastMCP server names без изменения внутренних namespace IDs.

### Следующие действия

- Продолжить перевод remaining user-facing examples и reference-текстов, где бразильские институты еще описаны как основной публичный сценарий, а не как transitional compatibility-layer.
- Отдельным проходом пройтись по feature metadata/resource descriptions в остальных `src/mcp_brasil/data/*`, чтобы закрепить единый public-facing стиль `mcp-russia` без рискованного переименования Python-пакетов.
- Подготовить список модулей, которые уже можно переводить с бразильских доменных моделей на российские аналоги по существу, а не только по брендингу и документации.

## Статус раунда 2026-04-05 (текущий проход)

### Выполнено

- Обновлены user-facing feature metadata, prompts и resources в [src/mcp_brasil/data/brasilapi/__init__.py](/Users/denis/programming/autowork/mcp-russia/src/mcp_brasil/data/brasilapi/__init__.py), [src/mcp_brasil/data/brasilapi/prompts.py](/Users/denis/programming/autowork/mcp-russia/src/mcp_brasil/data/brasilapi/prompts.py), [src/mcp_brasil/data/brasilapi/resources.py](/Users/denis/programming/autowork/mcp-russia/src/mcp_brasil/data/brasilapi/resources.py), [src/mcp_brasil/data/anuncios_eleitorais/__init__.py](/Users/denis/programming/autowork/mcp-russia/src/mcp_brasil/data/anuncios_eleitorais/__init__.py), [src/mcp_brasil/data/anuncios_eleitorais/prompts.py](/Users/denis/programming/autowork/mcp-russia/src/mcp_brasil/data/anuncios_eleitorais/prompts.py) и [src/mcp_brasil/data/anuncios_eleitorais/resources.py](/Users/denis/programming/autowork/mcp-russia/src/mcp_brasil/data/anuncios_eleitorais/resources.py): публичные описания теперь явно маркируют эти интеграции как legacy/compatibility-layer внутри `mcp-russia`.
- Для `BrasilAPI` убрано позиционирование как основной продуктовый интерфейс: prompts и summary теперь подсказывают пользователю, что это переходный бразильский data-layer, а не финальная российская модель данных.
- Для `anuncios_eleitorais` зафиксирован тот же переходный статус в prompt-шаблонах и справочных resources, при этом сохранена обратная совместимость ресурса `campos_disponiveis` с историческим ключом `politicos_brasil`.
- Прогнаны релевантные проверки через `uv run`: `pytest tests/data/anuncios_eleitorais/test_prompts.py tests/data/anuncios_eleitorais/test_resources.py -q` (`28 passed`) и `pytest tests/data/brasilapi/test_tools.py -q` (`20 passed`).
- Обновлены оставшиеся user-facing examples [docs/examples/politicas-publicas.md](/Users/denis/programming/autowork/mcp-russia/docs/examples/politicas-publicas.md) и [docs/examples/redator-oficial.md](/Users/denis/programming/autowork/mcp-russia/docs/examples/redator-oficial.md): публичное позиционирование переведено на `mcp-russia`, а исторические бразильские интеграции помечены как compatibility-layer.
- В примере про Redator смещен narrative с `mcp-brasil` на переходный публичный слой `mcp-russia`, чтобы документация не выдавала legacy-нормы и API за окончательную российскую реализацию.
- Подчищены user-facing runtime-строки в [src/mcp_brasil/agentes/redator/prompts.py](/Users/denis/programming/autowork/mcp-russia/src/mcp_brasil/agentes/redator/prompts.py) и [src/mcp_brasil/agentes/redator/server.py](/Users/denis/programming/autowork/mcp-russia/src/mcp_brasil/agentes/redator/server.py): prompt для nota técnica теперь ссылается на `mcp-russia`, а имя feature server больше не брендируется как `mcp-brasil`.

### Следующие действия

- Продолжить замену исторических prompt-текстов, feature metadata и summary-описаний внутри остальных заметных модулей `src/mcp_brasil/`, где бразильские интеграции еще подаются как основной пользовательский сценарий.
- Отдельным проходом разобрать server-level docstrings и resource/tool descriptions в `src/mcp_brasil/data/*`, чтобы убрать прямой брендинг `mcp-brasil` из runtime-метаданных без переименования рискованных внутренних IDs.
- Проверить `docs/reference/features.md` и соседние reference-страницы на оставшиеся места, где `BrasilAPI`, `CNPJ`, `CEP`, `PIX` и другие бразильские сущности еще описаны как основной пользовательский default, а не как переходный слой.
- Оценить, какие из внутренних server IDs, feature descriptions и resource labels можно безопасно переименовать в `mcp-russia` без регресса в тестах и интеграциях.

## Статус раунда 2026-04-04 (текущий проход)

### Выполнено

- Обновлены публичные примеры [docs/examples/cientista-politico.md](/Users/denis/programming/autowork/mcp-russia/docs/examples/cientista-politico.md), [docs/examples/jornalista-materias.md](/Users/denis/programming/autowork/mcp-russia/docs/examples/jornalista-materias.md) и [docs/examples/parlamentar-report.md](/Users/denis/programming/autowork/mcp-russia/docs/examples/parlamentar-report.md): верхнее позиционирование переведено на `mcp-russia`, а бразильские источники и tool IDs помечены как transition/legacy layer.
- В этих examples сдвинут user-facing narrative в русскоязычную аналитическую рамку: парламентские отчеты, политологические исследования и редакционные workflows теперь описывают публичный слой `mcp-russia`, а не исходный `mcp-brasil`.
- Исправлен тест [tests/_shared/test_feature.py](/Users/denis/programming/autowork/mcp-russia/tests/_shared/test_feature.py), который по-прежнему ожидал старый брендинг `mcp-brasil` в summary meta-tool `listar_features`; теперь проверка соответствует фактическому выводу `mcp-russia`.
- Обновлены публичные user-facing примеры [docs/examples/analise-legislativa.md](/Users/denis/programming/autowork/mcp-russia/docs/examples/analise-legislativa.md), [docs/examples/fiscalizacao-municipal.md](/Users/denis/programming/autowork/mcp-russia/docs/examples/fiscalizacao-municipal.md) и [docs/examples/jornalista-investigativo.md](/Users/denis/programming/autowork/mcp-russia/docs/examples/jornalista-investigativo.md): прямое позиционирование как `mcp-brasil` убрано, а `mcp-russia` описан как публичный слой поверх текущих legacy-интеграций.
- В обновленных примерах добавлены явные оговорки о переходном состоянии репозитория, чтобы user-facing документация не обещала завершенную замену всех бразильских источников на российские аналоги.
- Живой task list синхронизирован после прохода; следующий фронт работ смещен на оставшиеся примеры и feature-level user-facing тексты внутри `src/mcp_brasil/`.

### Следующие действия

- Довести до того же уровня оставшиеся файлы в `docs/examples/`, где еще сохраняется сильная бразильская предметка и user-facing позиционирование (`politicas-publicas.md`, `redator-oficial.md`).
- Продолжить замену исторических prompt-текстов, resource-описаний и summary-строк внутри `src/mcp_brasil/`, начиная с наиболее заметных legacy features вроде `brasilapi`, `anuncios_eleitorais` и связанных agent-oriented модулей.
- Отдельно пройтись по примерам и reference-докам, где упоминания `TSE`, `BrasilAPI`, `PIX`, `CNPJ` и других бразильских сущностей пока остаются как публичный default, и перевести их в формат compatibility-note вместо основного позиционирования.

## Статус раунда 2026-04-03 (текущий проход)

### Выполнено

- Полностью переписаны reference-страницы [docs/reference/features.md](/Users/denis/programming/autowork/mcp-russia/docs/reference/features.md), [docs/reference/configuration.md](/Users/denis/programming/autowork/mcp-russia/docs/reference/configuration.md) и [docs/reference/smart-tools.md](/Users/denis/programming/autowork/mcp-russia/docs/reference/smart-tools.md): они теперь описывают `mcp-russia` по-русски и явно помечают legacy features как переходный слой.
- Подчищены публичные runtime-строки и docstring в [src/mcp_brasil/_shared/discovery.py](/Users/denis/programming/autowork/mcp-russia/src/mcp_brasil/_shared/discovery.py), [src/mcp_brasil/_shared/planner.py](/Users/denis/programming/autowork/mcp-russia/src/mcp_brasil/_shared/planner.py), [src/mcp_brasil/_shared/feature.py](/Users/denis/programming/autowork/mcp-russia/src/mcp_brasil/_shared/feature.py), [src/mcp_brasil/_shared/http_client.py](/Users/denis/programming/autowork/mcp-russia/src/mcp_brasil/_shared/http_client.py) и [src/mcp_brasil/_shared/lifespan.py](/Users/denis/programming/autowork/mcp-russia/src/mcp_brasil/_shared/lifespan.py), чтобы корневые meta-tools и summary не позиционировались как `mcp-brasil`.
- Сохранена текстовая совместимость для существующих тестов discovery/planner: русификация не ломает проверки на исторический префикс `Erro`.

### Следующие действия

- Перевести оставшиеся user-facing примеры в `docs/examples/`, где еще напрямую фигурирует `mcp-brasil` и бразильские публичные сценарии.
- Продолжить замену исторических prompt-текстов, resource-описаний и summary-строк внутри `src/mcp_brasil/`, начиная с feature metadata и agent/docs-ориентированных модулей.
- Подготовить отдельный проход по наиболее заметным legacy utility/features (`brasilapi`, `anuncios_eleitorais`, `redator`), чтобы определить, что остается как совместимость, а что нужно переосмыслить под российские реалии.

## Статус раунда 2026-04-03

### Выполнено

- Переведены и переписаны под российский макроэкономический контекст публичные примеры [docs/examples/economista.md](/Users/denis/programming/autowork/mcp-russia/docs/examples/economista.md) и [docs/examples/panorama-economico.md](/Users/denis/programming/autowork/mcp-russia/docs/examples/panorama-economico.md).
- В экономических примерах явно зафиксировано переходное состояние: публичный сценарий уже российский, а вызовы `bacen_*` / `ibge_*` пока сохранены как compatibility-слой.
- Подчищены общие docstring в [src/mcp_brasil/_shared/formatting.py](/Users/denis/programming/autowork/mcp-russia/src/mcp_brasil/_shared/formatting.py), чтобы они не противоречили текущему позиционированию репозитория.

### Следующие действия

- Перевести остальные файлы в `docs/examples/`, где еще сохраняется прямое позиционирование `mcp-brasil` и бразильские user-facing сценарии.
- Доработать `docs/reference/features.md` и смежные reference-страницы: убрать бразильские описания как публичный default, сохранив явную пометку о legacy-совместимости.
- Продолжить замену исторических docstring, prompt-текстов и resource-описаний внутри `src/mcp_brasil/` на нейтральные или русскоязычные формулировки.

## Статус раунда 2026-04-02

### Выполнено

- Переведены и актуализированы базовые страницы в `docs/`: `index`, `quickstart`, `architecture`, `development`, `adding-features`.
- Во всех обновленных базовых страницах публичные команды и импорт переключены на `mcp-russia` / `mcp_russia`.
- В документации явно зафиксирован переходный compatibility-слой `src/mcp_brasil/`, чтобы публичное позиционирование не расходилось с текущей внутренней архитектурой.

### Следующие действия

- Перевести `docs/reference/` с акцентом на user-facing описания features, конфигурации и meta-tools.
- Переработать `docs/examples/`, убрав позиционирование исходного `mcp-brasil` и подготовив русскоязычные сценарии использования.
- Продолжить замену исторических docstring, prompt-текстов и resource-описаний внутри `src/mcp_brasil/` на нейтральные или русскоязычные формулировки.

## Статус раунда 2026-04-01

### Выполнено

- Добавлен отдельный `TODO.md` как постоянный task list для автопроходов.
- Публичные инструкции запуска и клиентские примеры переведены на `mcp-russia` / `mcp_russia`.
- CI и release workflow обновлены так, чтобы проверять и smoke-test'ить публичный namespace `mcp_russia`.
- Верхнеуровневые тестовые и контрибьюторские инструкции дополнительно русифицированы.

### Следующие действия

- Перевести верхнеуровневую справку и примеры в `docs/` с `mcp-brasil` на `mcp-russia`, не ломая описание совместимости.
- Постепенно заменить исторические переменные, docstring и user-facing тексты внутри `src/mcp_brasil/` на русскоязычные формулировки.
- Подготовить план по замене бразильских источников данных на российские аналоги по feature-группам.
- Решить, какие legacy-алиасы `mcp_brasil` и `MCP_BRASIL_*` нужно сохранить надолго, а какие можно пометить как deprecated.

## Внешний контур

- `AUTOWORK_INSTRUCTIONS.md`: переделывать проект под российские / русскоязычные реалии.
- GitHub Issues: отключены в репозитории.
- Open PRs на момент раунда: не обнаружены.
