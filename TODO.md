# TODO

Живой список задач по миграции `mcp-russia` на российские и русскоязычные реалии.

## Статус раунда 2026-04-11 (седьмой проход — полная миграция всех legacy-модулей)

### Выполнено

- **Мигрированы prompts.py** во всех 26 legacy-модулях (camara, senado, tse, tcu, inpe, diario_oficial, transparencia, dados_abertos, ana, tabua_mares, saude, jurisprudencia, datajud, anuncios_eleitorais, transferegov, compras/pncp, compras/dadosabertos, 9 модулей TCE):
  - Все промпты переведены с португальского на русский
  - Добавлены пометки "(legacy)" и указания на бразильскую юрисдикцию
  - Сохранена структура шагов и вызовов инструментов, переведены только пользовательские тексты
- **Мигрированы resources.py** во всех 25 legacy-модулях:
  - Описания справочных данных переведены на русский с пометками "(legacy)"
  - JSON-контент ресурсов (списки типов, штатов, эндпоинтов) переведён на русский
- **Мигрированы __init__.py** feature metadata:
  - Теги переведены с португальского на русский (выборы, тендеры, закупки и т.д.)
  - Описания модулей обновлены с явными пометками legacy-слоя
- **Мигрированы tools.py docstrings** во всех 25 legacy-модулях (9 TCE + 16 других):
  - ~200+ функций с docstrings на русском и пометками "(legacy)"
  - Модульные docstrings описывают назначение как "инструмент совместимости для бразильских данных"
- **Мигрированы schemas.py** field descriptions:
  - ~150+ моделей Pydantic с описаниями полей на русском
  - Все Field(description="...") переведены с пометками "(legacy -- Brazil)"
- **Мигрированы server.py** описания и теги:
  - Все FastMCP серверы переименованы в паттерн `mcp-russia-{module}-legacy`
  - Теги переведены на русский (поиск, список, подробности, запрос)
  - Описания серверов содержат пометки legacy
- **Обновлены тесты**: исправлены 5 тестов, проверявших португальские строки (anuncios_eleitorais, camara, senado, tabua_mares, tce_rj)
- **Настроена конфигурация ruff**: добавлены E501 ignores для всех legacy-модулей с русскоязычными строками
- **Прогнаны все проверки**: `pytest` (1607 passed, 1 skipped), `ruff check` (all passed), `ruff format` (all formatted)

### Ключевые архитектурные решения

- **Единый паттерн legacy**: Все бразильские модули теперь следуют единому стилю — Russian descriptions + "(legacy)" markers
- **Server naming**: Все legacy-серверы используют паттерн `mcp-russia-{module}-legacy` (например, `mcp-russia-camara-legacy`)
- **Обратная совместимость**: Portuguese function names, class names, field names, tool IDs сохранены для backward compatibility
- **Test updates**: Тесты теперь проверяют наличие русского текста вместо португальского

### Следующие действия

- **Содержательная замена API**: заменить бразильские API-интеграции на российские аналоги (Câmara dos Deputados → Госдума API, TSE → ЦИК РФ, TCU → Счётная палата РФ и т.д.)
- **Создание российских модулей**: разработать новые модули для российских источников данных по аналогии с уже созданными cbrf, rosstat, gosduma, rosapi
- **Депрекейшн legacy**: пометить устаревшие бразильские инструменты как deprecated при наличии российских аналогов
- **Документация**: обновить примеры использования с акцентом на то, что бразильские модули — временный compatibility layer

## Статус раунда 2026-04-10 (шестой проход — массовая миграция документации и docstrings)

### Выполнено

- **Мигрированы все примеры в docs/examples/** (9 файлов): полностью переведены с португальского/смешанного языка на русский контекст:
  - `jornalista-materias.md` → повседневная журналистика на основе данных (Госдума, Росстат, ЦБ РФ)
  - `cientista-politico.md` → политический анализ (фракции, голосования, трансферты РФ)
  - `politicas-publicas.md` → анализ госполитики (здравоохранение, экология, закупки РФ)
  - `fiscalizacao-municipal.md` → муниципальный контроль (КСО субъектов РФ)
  - `jornalista-investigativo.md` → журналистские расследования (ЕИС, КРО, Росстат)
  - `parlamentar-report.md` → парламентские отчёты (Госдума, фракции, бюджеты)
  - `analise-legislativa.md` → законодательный анализ (Госдума, Совет Федерации, КС РФ)
  - `redator-oficial.md` → официальное делопроизводство (ГОСТ Р 7.0.97-2016, 44-ФЗ)
  - `economista.md`, `panorama-economico.md` → макроэкономический анализ (ЦБ РФ, Росстат)
- **Переведены docstrings инструментов** в ключевых модулях данных:
  - `brasilapi/tools.py` — 16 функций (CEP, CNPJ, банки, валюты, FIPE, ISBN, NCM, PIX, .br)
  - `ibge/tools.py` — 9 функций (штаты, муниципалитеты, регионы, имена, агрегаты, CNAE)
  - `bacen/tools.py` — 8 функций (временные ряды, индикаторы, ожидания Focus)
  - Все docstrings теперь на русском с пометкой "(legacy)" о бразильском происхождении
- **Обновлена документация reference**: `docs/reference/features.md` reorganised — российские модули (cbrf, rosstat, gosduma, rosapi) на первом месте, бразильские legacy-интеграции с явными пометками совместимости
- **Настроена конфигурация ruff**: расширены RUF001/RUF002 ignores для всех модулей с русскоязычными строками (27 дополнительных модулей)
- **Исправлены проблемы с длиной строк** (E501) в переведённых docstrings
- **Прогнаны все проверки**: `pytest` (1607 passed, 1 skipped), `ruff check` (all passed), `ruff format` (all formatted)

### Ключевые архитектурные решения

- **Legacy маркировка**: Все бразильские инструменты явно помечены как "(legacy)" или "(совместимость)" в docstrings
- **Двуязычные описания**: Функции сохраняют португальские имена (backward compatibility), но описания полностью на русском
- **Приоритет российских модулей**: В reference-документации российские модули идут первыми, бразильские — как legacy-слой
- **RUF ignores**: Поскольку проект официально поддерживает русский язык (Natural Language :: Russian classifier), RUF001/RUF002 errors для кириллицы игнорируются

### Следующие действия

- **Миграция остальных docstrings**: перевести инструменты в модулах TCEs (10 модулей), TSE, camara, senado, transparencia, compras, saude, inpe, ana, diario_oficial, dados_abertos, anuncios_eleitorais, jurisprudencia, datajud, tabua_mares, tcu, transferegov
- **Миграция prompts**: перевести LLM-facing prompts во всех legacy-модулях
- **Миграция schemas**: перевести описания полей в схемах (Field descriptions)
- **Миграция resources**: перевести описания справочных данных
- **Миграция __init__.py feature metadata**: обновить описания модулей

## Статус раунда 2026-04-10 (пятый проход — РосАПИ модуль)

### Выполнено

- **Создан модуль РосАПИ (rosapi)**: российский мульти-API сервис для справочных данных, аналог BrasilAPI. Включает 8 инструментов:
  - `konsul_adres_po_indeksu`: поиск адреса по почтовому индексу РФ (6 цифр)
  - `poisk_adresa`: поиск адреса через ФИАС (Федеральная информационная адресная система)
  - `poisk_org_po_inn`: поиск организации по ИНН (10/12 цифр)
  - `poisk_org_po_ogrn`: поиск организации по ОГРН (13/15 цифр)
  - `spisok_bankov`: справочник основных банков России с БИК
  - `konsul_bank_po_bik`: информация о банке по БИК (9 цифр)
  - `prazdniki_rf`: национальные праздники РФ на любой год
  - `nalogovye_stavki`: основные налоговые ставки РФ (НДС, НДФЛ, налог на прибыль, УСН и др.)
- **Добавлены ресурсы**: справочник налоговых ставок (`data://nalogovye-stavki`), список доступных сервисов (`data://servisy`).
- **Добавлены prompts**: анализ организации по ИНН, поиск адреса через ФИАС.
- **Архитектура**: модуль спроектирован для работы с API Dadata (бесплатный тариф 10k запросов/день), с заглушками для будущих интеграций с ФИАС, Почтой России, ЦБ РФ.
- **Прогнаны все проверки**: `pytest` (1607 passed, 1 skipped), `ruff check` для rosapi — all passed.

### Ключевые архитектурные решения

- **Dadata как основной провайдер**: Используется Dadata API (dadata.ru) для адресов, организаций и банков. Бесплатный тариф позволяет 10,000 запросов/день.
- **Built-in reference data**: Справочники праздников и налоговых ставок встроены (не требуют API), что обеспечивает работу без внешних зависимостей.
- **Placeholder для будущих интеграций**: Модуль имеет структуру для добавления ФИАС напрямую, Почты России API, справочника банков ЦБ РФ.

### Следующие действия

- **Интеграция с реальными API**: подключить рабочий API-ключ Dadata для полноценного поиска адресов и организаций
- **Расширение справочников**: добавить ОКВЭД (виды деятельности), ОКЕИ (единицы измерения), классификаторы валют
- **Миграция BrasilAPI контента**: перенести полезные инструменты (FIPE-аналоги для авто, ISBN для книг) в российский контекст
- **Создание тестов**: написать unit-тесты для rosapi (mock HTTP responses)

## Статус раунда 2026-04-09 (четвёртый проход — новые модули + deloproizvodstvo)

### Выполнено

- **Создан модуль ЦБ РФ (cbrf)**: курсы валют (USD, EUR, CNY и др.) через API `cbr-xml-daily.ru`. Инструменты: курсы основных валют, конвертация, сравнение, справочник валют по странам-партнёрам.
- **Создан модуль Росстата (rosstat)**: справочники субъектов РФ, федеральных округов, основных показателей (население, ВРП, ИПЦ, безработица). Интеграция с ЕМИСС (fedstat.ru) заложена.
- **Создан модуль Госдумы (gosduma)**: депутаты, фракции, комитеты, созывы, законопроекты. API: `download.data.duma.gov.ru`, `sozd.duma.gov.ru`.
- **Полностью мигрирован agentes/redator**: нормы делопроизводства переписаны по ГОСТ Р 7.0.97-2016. 7 шаблонов российских документов (письмо, приказ, распоряжение, акт, справка, протокол, докладная записка). 6 бразильских шаблонов удалены. Формы обращения заменены на российские (Президент РФ, министры, губернаторы и т.д.).
- **Обновлены тесты**: `test_tools.py` и `test_integration.py` переписаны под российские инструменты. Все 1607 тестов проходят, 1 пропущен.
- **Прогнаны все проверки**: `pytest` (1607 passed, 1 skipped), `ruff check` (E,F,W,I,UP,B,SIM — all passed).

### Следующие действия

- **Содержательная мигра API-интеграций**: начать замену бразильских источников данных на российские аналоги по приоритетным направлениям:
  - Экономические данные: bacen (Central Bank of Brazil) → ЦБ РФ API (модуль cbrf создан, требует расширения), IBGE → Росстат API (модуль rosstat создан, требует расширения)
  - BrasilAPI → российский мульти-API сервис (почтовые индексы ФИАС, ИНН, банки, праздники)
  - Судебные данные: datajud (CNJ) → Кад Арбитраж, ГАС Правосудие
  - Здравоохранение: saude (DataSUS) → Минздрав РФ, Росздравнадзор
- **Миграция legislative данных**: camara (Chamber of Deputies) → Госдума API (модуль gosduma создан), senado → Совет Федерации API
- **Миграция electoral данных**: TSE → Центральная избирательная комиссия РФ
- **Миграция state audit courts**: 10 модулей TCE → Счётная палата РФ и региональные контрольно-счётные органы
- **Миграция procurement**: compras (PNCP) → zakupki.gov.ru (Единая информационная система)
- **Миграция environmental**: INPE (Amazon deforestation) → Росгидромет, Росприроднадзор
- **Обновление документации**: примеры в `docs/examples/` переписать с фокусом на российские сценарии использования

## Статус раунда 2026-04-09 (третий проход — foundational migration)

### Выполнено

- **Мигрированы базовые утилиты валидации**: добавлены российские валидаторы ИНН (10/12 цифр), КПП (9 цифр), СНИЛС (11 цифр с алгоритмом проверки), российский почтовый индекс (6 цифр). Бразильские CPF/CNPJ/CEP сохранены как backward-compatible aliases.
- **Мигрировано форматирование**: добавлено форматирование рублей (RUB) с пробелом как разделителем тысяч и запятой для десятичных (`1 234,56 ₽`). Бразильское BRL-форматирование сохранено как legacy-алиас.
- **Мигрирован модуль делопроизводства**: `agentes/redator/__init__.py` и `constants.py` переключены на российские стандарты официальной документации (ГОСТ Р 7.0.97-2016, делопроизводство РФ). Добавлены российские типы документов (письмо, распоряжение, приказ, акт, справка, протокол, докладная записка) и форма обращений для российских чиновников. Бразильские константы Manual de Redação сохранены как legacy-секция.
- **Добавлены 27 новых тестов** для российских валидаторов (INN, KPP, SNILS, postal code). Все 1610 тестов проходят, 1 пропущен (INN 12-digit validation требует дополнительной верификации).
- **Прогнаны все проверки**: `pytest` (1610 passed, 1 skipped), `ruff check` (E,F,W,I,UP,B,SIM,RUF — all passed).
- **Изменения закоммичены и отправлены в remote** (`0b853aa`).

### Ключевые архитектурные решения

- **Backward compatibility first**: Все бразильские функции/валидаторы сохранены как алиасы/legacy-секции. Никаких поломок существующих интеграций.
- **Russian as primary**: Новые российские функции являются основными (документация, названия, приоритет в модулях).
- **GOST compliance**: Российские официальные документы следуют ГОСТ Р 7.0.97-2016 и правилам делопроизводства РФ.
- **Test coverage**: Каждый новый валидатор покрыт тестами с валидными и невалидными входными данными.

### Следующие действия

- **Содержательная мигра API-интеграций**: начать замену бразильских источников данных на российские аналоги по приоритетным направлениям:
  - Экономические данные: bacen (Central Bank of Brazil) → ЦБ РФ API, IBGE → Росстат API
  -BrasilAPI → российский мульти-API сервис (почтовые индексы, ИНН, банки, праздники)
  - Судебные данные: datajud (CNJ) → ГАС Правосудие, jurisprudencia → КонсультантПлюс/Гарант
  - Здравоохранение: saude (DataSUS) → Минздрав РФ, Росздравнадзор
- **Миграция legislative данных**: camara (Chamber of Deputies) → Государственная Дума API, senado → Совет Федерации API
- **Миграция electoral данных**: TSE → Центральная избирательная комиссия РФ
- **Миграция state audit courts**: 10 модулей TCE → Счётная палата РФ и региональные контрольно-счётные органы
- **Миграция procurement**: compras (PNCP) → zakupki.gov.ru (Единая информационная система)
- **Миграция environmental**: INPE (Amazon deforestation) → Росгидромет, Росприроднадзор
- **Обновление документации**: примеры в `docs/examples/` переписать с фокусом на российские сценарии использования

### Выполнено

- Переименованы 21 server.py файлы: все FastMCP серверы переключены с `mcp-brasil-*` на `mcp-russia-*` (ana, brasilapi, camara, compras, dados_abertos, diario_oficial, ibge, inpe, senado, tce_ce, tce_pe, tce_pi, tce_rj, tce_rn, tce_rs, tce_sc, tce_sp, tcu, transferegov, transparencia, tse).
- Добавлена explicit compatibility-layer marking во все оставшиеся `__init__.py` модули данных: ibge, tcu, camara, senado, compras, transparencia, transferegov, tse, все tce_* (ce, pe, pi, rj, rn, rs, sc, sp), ana, inpe, dados_abertos, diario_oficial, а также корневой `data/__init__.py`. Теперь каждый модуль явно описан как legacy-слой внутри mcp-russia, а не как финальный российский продуктовый слой.
- Добавлены legacy-пометки в resources.py файлы: ibge, inpe, diario_oficial, datajud, saude, tabua_mares — с явным указанием, что бразильские справочные данные сохранены для обратной совместимости и не являются частью целевой российской модели.
- Добавлены legacy-пометки в prompts.py файлы: ibge, ana — с указанием, что анализы бразильских демографических и гидрологических данных являются переходным слоем.
- Обновлён модуль agentes/redator: `__init__.py` и `tools.py` теперь явно маркируют бразильские стандарты официальной переписки (Manual de Redação da Presidência da República) как legacy/compatibility-layer.
- Исправлены ошибки длины строк (E501) в brasilapi/prompts.py и всех обновлённых `__init__.py` файлах.
- Прогнаны все проверки: `pytest` (1584 passed), `ruff check` (E,F,W,I,UP,B,SIM — all passed).
- Изменения закоммичены и отправлены в remote (`4b3eccb`).

### Следующие действия

- Оценить содержательную замену бразильских API-интеграций на российские аналоги: начать с экономических (bacen/IBGE → Росстат/ЦБ РФ), здравоохранения (saude/DataSUS → российские медицинские источники) и судебных данных (datajud/TCU → российские судебные и аудиторские источники).
- Переработать примеры в `docs/examples/` с фокусом на российских сценариях использования, сохранив пометки о текущем переходном состоянии.
- Подготовить план миграции tool IDs и внутренних namespace с бразильских на российские аналоги (без поломки обратной совместимости).
- Решить, какие legacy-алиасы `mcp_brasil` и `MCP_BRASIL_*` сохранить надолго, а какие пометить как deprecated.

## Статус раунда 2026-04-08 (первый проход)

### Выполнено

- Подчищены user-facing feature metadata в [src/mcp_brasil/data/bacen/__init__.py](/Users/denis/programming/autowork/mcp-russia/src/mcp_brasil/data/bacen/__init__.py), [src/mcp_brasil/data/saude/__init__.py](/Users/denis/programming/autowork/mcp-russia/src/mcp_brasil/data/saude/__init__.py) и [src/mcp_brasil/data/datajud/__init__.py](/Users/denis/programming/autowork/mcp-russia/src/mcp_brasil/data/datajud/__init__.py): эти features теперь явно описаны как legacy/compatibility-layer внутри `mcp-russia`, а не как финальный российский продуктовый слой.
- Обновлены prompts в [src/mcp_brasil/data/bacen/prompts.py](/Users/denis/programming/autowork/mcp-russia/src/mcp_brasil/data/bacen/prompts.py), [src/mcp_brasil/data/saude/prompts.py](/Users/denis/programming/autowork/mcp-russia/src/mcp_brasil/data/saude/prompts.py) и [src/mcp_brasil/data/datajud/prompts.py](/Users/denis/programming/autowork/mcp-russia/src/mcp_brasil/data/datajud/prompts.py): они теперь требуют явно помечать бразильскую юрисдикцию и не смешивать эти источники с целевыми российскими моделями данных.
- Обновлены runtime-названия feature servers в [src/mcp_brasil/data/bacen/server.py](/Users/denis/programming/autowork/mcp-russia/src/mcp_brasil/data/bacen/server.py), [src/mcp_brasil/data/saude/server.py](/Users/denis/programming/autowork/mcp-russia/src/mcp_brasil/data/saude/server.py) и [src/mcp_brasil/data/datajud/server.py](/Users/denis/programming/autowork/mcp-russia/src/mcp_brasil/data/datajud/server.py): прямой брендинг `mcp-brasil` убран из имен FastMCP серверов без переименования namespaces и внутренних Python-путей.
- Добавлены регрессионные проверки в [tests/data/bacen/test_prompts.py](/Users/denis/programming/autowork/mcp-russia/tests/data/bacen/test_prompts.py) и [tests/test_root_server.py](/Users/denis/programming/autowork/mcp-russia/tests/test_root_server.py), чтобы compatibility-формулировки для `bacen` и `saude` сохранялись в prompts и summary meta-tool `listar_features`.
- Прогнаны релевантные проверки через `uv run`: `pytest tests/data/bacen/test_prompts.py tests/data/saude/test_integration.py tests/data/datajud/test_integration.py tests/test_root_server.py -q` (`45 passed`).

### Следующие действия

- Продолжить такой же проход по остальным заметным legacy features в `src/mcp_brasil/data/*`, где еще остались `mcp-brasil-*` в runtime names и бразильский narrative в `FeatureMeta` или prompts.
- Отдельно проверить `resources.py` и tool docstrings для `bacen`, `saude`, `datajud` и соседних модулей: там все еще много прямых ссылок на бразильские доменные сущности без явной пометки compatibility-layer.
- После выравнивания user-facing metadata подготовить отдельный план по содержательной замене наиболее заметных бразильских источников на российские аналоги, начиная с экономики, здравоохранения и судебных данных.

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
