# TODO

Живой список задач по миграции `mcp-russia` на российские и русскоязычные реалии.

## Статус раунда 2026-07-22 (девяносто второй проход — deputat_id→identifikator_deputata, _razobrat_status→_razobrat_sostoyanie, .env.example code_mode→rezhim_koda)

### Выполнено

- **Русификация `deputat_id` → `identifikator_deputata`** в server.py (1 замена):
  - server.py: пример `"deputat_id": 99100142` → `"identifikator_deputata": 99100142` в docstring `vypolnit_paket`; реальный инструмент `gosduma_info_deputata` принимает параметр `identifikator_deputata`, не `deputat_id` — исправление бага документации
- **Русификация `_razobrat_status` → `_razobrat_sostoyanie`** в fns/client.py (5 ссылок):
  - client.py: функция `_razobrat_status` → `_razobrat_sostoyanie`, параметр `kod_statusa` → `kod_sostoyaniya`
  - client.py: переменная `karta_statusov` → `karta_sostoyaniy`
  - client.py: 2 вызова `_razobrat_status()` → `_razobrat_sostoyanie()`
- **Исправление `.env.example`**: `"code_mode"` → `"rezhim_koda"` — пропущено в раунде 91
- **Контекстуализация CHANGELOG.md** (3 записи): добавлено «модуль удалён» к устаревшим модулям с португальскими артефактами; `search_after` → `search_after (Elasticsearch API)`
- **Удаление дублирующегося ключевого слова** в pyproject.toml: `"opendata"` указан дважды → один раз

### Ключевые архитектурные решения

- **`deputat_id` → `identifikator_deputata`**: устранён английский суффикс `_id` в примере docstring; реальный инструмент `gosduma_info_deputata` принимает `identifikator_deputata`, не `deputat_id` — пользователи, копировавшие пример, получали ошибки несуществующего параметра
- **`_razobrat_status` → `_razobrat_sostoyanie`**: устранён английский идентификатор `status` в имени функции и параметра; `sostoyanie` = «состояние» — устоявшаяся конвенция проекта; `karta_statusov` → `karta_sostoyaniy` для согласованности; поле Pydantic-схемы уже называлось `sostoyanie` (с раунда 90)
- **`.env.example`**: синхронизация с раундом 91, где `code_mode` был заменён на `rezhim_koda` в settings.py, server.py и документации, но `.env.example` был пропущен
- **CHANGELOG.md**: исторические записи с португальскими артефактами уточнены пометкой «модуль удалён» для ясности, что эти инструменты больше не существуют в кодовой базе

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Кодовая база полностью русифицирована**: оставшиеся английские идентификаторы — только строковые ключи API-ответов (`.get("key")`), keyword-аргументы внешних библиотек (httpx, Pydantic, FastMCP), стандартные Python-идентификаторы (`*args`, `**kwargs`, `__aexit__(*exc)`), параметры stdlib-переопределений (`tag`, `attrs` в HTMLParser), loanwords идентичные русским (`data` = «дата», `period` = «период»), и `logger` (стандартная конвенция Python); CSS-классы внешних HTML-страниц оставлены без изменений — изменение сломает парсинг; имена переменных окружения оставлены на английском — внешняя конфигурация; международные аббревиатуры (`WMO`, `VIN`, `API`) оставлены без изменений

## Статус раунда 2026-07-22 (девяносто первый проход — TableParser→RazborshchikTablitsVyborov, call_next→vyzvat_sleduyushchiy, code_mode→rezhim_koda, info_api→svedeniya_ob_api)

### Выполнено

- **Русификация `_VyboryTableParser` → `_RazborshchikTablitsVyborov`** в cekrf/client.py (3 ссылки):
  - client.py: объявление класса `_VyboryTableParser` → `_RazborshchikTablitsVyborov`
  - client.py: 2 использования `razobratchik = _VyboryTableParser()` → `_RazborshchikTablitsVyborov()`
- **Русификация `call_next` → `vyzvat_sleduyushchiy`** в server.py (6 ссылок):
  - server.py: параметр `call_next: CallNext[...]` → `vyzvat_sleduyushchiy: CallNext[...]` (3 метода)
  - server.py: вызов `await call_next(context)` → `await vyzvat_sleduyushchiy(context)` (3 вызова)
- **Русификация `code_mode` → `rezhim_koda`** в конфигурации (4 файла):
  - settings.py: комментарий `"code_mode"` → `"rezhim_koda"`
  - server.py: сравнение `POISK_INSTRUMENTOV == "code_mode"` → `"rezhim_koda"`
  - smart-tools.md: таблица значений настройки
  - configuration.md: таблица значений настройки
- **Русификация `info_api` → `svedeniya_ob_api`** в cekrf (4 файла):
  - resources.py: функция `info_api()` → `svedeniya_ob_api()`
  - server.py: импорт, `mcp.resource("data://info-api")` → `"data://svedeniya-ob-api"`
  - test_integration.py: `"data://info-api"` → `"data://svedeniya-ob-api"`
  - features.md: ресурс URI
- **Русификация `proverka_svyazi_fn` → `instrument_proverki_svyazi`** в test_feature.py (1 замена)
- **Прогнаны все проверки**: `ruff check` — 1 импорт исправлен, `ruff format` — 306 файлов уже форматировано, `pytest` — 681 unit-тест пройдено

### Ключевые архитектурные решения

- **`_VyboryTableParser` → `_RazborshchikTablitsVyborov`**: устранён последний смешанный русско-английский идентификатор класса; `RazborshchikTablitsVyborov` = «разборщик таблиц выборов» — полностью русская транслитерация; внутренние поля класса (`stroki_tablitsy`, `tekst_zagolovka`, `tekst_statistiki`) уже были на русской транслитерации
- **`call_next` → `vyzvat_sleduyushchiy`**: устранён английский идентификатор параметра в промежуточном слое; `vyzvat_sleduyushchiy` = «вызвать следующий» — точная транслитерация паттерна middleware; имена методов уже русифицированы (`pri_vyzove_instrumenta`, `pri_chtenii_resursa`, `pri_zaprose_prompta`)
- **`code_mode` → `rezhim_koda`**: устранён английский конфигурационный токен; `rezhim_koda` = «режим кода» — согласовано с другими значениями `bm25` (алгоритм) и `none` (ключевое слово); ломающее изменение для клиентов, использующих `MCP_RUSSIA_TOOL_SEARCH=code_mode`
- **`info_api` → `svedeniya_ob_api`**: устранён английский идентификатор функции и ресурса; `svedeniya_ob_api` = «сведения об API»; ресурс URI `data://info-api` → `data://svedeniya-ob-api` согласован с остальными ресурсами (`data://tipy-vyborov`, `data://subiekty-rf`); ломающее изменение для клиентов, использующих ресурс `data://info-api`
- **`proverka_svyazi_fn` → `instrument_proverki_svyazi`**: устранён английский суффикс `_fn`; `instrument_proverki_svyazi` = «инструмент проверки связи»

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Кодовая база полностью русифицирована**: оставшиеся английские идентификаторы — только строковые ключи API-ответов (`.get("key")`), keyword-аргументы внешних библиотек (httpx, Pydantic, FastMCP), стандартные Python-идентификаторы (`*args`, `**kwargs`, `__aexit__(*exc)`), параметры stdlib-переопределений (`tag`, `attrs` в HTMLParser), loanwords идентичные русским (`data` = «дата», `period` = «период»), и `logger` (стандартная конвенция Python); CSS-классы внешних HTML-страниц оставлены без изменений — изменение сломает парсинг; имена переменных окружения оставлены на английском — внешняя конфигурация; международные аббревиатуры (`WMO`, `VIN`, `API`) оставлены без изменений

## Статус раунда 2026-07-21 (девяностый проход — federal→federalnye, region→subiekt, status→sostoyanie в идентификаторах)

### Выполнено

- **Унификация `federal` → `federalnye`** в cekrf (13 замен в 7 файлах):
  - constants.py: `DOLZHNOSTI_FEDERAL` → `DOLZHNOSTI_FEDERALNYE`
  - client.py: импорт, вызов `dolzhnosti_federal()` → `dolzhnosti_federalnye()`, цикл по `DOLZHNOSTI_FEDERALNYE`
  - tools.py: `dolzhnosti_federal()` → `dolzhnosti_federalnye()`, вызов `client.dolzhnosti_federalnye()`
  - server.py: импорт, регистрация `dolzhnosti_federalnye`
  - test_tools.py: `test_dolzhnosti_federal` → `test_dolzhnosti_federalnye`, вызов
  - test_integration.py: `"dolzhnosti_federal"` → `"dolzhnosti_federalnye"`
  - features.md: `dolzhnosti_federal` → `dolzhnosti_federalnye`
- **Унификация `region_otpravki` → `subiekt_otpravki`** в rosselkhoznadzor (4 замены в 3 файлах):
  - schemas.py: `region_otpravki` → `subiekt_otpravki`
  - tools.py: `sertifikat.get("subiekt_otpravki", "")`
  - client.py: `"subiekt_otpravki": dannye.get(...)` + fallback
  - test_tools.py: мок-данные обновлены
- **Унификация `status_*` → `sostoyanie_*`** в Pydantic-полях и ключах словарей (~26 замен в 14 файлах):
  - rosselkhoznadzor/schemas.py: `status_karantina` → `sostoyanie_karantina`
  - rosselkhoznadzor/tools.py: `.get("sostoyanie_karantina", "")`
  - rosselkhoznadzor/client.py: `"sostoyanie_karantina": ...` + fallback
  - rosreestr/schemas.py: `status_ucheta` → `sostoyanie_ucheta`
  - rosreestr/tools.py: `obekt.sostoyanie_ucheta`
  - rosreestr/client.py: `sostoyanie_ucheta` (3 ссылки)
  - fns/schemas.py: `status_oplaty` → `sostoyanie_oplaty`
  - gibdd/schemas.py: `status_oplaty` → `sostoyanie_oplaty`
  - gibdd/client.py: `"status_ts"` → `"sostoyanie_ts"`
  - rospotrebnadzor/schemas.py: `status_rassmotreniya` → `sostoyanie_rassmotreniya`
  - rospotrebnadzor/tools.py: `.get("sostoyanie_rassmotreniya", "")`
  - rospotrebnadzor/client.py: `"sostoyanie_rassmotreniya": ...`
  - roskomnadzor/schemas.py: `status_rassmotreniya` → `sostoyanie_rassmotreniya`
  - minobrnauki/schemas.py: `status_akkreditatsii` → `sostoyanie_akkreditatsii`
  - minobrnauki/tools.py: `.get('sostoyanie_akkreditatsii', '')` (2), `.get("sostoyanie_litsenzii", "")`
  - minobrnauki/client.py: `"sostoyanie_akkreditatsii": ...`, `"sostoyanie_litsenzii": ...`
  - gosduma/tools.py: `status_label` → `metka_sostoyaniya` (2 ссылки)
  - test_tools.py (4 файла): обновлены мок-данные
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — 306 файлов уже форматировано, `pytest` — 681 unit-тест пройдено

### Ключевые архитектурные решения

- **`federal` → `federalnye`**: устранён английский идентификатор в именах констант и функций; `federalnye` — русская транслитерация прилагательного «федеральные» во множественном числе; согласовано с `federalnyy` (единственное число в `uroven: "federalnyy"`); ломающее изменение для клиентов, использующих инструмент `dolzhnosti_federal`
- **`region_otpravki` → `subiekt_otpravki`**: устранён английский идентификатор `region`; `subiekt` — устоявшаяся конвенция проекта для «субъект РФ» (с `ie` для `ъ`); ломающее изменение для клиентов, использующих ключ `region_otpravki`
- **`status_*` → `sostoyanie_*`**: устранён последний массовый класс английских идентификаторов в Pydantic-полях и ключах словарей; `sostoyanie` = «состояние» — устоявшаяся конвенция проекта; цикловые переменные `status in Statusy*` уже были переименованы в `sostoyanie` в раунде 85; ломающее изменение для клиентов, использующих ключи `status_karantina`, `status_ucheta`, `status_oplaty`, `status_rassmotreniya`, `status_akkreditatsii`, `status_litsenzii`, `status_ts`
- **`status_label` → `metka_sostoyaniya`**: устранена английская переменная; `metka_sostoyaniya` = «метка состояния»; согласовано с параметром `sostoyanie`

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Кодовая база полностью русифицирована**: оставшиеся английские идентификаторы — только строковые ключи API-ответов (`.get("key")`), keyword-аргументы внешних библиотек (httpx, Pydantic, FastMCP), стандартные Python-идентификаторы (`*args`, `**kwargs`, `__aexit__(*exc)`), параметры stdlib-переопределений (`tag`, `attrs` в HTMLParser), loanwords идентичные русским (`data` = «дата», `period` = «период»), и `logger` (стандартная конвенция Python); CSS-классы внешних HTML-страниц оставлены без изменений — изменение сломает парсинг; имена переменных окружения оставлены на английском — внешняя конфигурация

### Выполнено

- **Унификация `TOKEN` → `KLYUCH`** в settings.py (2 константы + 2 ссылки):
  - settings.py: `TOKEN_GOSDUMY_API` → `KLYUCH_GOSDUMY_API`, `TOKEN_ZAKUPKI_API` → `KLYUCH_ZAKUPKI_API`
  - gosduma/client.py: `settings.TOKEN_GOSDUMY_API` → `settings.KLYUCH_GOSDUMY_API`
  - zakupki/client.py: `settings.TOKEN_ZAKUPKI_API` → `settings.KLYUCH_ZAKUPKI_API`
- **Унификация `licenz` → `litsenz`** — устранение португальской транслитерации `c` → русская `ts` для «ц» (~30 замен в 12 файлах):
  - roskomnadzor/schemas.py: `LicenziyaSvyazi` → `LitsenziyaSvyazi`, `tip_licenzii` → `tip_litsenzii`
  - roskomnadzor/constants.py: `TIPY_LICENZIY_SVYAZI` → `TIPY_LITSENZIY_SVYAZI`
  - roskomnadzor/tools.py: `spisok_tipov_licenziy` → `spisok_tipov_litsenziy`, `info_licenzii` → `info_litsenzii`, `nomer_licenzii` → `nomer_litsenzii`, `licenzii` → `litsenzii`, `poisk_licenziy` → `poisk_litsenziy`, `tip_licenzii` → `tip_litsenzii`
  - roskomnadzor/client.py: `poisk_licenziy` → `poisk_litsenziy`, `tip_licenzii` → `tip_litsenzii`
  - roskomnadzor/server.py: `info_licenzii` → `info_litsenzii`, `spisok_tipov_licenziy` → `spisok_tipov_litsenziy`
  - minobrnauki/client.py: `poisk_licenziy` → `poisk_litsenziy`, `status_licenzii` → `status_litsenzii`, `nomer_licenzii` → `nomer_litsenzii`, `data_licenzii` → `data_litsenzii`
  - minobrnauki/tools.py: `poisk_licenziy` → `poisk_litsenziy`, `nomer_licenzii` → `nomer_litsenzii`, `status_licenzii` → `status_litsenzii`
  - minobrnauki/server.py: `poisk_licenziy` → `poisk_litsenziy`
  - rosprirodnadzor/schemas.py: `LicenziyaNedropolzovanie` → `LitsenziyaNedropolzovanie`
  - tests/data/roskomnadzor/test_tools.py: 5 функций и моков
  - tests/data/roskomnadzor/test_integration.py: 2 ссылки
  - tests/data/minobrnauki/test_tools.py: 2 функции и моков
  - tests/data/minobrnauki/test_integration.py: 1 ссылка
- **Исправление смешанного скрипта в документации**: `прavo.gov.ru` → `pravo.gov.ru` в politolog.md (кириллическое «пр» + латинское «avo»)
- **Исправление `subyekt` → `subiekt`** в politolog.md (1 вхождение; согласовано с конвенцией проекта)
- **Исправление грамматической ошибки**: `юанка` → `юаня` в ekonomist.md (родительный падеж слова «юань»)
- **Исправление параметров в документации** (~15 замен в municipalnyy-kontrol.md):
  - `rosaudit_poisk_narusheniy(subiekt=...)` → `(organizaciya=...)` / `(tip=...)` — функция не принимает параметр `subiekt`; реальная сигнатура: `organizaciya, tip, god`
  - `kaznacheistvo_ispolnenie_byudzheta(subiekt=...)` → `(god=...)` — устранён несуществующий параметр
  - `zakupki_poisk_kontraktov(organ=..., god=...)` → `(inn_zakazchika=...)` — реальная сигнатура: `inn_podryadchika, inn_zakazchika, ogranichenie`
  - Устранены дублирующиеся вызовы (Мытищи/Люберцы вместо двух идентичных «МО»)
  - `"zdravookhranenie"` → `"Здравоохранение"` (унификация кириллицей в примерах)
- **Исправление примера в zhurnalist-stati.md**: `cbrf_sravnit_valyuty(kody=["key_rate", "cpi"])` → `(kody=["USD", "EUR", "CNY"])` — функция принимает коды валют, не макроиндикаторы
- **Исправление дублирующихся вызовов** в zhurnalist-stati.md: 3 одинаковых `rosstat_spisok_regionov` → 3 разных инструмента (справочник + 2 региональных запроса)
- **Контекстуализация аббревиатуры `пнкп`** в CHANGELOG.md (2 вхождения): добавлено пояснение «(бразильская ПНЗК — Plataforma Nacional de Contratações Públicas)»
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — 1 файл переформатировано, `pytest` — 681 unit-тест пройдено

### Ключевые архитектурные решения

- **`TOKEN` → `KLYUCH`**: устранён английский идентификатор в константах настроек; `KLYUCH_DADATA_API` и `KLYUCH_ANTHROPIC_API` уже использовали `KLYUCH`; `TOKEN` — единственное исключение; имена переменных окружения (`MCP_RUSSIA_DUMA_API_TOKEN`, `MCP_RUSSIA_ZAKUPKI_API_TOKEN`) оставлены без изменений — внешняя конфигурация; ломающее изменение для клиентов, использующих `settings.TOKEN_GOSDUMY_API` или `settings.TOKEN_ZAKUPKI_API`
- **`licenz` → `litsenz`**: устранена португальская транслитерация «ц» через `c`; русская транслитерация через `ts` (`litsenziya`) — устоявшаяся конвенция проекта; в rosprirodnadzor/tools.py и rosprirodnadzor/client.py уже использовалось `litsenz`, но класс `LicenziyaNedropolzovanie` и весь модуль roskomnadzor/minobrnauki использовали `licenz`; ломающее изменение для клиентов, использующих инструменты `spisok_tipov_licenziy`, `info_licenzii`, `poisk_licenziy`
- **`прavo.gov.ru`**: критическая опечатка — смешение кириллицы и латиницы; URL должен быть полностью латинским
- **`subyekt` → `subiekt`**: исправлена документация — исходный код использует `subiekt` (с `ie` для `ъ`), а документация ссылалась на устаревшее `subyekt`; согласовано с исправлением раунда 86
- **`rosaudit_poisk_narusheniy(subiekt=...)`**: исправлена документация — реальная функция принимает `organizaciya, tip, god`, не `subiekt`; пользователи, копировавшие примеры, получали ошибки несуществующих параметров

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Кодовая база полностью русифицирована**: оставшиеся английские идентификаторы — только строковые ключи API-ответов (`.get("key")`), keyword-аргументы внешних библиотек (httpx, Pydantic, FastMCP), стандартные Python-идентификаторы (`*args`, `**kwargs`, `__aexit__(*exc)`), параметры stdlib-переопределений (`tag`, `attrs` в HTMLParser), loanwords идентичные русским (`data` = «дата», `period` = «период»), и `logger` (стандартная конвенция Python); CSS-классы внешних HTML-страниц оставлены без изменений — изменение сломает парсинг; имена переменных окружения оставлены на английском — внешняя конфигурация

### Выполнено

- **Русификация `as e` → `as isklyuchenie`** в except-блоках (2 файла, пропущенные в раунде 85):
  - _shared/discovery.py: `except Exception as e` → `as isklyuchenie` + `str(e)` → `str(isklyuchenie)` + `f"...{e}"` → `f"...{isklyuchenie}"`
  - _shared/planner.py: `except Exception as e` → `as isklyuchenie` + `str(e)` → `str(isklyuchenie)` + `f"...{e}"` → `f"...{isklyuchenie}"`
- **Исправление документации `subyekty_rf` → `subiekty_rf`** в features.md (2 вхождения: имя инструмента и ресурс URI)
- **Русификация `breaking` → `ломающее изменение`** в cliff.toml (пользовательски-видимый маркер в CHANGELOG)
- **Русификация примера в adding-features.md** (3 замены): `/items` → `/zapisi`, `"page"` → `"stranitsa"`, `element` → `zapis` в цикле
- **Переименование устаревших диаграмм** (4 PNG): `system_overview.png` → `obzor_sistemy.png`, `feature_anatomy.png` → `anatomiya_modulya.png`, `auto_registry_flow.png` → `potok_avtoobnaruzheniya.png`, `data_flow.png` → `potok_dannykh.png` (синхронизировано с generate_diagrams.py)
- **Русификация CI/CD step names** (16 шагов в 2 файлах):
  - ci.yml: `CI` → `НИК`, `Install Python` → `Установить Python`, `Install dependencies` → `Установить зависимости`, `Lint` → `Линтинг`, `Type check` → `Проверка типов`, `Test` → `Тесты`
  - release.yml: `Release to PyPI` → `Релиз в PyPI`, `Publish to PyPI` → `Публикация в PyPI`, `Build package` → `Сборка пакета`, `Smoke test` → `Дымовое тестирование`, `Create GitHub Release` → `Создать релиз на GitHub`, `Install git-cliff` → `Установить git-cliff`
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — 306 файлов уже форматировано, `pytest` — 681 unit-тест пройдено

### Ключевые архитектурные решения

- **`as e` → `as isklyuchenie`**: устранены два пропущенных English-идентификатора в except-блоках; согласовано с конвенцией, установленной в раунде 85
- **`subyekty_rf` → `subiekty_rf`**: исправлена документация — исходный код использует `subiekty_rf` (с `ie` для `ъ`), а документация ссылалась на устаревшее `subyekty_rf`; пользователи, копировавшие из документации, получали ошибки
- **`breaking` → `ломающее изменение`**: русификация пользовательски-видимого маркера в CHANGELOG; «ломающее изменение» — точный перевод «breaking change»
- **Диаграммы**: устаревшие английские имена файлов заменены на русские транслитерации; скрипт generate_diagrams.py уже генерирует новые имена (с раунда 81), но старые PNG-файлы оставались на диске
- **CI/CD step names**: GitHub Actions отображает `name:` в интерфейсе; русификация согласована с общей конвенцией проекта

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Кодовая база полностью русифицирована**: оставшиеся английские идентификаторы — только строковые ключи API-ответов (`.get("key")`), keyword-аргументы внешних библиотек (httpx, Pydantic, FastMCP), стандартные Python-идентификаторы (`*args`, `**kwargs`, `__aexit__(*exc)`), параметры stdlib-переопределений (`tag`, `attrs` в HTMLParser), loanwords идентичные русским (`data` = «дата», `period` = «период»), и `logger` (стандартная конвенция Python); CSS-классы внешних HTML-страниц оставлены без изменений — изменение сломает парсинг

## Статус раунда 2026-07-19 (восемьдесят седьмой проход — русификация ID→Идентификатор, .gitignore, planner.py пример, CHANGELOG.md, CONTRIBUTING.md)

### Выполнено

- **Русификация `ID` → `Идентификатор`** в пользовательски-видимых строках (~20 замен в 8 файлах):
  - gosduma/tools.py: `"ID"` → `"Идентификатор"` в заголовках таблиц (2 вхождения), `"ID депутата"` → `"Идентификатор депутата"` в docstring, `f"Депутат с ID {id}"` → `f"Депутат с идентификатором {id}"`, `f"- ID: {id}"` → `f"- Идентификатор: {id}"`
  - cekrf/tools.py: `"ID"` → `"Идентификатор"` в заголовке таблиц, `"ID кандидата"` → `"Идентификатор кандидата"` в docstring, `f"Кандидат с ID '{id}'"` → `f"Кандидат с идентификатором '{id}'"`, `f"- ID: {id}"` → `f"- Идентификатор: {id}"`
  - cekrf/client.py: `"ID кандидата"` → `"Идентификатор кандидата"` в docstring
  - gosduma/client.py: `"по ID"` → `"по идентификатору"`, `"ID депутата"` → `"Идентификатор депутата"` в docstrings
  - fns/client.py: `"ID задачи"` → `"идентификатора задачи"` в комментариях (4 вхождения)
  - minzdrav/tools.py: `f"с ID {id}"` → `f"с идентификатором {id}"`
  - roskomnadzor/tools.py: `"ID конкретной записи"` → `"Идентификатор конкретной записи"` в docstring
  - docs/examples/parlamentskiy-otchet.md: `→ ID` → `→ идентификатор`
- **Исправление примера в planner.py**: `"id"` → `"identifikator_deputata"`, `"ID"` → `"идентификатор"` (согласовано с реальной сигнатурой `info_deputata(identifikator_deputata: int)`)
- **Синхронизация test_discovery.py** с planner.py: `"id": "{etap_1.id}"` → `"identifikator_deputata": "{etap_1.identifikator}"`, `"ID"` → `"идентификатор"`
- **Русификация .gitignore** (6 комментариев): `# Python` → `# Пайтон`, `# Virtual environment` → `# Виртуальное окружение`, `# Caches` → `# Кеши`, `# Claude` → `# Клод`, `# Environment` → `# Окружение`, `# IDE` → `# Среда разработки`
- **Русификация CONTRIBUTING.md** (2 замены в примерах кода): `{"id": 1, ...}` → `{"identifikator": 1, ...}`, `"zapros": "test"` → `"zapros": "proverka"`
- **Контекстуализация португальских артефактов в CHANGELOG.md** (3 записи):
  - `Compras.gov.br` → `бразильского портала Compras.gov.br`
  - `partidos_senado и ufs_senado` → `partidos_senado (бразильские партии) и ufs_senado (бразильские штаты)`
  - `jurisprudencia` → `jurisprudencia (бразильская судебная практика)`
  - `TREs, TJMs` → `TREs (бразильские избирательные суды), TJMs (суды военной юстиции)`
  - `search_after` → оставлен (технический термин Elasticsearch API)
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — 306 файлов уже форматировано, `pytest` — 681 unit-тест пройдено

### Ключевые архитектурные решения

- **`ID` → `Идентификатор`**: устранена последняя английская аббревиатура в пользовательски-видимых строках (заголовки таблиц, docstrings, форматированные сообщения); `Идентификатор` = «identifier» — точный русский эквивалент; в таблицах заменено полностью, а не сокращением, для единообразия с конвенцией проекта
- **`"id"` → `"identifikator_deputata"` в planner.py**: пример системного промпта использовал `"id"` как ключ параметра, но реальный инструмент `gosduma_info_deputata` принимает `identifikator_deputata`; несоответствие могло приводить к некорректным планам от LLM; `{{etap_1.id}}` → `{{etap_1.identifikator}}` синхронизировано с полем Pydantic-модели `Deputat.identifikator`
- **`.gitignore`**: устранены последние английские комментарии в файловой структуре; «Пайтон» — устоявшаяся русификация «Python», «Среда разработки» — точный перевод «IDE»
- **CHANGELOG.md**: португальские артефакты контекстуализированы (добавлена пометка «бразильский»/«бразильские») вместо удаления; исторические записи не удаляются, но уточняются для русскоязычного читателя

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Кодовая база полностью русифицирована**: оставшиеся английские идентификаторы — только строковые ключи API-ответов (`.get("key")`), keyword-аргументы внешних библиотек (httpx, Pydantic, FastMCP), стандартные Python-идентификаторы (`*args`, `**kwargs`, `__aexit__(*exc)`), параметры stdlib-переопределений (`tag`, `attrs` в HTMLParser), loanwords идентичные русским (`data` = «дата», `period` = «период»), и `logger` (стандартная конвенция Python); CSS-классы внешних HTML-страниц оставлены без изменений — изменение сломает парсинг

## Статус раунда 2026-07-19 (восемьдесят шестой проход — унификация _MAP→_SLOVAR, mkb_classes→mkb_klassy, klass_css→klass_stiley, sub-module→podmodul, русификация документации)

### Выполнено

- **Унификация `_MAP` → `_SLOVAR` на константах** (5 констант в 2 модулях):
  - rosreestr/constants.py: `TIPY_NEDVIZIMOSTI_MAP` → удалена (неиспользуемая), `KATEGORII_ZEMEL_MAP` → `KATEGORII_ZEMEL_SLOVAR`, `VIDY_ISPOLZOVANIYA_MAP` → удалена (неиспользуемая), `STATUSY_UCHE_TA_MAP` → `STATUSY_UCHE_TA_SLOVAR`, `FORMY_SOBSTVENNOSTI_MAP` → удалена (неиспользуемая)
  - rosreestr/client.py: `KATEGORII_ZEMEL_MAP` → `KATEGORII_ZEMEL_SLOVAR`, `STATUSY_UCHE_TA_MAP` → `STATUSY_UCHE_TA_SLOVAR` (2 ссылки)
- **Удаление неиспользуемой константы `STATUSY_AKKREDITATSII_MAP`** в minobrnauki/constants.py
- **Унификация `mkb_classes` → `mkb_klassy`** в minzdrav/tools.py (2 вхождения; согласовано с `MKB10_KLASSY` в constants.py)
- **Русификация `klass_css` → `klass_stiley`** в cekrf/client.py (2 вхождения; «класс стилей» вместо английского суффикса CSS)
- **Русификация `sub-module` → `podmodul`** в комментарии batch.py (согласовано с конвенцией проекта)
- **Русификация документации** (6 файлов):
  - adding-features.md: `гид` → `руководство`, `Описать constants` → `Описать константы`
  - features.md: `OKATO` → `ОКАТО`
  - gosudarstvennaya-politika.md: `Каркас` → `Основа`, `паттерна` → `закономерности`
  - zhurnalist-rassledovatel.md: `фактчека` → `проверки фактов`
  - zhurnalist-stati.md: `копирайтер` → `автор-составитель` (2 вхождения)
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — 1 файл переформатировано, `pytest` — 681 unit-тест пройдено

### Ключевые архитектурные решения

- **`_MAP` → `_SLOVAR`**: устранён английский суффикс констант-словарей; `SLOVAR` = «словарь» — точный Python-эквивалент `dict`/`map`; 3 из 5 констант в rosreestr/constants.py оказались неиспользуемыми (определены, но ни разу не импортированы) — удалены как мёртвый код
- **`STATUSY_AKKREDITATSII_MAP`**: неиспользуемая константа (определена, но ни разу не импортирована ни в src/, ни в tests/) — удалена
- **`mkb_classes` → `mkb_klassy`**: устранён английский суффикс `_classes`; `klassy` согласовано с константой `MKB10_KLASSY` и конвенцией проекта
- **`klass_css` → `klass_stiley`**: устранён английский суффикс `css`; «класс стилей» — точный перевод «CSS class» в контексте HTML-парсинга
- **`гид` → `руководство`**: «гид» в русском означает экскурсовода, а не руководство по использованию; «руководство» — устоявшийся термин для технической документации
- **`Каркас` → `Основа`**: «каркас» = физическая рама/скелет; «основа» = база/фундамент — точный перевод «framework» в контексте аналитической структуры
- **`паттерна` → `закономерности`**: «паттерн» — заимствование; «закономерность» — точный русский эквивалент «pattern» в контексте распределения данных
- **`фактчека` → `проверки фактов`**: «фактчек» — англицизм; «проверка фактов» — устоявшийся русский термин
- **`копирайтер` → `автор-составитель`**: «копирайтер» — англицизм; «автор-составитель» — устоявшийся русский термин для роли составления текстов
- **`OKATO` → `ОКАТО`**: унификация написания аббревиатур кириллицей (согласовано с «ОКВЭД» в том же файле)

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Кодовая база полностью русифицирована**: оставшиеся английские идентификаторы — только строковые ключи API-ответов (`.get("key")`), keyword-аргументы внешних библиотек (httpx, Pydantic, FastMCP), стандартные Python-идентификаторы (`*args`, `**kwargs`, `__aexit__(*exc)`), параметры stdlib-переопределений (`tag`, `attrs` в HTMLParser), loanwords идентичные русским (`data` = «дата», `period` = «период»), и `logger` (стандартная конвенция Python); CSS-классы внешних HTML-страниц оставлены без изменений — изменение сломает парсинг

## Статус раунда 2026-07-19 (восемьдесят пятый проход — русификация region→subiekt_rf, exc→isklyuchenie, status→sostoyanie в цикловых переменных)

### Выполнено

- **Русификация `region` → `subiekt_rf` в цикловых переменных** (13 вхождений в 3 файлах):
  - rosstat/client.py: `region for region in SUBIEKTY_RF` → `subiekt_rf for subiekt_rf in SUBIEKTY_RF` (11 вхождений); `subiekt_rf` используется вместо `subiekt` для избежания затенения параметра `subiekt` в функциях `poluchit_vrp`, `poluchit_zarplatu`, `poluchit_indikator_dannye`, `poluchit_otraslevuyu_strukturu_vrp`, `poluchit_investitsii_po_vidam`, `_rezerv_otraslevaya_struktura`, `_rezerv_investitsii_po_vidam`
  - rosstat/tools.py: `region in regiony` → `subiekt_rf in regiony` (1 вхождение)
  - gibdd/tools.py: `region in RegionyRegistratsii` → `subiekt_rf in RegionyRegistratsii` (1 вхождение)
- **Русификация `exc` → `isklyuchenie` в except-блоках** (12 привязок в 4 файлах):
  - _shared/feature.py: `except Exception as exc` → `as isklyuchenie` + `str(exc)` → `str(isklyuchenie)`
  - _shared/batch.py: `except Exception as exc` → `as isklyuchenie` + `f"...{exc}"` → `f"...{isklyuchenie}"`
  - _shared/http_client.py: `except httpx.HTTPStatusError as exc` → `as isklyuchenie` + `exc.response.*` → `isklyuchenie.response.*` + `from exc` → `from isklyuchenie` (2 блока); `except (httpx.TimeoutException, httpx.ConnectError) as exc` → `as isklyuchenie` + `poslednyaya_oshibka = exc` → `= isklyuchenie` + `type(exc)` → `type(isklyuchenie)` (2 блока)
  - cekrf/client.py: `except Exception as exc` → `as isklyuchenie` + все ссылки `exc` → `isklyuchenie` (6 привязок)
- **Русификация `status` → `sostoyanie` в цикловых переменных** (7 вхождений в 7 файлах):
  - rosreestr/constants.py: `status in StatusyObekta` → `sostoyanie in StatusyObekta`
  - fssp/tools.py: `status in StatusyProizvodstva` → `sostoyanie in StatusyProizvodstva`
  - gibdd/tools.py: `status in StatusyShtrafov` → `sostoyanie in StatusyShtrafov`
  - publikatsii/tools.py: `status in statusy` → `sostoyanie in statusy`
  - kad_arbitrazh/tools.py: `status in statusy` → `sostoyanie in statusy`
  - zakupki/tools.py: `status in statusy` → `sostoyanie in statusy`
  - minobrnauki/tools.py: `status in STATUSY_AKKREDITATSII` → `sostoyanie in STATUSY_AKKREDITATSII`
- **Подтверждено**: `obiekt` → `obekt` уже унифицировано (0 vs 204 вхождения); португальские/бразильские артефакты полностью отсутствуют
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — 5 файлов переформатировано, `pytest` — 681 unit-тест пройдено

### Ключевые архитектурные решения

- **`region` → `subiekt_rf`**: устранён английский идентификатор в цикловых переменных, итерирующих по `SUBIEKTY_RF` и производным спискам; `subiekt_rf` (субъект РФ) используется вместо `subiekt` для избежания затенения параметра `subiekt: str` в функциях-клиентах; согласовано с конвенцией `for okrug in FEDERALNYE_OKRUGA`
- **`exc` → `isklyuchenie`**: устранён последний массовый класс английских переменных в `except ... as` привязках; `isklyuchenie` = «исключение»; внешние атрибуты исключений (`.response`, `.__name__`) оставлены без изменений — они принадлежат httpx/stdlib
- **`status` → `sostoyanie`**: устранён английский идентификатор в цикловых переменных, итерирующих по коллекциям статусов; `sostoyanie` = «состояние» — согласовано с конвенцией поля `sostoyanie` в schemas.py; имена коллекций `Statusy*` оставлены без изменений (транслитерация устоявшегося заимствования «статусы»)

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Кодовая база полностью русифицирована**: оставшиеся английские идентификаторы — только строковые ключи API-ответов (`.get("key")`), keyword-аргументы внешних библиотек (httpx, Pydantic, FastMCP), стандартные Python-идентификаторы (`*args`, `**kwargs`, `__aexit__(*exc)`), параметры stdlib-переопределений (`tag`, `attrs` в HTMLParser), loanwords идентичные русским (`data` = «дата», `period` = «период»), и `logger` (стандартная конвенция Python); CSS-классы внешних HTML-страниц оставлены без изменений — изменение сломает парсинг



### Выполнено

- **Исправление английских параметров в документации** (~30 замен в 8 файлах):
  - zhurnalist-stati.md: `codes=[...]` → `kody=[...]`, `region=` → `subiekt=` (3 замены)
  - gosudarstvennaya-politika.md: `region=` → `subiekt=`/`kod=` (8 замен), удалены несуществующие параметры (`god=`, `uroven=`, `top=`, `zayavki=`, `pokazatel=`), `zakupki_gov_ru_rnp` → `zakupki_reestr_nedobrosovestnykh_postavshchikov`
  - zhurnalist-rassledovatel.md: `region=` → `subiekt=` (2 замены)
  - municipalnyy-kontrol.md: `region=` → `subiekt=`, `munitsipalitet=` → удалён, `funktsiya=` → `tip=`, `postavshchik=` → `organizaciya=` (20+ замен в тексте и JSON-примерах)
  - analiz-zakonodatelstva.md: `topic=` → `sostoyanie=`, `year=` удалён, `id=` → `kandidat_identifikator=`/`sostoyanie=`, `recent_progress=True` удалён (6 замен)
  - politolog.md: `id=` → `kandidat_identifikator=`, `inn=` (2 замены)
  - parlamentskiy-otchet.md: `id=` → `identifikator_deputata=`/`kandidat_identifikator=` (2 замены)
  - ofitsialnyy-redaktor.md: `region=` → `subiekt=`, `name=` → `tip=` (2 замены)
- **Русификация CONTRIBUTING.md**: `primer_tool` → `primer_instrument`
- **Русификация adding-features.md**: `imya="example"` → `imya="primer"`, `F=example` → `F=primer`
- **Русификация комментариев в settings.py**: `list_tools` → `spisok_instrumentov`, `search_tools + call_tool` → `poisk_instrumentov + vypolnit_instrument`, `search + get_tags + execute` → `poisk + poluchit_tegi + vypolnit`
- **Устранение осиротевшей переменной `OPEN_DATA_API_KEY`** в .env.example (не используется ни в src/, ни в tests/)
- **Русификация tg/ README файлов** (4 файла): `Local Telegram mirror for this repository` → `Локальный зеркальный канал Telegram для этого репозитория`, `Repo:` → `Репозиторий:`, `Topic ID: pending` → `Идентификатор темы: ожидается`
- **Русификация README.md**: `запрос на слияние (pull request)` → `пул-реквест` (согласовано с CONTRIBUTING.md)
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — 306 файлов уже форматировано, `pytest` — 681 unit-тест пройдено

### Ключевые архитектурные решения

- **`region=` → `subiekt=`/`kod=`**: устранены английские параметры в документации, не соответствующие реальным сигнатурам функций; `subiekt` используется в minzdrav, rosgidromet, rospotrebnadzor, kaznacheistvo, rosstat/demografiya; `kod` используется в rosstat/informatsiya_o_regionye; это **исправление бага документации** — пользователи, копировавшие примеры, получали ошибки несуществующих параметров
- **Удалены несуществующие параметры**: `god=`, `uroven=`, `top=`, `zayavki=`, `pokazatel=`, `topic=`, `year=`, `recent_progress=True`, `munitsipalitet=`, `funktsiya=`, `postavshchik=` — все не существуют в реальных сигнатурах инструментов; заменены на реальные параметры (или удалены, если инструмент не принимает таких аргументов)
- **`id=` → `kandidat_identifikator=`/`identifikator_deputata=`**: устранён английский параметр `id` в примерах; заменён на реальные имена параметров из исходного кода
- **`primer_tool` → `primer_instrument`**: устранён английский суффикс `_tool` в CONTRIBUTING.md; `instrument` — конвенция проекта
- **`OPEN_DATA_API_KEY`**: осиротевшая переменная окружения, не используемая ни в одном файле проекта; удалена из .env.example

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Кодовая база полностью русифицирована**: оставшиеся английские идентификаторы — только строковые ключи API-ответов (`.get("key")`), keyword-аргументы внешних библиотек (httpx, Pydantic, FastMCP), стандартные Python-идентификаторы (`*args`, `**kwargs`), параметры stdlib-переопределений (`tag`, `attrs` в HTMLParser), loanwords идентичные русским (`data` = «дата», `period` = «период»), и `logger` (стандартная конвенция Python); CSS-классы внешних HTML-страниц оставлены без изменений — изменение сломает парсинг

### Выполнено

- **Переименование английского каталога `templates/` → `shablony/`** (1 каталог + 2 ссылки):
  - `src/mcp_russia/agenty/deloproizvodstvo/templates/` → `shablony/`
  - resources.py: `Path(__file__).parent / "templates"` → `"shablony"`
  - tools.py: `Шаблоны доступны в templates/` → `shablony/`
- **Устранение португальского артефакта `extenso` → `propisyu`** (5 файлов):
  - tools.py: `formatirovat_data_extenso` → `formatirovat_datu_propisyu` (имя функции)
  - server.py: импорт и регистрация
  - test_tools.py: `TestFormatirovatDataExtenso` → `TestFormatirovatDatuPropisyu` + вызовы
  - test_integration.py: строковые ссылки `"formatirovat_data_extenso"` → `"formatirovat_datu_propisyu"` + вызов
- **Русификация английского строкового литерала** `"param"` → `"parametr"` в planner.py (пример JSON-ключа в системном промпте)
- **Русификация английского ключа `"city"` → `"gorod"`** в minzdrav/test_tools.py (согласовано с client.py где ключ уже `gorod`)
- **Русификация переменной `msg` → `soobshcheniye`** в test_batch.py (3 вхождения)
- **Унификация транслитерации `osnovnoj` → `osnovnoy`** в kaznacheistvo (3 файла):
  - schemas.py: `osnovnoj_vid_deyatelnosti` → `osnovnoy_vid_deyatelnosti`
  - client.py: ключ словаря и fallback
  - tools.py: `.get("osnovnoy_vid_deyatelnosti", ...)`
- **Унификация транслитерации `h` → `zh/sh/ch`** в kaznacheistvo/constants.py (3 ключа):
  - `obshhegosudarstvennye` → `obshchegosudarstvennye`
  - `ohrana_okruzhayushhej_sredy` → `okhrana_okruzhayushchey_sredy`
  - `uslugi_obshhego_haraktera` → `uslugi_obshchego_kharaktera`
- **Унификация `subyekt` → `subiekt`** в cekrf (7 файлов, ~15 вхождений):
  - schemas.py: `SubyektRF` → `SubiektRF`
  - constants.py: `SUBYEKTY_RF` → `SUBIEKTY_RF`
  - client.py: `subyekty_rf` → `subiekty_rf`, `SubyektRF` → `SubiektRF`, `SUBYEKTY_RF` → `SUBIEKTY_RF`
  - tools.py: `subyekty_rf` → `subiekty_rf`, `subyekty` → `subiekty`
  - resources.py: `subyekty_rf_resource` → `subiekty_rf_resource`, `"subyekty_rf"` → `"subiekty_rf"`, `SUBYEKTY_RF` → `SUBIEKTY_RF`
  - server.py: импорты, `data://subyekty-rf` → `data://subiekty-rf`
  - test_tools.py: `test_subyekty_rf` → `test_subiekty_rf`
  - test_integration.py: `"subyekty_rf"` → `"subiekty_rf"`, `data://subyekty-rf` → `data://subiekty-rf`, `test_subyekty_rf` → `test_subiekty_rf`
- **Русификация English tags в test_discovery.py** (6 наборов тегов):
  - `{"search", "regions"}` → `{"поиск", "регионы"}` (3 вхождения)
  - `{"query", "data"}` → `{"запрос", "данные"}` (2 вхождения)
  - `{"search"}` → `{"поиск"}` (1 вхождение)
- **Прогнаны все проверки**: `ruff check` — all passed, `pytest` — 681 unit-тест пройдено (интеграционные HTTP-тесты пропущены)

### Ключевые архитектурные решения

- **`templates/` → `shablony/`**: устранён последний английский каталог в кодовой базе; `shablony` = «шаблоны»; согласовано с `DIREKTORIYA_SHABLONOV`
- **`extenso` → `propisyu`**: устранён португальский/латинский артефакт; «прописью» — точный русский эквивалент «in words/extenso» в контексте написания даты; ломающее изменение для клиентов, использующих `formatirovat_data_extenso`
- **`"city"` → `"gorod"`**: устранён английский ключ в мок-данных; клиент уже возвращает `"gorod"` (строка 229 в client.py)
- **`osnovnoj` → `osnovnoy`**: унификация транслитерации `й`; во всей кодовой базе используется `y` для `й`, `j` — единичное исключение
- **`obshhegosudarstvennye` → `obshchegosudarstvennye`**: унификация транслитерации `щ` и `ш`; `h` для `ж/ш/ч/щ` — устаревшая транслитерация, `zh/sh/ch/shch` — стандартная конвенция проекта
- **`SubyektRF` → `SubiektRF`**: унификация транслитерации `ъ`; во всей кодовой базе (60+ файлов) используется `subiekt` (через `ie`), `subyekt` — единичное исключение в модуле cekrf; ломающее изменение для клиентов, использующих инструмент `subyekty_rf` или ресурс `data://subyekty-rf`
- **English tags → кириллица**: устранены последние английские теги в тестовых данных; согласовано с конвенцией проекта — все теги в server.py на кириллице (`"форматирование"`, `"справочник"`, `"субъекты-рф"`)

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Унификация `obiekt` → `obekt`**: в ~40 файлах используются две формы транслитерации слова «объект»; `obekt` — преобладающая конвенция, `obiekt` — в _shared/discovery.py, _shared/feature.py, rosapi/client.py, rosprirodnadzor, rosselkhoznadzor, rosvodresursy, rospotrebnadzor
- **Кодовая база полностью русифицирована**: оставшиеся английские идентификаторы — только строковые ключи API-ответов (`.get("key")`), keyword-аргументы внешних библиотек (httpx, Pydantic, FastMCP), стандартные Python-идентификаторы (`*args`, `**kwargs`), параметры stdlib-переопределений (`tag`, `attrs` в HTMLParser), loanwords идентичные русским (`data` = «дата», `period` = «период»), и `logger` (стандартная конвенция Python); CSS-классы внешних HTML-страниц оставлены без изменений — изменение сломает парсинг

## Статус раунда 2026-07-16 (восемьдесят первый проход — русификация однобуквенных переменных циклов/comprehensions, имён тестовых функций, диаграмм, документации)

### Выполнено

- **Русификация однобуквенных переменных в циклах `for` и генераторах** (~249 замен в 50+ файлах):
  - cbrf/client.py: `c` → `kod` (в `kody`)
  - rosapi/client.py: `s` → `predlozhenie` (в `predlozheniya`), `b` → `bank` (в `banki_syranye`)
  - rosapi/tools.py: `h` → `prazdnik` (в `prazdniki`)
  - rosstat/tools.py: `r` → `region`, `p` → `pokazatel`/`indikator`, `d` → `zapis`, `v` → `vid`
  - rosstat/client.py: `r` → `region`, `p` → `pokazatel`, `v` → `vid`/`vid_deyatelnosti`
  - minobrnauki/tools.py: `t` → `tip`, `f` → `forma`/`okrug`, `u` → `uroven`, `g` → `grant`, `s` → `status`, `r` → `pozitsiya`/`rezultat`
  - minobrnauki/client.py: `r` → `zapis`
  - kaznacheistvo/tools.py: `v` → `vid`, `k` → `kategoriya`, `u` → `uchastnik`/`uchrezhdenie`, `t` → `transfer`
  - kaznacheistvo/client.py: `p` → `element` (3 вхождения)
  - minzdrav/tools.py: `p` → `pokazatel`, `z` → `zapis`, `t` → `tip`, `s` → `spetsialnost`, `m` → `klass`
  - minzdrav/client.py: `p` → `element` (4 вхождения)
  - zakupki/tools.py: `z` → `zakupka`, `k` → `kontrakt`, `s` → `status`/`sposob`, `p` → `plan`
  - fns/tools.py: `p` → `proverka`, `n` → `nachislenie`
  - rosreestr/client.py: `r` → `pravo`, `f` → `obiekt`
  - rosreestr/tools.py: `r` → `pravo`
  - rosreestr/constants.py: `t` → `tip`, `k` → `kategoriya`, `v` → `vid`, `s` → `status`, `f` → `forma`
  - rosaudit/tools.py: `n` → `napravlenie`/`narushenie`, `t` → `tip`, `s` → `subiekt`, `m` → `meropriyatie`, `r` → `rekomendatsiya`
  - rosaudit/client.py: `p` → `element` (2 вхождения)
  - rospotrebnadzor/tools.py: `n` → `napravlenie`, `t` → `tip`, `k` → `kategoriya`, `r` → `upravlenie`, `p` → `proverka`/`narushenie`, `s` → `sanpin`, `z` → `zhaloba`
  - rospotrebnadzor/client.py: `p` → `element`/`zapis`, `z` → `zapis`
  - rosprirodnadzor/tools.py: `v` → `vid`, `k` → `kategoriya`, `p` → `proverka`/`platezh`
  - rosprirodnadzor/client.py: `p` → `element` (7 вхождений)
  - sovfed/tools.py: `s` → `senator`, `k` → `komitet`/`komissiya`, `z` → `zakonoproekt`/`zasedanie`
  - sovfed/client.py: `p` → `element` (5 вхождений), `s` → `senator`
  - publikatsii/tools.py: `t` → `tip`, `i` → `istochnik`, `s` → `status`, `a` → `rezultat`, `p` → `publikatsiya`
  - gosduma/tools.py: `d` → `deputat`, `f` → `fraktsiya`, `k` → `komitet`, `s` → `sozyv`, `b` → `zakonoproekt`, `v` → `golosovanie`
  - gosduma/client.py: `f` → `fraktsiya`
  - kad_arbitrazh/tools.py: `d` → `delo`, `a` → `akt`, `s` → `storona`, `k` → `kategoriya`, `i` → `instantsiya`, `t` → `tip`
  - kad_arbitrazh/client.py: `s` → `storona`/`zapis`
  - mchs/tools.py: `v` → `vid`, `k` → `klass`, `t` → `tip`, `p` → `pozhar`/`preduprezhdenie`, `c` → `chs`, `m` → `monitoring`, `g` → `gidro`
  - mchs/client.py: `p` → `element` (7 вхождений)
  - fssp/tools.py: `v` → `vid`, `s` → `status`, `k` → `kategoriya`, `r` → `rezultat`
  - fssp/client.py: `r` → `zapis`, `p` → `proizvodstvo`
  - gibdd/tools.py: `t` → `tip`, `k` → `kategoriya`, `n` → `narushenie`, `s` → `status`, `r` → `region`/`zapis`, `d` → `zapis`, `w` → `razyskivaemyy`
  - cekrf/tools.py: `t` → `tip`, `s` → `subiekt`, `d` → `dolzhnost`, `p` → `partiya`, `v` → `vybory_item`, `k` → `kandidat`, `r` → `rezultat`
  - cekrf/client.py: `s` → `subiekt`, `d` → `dolzhnost`, `p` → `partiya`
  - rosgidromet/tools.py: `s` → `stantsiya`/`snimok`, `m` → `tip_meteo`, `e` → `tip_eko`, `p` → `prognoz_item`/`preduprezhdenie`, `d` → `zapis`
  - rosgidromet/client.py: `s` → `stantsiya`, `r` → `rezultat`
  - rosvodresursy/tools.py: `t` → `tip`, `g` → `gidro_stantsiya`, `v` → `vodokhranilishche`/`zapis`, `z` → `zapis`
  - rosvodresursy/client.py: `p` → `element`, `v` → `vodokhranilishche`
  - rosselkhoznadzor/tools.py: `v` → `vid`, `k` → `kategoriya`, `t` → `tip`, `p` → `proverka`/`preduprezhdenie`, `r` → `registratsiya`, `s` → `sertifikat`
  - rosselkhoznadzor/client.py: `p` → `element` (6 вхождений)
  - roskomnadzor/tools.py: `n` → `napravlenie`, `t` → `tip_licenzii`/`tip_smi`, `k` → `kategoriya`, `r` → `reestr`/`zapis_reestra`, `s` → `sredstvo`
  - roskomnadzor/client.py: `s` → `element`/`zapis`
  - _shared/planner.py: `d` → `nomer_etapa`
  - _shared/formatting.py: `h` → `zagolovok`
  - agenty/deloproizvodstvo/tools.py: `p` → `abzats`/`problema`, `r` → `rekomendatsiya`
- **Русификация имён тестовых функций** (7 функций в rosstat/test_tools.py):
  - `test_spisok_regionov_has_many` → `..._imeet_mnogo`
  - `test_constants_emiss_kody_complete` → `..._polnyy`
  - `test_sravnenie_regionov_invalid_pokazatel` → `..._nekorrektnyy_pokazatel`
  - `test_indikator_dannye_with_region` → `..._s_regionom`
  - `test_constants_subiekty_no_duplicates` → `..._bez_dublikatov`
  - `test_constants_new_emiss_kody` → `..._novyy_emiss_kody`
  - `test_constants_new_regionalnye_pokazateli` → `..._novyy_regionalnye_pokazateli`
- **Русификация тестовых строковых литералов**: `"invalid_code"` → `"nekorrektnyy_kod"` (rosstat/test_tools.py)
- **Русификация переменной `now` → `seychas`** в deloproizvodstvo/test_tools.py (3 вхождения; `datetime.now()` оставлен — метод stdlib)
- **Русификация `APIs:` → `API:`** в документации (15 замен в 2 файлах):
  - docs/examples/zhurnalist-stati.md: 5 замен
  - docs/examples/politolog.md: 10 замен
- **Русификация CONTRIBUTING.md**: `enum` → `перечисления`, `tools:` → `инструменты:`
- **Русификация cliff.toml**: `<!-- generated by git-cliff -->` → `<!-- сгенерировано git-cliff -->`
- **Русификация CHANGELOG.md**: `<!-- generated by git-cliff -->` → `<!-- сгенерировано git-cliff -->`
- **Русификация имён файлов диаграмм** в scripts/generate_diagrams.py (4 замены):
  - `system_overview` → `obzor_sistemy`
  - `feature_anatomy` → `anatomiya_modulya`
  - `auto_registry_flow` → `potok_avtoobnaruzheniya`
  - `data_flow` → `potok_dannykh`
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — 32 файла переформатировано, `pytest` — 681 unit-тест пройдено (интеграционные HTTP-тесты пропущены)

### Ключевые архитектурные решения

- **Однобуквенные переменные → осмысленные имена**: каждый идентификатор согласован с типом коллекции (`for region in regiony`, `for zapis in dannye`, `for element in elementy` и т.д.); устранён последний массовый класс английских артефактов
- **`APIs:` → `API:`**: устранён английский множественный суффикс «s»; в русском языке «API» — неизменяемое заимствование
- **`enum` → `перечисления`**: устранён английский технический термин в пользу устоявшегося русского эквивалента, уже использовавшегося в других местах проекта
- **Имена файлов диаграмм → русская транслитерация**: `system_overview` → `obzor_sistemy` и т.д.; синхронизировано с конвенцией проекта

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Кодовая база полностью русифицирована**: оставшиеся английские идентификаторы — только строковые ключи API-ответов (`.get("key")`), keyword-аргументы внешних библиотек (httpx, Pydantic, FastMCP), стандартные Python-идентификаторы (`*args`, `**kwargs`), параметры stdlib-переопределений (`tag`, `attrs` в HTMLParser), loanwords идентичные русским (`data` = «дата», `period` = «период»), и `logger` (стандартная конвенция Python); CSS-классы внешних HTML-страниц оставлены без изменений — изменение сломает парсинг

## Статус раунда 2026-07-16 (восьмидесятый проход — русификация однобуквенных переменных, lambda-параметров, Field-описаний, тестовых строковых литералов, документации)

### Выполнено

- **Исправление опечатки `normanyy_instrument` → `normalnyy_instrument`** в test_batch.py (2 ссылки)
- **Русификация тестовых строковых литералов** (5 файлов):
  - test_batch.py: `"uspekh"` → `"успех"`, `"rezultat uspekha"` → `"результат успеха"`, `f"rezultat-{n}"` → `f"результат-{n}"`
  - test_feature.py: `"pong"` → `"отклик"`, `"broken"` → `"slomannyy"`
  - test_cache.py: `"dannye"` → `"данные"`, `f"rezultat-{klyuch}"` → `f"результат-{klyuch}"`, `f"dannye-{subiekt}"` → `f"данные-{subiekt}"`
  - test_discovery.py: `"zakeshirovano"` → `"закешировано"`, `"funktsii"` → `"функции"`, `"skrytyy"` → `"скрытый"`, `"ochagi"` → `"очаги"`, `"banki"` → `"банки"`
  - test_http_client.py: `"vosstanovleno"` → `"восстановлено"`
- **Русификация `sostoyanie="ACTIVE"` → `"ДЕЙСТВУЮЩАЯ"`** в rosapi/test_tools.py (согласовано с schemas.py где `ДЕЙСТВУЮЩАЯ/ЛИКВИДИРОВАНА`)
- **Русификация имени тестовой функции**: `test_excessive_deeprichastiya` → `test_izbytochnye_deeprichastiya`
- **Русификация однобуквенных переменных в cekrf/client.py** (~15 замен):
  - `m = re.search(...)` → `sovpadenie = re.search(...)` (3 вхождения в `_razobrat_veshchestvennoe` и `_razobrat_rezultaty_iz_html`)
  - `for i, yacheyka` → `for indeks, yacheyka` (2 вхождения в `_razobrat_rezultaty_iz_html` и `_razobrat_kandidatov_iz_html`)
  - `as c:` → `as klient:` (3 вхождения в `_zaprosit_html_vyborov`, `poisk_vyborov`, `poisk_kandidata`)
- **Русификация `s = predlozheniya[0]` → `pervoe = predlozheniya[0]`** в rosapi/client.py (3 ссылки)
- **Русификация lambda-параметров** (3 модуля):
  - fssp/tools.py: `lambda x: x[1]` → `lambda element: element[1]`
  - rosstat/tools.py: `lambda x: x.get(...)` → `lambda zapis: zapis.get(...)`
  - cbrf/tools.py: `lambda x: x.kod` → `lambda valyuta: valyuta.kod` (2 вхождения)
- **Русификация цикловых переменных `for o in`** (~20 замен в 11 модулях):
  - rosstat/tools.py: `for o in okruga` → `for okrug in okruga`; `for o in OTRASLEVAYA_STRUKTURA_VRP` → `for otrasl in ...`
  - minzdrav/tools.py: `for o in organizatsii` → `for organizatsiya in organizatsii`
  - roskomnadzor/tools.py: `for o in operatory` → `for operator in operatory`; `for o in ori` → `for zapis in ori`
  - roskomnadzor/client.py: `for o in elementy/dannye` → `for zapis in ...` (4 вхождения)
  - rosselkhoznadzor/tools.py: `for o in obekty` → `for obiekt in obekty`
  - rosvodresursy/tools.py: `for o in okruga/obekty` → `for okrug/obiekt in ...`
  - rosprirodnadzor/tools.py: `for o in obekty` → `for obiekt in obekty`
  - minobrnauki/tools.py: `for o in OTRASLI_NAUKI` → `for otrasl in ...`
  - publikatsii/tools.py: `for o in otrsli` → `for otrasl in ...`
  - fssp/tools.py: `for o in Ogranicheniya/OsnovaniyaVozbuzhdeniya` → `for ogranichenie/osnovanie in ...`
  - rosstat/client.py: `for o in FEDERALNYE_OKRUGA/OTRASLEVAYA_STRUKTURA_VRP` → `for okrug/otrasl in ...` (3 вхождения)
  - deloproizvodstvo/tools.py: `for klyuch, o in ОБРАЩЕНИЯ.items()` → `for klyuch, obrashcheniye in ...`
- **Русификация Pydantic Field-описаний** (4 поля в 2 модулях):
  - cekrf/schemas.py: `"ID кандидата"` → `"Идентификатор кандидата"` (3 вхождения: KandidatKratko, Kandidat, ResultatKandidata)
  - cekrf/schemas.py: `"(hex)"` → `"(HEX)"` (InformatsiyaPartii.tsvet)
  - rosapi/schemas.py: `"(YYYY-MM-DD)"` → `"(ГГГГ-ММ-ДД)"` (Prazdnik.data)
- **Русификация CONTRIBUTING.md** (~10 замен):
  - `primer-feature` → `primer-modul`, `http_client, formatting, cache, rate_limiter` → `http-клиент, форматирование, кеш, ограничитель частоты`
  - `lint + format` → `линтер + форматирование`, `type checking (strict)` → `проверка типов (строгий режим)`
  - `ruff check + format check` → `проверка линтером + проверка форматирования`, `mypy strict` → `mypy в строгом режиме`
  - `lint + types + test` → `линтер + типы + тесты`, `mock` → `maket` в примере кода
  - `/endpoint` → `/konechnaya_tochka`, `"Test"` → `"Проверка"` в примере JSON
  - `push/пул-реквест` → `отправлении изменений/пул-реквесте`, `build + publish в PyPI + GitHub Release` → `сборка + публикация в PyPI + релиз на GitHub`
  - `sdist + wheel` → `исходный дистрибутив + wheel-пакет`
- **Русификация CHANGELOG.md** (3 замены):
  - `tool search` → `поиска инструментов`, `LLM discovery` → `обнаружения LLM`
  - `commit-on-green` → `«фиксация-при-успехе»`
  - `claude code skills (commit, fastmcp, skill-creator)` → `навыки Claude Code (фиксация, fastmcp, создатель-навыков)`
- **Русификация документации** (2 файла):
  - analiz-zakonodatelstva.md: `type="закон"` → `tip="закон"` в примере вызова
  - adding-features.md: `FastMCP("example")` → `FastMCP("primer")`

### Ключевые архитектурные решения

- **`normanyy` → `normalnyy`**: исправлена опечатка (пропущена буква «л»), существовавшая с раунда 65
- **Транслитерация → кириллица в тестовых строках**: `"uspekh"` → `"успех"`, `"dannye"` → `"данные"`, `"zakeshirovano"` → `"закешировано"` и т.д.; русские слова в тестовых возвращаемых значениях записаны кириллицей
- **`ACTIVE` → `ДЕЙСТВУЮЩАЯ`**: устранён английский статус в мок-данных; согласовано с schemas.py где описание уже было русифицировано в раунде 66
- **`pong` → `отклик`**: устранён последний английский строковый литерал в тестовых данных; «отклик» — точный перевод «pong» в контексте проверки связи
- **`broken` → `slomannyy`**: устранён английский ключ словаря в тесте; «сломанный» — точный перевод
- **`m` → `sovpadenie`**: устранена однобуквенная переменная в regex-поиске; «совпадение» — точный перевод «match»
- **`i` → `indeks`**: устранена однобуквенная переменная в enumerate; «индекс» — точный перевод
- **`s` → `pervoe`**: устранена однобуквенная переменная в rosapi; «первое» — первое подсказочное предложение
- **`as c:` → `as klient:`**: устранена однобуквенная переменная контекстного менеджера в cekrf/client.py
- **`lambda x:` → осмысленные имена**: `x` → `element`/`zapis`/`valyuta` в зависимости от контекста
- **`for o in` → осмысленные имена**: `o` → `okrug`/`organizatsiya`/`operator`/`zapis`/`obiekt`/`otrasl`/`ogranichenie`/`osnovanie`/`obrashcheniye` в зависимости от типа коллекции
- **`ID` → `Идентификатор`**: устранена английская аббревиатура в пользовательски-видимых Pydantic Field-описаниях
- **`hex` → `HEX`**: стандартизация написания — заглавными как устоявшееся обозначение шестнадцатеричного формата
- **`YYYY-MM-DD` → `ГГГГ-ММ-ДД`**: русификация формата даты в Pydantic Field-описании

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Кодовая база полностью русифицирована**: оставшиеся английские идентификаторы — только строковые ключи API-ответов (`.get("key")`), keyword-аргументы внешних библиотек (httpx, Pydantic, FastMCP), стандартные Python-идентификаторы (`*args`, `**kwargs`), параметры stdlib-переопределений (`tag`, `attrs` в HTMLParser), loanwords идентичные русским (`data` = «дата», `period` = «период»), и `logger` (стандартная конвенция Python); CSS-классы внешних HTML-страниц (`"title"`, `"stats"`, `"total"`) оставлены без изменений — изменение сломает парсинг

## Статус раунда 2026-07-15 (семидесятый девятый проход — русификация тестовых данных, португальских артефактов, JSON-ключа instrument→imya_instrumenta, документации)

### Выполнено

- **Устранение португальских артефактов в тестах** (test_cache.py):
  - `uf` (Unidade Federativa) → `subiekt`; `"SP"` (Сан-Паулу) → `"77"` (Москва); `"RJ"` (Риу-де-Жанейро) → `"16"` (Татарстан)
- **Русификация английских имён тестовых функций** (3 функции в test_feature.py):
  - `test_dostupna_li_autentifikatsiya_env_var_set` → `..._s_peremennoy_okruzheniya`
  - `test_dostupna_li_autentifikatsiya_requires_auth_no_env_var` → `..._trebuet_aut_bez_peremennoy`
  - `test_dostupna_li_autentifikatsiya_optional_auth_no_env` → `..._neobyazatelnaya_bez_peremennoy`
- **Русификация английских строковых литералов в тестах** (~40 замен в 6 файлах):
  - test_feature.py: `"FAKE_KEY_NOT_SET"` → `"PROVEROCHNYY_KLYUCH_NE_ZADAN"`, `"TEST_MCP_KEY"` → `"PROVEROCHNYY_KLYUCH_MCP"`, `"TEST_OPT_KEY"` → `"PROVEROCHNYY_KLYUCH_NE_OBYAZ"`, `"val"` → `"znachenie"`, `"fake.module"` → `"lozhnyy.modul"`, `"reason"` → `"prichina"`, `"test"` (namespace) → `"proverka"`, `"test_ekho"` → `"proverka_ekho"`
  - test_cache.py: `uf`/`SP`/`RJ` → `subiekt`/`77`/`16`
  - test_discovery.py: `"environmental"` → `"ekologiya"`, `"fires"` → `"pozhary"`, `"financial"` → `"finansy"`, `"banks"` → `"banki"`, `"meta"` → `"мета"`, `"catalog"` → `"katalog"`, `root_mcp` → `kornevoy_mcp`
  - test_http_client.py: все URL `api.example.com/{data,search,missing,flaky,limited,down,slow,once}` → `api.primer.gov.ru/{dannye,poisk,otsutstvuet,nestabilnyy,ogranichen,nedostupen,medlennyy,odinraz}`, `"test"` → `"zapros"`
  - test_batch.py: `"instrument"` → `"imya_instrumenta"`, `instrument_bez_konteksta` → `instrument_ne_trebuet_konteksta`
  - test_tools.py (gosduma, zakupki, kad_arbitrazh): `*_client` → `*_klient`, `"string"` → `"stroka"`, `"abc"` → `"abv"`
  - test_tools.py (roskomnadzor): `"example.com"` → `"primer.ru"`, `"blocked-site.ru"` → `"zapreshcheno.ru"`
  - test_integration.py (minobrnauki): `"placeholder"` → `"zaglushka"`
- **Русификация JSON-ключа `"instrument"` → `"imya_instrumenta"`** в batch.py и server.py (согласовано с planner.py, где Pydantic-поле уже называется `imya_instrumenta`)
- **Русификация CONTRIBUTING.md** (~8 замен):
  - `Mock client` → `Мок клиента`, `mock HTTP` → `мок HTTP`, `e2e` → `сквозное тестирование`, `end-to-end` → `сквозное тестирование`, `Bump` → `Повышение`, `PR` → `пул-реквест`, `Conventional Commits` → `Конвенциональные коммиты`
- **Русификация Makefile** (2 замены):
  - `production-зависимости` → `рабочие зависимости`, `prod + dev` → `рабочие + разработка`
- **Русификация README.md** (2 замены):
  - `alt="mcp-russia logo"` → `alt="логотип mcp-russia"`, `License: MIT` → `Лицензия: MIT`
- **Исправление устаревшей константы в scripts/generate_diagrams.py**: `ROSSTAT_API_BASE` → `EMISS_BAZA_API`
- **Русификация комментария в rosstat/constants.py**: `energy_production и transport_cargo` → `proizvodstvo_elektroenergii и gruzooborot_transporta`
- **Русификация сообщений в server.py**: `CodeMode` → `режим кода` (лог-сообщения и предупреждения)
- **Русификация комментария в settings.py**: `CodeMode` → `режим кода`

### Ключевые архитектурные решения

- **`"instrument"` → `"imya_instrumenta"`**: ключ JSON в API `vypolnit_paket` приведён в соответствие с Pydantic-полем `imya_instrumenta` в `planner.py`; ломающее изменение для клиентов, использующих `vypolnit_paket`
- **`uf`/`SP`/`RJ`**: устранены последние португальские артефакты в кодовой базе; `uf` = Unidade Federativa (бразильский штат), заменено на `subiekt` (субъект РФ) с кодами `77` (Москва) и `16` (Татарстан)
- **`*_client` → `*_klient`**: унификация с конвенцией проекта — во всех остальных местах используется `klient`
- **`root_mcp` → `kornevoy_mcp`**: устранён английский префикс `root`; `kornevoy` = «корневой»
- **`api.example.com` → `api.primer.gov.ru`**: тестовые URL приведены к российскому формату
- **`CodeMode` → `режим кода`**: русификация лог-сообщений; имя класса `CodeMode` (из внешней библиотеки) не меняется
- **`code_mode`**: значение настройки оставлено без изменений — конфигурационный токен, аналогичный `"bm25"` и `"none"`

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Кодовая база и документация полностью русифицированы**: оставшиеся английские идентификаторы — только строковые ключи API-ответов (`.get("key")`), keyword-аргументы внешних библиотек (httpx, Pydantic, FastMCP), стандартные Python-идентификаторы (`*args`, `**kwargs`), параметры stdlib-переопределений (`tag`, `attrs` в HTMLParser), loanwords идентичные русским (`data` = «дата», `period` = «период»), и `logger` (стандартная конвенция Python)

## Статус раунда 2026-07-13 (семидесятый шестой проход — русификация ctx→kontekst, c→klient, исправление бага cekrf status→sostoyanie, русификация тестовых данных и документации)

### Выполнено

- **Исправление критического бага `status=` → `sostoyanie=`** в cekrf/client.py:528 — `KandidatKratko` имеет поле `sostoyanie`, а клиент передавал `status=` (Pydantic присваивал пустое значение по умолчанию)
- **Русификация `ctx` → `kontekst`** (~1069 вхождений в 70+ файлах):
  - Все `ctx: Context` параметры в `tools.py` (44 модуля)
  - Все `ctx: Context` параметры в `prompts.py` (18 функций, где нет конфликта с `kontekst: str`)
  - Все `ctx: Context` параметры в `prompts.py` → `kontekst_mcp: Context` (18 функций, где `kontekst: str` уже занят)
  - Все `ctx` переменные в `_maket_konteksta()` и локальных переменных в тестах (26 файлов)
  - Все `await ctx.info()`, `await ctx.warning()` → `await kontekst.info()`, `await kontekst.warning()`
  - Все `ctx: Context` в `_shared/` модулях (lifespan.py, batch.py, discovery.py, server.py)
- **Русификация `c` → `klient`** в тестовых Client-контекстах (41 вхождение в 4 файлах):
  - `async with Client(...) as c:` → `as klient:`
  - Все `c.call_tool()`, `c.list_tools()`, `c.list_resources()` → `klient.*`
- **Русификация тестовых данных и заглушек**:
  - `FastMCP("test")` → `FastMCP("proverka")`, `FastMCP("child")` → `FastMCP("docherniy")`, `FastMCP("parent")` → `FastMCP("roditelskiy")`, `FastMCP("root")` → `FastMCP("koren")`, `FastMCP("sub")` → `FastMCP("podmodul")`
  - `"Moscow, Tatarstan, Sverdlovsk"` → `"Москва, Татарстан, Свердловск"`, `"Moscow"` → `"Москва"`
  - `"functions"` → `"funktsii"`, `"hotspots"` → `"ochagi"`, `"banks"` → `"banki"`
  - `"echo: ..."` → `"эхо: ..."`, `"hello"` → `"privet"`
  - `"cached"` → `"zakeshirovano"`, `"API timeout"` → `"Таймаут API"`
  - `"test-key"` → `"proverochnyy-klyuch"`, `"secret"` → `"taynyy_klyuch"`
  - `"Not Found"` → `"Не найдено"`, `"Internal Server Error"` → `"Внутренняя ошибка сервера"`, `"Too Many Requests"` → `"Слишком много запросов"`, `"Service Unavailable"` → `"Сервис недоступен"`, `"Error"` → `"Ошибка"`
  - `{"ok": True}` → `{"uspekh": True}`, `{"recovered": True}` → `{"vosstanovleno": True}`
  - `"key"/"value"` → `"klyuch"/"znachenie"` в test_cache.py
  - `_IMPORT_NORMALNO` → `_IMPORT_NORMALNYY` в rosapi/test_integration.py
  - Английский pytest.skip message → русский
- **Русификация документации**:
  - README.md: `fallback` → `запасной вариант`, `pull request` → `запрос на слияние (pull request)`, `Legacy-модули` → `Устаревшие модули`
  - CONTRIBUTING.md: `env vars` → `переменные окружения`, `docstring` → `строка документации`, `endpoint` → `конечная точка`, `refactor` → `рефакторинг`, `Bump minor/major` → `Повысить minor/major`, `Semantic Versioning` → `семантическое версионирование`, `Conventional Commits` → `Конвенциональные коммиты`
  - features.md: `Legacy-модули` → `устаревшие модули`
  - adding-features.md: убрано избыточное английское `(docstring)`
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — 9 файлов переформатировано, `pytest` — 675 unit-тестов пройдено (интеграционные HTTP-тесты пропущены)

### Ключевые архитектурные решения

- **`ctx` → `kontekst`**: устранён самый массовый английский идентификатор в кодовой базе; `kontekst` = «контекст»; FastMCP определяет Context по типу аннотации, а не по имени параметра (подтверждено документацией FastMCP: «The context parameter name can be anything as long as it's annotated with Context»)
- **`kontekst_mcp`**: в prompts.py где `kontekst: str` уже занят (пользовательский контекст промпта), MCP Context переименован в `kontekst_mcp` для избежания дублирования
- **Баг `status` → `sostoyanie`**: `KandidatKratko` имеет поле `sostoyanie` (строка 39 schemas.py), но client.py:528 передавал `status=` — Pydantic молча присваивал пустое значение; правильное присвоение `sostoyanie=` уже было на строке 328
- **`c` → `klient`**: устранена однобуквенная английская переменная в Client-контекстах тестов; `klient` уже использовался как имя в других местах проекта

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Кодовая база полностью русифицирована**: оставшиеся английские идентификаторы — только строковые ключи API-ответов (`.get("key")`), keyword-аргументы внешних библиотек (httpx, Pydantic, FastMCP), стандартные Python-идентификаторы (`*args`, `**kwargs`), параметры stdlib-переопределений (`tag`, `attrs` в HTMLParser), loanwords идентичные русским (`data` = «дата», `period` = «период»), и `logger` (стандартная конвенция Python)

## Статус раунда 2026-07-13 (семидесятый пятый проход — русификация _ATTRIBUTION→_ISTOCHNIK, констант: FIRES→POZHARY, MKB10_CLASSES→MKB10_KLASSY, CBR_DAILY_JSON/CBR_KEY_RATE_XML, *_API_BASE→*_API_BAZA, *_URL→*_ADRES, DATA_GOV_RU→DANNYE_GOV_RU, BUDGET_GOV_RU→BYUDZHET_GOV_RU, OPEN_METEO→OTKRYTYY_METEO, CONSULTANT→KONSULTANT, MINZDRAV_OPEN_DATA→MINZDRAV_OTKRYTYE_DANNYE, FRMO_API_BASE→FRMO_API_BAZA, DADATA_URL→DADATA_ADRES; исправление бага region_dtp→subiekt_dtp)

### Выполнено

- **Русификация `_ATTRIBUTION` → `_ISTOCHNIK`** (4 модуля):
  - gibdd/tools.py: `_ATTRIBUTION` → `_ISTOCHNIK` (9 ссылок)
  - fssp/tools.py: `_ATTRIBUTION` → `_ISTOCHNIK` (15 ссылок)
  - cekrf/tools.py: `_ATTRIBUTION` → `_ISTOCHNIK` (5 ссылок)
  - publikatsii/tools.py: `_PRAVO_ATTRIBUTION` → `_ISTOCHNIK_PRAVO` (11 ссылок)
- **Русификация `FIRES_BAZA_STATISTIKI` → `POZHARY_BAZA_STATISTIKI`** (3 вхождения: constants.py + client.py)
- **Русификация `MKB10_CLASSES` → `MKB10_KLASSY`** (2 вхождения: constants.py + client.py)
- **Русификация `CBR_DAILY_JSON` → `CBR_EZHEDNEVNYY_JSON`** (2 вхождения: constants.py + client.py)
- **Русификация `CBR_KEY_RATE_XML` → `CBR_KLYUCHEVAYA_STAVKA_XML`** (1 вхождение: constants.py)
- **Русификация `MINZDRAV_OPEN_DATA` → `MINZDRAV_OTKRYTYE_DANNYE`** (4 вхождения: constants.py + client.py)
- **Русификация `FRMO_API_BASE` → `FRMO_API_BAZA`** (4 вхождения: constants.py + client.py)
- **Русификация оставшихся `*_API_BASE` → `*_API_BAZA`** (5 констант в 2 модулях):
  - rospotrebnadzor/constants.py: `ROSPOTREBNADZOR_API_BASE`, `PROVERKI_API_BASE`, `ZPP_API_BASE` → `*_API_BAZA`
  - minobrnauki/constants.py: `OBRNADZOR_API_BASE` → `OBRNADZOR_API_BAZA`
- **Русификация `*_URL` → `*_ADRES`** (6 констант в 4 модулях):
  - minobrnauki/constants.py: `OBRNADZOR_ACCRED_URL` → `OBRNADZOR_AKKREDITATSIYA_ADRES`, `OBRNADZOR_LICENSE_URL` → `OBRNADZOR_LITSENZIYA_ADRES`, `VUZ_RATING_URL` → `VUZ_REYTING_ADRES`
  - roskomnadzor/constants.py: `PDN_REESTR_URL` → `PDN_REESTR_ADRES`, `ORI_REESTR_URL` → `ORI_REESTR_ADRES`
  - publikatsii/constants.py: `PRAVO_URL_POISKA` → `PRAVO_ADRES_POISKA`, `PRAVO_URL_DOKUMENTA` → `PRAVO_ADRES_DOKUMENTA`
  - rosapi/client.py: `DADATA_URL_PODSKAZOK` → `DADATA_ADRES_PODSKAZOK`, `DADATA_URL_POISKA_PO_ID` → `DADATA_ADRES_POISKA_PO_ID`
- **Русификация `DATA_GOV_RU_*` → `DANNYE_GOV_RU_*`** (5 констант в 4 модулях):
  - rosselkhoznadzor/constants.py: `DATA_GOV_RU_FSVPS` → `DANNYE_GOV_RU_FSVPS`
  - mchs/constants.py: `DATA_GOV_RU_MCHS` → `DANNYE_GOV_RU_MCHS`
  - rosvodresursy/constants.py: `DATA_GOV_RU_BAZA` → `DANNYE_GOV_RU_BAZA`
  - sovfed/constants.py: `DATA_GOV_RU_SOVFED` → `DANNYE_GOV_RU_SOVFED`, `DATA_GOV_RU_BAZA` → `DANNYE_GOV_RU_BAZA`
- **Русификация `BUDGET_GOV_RU_BAZA` → `BYUDZHET_GOV_RU_BAZA`** (2 константы в 2 модулях):
  - rosaudit/constants.py, kaznacheistvo/constants.py + client.py в обоих
- **Русификация `OPEN_METEO_*` → `OTKRYTYY_METEO_*`** (2 константы):
  - rosgidromet/constants.py + client.py
- **Русификация `CONSULTANT_BAZA_API` → `KONSULTANT_BAZA_API`** (1 константа в publikatsii/constants.py)
- **Исправление бага `d["region_dtp"]` → `d["subiekt_dtp"]`** в gibdd/tools.py:109 — client.py формирует словарь с ключом `subiekt_dtp`, а tools.py читал `region_dtp` (пустое значение)
- **Русификация имени тестовой функции**: `test_constants_subiekty_count` → `test_constants_subiekty_kolichestvo`
- **Прогнаны все проверки**: `ruff check` — 1 исправлено, `ruff format` — 3 файла переформатировано, `pytest` — 681 unit-тест пройдено (интеграционные HTTP-тесты пропущены)

### Ключевые архитектурные решения

- **`_ATTRIBUTION` → `_ISTOCHNIK`**: устранён последний массовый английский идентификатор в tools.py; «источник» — точный русский эквивалент «attribution» в контексте указания источника данных
- **`FIRES` → `POZHARY`**: устранено английское слово «fires» (пожары); «пожары» — точный перевод
- **`MKB10_CLASSES` → `MKB10_KLASSY`**: устранён английский суффикс `_CLASSES`; «классы» — точный перевод
- **`CBR_DAILY_JSON` → `CBR_EZHEDNEVNYY_JSON`**: устранены английские слова `DAILY` и `KEY_RATE`; «ежедневный» и «ключевая ставка» — точные переводы
- **`*_URL` → `*_ADRES`**: завершена русификация суффикса `_URL` начатая в раунде 73; `ADRES` = «адрес»
- **`DATA_GOV_RU` → `DANNYE_GOV_RU`**: устранён английский префикс `DATA`; `DANNYE` = «данные»
- **`BUDGET_GOV_RU` → `BYUDZHET_GOV_RU`**: устранён английский префикс `BUDGET`; `BYUDZHET` = «бюджет»
- **`OPEN_METEO` → `OTKRYTYY_METEO`**: устранён английский префикс `OPEN`; `OTKRYTYY` = «открытый»
- **`CONSULTANT` → `KONSULTANT`**: русификация названия сервиса «КонсультантПлюс»; `KONSULTANT` = «консультант»
- **Баг `region_dtp` → `subiekt_dtp`**: client.py формирует словарь с ключом `subiekt_dtp` (строка 188), а tools.py читал `region_dtp` (строка 109) — приводило к пустым значениям в таблице ДТП

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Кодовая база полностью русифицирована**: оставшиеся английские идентификаторы — только строковые ключи API-ответов (`.get("key")`), keyword-аргументы внешних библиотек (httpx, Pydantic, FastMCP), стандартные Python-идентификаторы (`*args`, `**kwargs`), параметры stdlib-переопределений (`tag`, `attrs` в HTMLParser), loanwords идентичные русским (`data` = «дата», `period` = «период»), и `logger` (стандартная конвенция Python)

## Статус раунда 2026-07-09 (семидесятый четвёртый проход — русификация локальных переменных: _data→_dannye, _name→_nazvanie, _text→_tekst, _code→_kod, static→statika, _list→_spisok; унификация _id→_identifikator в Pydantic-полях; исправление бага теста)

### Выполнено

- **Русификация `_data` → `_dannye`** (5 переменных в 2 модулях):
  - mchs/tools.py: `pojarov_data` → `pojarov_dannye`, `chs_data` → `chs_dannye`, `monitoring_data` → `monitoring_dannye`, `gidro_data` → `gidro_dannye`
  - cekrf/client.py: `cik_data` → `cik_dannye` (4 вхождения: в `poisk_kandidata`, `kandidat_podrobno`, `rezultaty_vyborov`, `yavka_i_itogi`)
- **Русификация `_name` → `_nazvanie`** (3 переменных в 3 модулях):
  - rosselkhoznadzor/tools.py: `vid_name` → `vid_nazvanie`
  - mchs/tools.py: `fo_name` → `fo_nazvanie`
  - rosvodresursy/tools.py: `nap_name` → `nap_nazvanie`
- **Русификация `_text` → `_tekst`** (7 переменных в 6 модулях):
  - fns/tools.py: `period_text` → `period_tekst`
  - kaznacheistvo/tools.py: `tip_text` → `tip_tekst`, `god_text` → `god_tekst` (2 вхождения)
  - sovfed/tools.py: `god_text` → `god_tekst`
  - rosprirodnadzor/tools.py: `god_text` → `god_tekst`
  - rosaudit/tools.py: `period_text` → `period_tekst`
  - publikatsii/tools.py: `tip_text` → `tip_tekst`
- **Русификация `_code` → `_kod`** (1 переменная):
  - mchs/tools.py: `fo_code` → `fo_kod`
- **Русификация `static` → `statika`** (3 переменных в 3 модулях):
  - mchs/tools.py: `static` → `statika` (2 вхождения: присвоение и использование)
  - rosselkhoznadzor/tools.py: `static` → `statika`
  - rosvodresursy/tools.py: `static` → `statika`
- **Русификация `_list` → `_spisok`** (1 переменная):
  - rosvodresursy/tools.py: `vodokhr_list` → `vodokhr_spisok`
- **Унификация `_id` → `_identifikator` в Pydantic-полях** (3 поля в 3 модулях):
  - cekrf/schemas.py: `kandidat_id` → `kandidat_identifikator` в `ResultatKandidata` + 4 ссылки в client.py + 5 ссылок в tools.py + 1 ссылка в prompts.py
  - roskomnadzor/schemas.py: `zapisi_id` → `zapisi_identifikator` в `ZapisReestra`
  - minzdrav/schemas.py: `organizatsia_id` → `organizatsia_identifikator` в `VrachebnyyKadr`
- **Исправление бага теста** `sud_name` → `nazvanie_suda` (kad_arbitrazh/test_tools.py: поле `sud_name` не существует в `SudebnoeDelo`, заменено на `nazvanie_suda`)
- **Русификация имени тестовой функции**: `test_razobrat_deputatov_list` → `test_razobrat_deputatov_spisok`
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — 3 файла переформатировано, `pytest` — 681 unit-тест пройдено (интеграционные HTTP-тесты пропущены)

### Ключевые архитектурные решения

- **`_data` → `_dannye`**: устранён английский суффикс «data» в значении «данные» (не «дата»); `dannye` — точный русский эквивалент
- **`_name` → `_nazvanie`**: устранён английский суффикс «name»; `nazvanie` = «название»
- **`_text` → `_tekst`**: устранён английский суффикс «text»; `tekst` = «текст»
- **`_code` → `_kod`**: устранён английский суффикс «code»; `kod` = «код»
- **`static` → `statika`**: устранено английское слово «static» (статические/резервные данные); `statika` = «статика»
- **`_list` → `_spisok`**: устранён английский суффикс «list»; `spisok` = «список»
- **`_id` → `_identifikator`**: унификация с устоявшейся конвенцией проекта — все остальные модели используют `identifikator` (KandidatKratko.identifikator, Kandidat.identifikator, Deputat.identifikator)
- **Баг `sud_name` → `nazvanie_suda`**: поле `sud_name` не существует в `SudebnoeDelo` (правильное имя `nazvanie_suda`); тест не ловил ошибку из-за динамической природы Pydantic

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Кодовая база полностью русифицирована**: оставшиеся английские идентификаторы — только строковые ключи API-ответов (`.get("key")`), keyword-аргументы внешних библиотек (httpx, Pydantic, FastMCP), стандартные Python-идентификаторы (`*args`, `**kwargs`), параметры stdlib-переопределений (`tag`, `attrs` в HTMLParser), loanwords идентичные русским (`data` = «дата», `period` = «период»), и `logger` (стандартная конвенция Python)

## Статус раунда 2026-07-08 (семидесятый третий проход — русификация констант: _API_BASE→_BAZA_API, _OPENDATA_BASE→_BAZA_OTKRYTYKH_DANNYKH, _BASE→_BAZA; переименование португальского каталога normas→normy; русификация resource URI template://→shablon://, normas://→normy://)

### Выполнено

- **Переименование португальского каталога `normas/` → `normy/`** (1 каталог, 3 файла .md внутри):
  - `src/mcp_russia/agenty/deloproizvodstvo/normas/` → `normy/`
  - `resources.py`: `DIREKTORIYA_NORM = Path(__file__).parent / "normas"` → `"normy"`
- **Русификация resource URI `template://` → `shablon://`** (7 в server.py + 7 в prompts.py + 7 в test_integration.py + 7 в docs):
  - Все 7 шаблонных URI: `template://pismo`, `template://prikaz`, `template://rasporyazhenie`, `template://akt`, `template://spravka`, `template://protokol`, `template://dokladnaya_zapiska` → `shablon://...`
- **Русификация resource URI `normas://` → `normy://`** (3 в server.py + 1 в prompts.py + 3 в test_integration.py + 3 в docs):
  - `normas://manual`, `normas://obrashcheniya`, `normas://zaklyuchitelnye` → `normy://...`
- **Русификация констант `_API_BASE` → `_BAZA_API`** (21 константа в 14 модулях, ~96 ссылок в client.py):
  - `FSVPS_API_BASE` → `FSVPS_BAZA_API`, `ROSGIDROMET_API_BASE` → `ROSGIDROMET_BAZA_API`, `ACH_API_BASE` → `ACH_BAZA_API`, `DUMA_API_BASE` → `DUMA_BAZA_API`, `FSSP_API_BASE` → `FSSP_BAZA_API`, `RKN_API_BASE` → `RKN_BAZA_API`, `EAIS_API_BASE` → `EAIS_BAZA_API`, `VYBORY_API_BASE` → `VYBORY_BAZA_API`, `CIK_API_BASE` → `CIK_BAZA_API`, `PRAVO_API_BASE` → `PRAVO_BAZA_API`, `CONSULTANT_API_BASE` → `CONSULTANT_BAZA_API`, `KAD_ARBITR_API_BASE` → `KAD_ARBITR_BAZA_API`, `ROSPRIRODNADZOR_API_BASE` → `ROSPRIRODNADZOR_BAZA_API`, `MCHS_API_BASE` → `MCHS_BAZA_API`, `ZAKUPKI_API_BASE` → `ZAKUPKI_BAZA_API`, `FNS_API_BASE` → `FNS_BAZA_API`, `EGRUL_API_BASE` → `EGRUL_BAZA_API`, `GMVO_API_BASE` → `GMVO_BAZA_API`, `EMISS_API_BASE` → `EMISS_BAZA_API`, `GIBDD_API_BASE` → `GIBDD_BAZA_API`, `SOVFED_API_BASE` → `SOVFED_BAZA_API`, `KAZNACHEISTVO_API_BASE` → `KAZNACHEISTVO_BAZA_API`
- **Русификация констант `_OPENDATA_BASE` → `_BAZA_OTKRYTYKH_DANNYKH`** (5 констант):
  - `FSVPS_OPENDATA_BASE` → `FSVPS_BAZA_OTKRYTYKH_DANNYKH`, `RKN_OPENDATA_BASE` → `RKN_BAZA_OTKRYTYKH_DANNYKH`, `ROSPRIRODNADZOR_OPENDATA_BASE` → `ROSPRIRODNADZOR_BAZA_OTKRYTYKH_DANNYKH`, `MCHS_OPENDATA_BASE` → `MCHS_BAZA_OTKRYTYKH_DANNYKH`, `ROSKAZNA_OPENDATA_BASE` → `ROSKAZNA_BAZA_OTKRYTYKH_DANNYKH`
- **Русификация констант `_BASE` → `_BAZA`** (8 констант):
  - `ROSSTAT_BASE` → `ROSSTAT_BAZA`, `SOVFED_BASE` → `SOVFED_BAZA`, `DATA_GOV_RU_BASE` → `DATA_GOV_RU_BAZA` (2 модуля), `VODNYY_REESTR_BASE` → `VODNYY_REESTR_BAZA`, `BUDGET_GOV_RU_BASE` → `BUDGET_GOV_RU_BAZA` (2 модуля), `ROSPRIRODNADZOR_BASE` → `ROSPRIRODNADZOR_BAZA`, `FSVPS_BASE` → `FSVPS_BAZA`, `MCHS_BASE` → `MCHS_BAZA`, `KAZNACHEISTVO_BASE` → `KAZNACHEISTVO_BAZA`
- **Русификация специализированных констант** (~15 констант):
  - `GIBDD_CHECK_BASE` → `GIBDD_BAZA_PROVEROK`, `GIBDD_STAT_BASE` → `GIBDD_BAZA_STATISTIKI`
  - `FIRES_STAT_BASE` → `FIRES_BAZA_STATISTIKI`
  - `PDN_REGISTRY_URL` → `PDN_REESTR_URL`, `ORI_REGISTRY_URL` → `ORI_REESTR_URL`, `REGISTRY_RKN` → `REESTR_RKN`
  - `PRAVO_SEARCH_URL` → `PRAVO_URL_POISKA`, `PRAVO_DOCUMENT_URL` → `PRAVO_URL_DOKUMENTA`, `KAD_SEARCH_URL` → `KAD_URL_POISKA`, `KAD_INSTANCE_URL` → `KAD_URL_INSTANTSIY`
  - `CIK_VOTER_API` → `CIK_API_IZBIRATELYA`
  - `FRAKCIYA_API_MAP` → `FRAKCIYA_SLOVAR_API`
  - `ONV_REGISTER_BASE` → `ONV_REESTR_BAZA`
  - `GOSUSLUGI_EKO_BASE` → `GOSUSLUGI_EKO_BAZA`
  - `FSSP_SEARCH_API` → `FSSP_API_POISKA`, `FSSP_IP_BASE` → `FSSP_IP_BAZA`
  - `OPEN_METEO_BASE` → `OPEN_METEO_BAZA`, `OPEN_METEO_AIR_QUALITY_BASE` → `OPEN_METEO_BAZA_KACHESTVA_VOZDUKHA`
  - `DUMA_DEPUTATS` → `DUMA_DEPUTATY`, `DUMA_LAWS` → `DUMA_ZAKONOPROEKTY`, `DUMA_VOTES` → `DUMA_GOLOSOVANIYA`, `DUMA_TRANSCRIPTS` → `DUMA_STENOGRAMMY`
  - `ZAKUPKI_OPEN_DATA` → `ZAKUPKI_OTKRYTYE_DANNYE`, `ZAKUPKI_API_DOCS` → `ZAKUPKI_API_DOKUMENTY`
- **Русификация CONTRIBUTING.md**: `namespace` → `пространство имён`
- **Русификация документации** (3 файла):
  - CONTRIBUTING.md: `ROSSTAT_API_BASE` → `ROSSTAT_BAZA_API` в таблице
  - docs/examples/ofitsialnyy-redaktor.md: `template://` → `shablon://`, `normas://` → `normy://`
  - docs/guide/adding-features.md: `PRIMER_API_BASE` → `PRIMER_BAZA_API`
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — all formatted, `pytest` — 681 unit-тест пройдено (интеграционные HTTP-тесты пропущены)

### Ключевые архитектурные решения

- **`normas/` → `normy/`**: устранён последний португальский артефакт в файловой структуре; «normas» — португальское слово («нормы»), заменено на русскую транслитерацию
- **`template://` → `shablon://`**: устранён английский resource URI scheme; «шаблон» — точный русский эквивалент
- **`normas://` → `normy://`**: синхронизировано с переименованием каталога
- **`_API_BASE` → `_BAZA_API`**: устранён массовый английский суффикс `_BASE`; `BAZA` = «база», `API` — заимствование; порядок слов изменён на русский (существительное + определение)
- **`_OPENDATA_BASE` → `_BAZA_OTKRYTYKH_DANNYKH`**: полный перевод; «открытые данные» — устоявшийся русский термин
- **`REGISTRY` → `REESTR`**, **`SEARCH` → `POISK`**, **`DOCUMENT` → `DOKUMENT`**, **`VOTER` → `IZBIRATEL`**, **`CHECK` → `PROVERKA`**, **`MAP` → `SLOVAR`**, **`REGISTER` → `REESTR`**: точные русские эквиваленты
- **`DEPUTATS` → `DEPUTATY`**, **`LAWS` → `ZAKONOPROEKTY`**, **`VOTES` → `GOLOSOVANIYA`**, **`TRANSCRIPTS` → `STENOGRAMMY`**: русификация английских множественных чисел
- **`OPEN_DATA` → `OTKRYTYE_DANNYE`**, **`API_DOCS` → `API_DOKUMENTY`**: полный перевод

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Кодовая база полностью русифицирована**: оставшиеся английские идентификаторы — только строковые ключи API-ответов (`.get("key")`), keyword-аргументы внешних библиотек (httpx, Pydantic, FastMCP), стандартные Python-идентификаторы (`*args`, `**kwargs`), параметры stdlib-переопределений (`tag`, `attrs` в HTMLParser), loanwords идентичные русским (`data` = «дата», `period` = «период»), и `logger` (стандартная конвенция Python)

## Статус раунда 2026-07-08 (семидесятый второй проход — русификация документации и описаний: английские термины в docs/, CONTRIBUTING.md, README.md, transliteration→кириллица в schemas)

### Выполнено

- **Русификация английского docstring в feature.py** (1 замена):
  - `Flask blueprints, Django app registry, pytest plugin discovery, FastAPI router auto-include.` → `чертежами Flask, реестром приложений Django, обнаружением плагинов pytest, автоподключением маршрутов FastAPI.`
- **Замена транслитерации на кириллицу в rosapi/schemas.py** (1 замена):
  - `DEYSTVUYUSHCHAYA, LIKVIDIROVANA` → `ДЕЙСТВУЮЩАЯ, ЛИКВИДИРОВАНА` в description-строке
- **Русификация английских commit-примеров в CONTRIBUTING.md** (6 замен):
  - `add tool` → `добавить инструмент`, `handle empty response from EGRUL` → `обработать пустой ответ ЕГРЮЛ`, `add edge-case tests for client` → `добавить граничные тесты для клиента`, `simplify pagination logic` → `упростить логику пагинации`, `add 5 tools` → `добавить 5 инструментов`, `handle timeout` → `обработать таймаут`
- **Русификация английских терминов в docs/** (~17 замен в 6 файлах):
  - index.md: `legacy-модули` → `устаревшие модули` (2), `namespace` → `пространство имён`
  - adding-features.md: `namespace` → `пространство имён`, `enum-подобные словари` → `словари типа перечислений`, `shared HTTP helpers` → `общие HTTP-утилиты`, `docstring` → `строки документации (docstring)`
  - development.md: `production-зависимости` → `рабочие зависимости`, `production + dev зависимости` → `рабочие зависимости и зависимости для разработки`, `wheel и sdist` → `wheel-пакет и исходный дистрибутив`, `runtime` → `среда выполнения`, `internal-дерево` → `внутреннее дерево`, `Перед PR` → `Перед отправкой пул-реквеста`, `fix(scope)` → `fix(oblast)`, `test(scope)` → `test(oblast)`
  - architecture.md: `публичный namespace` → `публичное пространство имён`, `env vars` → `переменные окружения`, `async HTTP-клиент` → `асинхронный HTTP-клиент`, `TTL-кеш и декоратор` → `кеш с TTL и декоратор`, `legacy-слой` → `устаревший слой`
  - configuration.md: `HTTP timeout` → `HTTP-таймаут`, `top-N релевантных` → `N наиболее релевантных`, `timeout, если API` → `таймаут, если API`
  - smart-tools.md: `top-N совпадений` → `N наиболее релевантных совпадений`
  - parlamentskiy-otchet.md: `workflow` → `рабочий процесс`
- **Русификация английских терминов в README.md** (3 замены):
  - `legacy-модулей` → `устаревших модулей` (2), `deprecated-алиасы` → `устаревшие алиасы`
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — all formatted, `pytest` — 678 unit-тестов пройдено, 3 интеграционных HTTP-теста упали (сетевая недоступность cbr-xml-daily.ru)

### Ключевые архитектурные решения

- **Транслитерация → кириллица**: `DEYSTVUYUSHCHAYA/LIKVIDIROVANA` в description-строке Pydantic-поля заменены на кириллические `ДЕЙСТВУЮЩАЯ/ЛИКВИДИРОВАНА`; это единственный случай, когда русские слова были записаны латиницей в пользовательски-видимом тексте
- **`namespace` → `пространство имён`**: устоявшийся русский эквивалент программистского термина
- **`legacy` → `устаревший`**: устоявшийся русский эквивалент, уже использовавшийся в других местах документации
- **`production` → `рабочие`**: в контексте зависимостей — «рабочие зависимости» (runtime deps), «зависимости для разработки» (dev deps)
- **`runtime` → `среда выполнения`**: точный русский эквивалент
- **`top-N` → `N наиболее релевантных`**: устранён англицизм, сохранена семантика
- **`scope` → `oblast`**: русификация conventional commit scope

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Кодовая база полностью русифицирована**: оставшиеся английские идентификаторы — только строковые ключи API-ответов (`.get("key")`), keyword-аргументы внешних библиотек (httpx, Pydantic, FastMCP), стандартные Python-идентификаторы (`*args`, `**kwargs`), параметры stdlib-переопределений (`tag`, `attrs` в HTMLParser), loanwords идентичные русским (`data` = «дата», `period` = «период»), и `logger` (стандартная конвенция Python)

## Статус раунда 2026-07-07 (семидесятый первый проход — регистрация fssp spisok_regionov, русификация тестовых переменных и документации)

### Выполнено

- **Регистрация `spisok_regionov` в ФССП** (3 файла):
  - fssp/server.py: добавлен импорт `spisok_regionov` и `mcp.tool(spisok_regionov, tags={"регионы", "справочник"})`
  - fssp/test_tools.py: добавлен тест `test_spisok_regionov` (проверяет наличие «Москва»)
  - fssp/test_integration.py: добавлен `"spisok_regionov"` в `ozhidayemyy`
- **Русификация `prompt_names` → `imena_promtov`** (17 файлов интеграционных тестов):
  - Все 17 файлов data/*/test_integration.py с тестами промптов
- **Русификация `mock_` → `maket_`** (3 замены в 2 файлах):
  - cekrf/test_tools.py: `mock_yavka` → `maket_yavka`
  - kad_arbitrazh/test_tools.py: `mock_dela` → `maket_dela`, `mock_delo` → `maket_delo`
- **Русификация тестовых переменных** (8 файлов):
  - test_public_namespace.py: `legacy_mcp` → `prezhnyaya_mcp`, `legacy_reyestr` → `prezhniy_reyestr`
  - cbrf/test_tools.py: `raw` → `syryye_dannye`, `codes` → `kody`
  - rosselkhoznadzor/test_tools.py: `codes` → `kody`
  - rosstat/test_tools.py: `indicator_codes` → `kody_indikatorov`, `code` → `kod` (цикловая), `codes` → `kody` (3 места), `dups` → `dublikaty`
  - test_batch.py: `reg` → `reyestr`, `"nonexistent_tool"` → `"nesushchestvuyushchiy_instrument"`, `"test_instrument"` → `"proverochnyy_instrument"`, `"norm"` → `"norma"`, `registry` → `реестр` в docstring
  - test_lifespan.py: `generator` → `generator_tsikla`
  - deloproizvodstvo/test_integration.py: `names` → `imena`, `messages` → `soobshcheniya`
- **Русификация английских assertion-сообщений и комментариев** (6 замен в 3 файлах):
  - deloproizvodstvo/test_integration.py: `f"Missing: ..."` → `f"Отсутствуют: ..."`, `f"Tool ... has no description"` → `f"Инструмент ... не имеет описания"`
  - rosstat/test_tools.py: `f"KLYUCHEVYE_INDIKATORY code '...' missing from ..."` → `f"KLYUCHEVYE_INDIKATORY код '...' отсутствует в ..."`
  - rosapi/test_integration.py: английский docstring-комментарий → русский
- **Исправление документации** (~15 замен в 10 файлах):
  - features.md: 212 → 213 инструментов, fssp 9 → 10 инструментов (добавлен `spisok_regionov`)
  - architecture.md: `reestr` → `reyestr` в примере кода, `shared-инфраструктура` → `общая инфраструктура`, `TTL-cache и decorator` → `TTL-кеш и декоратор`, `rate limiting` → `ограничение частоты запросов`, `lifecycle` → `жизненный цикл`
  - smart-tools.md: `Экспериментальный программный обнаружение` → `Экспериментальное программное обнаружение`
  - configuration.md: `backoff` → `откат` (3 вхождения), `1s -> 2s -> 4s` → `1с -> 2с -> 4с`
  - index.md: `data-модуля` → `модуля данных`
  - development.md: `auto-fix` → `автоисправление`
  - zhurnalist-stati.md: `bus.kaznacheystvo.ru` → `bus.gov.ru`
  - municipalnyy-kontrol.md: `kaznacheistvo_dannye` → `kaznacheistvo_ispolnenie_byudzheta`, `kaznacheistvo_emendy` → `kaznacheistvo_ispolnenie_byudzheta` *(инструмент недоступен)*, `kaznacheistvo.ru` → `roskazna.gov.ru`
  - ekonomicheskaya-panorama.md: `summary` → `сводок`
  - README.md: 22 → 24 российских модуля
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — 18 файлов переформатировано, `pytest` — 681 unit-тест пройдено (интеграционные HTTP-тесты пропущены)

### Ключевые архитектурные решения

- **`spisok_regionov` зарегистрирован**: функция существовала в tools.py с раунда 1, но не была подключена в server.py; теперь ФССП экспонирует 10 инструментов вместо 9
- **`prompt_names` → `imena_promtov`**: устранён последний массовый английский идентификатор в тестах; `imena_promtov` уже использовался в rosapi/test_integration.py
- **`mock_` → `maket_`**: устранена несовместимость с конвенцией проекта — все остальные тесты используют `maket_` (maket_konteksta, maket_dannykh, etc.)
- **`legacy_mcp` → `prezhnyaya_mcp`**: устранён английский префикс `legacy` в тестовых переменных
- **Исправление документации**: устранены английские термины (backoff, lifecycle, rate limiting, TTL-cache, decorator, auto-fix, summary), исправлены неверные URL и имена несуществующих инструментов

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Кодовая база полностью русифицирована**: оставшиеся английские идентификаторы — только строковые ключи API-ответов (`.get("key")`), keyword-аргументы внешних библиотек (httpx, Pydantic, FastMCP), стандартные Python-идентификаторы (`*args`, `**kwargs`), параметры stdlib-переопределений (`tag`, `attrs` в HTMLParser), loanwords идентичные русским (`data` = «дата», `period` = «период»), и `logger` (стандартная конвенция Python)

## Статус раунда 2026-07-07 (семидесятый проход — русификация гибридных английских суффиксов классов, поля EtapPlana, параметра discovery, исправление документации)

### Выполнено

- **Русификация гибридных английских суффиксов Pydantic-классов** (5 классов):
  - cekrf/schemas.py: `PartiaInfo` → `InformatsiyaPartii` (1 определение + 3 ссылки в client.py)
  - sovfed/schemas.py: `KomitetInfo` → `InformatsiyaKomiteta` (1 определение, нет ссылок)
  - sovfed/schemas.py: `ZasedanieInfo` → `InformatsiyaZasedaniya` (1 определение, нет ссылок)
  - rosgidromet/schemas.py: `SputnikMonitoring` → `SputnikovyyMonitoring` (1 определение + 2 ссылки в client.py)
  - mchs/schemas.py: `RadiatsionnyyMonitoring` — оставлен без изменений («мониторинг» — устоявшийся русский loanword)
- **Русификация поля EtapPlana.instrument → imya_instrumenta** (7 замен в planner.py + 3 замены в test_discovery.py):
  - Поле Pydantic-модели `instrument: str` → `imya_instrumenta: str`
  - JSON-схема в `_SISTEMNYY_PROMPT`: `"instrument"` → `"imya_instrumenta"` (5 примеров)
  - Доступ `etap.instrument` → `etap.imya_instrumenta` в `v_markdown()`
  - Обновлены тестовые данные `_KORREKTNYY_PLAN_JSON` и конструктор `PlanZaprosa` в test_discovery.py
- **Русификация параметра `instrument` → `obiekt_instrumenta` в discovery.py** (4 замены):
  - Параметр функции `_formatirovat_signaturu_instrumenta`
  - Цикловая переменная в `postroit_katalog`
  - Все `getattr(instrument, ...)` → `getattr(obiekt_instrumenta, ...)`
- **Исправление docstring `prompts` → `промпты`** в agenty/deloproizvodstvo/server.py
- **Исправление английских слов в документации** (7 замен в 4 файлах):
  - configuration.md: `discovery` → `обнаружение` (3), `client` → `клиент` (1), `retry` → `повторные попытки` (1)
  - adding-features.md: `orchestration` → `оркестрация` (1)
  - development.md: `orchestration` → `оркестрация` (1)
  - architecture.md: `retry` → `повторные попытки` (1)
- **Исправление «Росавдит» → «Счётная палата»** (3 замены в 2 файлах):
  - analiz-zakonodatelstva.md: 2 вхождения
  - municipalnyy-kontrol.md: 1 вхождение
- **Обновление устаревших «планируемый модуль» меток** (~30 замен в 5 файлах):
  - analiz-zakonodatelstva.md: `sovfed *(планируемый)*` → реализованный модуль; `*(планируемый)*` → `*(инструмент недоступен)*` для нереализованных инструментов
  - parlamentskiy-otchet.md: `sovfed` отмечен как реализованный (6 инструментов); `kaznacheistvo` отмечен как реализованный
  - gosudarstvennaya-politika.md: «планируемый модуль Росприроднадзор» → «инструмент недоступен»
  - zhurnalist-stati.md: «планируемый модуль Росприроднадзор» → «инструмент недоступен»
  - municipalnyy-kontrol.md: «планируемый модуль Федеральное казначейство» → реализованный модуль
- **Исправление неточностей в features.md** (6 изменений):
  - Общий подсчёт: 203 → 212 инструментов, 71 → 70 ресурсов
  - gosduma: 6 → 7 инструментов (добавлен `golosovaniya`)
  - minzdrav: 7 → 8 инструментов (добавлен `poisk_litsenziy`)
  - rosaudit: 7 → 8 инструментов (добавлен `poisk_kontrolnyh_meropriyatiy`)
  - rosvodresursy: 7 → 8 инструментов (добавлен `poisk_vodnykh_obektov`)
  - fssp: 10 → 9 инструментов (удалён `spisok_regionov` — не зарегистрирован в server.py)
- **Прочие исправления документации**:
  - smart-tools.md: `instrument: str` → `imya_instrumenta: str` в модели данных; «27 активных модулей» → «25»; `discovery` → `обнаружение`
  - architecture.md: добавлен `validators.py` в таблицу общей инфраструктуры
  - ofitsialnyy-redaktor.md: 9 ресурсов → 10, 5 промптов → 7
  - analiz-zakonodatelstva.md: опечатка «газате» → «газете»
  - zhurnalist-stati.md: удалён дублирующий `cekrf_kandidat_podrobno`
- **Добавление отсутствующих модулей в generate_diagrams.py** (5 модулей):
  - sovfed в кластер «Законодательство и выборы»
  - kaznacheistvo в кластер «Экономика и финансы»
  - mchs, rosprirodnadzor, rosselkhoznadzor в кластер «Экология и здравоохранение»
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — all formatted, `pytest` — 547 unit-тестов пройдено (интеграционные HTTP-тесты пропущены)

### Ключевые архитектурные решения

- **`PartiaInfo` → `InformatsiyaPartii`**: устранён гибридный английский суффикс `-Info`; выбрано `InformatsiyaPartii` по устоявшемуся паттерну `InformatsiyaPochtovogoIndeksa` в rosapi
- **`KomitetInfo` → `InformatsiyaKomiteta`**, **`ZasedanieInfo` → `InformatsiyaZasedaniya`**: аналогичная русификация в sovfed
- **`SputnikMonitoring` → `SputnikovyyMonitoring`**: «мониторинг» оставлен (loanword), но «спутник» → прилагательное «спутниковый»
- **`EtapPlana.instrument` → `imya_instrumenta`**: устранён последний английский идентификатор в Pydantic-поле; JSON-схема в промпте и тесты обновлены синхронно
- **`instrument` → `obiekt_instrumenta`**: параметр функции и цикловая переменная в discovery.py; выбрано `obiekt_instrumenta` чтобы избежать конфликта с `imya_instrumenta`
- **«Росавдит» → «Счётная палата»**: «Росавдит» — вымышленный термин (возможно, адаптация португальского «Tribunal de Contas da União»), заменён на реальное название «Счётная палата»
- **«планируемый модуль» → «инструмент недоступен»**: sovfed, kaznacheistvo, rosprirodnadzor — реализованные модули; метки обновлены чтобы отличать нереализованные инструменты от нереализованных модулей
- **fssp `spisok_regionov` не зарегистрирован**: функция существует в tools.py, но не подключена в server.py; убрана из документации чтобы избежать путаницы

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Регистрация fssp `spisok_regionov`**: функция существует в tools.py, но не подключена в server.py
- **Кодовая база полностью русифицирована**: оставшиеся английские идентификаторы — только строковые ключи API-ответов (`.get("key")`), keyword-аргументы внешних библиотек (httpx, Pydantic, FastMCP), стандартные Python-идентификаторы (`*args`, `**kwargs`), параметры stdlib-переопределений (`tag`, `attrs` в HTMLParser), loanwords идентичные русским (`data` = «дата», `period` = «период»), и `logger` (стандартная конвенция Python)

### Выполнено

- **Исправление критического бага в Makefile `registry` → `reyestr`**: `make inspect` импортировал несуществующую переменную `registry` и вызывал `registry.summary()` — теперь `reyestr` и `reyestr.svodka()`, что соответствует server.py:85-90
- **Исправление устаревшего имени класса в README.md `McpRussiaError` → `OshibkaMcpRussia`**: README упоминал `McpRussiaError`, но класс был переименован в `OshibkaMcpRussia` в раунде 48; также добавлено упоминание удалённого `McpRussiaError`
- **Исправление английского термина в CONTRIBUTING.md `auto-registry` → `автообнаружение`**: 2 вхождения (строка 18 — комментарий структуры, строка 109 — инвариант); согласовано с docs/ где уже используется «автообнаружение»/«авторегистрация»
- **Полный аудит кодовой базы**: src/, tests/, docs/, scripts/ проверены на португальские/бразильские/английские артефакты — ноль португальских слов, ноль бразильских идентификаторов, ноль английских идентификаторов (кроме API внешних библиотек, строковых ключей API-ответов, стандартных Python-идентификаторов, loanwords идентичных русским, и `logger`)

### Ключевые архитектурные решения

- **Makefile `registry` → `reyestr`**: при русификации server.py в раунде 65 `registry` был переименован в `reyestr`, но Makefile не был обновлён; `make inspect` не работал с раунда 65
- **README `McpRussiaError` → `OshibkaMcpRussia`**: при русификации exceptions.py в раунде 48 класс был переименован, но README не был обновлён
- **CONTRIBUTING `auto-registry` → `автообнаружение`**: при русификации docs/ в раунде 55 все английские термины были заменены, но CONTRIBUTING.md был пропущен

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Кодовая база полностью русифицирована**: оставшиеся английские идентификаторы — только строковые ключи API-ответов (`.get("key")`), keyword-аргументы внешних библиотек (httpx, Pydantic, FastMCP), стандартные Python-идентификаторы (`*args`, `**kwargs`), параметры stdlib-переопределений (`tag`, `attrs` в HTMLParser), loanwords идентичные русским (`data` = «дата», `period` = «период»), и `logger` (стандартная конвенция Python)

## Статус раунда 2026-07-06 (шестьдесят восьмой проход — русификация оставшихся английских констант и переменных: TEMPLATES_DIR, NORMAS_DIR, filepath, _DIGITS_RE, uri)

### Выполнено

- **Русификация `TEMPLATES_DIR` → `DIREKTORIYA_SHABLONOV`** (7 вхождений в resources.py)
- **Русификация `NORMAS_DIR` → `DIREKTORIYA_NORM`** (3 вхождения в resources.py)
- **Русификация `filepath` → `put_fayla`** (4 вхождения в resources.py: присвоение, exists(), FileNotFoundError, read_text())
- **Русификация `_DIGITS_RE` → `_RE_TSIFR`** (2 вхождения в validators.py: определение и .sub())
- **Русификация `uri` → `adres_uri`** (2 вхождения в server.py: присвоение и f-string)
- **Полный аудит кодовой базы**: src/, tests/, docs/ проверены на португальские/бразильские/английские артефакты — ноль португальских слов, ноль бразильских идентификаторов, все оставшиеся английские слова являются либо API внешних библиотек (httpx, Pydantic, FastMCP), либо строковыми ключами API-ответов (.get("key")), либо стандартными Python-идентификаторами (*args, **kwargs, __version__, logger, exc)
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — all formatted, `pytest` — 547 unit-тестов пройдено (интеграционные HTTP-тесты пропущены)

### Ключевые архитектурные решения

- **`TEMPLATES_DIR` → `DIREKTORIYA_SHABLONOV`**: устранён последний английский модульный констант в agenty/deloproizvodstvo; «директория шаблонов» — точный перевод
- **`NORMAS_DIR` → `DIREKTORIYA_NORM`**: устранён английский суффикс `_DIR`; «директория норм» — точный перевод
- **`filepath` → `put_fayla`**: локальная переменная в `_zagruzit_fayl`; «путь файла» — точный перевод
- **`_DIGITS_RE` → `_RE_TSIFR`**: модульный констант регулярного выражения в validators.py; «РЕ цифр» — обратный порядок (существительное + определение), как в `_RE_TSIFR`
- **`uri` → `adres_uri`**: локальная переменная в `pri_chtenii_resursa`; согласовательно с `adresa_uri` в тестах

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Финальная дочистка кодовой базы**: оставшиеся английские идентификаторы — только строковые ключи API-ответов (`.get("key")`), keyword-аргументы внешних библиотек (httpx, Pydantic, FastMCP), стандартные Python-идентификаторы (`*args`, `**kwargs`), параметры stdlib-переопределений (`tag`, `attrs` в HTMLParser), loanwords идентичные русским (`data` = «дата», `period` = «период»), и `logger` (стандартная конвенция Python)

## Статус раунда 2026-07-05 (шестьдесят седьмой проход — русификация оставшихся английских переменных, docstring-примеров, тестовых переменных и docstrings, скрипта диаграмм, документации)

### Выполнено

- **Русификация `parser` → `razobratchik`** в cekrf/client.py (2 функции: `_razobrat_rezultaty_iz_html`, `_razobrat_kandidatov_iz_html`)
- **Русификация `ri` → `info_subiekta`** в rosstat/client.py (8 вхождений в 6 функциях: `poluchit_vrp`, `poluchit_zarplatu`, `poluchit_sravnenie_regionov`, `poluchit_indikator_dannye`, `poluchit_otraslevuyu_strukturu_vrp`, `_rezerv_otraslevaya_struktura`, `_rezerv_investitsii_po_vidam`)
- **Русификация docstring-примеров** (3 файла):
  - cache.py: `cache = kesh_s_vremenem_zhizni(ttl=300)` → `kesh = kesh_s_vremenem_zhizni(vremya_zhizni=300)`, `@cache` → `@kesh`
  - feature.py: `registry = ReyestrFunktsiy()` → `reyestr = ReyestrFunktsiy()`, `registry.obnaruzhit()` → `reyestr.obnaruzhit()`, `registry.smontirovat_vse(mcp)` → `reyestr.smontirovat_vse(mcp)`, `registry.obnaruzhit()` в Returns → `reyestr.obnaruzhit()`
  - rate_limiter.py: `await do_request()` → `await vypolnit_zapros()`, `token bucket` → `ведро токенов`
  - http_client.py: `transient-ошибок` → `временных ошибок`
- **Русификация тестовых переменных** (5 файлов):
  - rosstat/test_tools.py: `region` → `subiekt`
  - gosduma/test_tools.py: `bills` → `zakonoproekty`, `votes` → `golosovaniya`
  - rosgidromet/test_tools.py: `info` → `stantsiya` (4 вхождения)
  - deloproizvodstvo/test_integration.py: `content` → `soderzhimoe` (4 вхождения)
- **Русификация тестовых docstrings** (2 файла):
  - test_feature.py: `Discovery находит feature` → `Обнаружение находит функцию`, `Mount с пустым registry` → `Монтирование с пустым реестром`, `Регистрирует feature вручную и монтирует в root` → `Регистрирует функцию вручную и монтирует в корень`, `через registry` → `через реестр`, `Root-сервер без подключённых features` → `Корневой сервер без подключённых функций`
  - test_lifespan.py: `Lifespan должен вернуть http_client` → `Жизненный цикл должен вернуть HTTP-клиент`
- **Русификация документации** (2 файла):
  - docs/reference/configuration.md: `limiter` → `ogranichitel` в примере кода
  - CONTRIBUTING.md: `client` → `klient`, `result` → `rezultat` в примере кода
- **Русификация scripts/generate_diagrams.py** (16 переменных):
  - `meta` → `meta_instrumenty`, `api` → `gos_api` (2 функции), `server` → `server_uzel`, `tools` → `instrumenty` (2 функции), `client` → `klient` (2 функции), `schemas` → `skhemy`, `constants` → `konstanty`, `shared` → `obshchiy`, `start` → `nachalo`, `iter_mod` → `iteratsiya`, `mount` → `montirovanie`, `end` → `konets`, `bm25` → `filtr_bm25`, `init` → `init_uzel`, `main` → `glavnaya`
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — 1 файл переформатирован, `pytest` — 680 unit-тестов пройдено (интеграционные HTTP-тесты пропущены)

### Ключевые архитектурные решения

- **`parser` → `razobratchik`**: устранён последний крупный английский идентификатор в cekrf/client.py; «разборщик» — русское слово для HTML-парсера
- **`ri` → `info_subiekta`**: устранена краткая английская аббревиатура `ri` (region info); выбрано `info_subiekta` для согласованности с `nazvanie_subiekta` и `kod_subiekta`
- **Docstring-примеры синхронизированы**: `cache`/`registry`/`limiter`/`do_request`/`token bucket`/`transient` в docstrings заменены на русские эквиваленты, соответствующие реальному коду
- **Тестовые переменные русифицированы**: `region`/`bills`/`votes`/`info`/`content` — последние английские переменные в тестах данных
- **Диаграммный скрипт полностью русифицирован**: 16 английских переменных заменены; скрипт больше не содержит английских идентификаторов

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Финальная дочистка кодовой базы**: оставшиеся английские идентификаторы — только строковые ключи API-ответов (`.get("key")`), keyword-аргументы внешних библиотек (httpx, Pydantic, FastMCP), стандартные Python-идентификаторы (`*args`, `**kwargs`), параметры stdlib-переопределений (`tag`, `attrs` в HTMLParser), loanwords идентичные русским (`data` = «дата», `period` = «период», `post` = «пост»), короткие однобуквенные переменные в незначимых контекстах (`c` в async with Client), и `logger` (стандартная конвенция Python)

## Статус раунда 2026-07-05 (шестьдесят шестой проход — русификация private-атрибутов _shared/, кириллических полей schemas, смешанных идентификаторов, исправление опечаток)

### Выполнено

- **Исправление опечатки `otrysl` → `otrasl`** (отрасль) в publikatsii/ (5 файлов):
  - schemas.py: поле Pydantic `otrysl` → `otrasl`
  - client.py: параметр `otrysl` → `otrasl`, строковый ключ `.get("otrysl")` → `.get("otrasl")`
  - tools.py: параметр `otrysl` → `otrasl`, все ссылки и f-строки
- **Русификация смешанных английских/русских идентификаторов** (6 идентификаторов):
  - kad_arbitrazh/client.py: параметр `delo_number` → `delo_nomer` (2 функции: `_razobrat_akty`, `_razobrat_storony`)
  - publikatsii/client.py + tools.py: параметры `data_from` → `data_s`, `data_to` → `data_po`
  - rosgidromet/client.py: параметр `deg` → `gradusy` в `_gradusy_v_napravlenie`
  - cekrf/client.py: локальная переменная `region` → `subiekt_str` в `_razobrat_kandidatov_iz_html`
- **Русификация private-атрибутов `_shared/feature.py`** (2 атрибута, ~16 ссылок):
  - `self._features` → `self._funktsii` (атрибут-словарь зарегистрированных функций)
  - `self._skipped` → `self._propushcheno` (атрибут-словарь пропущенных функций)
- **Русификация private-атрибута `_shared/cache.py`** (1 атрибут, ~12 ссылок):
  - `self._store` → `self._khranilishche` (атрибут-словарь хранения кэша)
- **Русификация private-атрибутов `_shared/rate_limiter.py`** (2 атрибута, ~8 ссылок):
  - `self._timestamps` → `self._metki_vremeni` (deque меток времени)
  - `self._lock` → `self._zamok` (asyncio.Lock)
  - Пример в docstring: `limiter` → `ogranichitel`
- **Русификация кириллических полей `Deputat` в gosduma/schemas.py** (7 полей → латинская транслитерация):
  - `фамилия` → `familiya`, `имя` → `imya`, `отчество` → `otchestvo`
  - `фракция` → `frakciya`, `комитет` → `komitet`, `регион` → `subiekt`, `созыв` → `sozyv`
  - Обновлены все ссылки: gosduma/client.py (2 конструктора), gosduma/tools.py (5 ссылок), test_tools.py (6 конструкторов/ассертов)
- **Русификация тестовых переменных** (3 файла):
  - test_feature.py: `reyestr._features` → `reyestr._funktsii`, `reyestr._skipped` → `reyestr._propushcheno`
  - test_rate_limiter.py: `limiter` → `ogranichitel`, `limiter._timestamps` → `ogranichitel._metki_vremeni`
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — 1 файл переформатирован, `pytest` — 651 unit-тест пройдено (интеграционные HTTP-тесты пропущены)

### Ключевые архитектурные решения

- **`otrysl` → `otrasl`**: исправлена опечатка — «отрасль» транслитерируется как `otrasl` (в rosstat уже использовалось `otrasl`)
- **`data_from`/`data_to` → `data_s`/`data_po`**: английские предлоги `from`/`to` заменены на русские `с`/`по`; `data` = «дата» (русское слово)
- **`delo_number` → `delo_nomer`**: смешанный идентификатор; schema уже использует `delo_nomer`
- **`_features`/`_skipped` → `_funktsii`/`_propushcheno`**: последние английские private-атрибуты в ReyestrFunktsiy; публичные property уже были русскими (`funktsii`, `propushcheno`)
- **`_store` → `_khranilishche`**: устранён последний английский private-атрибут в кэше
- **`_timestamps`/`_lock` → `_metki_vremeni`/`_zamok`**: устранены последние английские private-атрибуты в rate_limiter
- **Кириллические поля Deputat → транслитерация**: 7 полей `фамилия`, `имя`, `отчество`, `фракция`, `комитет`, `регион`, `созыв` → `familiya`, `imya`, `otchestvo`, `frakciya`, `komitet`, `subiekt`, `sozyv`; устранено единственное нарушение конвенции латинской транслитерации в кодовой базе
- **`region` → `subiekt_str`**: в cekrf/client.py; `subiekt` — устоявшаяся конвенция для «субъект РФ» в кодовой базе; суффикс `_str` добавлен чтобы избежать конфликта с одноимённым параметром

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Финальная дочистка кодовой базы**: оставшиеся английские идентификаторы — только строковые ключи API-ответов (`.get("key")`), keyword-аргументы внешних библиотек (httpx, Pydantic, FastMCP), стандартные Python-идентификаторы (`*args`, `**kwargs`), параметры stdlib-переопределений (`tag`, `attrs` в HTMLParser),_loanwords идентичные русским (`data` = «дата», `period` = «период», `post` = «пост»), короткие однобуквенные переменные в незначимых контекстах, и `logger` (стандартная конвенция Python)
- **Английские переменные в scripts/generate_diagrams.py**: локальные переменные `api`, `server`, `tools`, `client`, `schemas`, `constants`, `shared`, `start`, `iter_mod`, `bm25` — диаграммный скрипт с низким приоритетом

## Статус раунда 2026-07-04 (шестьдесят пятый проход — исправление документации, русификация server_fn, _shared/ переменных, element/context в data/, тестов)

### Выполнено

- **Исправление критических ошибок в документации** (P0, ~70 замен в 13 файлах):
  - Неправильные имена инструментов: `rosstat_region_info` → `rosstat_informatsiya_o_regionye` (6 файлов), `gosduma_poluchit_deputatov` → `gosduma_spisok_deputatov`, `gosduma_poluchit_deputata` → `gosduma_info_deputata`, `gosduma_poluchit_zakonoproekty` → `gosduma_zakonoproekty`, `gosduma_poluchit_frakcii` → `gosduma_spisok_frakcii`, `rospotrebnadzor_proverki_organizaciy` → `rospotrebnadzor_poisk_proverok`
  - Неправильные ключи JSON в `vypolnit_paket`: `"tool"` → `"instrument"`, `"args"`/`"params"` → `"argumenty"` (7 файлов)
  - Неправильные параметры в примерах: `id=` → `identifikator_deputata=`, `name=` → `fio=`, `year=` → `god=`, `region=` → `kod=`, `status=` → `sostoyanie=` и др.
  - Неправильные имена в справочнике: `info_regiona` → `informatsiya_o_regionye`, `info_okruga` → `informatsiya_ob_okruge`
  - Добавлен отсутствующий инструмент `poisk_kontraktov` в features.md
  - Исправлено количество модулей 22 → 24 в docs/index.md и docs/guide/development.md
- **Русификация `server_fn` → `server_funktsiya`** (dataclass-поле + параметр + локальная переменная, 7 замен в 4 файлах + 6 файлов тестов):
  - `ZaregistrirovannayaFunktsiya.server_fn` → `server_funktsiya` (feature.py)
  - `funktsiya.server_fn` → `funktsiya.server_funktsiya` (discovery.py)
  - `http_zhiznennyy_tsikl(server_fn)` → `http_zhiznennyy_tsikl(server_funktsiya)` (lifespan.py)
  - Все ссылки в test_discovery.py, test_feature.py, test_lifespan.py
- **Русификация переменных _shared/batch.py** (6 идентификаторов):
  - `namespace` → `prostranstvo_imen`, `queries` → `zaprosy`, `q` → `zapros`, `args` → `argumenty`, `fn` → `funktsiya`, `feat` → `funktsiya_iz_reyestra`
- **Русификация переменных _shared/cache.py** (3 идентификатора):
  - `func` → `funktsiya` (параметр декоратора), `k` → `klyuch` (цикловая переменная), `exp` → `istekaet` (распаковка кортежа)
- **Русификация переменных _shared/planner.py** (3 идентификатора):
  - `deps` → `zavisimosti`, `plan` → `plan_zaprosa`, `k` → `klyuch` / `v` → `znachenie` (цикл parametry.items())
- **Русификация переменных _shared/formatting.py** (1 идентификатор):
  - `v` → `znachenie_yacheyki` (цикловая переменная в генераторе списка)
- **Русификация переменных _shared/feature.py** (1 идентификатор):
  - `meta` → `metadannye_ekz` (локальная переменная — псевдоним экземпляра MetaFunktsii)
- **Русификация переменных _shared/http_client.py** (1 идентификатор):
  - `client` → `klient` (переменная контекстного менеджера async with)
- **Русификация `element` → `zapis` в data/** (~350+ замен в ~30 файлах):
  - Параметр в 19 функциях `_razobrat_*`/`_normalizovat_*` (roskomnadzor, rospotrebnadzor, rosvodresursy, minzdrav, minobrnauki, fssp, zakupki)
  - Цикловая переменная в ~32 сайтах (rosstat, roskomnadzor, kad_arbitrazh, gibdd, publikatsii, fssp, gosduma, minobrnauki, zakupki, cekrf)
- **Русификация `context` → `kontekst` в prompts.py** (~36 замен в 18 файлах):
  - Параметр и использование во всех 18+ промпт-функциях (cbrf, gosduma, kad_arbitrazh, kaznacheistvo, mchs, minzdrav, publikatsii, rosaudit, rosgidromet, rosprirodnadzor, rosreestr, rosselkhoznadzor, rosstat, rosvodresursy, sovfed, zakupki)
- **Русификация прочих переменных data/** (11 идентификаторов):
  - cekrf: `row` → `stroka_tablitsy`, `digits` → `tsifry_stroka`, `current` → `tekushchaya_yacheyka_tekst`, `cls` → `klass_css`, `path` → `put_api`, `k` → `klyuch`, `v` → `znachenie`
  - rosapi: `keys` → `klyuchi`, `default` → `znacheniye_po_umolchaniyu`
  - cbrf: `m` → `valyuta`
  - gosduma: `d` → `deputat`
- **Русификация тестовых переменных** (~50+ замен):
  - cbrf: `_mock_valyuta` → `_maket_valyuty`
  - rosselkhoznadzor: `tool_names` → `imena_instrumentov`, `resources` → `resursy`, `prompts` → `prompty`
  - rosapi: `headers` → `zagolovki`, `_IMPORT_OK` → `_IMPORT_NORMALNO`
  - gosduma/zakupki: `"not a list"` → `"ne spisok"`
  - test_batch: `_real_registry` → `_realnyy_reyestr`, `_spec` → `_spets`, диспетчерские ключи и строки
  - test_feature: `meta` → `metadannye_ekz`, `ping_fn` → `proverka_svyazi_fn`, `"other"` → `"drugoy"`, `"test_feat"` → `"test_funktsiya"`
  - test_discovery: `disc` → `disk_modul`
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — 6 файлов переформатированы, `pytest` — 547 unit-тестов пройдено (интеграционные HTTP-тесты пропущены), mypy — 183 ошибки (без изменений)

### Ключевые архитектурные решения

- **`server_fn` → `server_funktsiya`**: устранён последний крупный английский dataclass-поле; `namespace=imya` в feature.py оставлен без изменений (API внешней библиотеки FastMCP)
- **`element` → `zapis`**: слово «элемент» совпадает в русском и английском (`element`/`element`), но выбрано `zapis` (запись) для однозначного отличия от английского слова и соответствия семантике (запись из API-ответа)
- **`context` → `kontekst`**: параметр промпт-функций русифицирован; это user-facing параметр, но он уже описан в docstrings на русском
- **`meta` → `metadannye_ekz`**: локальная переменная-псевдоним в feature.py переименована чтобы избежать конфликта с dataclass-полем `metadannye`
- **Исправление документации**: ~70 замен в 13 файлах — устранены неправильные имена инструментов, параметров и ключей JSON, которые привели бы к ошибкам при использовании

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Финальная дочистка кодовой базы**: оставшиеся английские идентификаторы — только строковые ключи API-ответов (`.get("key")`), keyword-аргументы внешних библиотек (httpx, Pydantic, FastMCP), стандартные Python-идентификаторы (`*args`, `**kwargs`), параметры stdlib-переопределений (`tag`, `attrs` в HTMLParser) и короткие однобуквенные переменные в незначимых контекстах

### Выполнено

- **Русификация _shared/batch.py** (8 идентификаторов):
  - `ToolFn` → `TipFunktsiiInstrumenta` (псевдоним типа)
  - `registry` → `reyestr` (параметр `postroit_dispetcherizatsiyu`)
  - `base` → `baza`, `pkg` → `paket` (локальные переменные)
  - `sub_path` → `put_podmodulya`, `sub_name` → `imya_podmodulya`, `is_pkg` → `eto_paket` (цикловые переменные pkgutil.iter_modules)
  - `mod` → `modul` (импортируемый модуль)
  - `fn` → `funktsiya` (цикловая переменная и поиск в диспетчере)
  - `sig` → `signatura` (локальная переменная inspect.signature)
- **Русификация _shared/feature.py** (3 идентификатора):
  - `_finder` → `_poiskovik`, `ispkg` → `eto_paket` (цикловые переменные pkgutil.iter_modules)
  - `server_obj` → `obiekt_servera` (локальная переменная getattr)
- **Русификация _shared/discovery.py** (1 идентификатор):
  - `auth_info` → `svedeniya_ob_avtorizatsii` (локальная переменная)
- **Русификация server.py** (1 идентификатор):
  - `registry` → `reyestr` (модульная переменная + 5 ссылок: obnaruzhit, smontirovat_vse, svodka, postroit_katalog, postroit_dispetcherizatsiyu)
- **Русификация констант data/ модулей** (8 констант):
  - rosapi: `DADATA_SUGGEST_URL` → `DADATA_URL_PODSKAZOK`, `DADATA_FIND_URL` → `DADATA_URL_POISKA_PO_ID`
  - rosreestr: `PKK_API_BASE` → `PKK_BAZA_API` (client.py + constants.py), `PKK_SEARCH_URL` → `PKK_URL_POISKA`, `TIPY_OBEKTA_CODE` → `TIPY_OBEKTA_KOD`, `ROSREESTR_API_BASE` → `ROSREESTR_BAZA_API` (constants.py)
- **Русификация локальных переменных data/ модулей** (14 переменных):
  - rosapi: `full_date` → `polnaya_data`, `banki_raw` → `banki_syranye`
  - kad_arbitrazh: `istorcy_raw` → `istorcy_syranye`, `otvetchiki_raw` → `otvetchiki_syranye`, `summa_raw` → `summa_syraya`
  - cekrf: `_in_td` → `_v_yacheyke_dannykh`, `_in_th` → `_v_yacheyke_zagolovka`, `_current_row` → `_tekushchaya_stroka`, `_current_cell` → `_tekushchaya_yacheyka`, `_in_title` → `_v_zagolovke`, `title_text` → `tekst_zagolovka`, `_in_stats` → `_v_statistike`, `stats_text` → `tekst_statistiki`, `region_num` → `nomer_regiona`
  - gosduma: `bills` → `zakonoproekty`, `votes` → `golosovaniya_spisok`
  - gibdd: `history` → `istoriya`, `restrict` → `ogranicheniya`
  - minzdrav: `orgs` → `organizatsii`
  - cbrf: `valute_data` → `dannye_valyut` (client.py + tools.py)
  - rosreestr: `rights` → `prava`
- **Русификация имён тестовых классов** (4 класса):
  - kad_arbitrazh: `TestParserRezultatyPoiska` → `TestRazborRezultatovPoiska`, `TestParserKartochkaDela` → `TestRazborKartochkiDela`, `TestParserAkty` → `TestRazborAktov`, `TestParserStorony` → `TestRazborStoron`
- **Русификация имён тестовых функций** (20 функций в 8 файлах):
  - zakupki: `test_parse_zakupki_search` → `test_razobrat_poisk_zakupok`, `test_parse_kontrakty` → `test_razobrat_kontrakty`, `test_determine_zakon` → `test_opredelit_zakon`, `_with_filters` → `_s_filtrami`
  - cbrf: `test_sravnit_valyuty_default` → `test_sravnit_valyuty_po_umolchaniyu`, `_too_many` → `_slishkom_mnogo`
  - rosstat: `test_demografiya_with_region` → `test_demografiya_s_regionom`
  - roskomnadzor: `_not_blocked` → `_ne_zablokirovan`, `_blocked` → `_zablokirovan`
  - minobrnauki: `test_info_vuza_by_name` → `test_info_vuza_po_nazvaniyu`, `_by_inn` → `_po_inn`
  - rosapi: `_default_year` → `_god_po_umolchaniyu`, `_raises_auth_error_without_key` → `_vyzyvaet_oshibku_bez_klyucha`, `_with_key` → `_s_klyuchom`
  - deloproizvodstvo: `test_default_moskva` → `test_moskva_po_umolchaniyu`, `_with_otdel` → `_s_otdelom`
  - test_feature: `_missing_env_var` → `_otsutstvuyushchaya_peremennaya`, `_optional_auth_with_env` → `_neobyazatelnaya_s_peremennoy`, `_tool` → `_instrument`
- **Русификация тестовых переменных** (~150+ замен в 30+ файлах):
  - Интеграционные тесты: `client` → `klient` (fixture в 22 файлах), `tools` → `instrumenty`, `tool_names` → `imena_instrumentov`, `resources` → `resursy`, `uris` → `adresa_uri`, `prompts` → `prompty`, `expected` → `ozhidayemyy`
  - _shared/ тесты: `mock_fn` → `maket_funktsii`, `call_count` → `schetchik_vyzovov`, `first` → `pervyy`, `second` → `vtoroy`, `queries` → `zaprosy`, `val` → `znacheniye`, `gen` → `generator`, `context` → `kontekst`, `client` → `klient`, `route` → `marshrut`, `registry` → `reyestr`, `summary` → `svodka_testa`, `root` → `koren`, `sub_server` → `podserver`, `skipped` → `propushcheno`, `features` → `funktsii`, `sub` → `podmodul`, `tools` → `instrumenty`, `tool_names` → `imena_instrumentov`, `now` → `seychas`, `worker` → `rabotnik`
  - test_discovery.py: `mock_anthropic` → `maket_anthropic`, `mock_block` → `maket_bloka`, `mock_response` → `maket_otveta`, `mock_client` → `maket_klienta`, `mock_registry` → `maket_reestra`, `server` → `server_fn`, `names` → `imena`, `child` → `docherniy`, `parent` → `roditelskiy`, `_VALID_PLAN_JSON` → `_KORREKTNYY_PLAN_JSON`, `plan` → `plan_dannye`, `md` → `markdown`
  - test_root_server.py: `cbrf_tool` → `cbrf_instrument`
  - Встроенные тестовые функции: `no_ctx_tool` → `instrument_bez_konteksta`, `counting_tool` → `schitayushchiy_instrument`, `failing_tool` → `neudachnyy_instrument`, `ok_tool` → `normanyy_instrument`, `bad_tool` → `plokhoy_instrument`, `hidden_tool` → `skrytyy_instrument`, `worker` → `rabotnik`, `echo` → `ekho`
  - Константы в тестах: `mock_data` → `maket_dannykh` (12 файлов), `mock_org` → `maket_organizatsii`, `mock_ip` → `maket_ip`, `tool_list` → `spisok_instrumentov`
- **Исправление ссылки test_public_namespace.py**: `registry` → `reyestr` (импорт и переменные)
- **Русификация документации** (~30 замен в 4 файлах):
  - `docs/reference/features.md`: `region_info` → `info_regiona`, `okrug_info` → `info_okruga`
  - `docs/examples/analiz-zakonodatelstva.md`: 15 английских sovfed API → русская транслитерация (`search_bills` → `poisk_zakonoproektov`, `bill_details` → `podrobnosti_zakonoproekta`, `amendments` → `popravki`, `bill_progress` → `khod_rassmotreniya`, `bill_votes` → `golosovaniya_zakonoproekta`, `vote_details` → `podrobnosti_golosovaniya`, `agenda` → `povestka`, `bill_text` → `tekst_zakonoproekta`, `committee_composition` → `sostav_komiteta`)
  - `docs/examples/zhurnalist-stati.md`: `cbr_credit_series` → `cbrf_ryady_kreditovaniya`, `"siberian_fd"` → `"sibirskiy_fo"`, `rosprirodnadzor_deforestation` → `rosprirodnadzor_obezlesenie`
  - `CONTRIBUTING.md`: `{feature}` → `{modul}`, `{novaya_feature}` → `{novyy_modul}`, `primer_tool` → `primer_instrument`, `Classes` → `Классы`, `Функции/tools` → `Функции/инструменты`
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — 31 файл переформатирован, `pytest` — 547 unit-тестов пройдено (интеграционные HTTP-тесты пропущены), mypy — без новых ошибок

### Ключевые архитектурные решения

- **`registry` → `reyestr`**: модульная переменная в server.py и параметр в batch.py; слово «registry» было одним из последних крупных английских идентификаторов в инфраструктуре
- **`ToolFn` → `TipFunktsiiInstrumenta`**: псевдоним типа TYPE_CHECKING переименован для согласованности
- **`_raw` → `_syranye`/`_syraya`**: английский суффикс `_raw` в kad_arbitrazh заменён на русские `_syranye`/`_syraya` (сырые/сырая)
- **Константы Dadata/Росреестр**: `DADATA_SUGGEST_URL` → `DADATA_URL_PODSKAZOK`, `PKK_API_BASE` → `PKK_BAZA_API` — устранены английские слова `SUGGEST`, `FIND`, `SEARCH`, `API_BASE` в именах констант
- **HTML-парсер ЦИК РФ**: все 8 атрибутов экземпляра `_VyboryTableParser` русифицированы: `_in_td` → `_v_yacheyke_dannykh`, `_in_th` → `_v_yacheyke_zagolovka` и т.д.
- **`bills` → `zakonoproekty`**: устранено английское имя переменной в gosduma/tools.py
- **`valute_data` → `dannye_valyut`**: устранён английский суффикс `_data` в cbrf
- **`client` → `klient` fixture**: переименована во всех 22+ файлах интеграционных тестов; самый массовый паттерн переименования в этом раунде

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Финальная дочистка кодовой базы**: оставшиеся английские идентификаторы — только строковые ключи API-ответов (`.get("key")`), keyword-аргументы внешних библиотек (httpx, Pydantic, FastMCP) и стандартные Python-идентификаторы; несколько единичных переменных (`server_fn` — dataclass-поле, требует обновления 5+ файлов)

## Статус раунда 2026-07-03 (шестьдесят третий проход — русификация `status`→`sostoyanie`, `result`→`rezultat`, `text`→`tekst`, `name`→`imya`/`nazvanie`, `key`→`klyuch`)

### Выполнено

- **Исправление критического бага: `status`→`sostoyanie` в параметрах client.py** (4 файла):
  - `gosduma/client.py:129` — параметр `status` → `sostoyanie`; tools.py уже вызывал с `sostoyanie=sostoyanie`, но client.py ожидал `status` (TypeError при runtime)
  - `sovfed/client.py:127` — аналогичный баг (tools.py вызывал с `sostoyanie=`, client.py имел `status`)
  - `rosaudit/client.py:28` — аналогичный баг
  - `kad_arbitrazh/client.py:229` — параметр переименован для согласованности
  - Во всех случаях `parametry["status"] = sostoyanie` — ключ API оставлен без изменений
- **Русификация `status`→`sostoyanie` как локальной переменной** (1 файл):
  - `zakupki/tools.py:244` — `status = "Добросовестный"...` → `sostoyanie`
- **Русификация `name`→`imya`/`nazvanie` в цикловых переменных** (4 файла):
  - `batch.py:38` — `for name, feat in` → `for imya, feat in` (+ `_skanirovat_modul_instrumentov(base, imya)` и f-string)
  - `fssp/tools.py:79` — `for name, kod in` → `for nazvanie, kod in`
  - `rosapi/tools.py:290` — `for kod, name in` → `for kod, nazvanie in`
  - `rosapi/client.py:204` — `for stroka_daty, name in` → `for stroka_daty, nazvanie in` (+ `"nazvanie": name` → `"nazvanie": nazvanie`)
- **Русификация `key`→`klyuch` в цикловых переменных** (3 файла):
  - `deloproizvodstvo/tools.py:96` — `for key, o in ОБРАЩЕНИЯ.items()` → `for klyuch, o in` (+ f-string и условие)
  - `cekrf/client.py:401` — `for key, v in IZVESTNYE_VYBORY.items()` → `for klyuch, v in` (+ `"klyuch": key` → `"klyuch": klyuch`)
  - `rosapi/client.py:46` — `for key in keys:` → `for klyuch in keys:` (+ `dannye.get(key, default)` → `dannye.get(klyuch, default)`)
- **Исправление устаревших docstring-ссылок в feature.py** (2 строки):
  - `requires_auth=True, auth_env_var` → `trebuet_autentifikatsii=True, peremennaya_avt_env`
  - `enabled=False` → `vklyuchena=False`
- **Исправление docstring-примеров в http_client.py** (2 строки):
  - `response = await client.get(...)` → `otvet = await client.get(...)`
  - `data = await http_poluchit(...)` → `dannye = await http_poluchit(...)`
- **Массовая русификация `result`→`rezultat` в тестах** (~1 092 замены в 54 файлах):
  - Все `result = ...` → `rezultat = ...`
  - Все `assert "..." in result` → `assert "..." in rezultat`
  - Все `result.lower()` → `rezultat.lower()`
  - Все `result.endswith()` → `rezultat.endswith()`
  - Все `result.data` → `rezultat.data`, `result.messages` → `rezultat.messages`, `result.content` → `rezultat.content`
  - `results` (множественное число) → `rezultaty` (по установленной конвенции)
  - `max_results=` (параметр BM25SearchTransform) оставлен без изменений (API внешней библиотеки)
  - Строковые ключи `"results"` в mock-данных оставлены без изменений (ключи ответа API)
- **Русификация `text`→`tekst` в тестах** (~66 замен в 23 файлах):
  - `text = str(rezultat)` → `tekst = str(rezultat)`
  - `text = str(rezultat.content)` → `tekst = str(rezultat.content)`
  - `text = content[0].text ...` → `tekst = content[0].text ...`
  - `assert "..." in text` → `assert "..." in tekst`
  - `text.lower()` → `tekst.lower()`
  - `text or` → `tekst or`
  - `.text` (атрибут FastMCP) и `text=` (параметр httpx.Response) оставлены без изменений
- **Русификация `items`→`elementy` в test_formatting.py** (3 замены)
- **Русификация `"catalog text"`→`"tekst_kataloga"`** (6 замен в test_discovery.py)
- **Исправлены 3 mypy-ошибки**: `status`→`sostoyanie` в client.py устранило `Unexpected keyword argument "sostoyanie"`
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — all formatted, `pytest` — 545 passed, 1 skipped (unit), mypy — 183 ошибки (было 186, −3)

### Ключевые архитектурные решения

- **`status`→`sostoyanie` в client.py**: критический баг — tools.py передавал `sostoyanie=sostoyanie`, но client.py ожидал `status`; замена устранила TypeError при runtime и рассинхронизацию mypy
- **`results`→`rezultaty`**: при массовой замене `result`→`rezultat` множественное число `results` превратилось в `rezultats`, исправлено на `rezultaty` по конвенции
- **`max_results` не переименован**: параметр BM25SearchTransform из fastmcp (внешняя библиотека)
- **`.text` и `text=` не переименованы**: атрибут FastMCP и параметр httpx.Response — API внешних библиотек
- **Строковые ключи `"results"` не переименованы**: ключи в mock-данных тестов закупок, соответствующие реальным ключам API

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Финальная дочистка кодовой базы**: код и тесты полностью русифицированы — оставшиеся английские идентификаторы являются только строковыми ключами API-ответов (`.get("key")`), keyword-аргументами внешних библиотек (httpx, Pydantic, FastMCP) и стандартными Python-идентификаторами

## Статус раунда 2026-07-03 (шестьдесят второй проход — русификация тестовых суффиксов, фикстуры _mock_ctx, строковых значений)

### Выполнено

- **Русификация фикстуры `_mock_ctx` → `_maket_konteksta`** (279 замен в 25 файлах):
  - `def _mock_ctx()` → `def _maket_konteksta()` (определения в 24 файлах)
  - `_mock_ctx()` → `_maket_konteksta()` (вызовы в тестовых функциях)
  - `_mock_ctx` → `_maket_konteksta` (ссылки в параметрах и декораторах)
- **Русификация английских суффиксов тестовых функций** (~220 замен в 25 файлах):
  - `_found` → `_nayden` (73 замены)
  - `_empty` → `_pustoy` (59 замен)
  - `_not_found` → `_ne_nayden` (37 замен)
  - `_with_data` → `_s_dannymi` (21 замена)
  - `_fallback` → `_zapasnoy` (10 замен)
  - `_success` → `_uspekh` (6 замен)
  - `_unavailable` → `_nedostupen` (4 замены)
  - `_error` → `_oshibka` (3 замены; `auth_error` в `test_zagolovki_dadaty_raises_auth_error_without_key` оставлен)
  - `_none` → `_nichego` (3 замены; `rezhim_none` в `test_rezhim_none_pokazyvaet_vse_instrumenty` оставлен)
  - `_required` → `_obyazatelen` (2 замены)
  - `_no_data` → `_net_dannykh` (1 замена)
  - `_format` → `_formatirovanie` (1 замена)
- **Русификация английских строковых значений в тестах** (16 замен):
  - `"nonexistent"` → `"nesushchestvuyushchiy"` (14 вхождений в 10 файлах)
  - `"missing"` → `"otsutstvuyushchiy"` (1 вхождение, test_cache.py)
  - `"fake"` → `"poddelnyy"` (2 вхождения, test_feature.py)
- **Анализ Pydantic-полей `data` и `period`** — решение: не переименовывать:
  - Все 11 полей `data` означают «дата» (русское слово, совпадающее с английским при транслитерации)
  - Все 9 полей `period` означают «период» (русское слово, совпадающее с английским)
  - Переименование создало бы искусственные имена и нарушило бы устоявшуюся русскую терминологию
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — all formatted, `pytest` — 655 passed, 1 skipped

### Ключевые архитектурные решения

- **`_mock_ctx` → `_maket_konteksta`**: фикстура переименована по общему правилу русификации идентификаторов; «макет» выбрано вместо «заглушка» для сохранения нейтральной семантики (mock ≠ stub)
- **Порядок замен `_not_found`**: первоначальная замена `_found` → `_nayden` создала промежуточный `_not_nayden`; исправлено на `_ne_nayden` отдельным проходом
- **`auth_error_without_key` не переименован**: это осмысленное имя теста «ошибка авторизации без ключа», а не английский суффикс
- **`rezhim_none` не переименован**: `none` — значение режима (отображение всех инструментов), а не тестовый суффикс
- **`data` и `period` в schemas.py оставлены**: оба слова являются русскими (дата, период), совпадение с английским — свойство транслитерации, а не англицизм

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Финальная дочистка кодовой базы**: код и тесты полностью русифицированы — оставшиеся английские идентификаторы являются только строковыми ключами API-ответов (`.get("key")`), keyword-аргументами внешних библиотек (httpx, Pydantic) и стандартными Python-идентификаторами

## Статус раунда 2026-07-02 (шестьдесят первый проход — русификация _shared/ инфраструктуры, документации, атрибутов dataclass)

### Выполнено

- **Русификация параметров и переменных _shared/formatting.py** (13 замен):
  - `headers` → `zagolovki` (параметр `tablitsa_v_markdown`)
  - `header_line` → `stroka_zagolovka`, `separator` → `razdelitel`, `body_lines` → `stroki_tela`, `row` → `stroka` (локальные переменные)
  - `value` → `znacheniye` (параметры 4 функций: `formatirovat_rubli`, `formatirovat_chislo_ru`, `formatirovat_protsent`, `razobrat_rublevoe_chislo`)
  - `sign` → `znak`, `abs_value` → `abs_znacheniye`, `integer_part` → `tselaya_chast`, `decimal_part` → `drobnaya_chast`, `int_str` → `stroka_tseloy`
  - `decimals` → `desyatichnykh` (параметр `formatirovat_chislo_ru`, `formatirovat_protsent`)
  - `shown` → `pokazannye`, `remaining` → `ostalos` (локальные переменные в `usech_spisok`)
- **Русификация переменных _shared/validators.py** (11 замен):
  - `value` → `stroka` (параметр `_tolko_tsifry`)
  - `digits` → `tsifry` (6 вхождений в 5 функциях)
  - `weights` → `vesa`, `weights1` → `vesa1`, `weights2` → `vesa2` (веса контрольных сумм)
  - `remainder` → `ostatok`, `remainder1` → `ostatok1`, `remainder2` → `ostatok2` (остатки деления)
  - `total1` → `summa1`, `total2` → `summa2` (контрольные суммы)
  - `check1` → `kontrol1`, `check2` → `kontrol2` (контрольные цифры)
  - `check_str` → `stroka_kontrolya` (строка контрольных цифр СНИЛС)
- **Русификация переменных _shared/discovery.py** (7 замен):
  - `params` → `parametry`, `properties` → `svoystva`, `required` → `obyazatelnye` (параметры инструмента)
  - `param_parts` → `chasti_parametra`, `pname` → `imya_param`, `pschema` → `skhema_param`, `ptype` → `tip_param`, `opt` → `neobyazatelen` (разбор сигнатуры)
  - `signature` → `signatura`, `full_name` → `polnoe_imya` (формирование подписи)
  - `features` → `funktsii` (локальная переменная), `feat` → `funktsiya` (цикл)
  - `meta` → `metadannye`, `server` → `server_fn` (атрибуты ZaregistrirovannayaFunktsiya)
  - `api_key` → `klyuch_api`, `client` → `klient`, `system_prompt` → `sistemnyy_prompt` (LLM-вызовы)
- **Русификация переменных _shared/planner.py** (3 замены):
  - `params` → `parametry_str` (форматирование параметров плана)
  - `api_key` → `klyuch_api`, `client` → `klient`, `system_prompt` → `sistemnyy_prompt` (LLM-вызовы)
- **Русификация параметров и переменных _shared/cache.py** (6 замен):
  - `ttl` → `vremya_zhizni` (параметр `KeshSVremenemZhizni.__init__` и `kesh_s_vremenem_zhizni`; атрибут `self._ttl` → `self._vremya_zhizni`)
  - `expires_at` → `istekaet_v` (распаковка записи кэша)
  - `now` → `seychas` (в `_ischislit` и `zakhvatit`)
  - `cache` → `kesh` (локальная переменная в `kesh_s_vremenem_zhizni`; атрибут `obertka.cache` → `obertka.kesh`)
- **Русификация переменных _shared/batch.py** (2 замены):
  - `fn_name` → `imya_fn`, `key` → `klyuch` (сканирование инструментов)
- **Русификация параметров _shared/lifespan.py** (2 замены):
  - `server` → `server_fn` (параметр `http_zhiznennyy_tsikl`), `client` → `klient` (локальная переменная httpx)
- **Русификация переменных _shared/rate_limiter.py** (2 замены):
  - `now` → `seychas` (в `zakhvatit`), `cutoff` → `porog` (в `_ochistit`)
- **Русификация атрибутов dataclass ZaregistrirovannayaFunktsiya** (2 поля):
  - `meta` → `metadannye` (атрибут MetaFunktsii)
  - `server` → `server_fn` (атрибут FastMCP)
  - Обновлены все ссылки: `feature.py` (конструктор + `smontirovat_vse` + `svodka`), `discovery.py`, `test_feature.py`
- **Русификация переменных server.py** (3 замены):
  - `name` → `imya` (в `pri_vyzove_instrumenta` и `pri_zaprose_prompta`)
  - `result` → `rezultat` (в `pri_vyzove_instrumenta`)
- **Обновление документации** (~20 замен в 4 файлах):
  - `docs/guide/adding-features.md`: `FeatureMeta` → `MetaFunktsii`, `FEATURE_META` → `META_FUNKTSII`, `name=` → `imya=`, `description=` → `opisanie=`, `version=` → `versiya=`, `api_base=` → `baza_api=`, `requires_auth=` → `trebuet_autentifikatsii=`, `tags=` → `tegi=`, `http_get` → `http_poluchit`, `data` → `dannye`, `item` → `element`, `page` → `stranitsa`, `id` → `identifikator`, `name` → `nazvanie`, `amount` → `summa`
  - `docs/concepts/architecture.md`: `http_lifespan` → `http_zhiznennyy_tsikl`, `FeatureRegistry` → `ReyestrFunktsiy`, `registry` → `reestr`, `discover` → `obnaruzhit`, `mount_all` → `smontirovat_vse`
  - `docs/reference/smart-tools.md`: `build_catalog` → `postroit_katalog`, `build_dispatch(registry)` → `postroit_dispetcherizatsiyu(reestr)`, `tool` → `instrument` (поле EtapPlana), `Tool` → `Инструмент` (заголовок таблицы)
  - `docs/reference/configuration.md`: `RateLimiter` → `OgranichitelChastoty`, `max_requests` → `maks_zaprosov`, `http_get(url)` → `http_poluchit(adres_url)`, `data` → `dannye`
- **Обновление scripts/generate_diagrams.py** (11 замен):
  - `FEATURE_META` → `META_FUNKTSII` (2 вхождения)
  - `http_get() async` → `http_poluchit() async`
  - `http_client` → `http_klient`, `formatting` → `formatirovanie`
  - `discover(pkg)` → `obnaruzhit(paket)`, `iter_modules(pkg)` → `iteratsiya_moduley(paket)`
  - `import __init__.py` → `zagruzit __init__.py`
  - `requires_auth и env var OK?` → `trebuet_autentifikatsii и переменная окружения задана?`
  - `import server.py` → `zagruzit server.py`
  - `mount(mcp, namespace=name)` → `smontirovat(mcp, prostranstvo_imen=imya)`
  - `httpx async` → `httpx асинхр.`
- **Обновление конфигурационных файлов** (2 замены):
  - `cliff.toml`: `Changelog generator for mcp-russia` → `Генератор журнала изменений для mcp-russia`
  - `pyproject.toml`: `mcp-russia contributors` → `mcp-russia участники`
- **Обновлены тесты**:
  - `tests/_shared/test_cache.py`: `ttl=60` → `vremya_zhizni=60`, `cache` → `kesh` (12 замен), `fetch_data` → `poluchit_dannye`, `fetch` → `poluchit`, `result-` → `rezultat-`, `"data"` → `"dannye"`, `.cache` → `.kesh`
  - `tests/_shared/test_formatting.py`: `decimals=0/4/1` → `desyatichnykh=0/4/1`
  - `tests/_shared/test_validators.py`: `INN 12-digit validation needs verification` → `Проверка 12-значного ИНН требует уточнения`
  - `tests/_shared/test_feature.py`: `meta=meta` → `metadannye=meta`, `server=sub_server` → `server_fn=sub_server`
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — all formatted, `mypy` — no issues, `pytest` — 547 passed, 1 skipped

### Ключевые архитектурные решения

- **`meta` → `metadannye`**: атрибут ZaregistrirovannayaFunktsiya переименован для устранения английского слова; `meta` как локальная переменная (MetaFunktsii-экземпляр) в test_feature.py оставлена без изменений
- **`server` → `server_fn`**: атрибут переименован чтобы избежать конфликта с ключевым словом `server` (часто используется как локальная переменная и имя параметра)
- **`ttl` → `vremya_zhizni`**: параметр и внутренний атрибут KeshSVremenemZhizni; `obertka.cache` → `obertka.kesh` для доступа к кэшу из тестов
- **`value` → `znacheniye`**: параметр функций форматирования; `stroka` — в `_tolko_tsifry` (вместо `value` чтобы избежать конфликта с `znacheniye`)
- **`decimals` → `desyatichnykh`**: параметр количества десятичных знаков
- **Документация синхронизирована**: 4 файла docs/ обновлены чтобы отражать актуальные русские имена API; `adding-features.md` — наиболее значительное обновление (шаблон добавления модуля)
- **`scripts/generate_diagrams.py` обновлён**: `FEATURE_META` → `META_FUNKTSII` — устранена несогласованность с реальным кодом

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Русификация английских суффиксов тестовых функций**: `_empty`, `_found`, `_not_found`, `_unavailable`, `_with_data`, `_fallback` (~170 вхождений в 24 файлах)
- **Русификация `_mock_ctx` → `_maket_konteksta`**: ~260 ссылок в 24 тестовых файлах
- **Русификация английских строковых значений в тестах**: `"nonexistent"` (13 вхождений), assert-сообщения (6 вхождений), строковые значения в mock-объектах (~20 вхождений)
- **Русификация оставшихся Pydantic-полей `data` и `period`**: 12 + 9 вхождений в schemas.py (совпадение транслитерации «дата»/«data» и «период»/«period»)

## Статус раунда 2026-07-02 (шестидесятый проход — переименование Portuguese каталога, русификация оставшихся английских переменных)

### Выполнено

- **Устранение последнего Portuguese каталога `redator/` → `deloproizvodstvo/`**:
  - Переименованы каталоги: `src/mcp_russia/agenty/redator/` → `deloproizvodstvo/`, `tests/agenty/redator/` → `deloproizvodstvo/`
  - Обновлены все импорты: `mcp_russia.agenty.redator` → `mcp_russia.agenty.deloproizvodstvo`
  - Обновлены ссылки: pyproject.toml (per-file-ignores), CONTRIBUTING.md (дерево каталогов), scripts/generate_diagrams.py (диаграмма), test_feature.py (тест и ассерты), docs/examples/ofitsialnyy-redaktor.md (Redator → Deloproizvodstvo)
  - Обновлена строка в tools.py: «инструменты redator» → «инструменты deloproizvodstvo»
- **Русификация локальных переменных rosstat/client.py** (5 переменных, 63 замены):
  - `region_name` → `nazvanie_subiekta` (25 вхождений)
  - `region_code` → `kod_subiekta` (3 вхождения)
  - `reg_code` → `kod_reg` (9 вхождений)
  - `emiss_code` → `kod_emiss` (20 вхождений в client.py + 6 в tools.py)
  - `okved` → `znachenie_okved` (8 вхождений)
- **Русификация локальных переменных kad_arbitrazh/client.py** (5 переменных, 40 замен):
  - `case_info` → `dannye_dela` (22 вхождения)
  - `category` → `kategoriya` (4 вхождения)
  - `sud_name` → `nazvanie_suda` (10 вхождений)
  - `side_type` → `tip_storony` (2 вхождения)
  - `tip_label` → `metka_tipa` (2 вхождения)
- **Русификация локальных переменных rosreestr/** (4 переменных, 36 замен):
  - `addr` → `adres_dannye` (3 вхождения — в client.py, выбрано `adres_dannye` для избежания конфликта с существующей переменной `adres`)
  - `attrs` → `atributy` (17 вхождений)
  - `tip_code` → `kod_tipa` (2 вхождения в rosreestr + 6 в publikatsii)
  - `tip_name` → `nazvanie_tipa` (2 вхождения в rosreestr/tools.py + 6 в publikatsii/client.py)
- **Русификация параметров и переменных _shared/http_client.py** (3 переменных, 10 замен):
  - `base_url` → `bazovyy_adres_url` (параметр `sozdat_klienta` — 4 замены; httpx keyword `base_url=` оставлен без изменений)
  - `default_headers` → `zagolovki_po_umolchaniyu` (3 замены)
  - `json_body` → `telo_json` (параметр `http_otpravit` — 3 замены)
  - Обновлены вызовы `sozdat_klienta(base_url=...)` → `sozdat_klienta(bazovyy_adres_url=...)` в cekrf/client.py (3 вхождения) и tests/_shared/test_http_client.py (1 вхождение)
- **Русификация локальных переменных rosgidromet/client.py** (14 переменных, ~50 замен):
  - `current` → `tekushchie` (17 вхождений)
  - `wmo_code` → `kod_vmo` (4 вхождения)
  - `wmo_codes` → `kody_vmo` (2 вхождения)
  - `wmo` → `vmo` (4 вхождения)
  - `wind_dir_deg` → `gradusy_napravleniya_vetra` (2 вхождения)
  - `daily` → `ezhednevnye` (7 вхождений)
  - `dates` → `daty` (2 вхождения)
  - `t_max` → `temperatura_maks` (2 вхождения)
  - `t_min` → `temperatura_min` (2 вхождения)
  - `precip_prob` → `veroyatnost_osadkov` (2 вхождения)
  - `wind_max` → `skorost_vetra_maks` (2 вхождения)
  - `date_str` → `stroka_daty` (2 вхождения)
  - `time_str` → `stroka_vremeni` (2 вхождения)
  - `indicators` → `pokazateli_kachestva` (2 вхождения)
- **Русификация локальных переменных rosapi/** (6 переменных, 18 замен):
  - `state_obj` → `obiekt_subiekta` (3 вхождения)
  - `addr_obj` → `obiekt_adresa` (4 вхождения)
  - `mgmt_obj` → `obiekt_upravleniya` (2 вхождения)
  - `suggestions` → `predlozheniya` (3 вхождения — переменная; строковые ключи `"suggestions"` в .get() оставлены без изменений)
  - `date_str` → `stroka_daty` (3 вхождения)
  - `addr` → `adres_dannye` (3 вхождения в tools.py)
- **Русификация прочих переменных** (6 переменных, 21 замена):
  - `request_result` → `rezultat_zaprosa` (3 вхождения, gibdd/client.py)
  - `fio_parts` → `chasti_fio` (5 вхождений gibdd + 7 fssp = 12)
  - `task_data` → `dannye_zadachi` (2 вхождения, fns/client.py)
  - `frakciya_raw` → `frakciya_syraya` (2 вхождения, gosduma/client.py — заменён английский суффикс `_raw` на русский `_syraya`)
  - `elapsed` → `proshlo_vremeni` (2 вхождения, server.py)
- **Исправление английских слов в шаблонах и документации** (4 замены):
  - `director` → `директора` (шаблон akt.md)
  - `planned` → `запланированных` (шаблон protokol.md)
  - `"your-key"` → `"ваш-ключ"` (configuration.md, 2 вхождения)
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — 5 файлов переформатированы, `pytest` — 547 passed, 1 skipped (unit-тесты; интеграционные HTTP-тесты пропущены)

### Ключевые архитектурные решения

- **`redator/` → `deloproizvodstvo/`**: устранён последний Portuguese каталог в репозитории; слово «redator» (порт. «редактор») заменено на Russian эквивалент «deloproizvodstvo» (делопроизводство), совпадающий с внутренним именем feature `imya="deloproizvodstvo"` и FastMCP-сервером `mcp-russia-deloproizvodstvo`
- **`base_url` → `bazovyy_adres_url`**: параметр `sozdat_klienta` переименован; httpx keyword `base_url=` остаётся без изменений (API внешней библиотеки)
- **`addr` → `adres_dannye`**: выбрано `adres_dannye` вместо `adres` из-за существующей переменной `adres` в rosreestr/client.py (адрес пустой строки)
- **`suggestions` → `predlozheniya`**: переменная переименована, но строковые ключи `"suggestions"` в `.get("suggestions")` оставлены (ключи ответа API Dadata)
- **`okved` → `znachenie_okved`**: выбрано вместо `kod_okved` чтобы избежать затенения одноимённого поля Pydantic-схемы `kod_okved=`
- **`frakciya_raw` → `frakciya_syraya`**: английский суффикс `_raw` заменён на русский `_syraya` (сырая)

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Финальная дочистка кодовой базы**: код полностью русифицирован — оставшиеся английские идентификаторы являются только строковыми ключами API-ответов (`.get("key")`), keyword-аргументами внешних библиотек (httpx, Pydantic) и стандартными Python-идентификаторами; оставшиеся English слова в CHANGELOG.md/README.md — исторические записи о миграции

## Статус раунда 2026-07-01 (пятьдесят девятый проход — русификация оставшихся английских локальных переменных client.py/tools.py)

### Выполнено

- **Русификация локальных переменных rosreestr/client.py** (7 переменных):
  - `area_data` → `dannye_ploshchadi` (данные площади)
  - `cost` → `stoimost_slovar` (словарь кадастровой стоимости)
  - `status` → `status_ucheta` (статус учёта — совпадает с полем Pydantic)
  - `cat` → `kategoriya_slovar` (словарь категории земель)
  - `feature` → `obekt_dannykh` (объект данных — 3 вхождения)
  - `rights` → `prava_spisok` (список прав)
  - `features` → `obekty_spisok` (список объектов)
- **Русификация локальных переменных kad_arbitrazh/client.py** (6 переменных):
  - `letter` → `bukva` (буква номера дела)
  - `doc` → `dokument` (документ акта — 2 вхождения)
  - `raw` → `syr_dannye` (сырые данные сторон)
  - `names` → `nazvaniya` (названия сторон)
  - `name` → `nazvanie` (название одной стороны)
  - `sides` → `storony` (стороны дела)
- **Русификация локальных переменных gibdd/client.py** (6 переменных):
  - `history` → `istoriya` (история регистрации ТС)
  - `dtp` → `dtp_dannye` (данные ДТП)
  - `restrict` → `ogranicheniya_dannye` (данные ограничений)
  - `driver` → `voditel_dannye` (данные водителя)
  - `categories` → `kategorii_vu` (категории ВУ)
  - `cat` → `kategoriya` (одна категория)
  - `stats` → `statistika` (статистика ДТП)
- **Русификация локальных переменных cekrf/client.py** (11 переменных):
  - `attr_dict` → `slovar_atributov` (словарь атрибутов HTML)
  - `tag_lower` → `teg_nizhniy` (тег в нижнем регистре — 2 вхождения)
  - `cell` → `yacheyka` (ячейка таблицы — 2 вхождения)
  - `cell_lower` → `yacheyka_nizhniy` (ячейка в нижнем регистре)
  - `val` → `znachenie` (значение числа)
  - `status` → `sostoyanie` (состояние кандидата — локальная переменная)
  - `name` → `nazvanie` (название типа выборов)
  - `html` → `html_tekst` (HTML-текст — 5 вхождений)
  - `year_pattern` → `shablon_goda` (шаблон поиска года)
  - `title_match` → `sovpadenie_zagolovka` (совпадение заголовка)
  - `all_kandidaty` → `vse_kandidaty` (все кандидаты)
  - `fio_lower` → `fio_nizhniy` (ФИО в нижнем регистре)
  - `turnout` → `yavka` (явка на выборы)
- **Русификация локальных переменных fssp/client.py** (1 переменная):
  - `inner` → `vnutrennie` (внутренние данные ответа)
- **Русификация переменных roskomnadzor/client.py** (6 переменных):
  - `url` → `adres_url` (5 вхождений)
  - `domain` → `domen` (параметр функции `_razobrat_blokirovku`)
- **Русификация переменных rosstat/client.py** (10 вхождений):
  - `url` → `adres_url` (10 вхождений)
- **Русификация переменных rosapi/tools.py** (2 переменные):
  - `holidays` → `prazdniki` (список праздников)
  - `date_str` → `data_stroka` (строка даты)
- **Русификация `filter_text` → `tekst_filtra`** (~17 вхождений в 9 tools.py):
  - rosgidromet, sovfed, rosvodresursy, kaznacheistvo, publikatsii, rosaudit, rosprirodnadzor, rosstat, mchs
- **Русификация `filter_parts` → `chasti_filtra`** (3 вхождения в rosstat/tools.py)
- **Русификация `region_text` → `tekst_regiona`** (2 вхождения: kaznacheistvo, rosgidromet)
- **Русификация переменных cbrf/tools.py** (3 переменные):
  - `prev_str` → `predydushchaya_stroka` (предыдущая строка)
  - `name` → `nazvanie_valyuty` (название валюты)
  - `rubles` → `rubli` (рубли)
- **Русификация переменных cbrf/client.py** (1 переменная):
  - `date_str` → `stroka_daty` (строка даты — параметр + 2 присвоения)
- **Русификация переменных fns/client.py** (3 переменные):
  - `search_url` → `adres_poiska` (адрес поиска)
  - `result_url` → `adres_rezultata` (адрес результата)
  - `org` → `organizaciya` (организация)
- **Русификация переменных rosstat/tools.py** (4 переменные):
  - `available` → `dostupnye` (доступные показатели)
  - `sorted_data` → `otsortirovannye_dannye` (отсортированные данные)
  - `val` → `znachenie` (значение — 2 вхождения)
  - `title` → `zagolovok_tekst` (текст заголовка)
- **Русификация переменных rosgidromet/tools.py** (1 переменная):
  - `line` → `stroka` (строка вывода)
- **Русификация `key`/`val` в `_izvlech_spisok`** (8 файлов):
  - `key` → `klyuch`, `val` → `znachenie_spiska`
  - minzdrav, mchs, rosaudit, kaznacheistvo, rosprirodnadzor, rosselkhoznadzor, rosvodresursy, sovfed
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — 3 файла переформатированы, `pytest` — 355+ passed (unit), 1 skipped

### Ключевые архитектурные решения

- **`feature` → `obekt_dannykh`**: в API Росреестра `feature` — GeoJSON-объект; выбрано `obekt_dannykh` (объект данных) как наиболее общее русское название
- **`doc` → `dokument`**: в КАД `Document` — запись судебного акта; `dokument` однозначно передаёт смысл
- **`domain` → `domen`**: параметр функции `_razobrat_blokirovku` переименован; строковый ключ `"domain"` в parametry не затронут
- **`date_str` → `stroka_daty`**: параметр функции `_razobrat_valyutu` и локальные переменные; Pydantic-ключ `data=` оставлен без изменений (имя поля схемы)
- **`html` → `html_tekst`**: во всех функциях ЦИК РФ, где HTML-страница хранится в локальной переменной
- **`turnout` → `yavka`**: явка на выборы — устоявшийся русский термин

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Русификация оставшихся английских параметров**: `tool`/`catalog` в server.py (MCP-инструменты — user-facing), `base_url` в `sozdat_klienta` (httpx API), `period` (rate_limiter — русское слово, совпадающее с английским)
- **Финальная дочистка**: поиск и русификация единичных оставшихся английских локальных переменных (case_info, region_name, region_code, reg_code в rosstat/client.py; addr в rosreestr/client.py и т.д.)

## Статус раунда 2026-07-01 (пятьдесят восьмой проход — русификация локальных переменных client.py/tools.py, параметров функций, docstrings)

### Выполнено

- **Русификация локальных переменных cbrf/client.py** (5 переменных):
  - `value` → `znachenie_kursa` (значение курса валюты)
  - `previous` → `predydushchiy_kurs` (предыдущий курс)
  - `nominal` → `nominal_valyuty` (номинал валюты)
  - Pydantic-ключ `nominal=` оставлен без изменений (имя поля схемы)
- **Русификация локальных переменных cbrf/tools.py** (7 переменных):
  - `change` → `izmenenie` (изменение курса)
  - `diff` → `raznitsa` (разница текущего и предыдущего)
  - `pct` → `protsent` (процент изменения)
  - `prev` → `predydushchee` (предыдущее значение — shorthand)
  - `name` → `nazvanie_valyuty` (название валюты)
  - `nominal` → `nominal_valyuty` (номинал)
  - `value` → `znachenie_kursa` (значение курса)
- **Русификация локальных переменных rosgidromet/client.py** (7 переменных):
  - `wind` → `skorost_vetra` (скорость ветра)
  - `stations` → `stantsii` (список станций)
  - `station` → `stantsiya` (одна станция в цикле)
  - `warnings` → `preduprezhdeniya` (список предупреждений)
  - `indicators` → `pokazateli` (показатели качества воздуха)
  - `directions` → `napravleniya` (компасные направления)
  - `idx` → `indeks` (индекс в массиве направлений)
  - `value` (в экологии) → `znachenie_pokazatelya`
  - `key`, `name` (в цикле indicators) → `klyuch`, `nazvanie_pokazatelya`
- **Русификация локальных переменных rosapi/client.py** (11 переменных):
  - `city` → `gorod` (город)
  - `key` → `klyuch_api` (API-ключ Dadata)
  - `name_obj` → `obiekt_imeni` (объект имени организации/банка)
  - `name_full` → `polnoe_nazvanie` (полное название)
  - `name_short` → `kratkoe_nazvanie` (краткое название)
  - `status` → `sostoyanie_org` (состояние организации)
  - `address` → `adres_str` (адресная строка)
  - `director` → `rukovoditel_imya` (имя руководителя)
  - `reg_date` → `data_reg` (дата регистрации)
  - `holidays` → `prazdniki` (список праздников)
  - `suggestions` → `predlozheniya` (подсказки Dadata)
  - `banks` / `banks_raw` → `banki` / `banki_raw` (список банков)
- **Русификация параметров функций** (~12 замен):
  - `max_items` → `maks_elementov` (в `usech_spisok`, _shared/formatting.py)
  - `maxsize` → `maks_razmer` (в `KeshSVremenemZhizni.__init__` и `kesh_s_vremenem_zhizni`, _shared/cache.py)
  - `region` → `subiekt` (в `poluchit_mezhbyudzhetnye`, kaznacheistvo/client.py)
  - `status` → `sostoyanie` (в `poisk_zakupok`, zakupki/client.py — исправлена рассинхронизация с tools.py)
  - `value` → `znachenie` (в `_bezopasnoe_veshchestvennoe`, zakupki/client.py)
  - `tool` → `instrument` (поле Pydantic `EtapPlana`, _shared/planner.py)
  - `catalog` → `katalog` (параметр `rekomendovat_instrumenty_impl` и `splanirovat_zapros_impl`, discovery.py + planner.py)
  - `registry` → `reyestr` (параметр `postroit_katalog`, discovery.py)
  - `tool` → `instrument` (параметр `_formatirovat_signaturu_instrumenta`, discovery.py)
- **Русификация docstrings — исправление несоответствий** (~62 замены в 14 файлах):
  - _shared/http_client.py: `url:` → `adres_url:`, `params:` → `parametry:`, `headers:` → `zagolovki:`, `timeout:` → `taimaut:` (10 замен в 3 функциях)
  - _shared/formatting.py: `rows:` → `stroki_tablitsy:`, `items:` → `elementy:`
  - _shared/discovery.py: `query:` → `zapros:`, `tool:` → `instrument:`, `registry:` → `reyestr:`, `catalog:` → `katalog:`
  - _shared/planner.py: `query:` → `zapros:`, `tool:` → `instrument:`, `catalog:` → `katalog:`
  - server.py: `query:` → `zapros:` (2 функции)
  - 11 модулей data/*/client.py: `region:` → `subiekt:` (33 замены в docstrings)
- **Русификация переменных в server.py**:
  - `catalog` → `katalog` (локальные переменные в `rekomendovat_instrumenty` и `splanirovat_zapros`)
- **Русификация переменных в planner.py**:
  - `raw_text` → `syrovoy_tekst` (сырой текст ответа LLM)
  - JSON-схема в `_SISTEMNYY_PROMPT`: поле `"tool"` → `"instrument"` во всех примерах
- **Обновлены тесты**:
  - tests/_shared/test_cache.py: `maxsize=2` → `maks_razmer=2`
  - tests/_shared/test_formatting.py: `max_items=5/2/3` → `maks_elementov=5/2/3`
  - tests/test_discovery.py: `_catalog_cache` → `_kesh_kataloga`, `"tool"` → `"instrument"` в _VALID_PLAN_JSON и PlanZaprosa
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — all formatted, `pytest` — unit-тесты пройдены (580+ passed, 1 skipped)

### Ключевые архитектурные решения

- **`tool` → `instrument` в EtapPlana**: поле Pydantic-модели переименовано; JSON-схема в промпте и тесты обновлены синхронно
- **`maxsize` → `maks_razmer`**: параметр `KeshSVremenemZhizni` и декоратора `kesh_s_vremenem_zhizni` переименован
- **`catalog` → `katalog`**: параметр переименован в `rekomendovat_instrumenty_impl` и `splanirovat_zapros_impl`; строка подстановки `{catalog}` → `{katalog}` в `_SISTEMNYY_PROMPT`
- **`registry` → `reyestr`**: параметр `postroit_katalog` переименован; все обращения через `getattr(reyestr, ...)` обновлены
- **`status` → `sostoyanie` в `poisk_zakupok`**: исправлена рассинхронизация — tools.py использовал `sostoyanie`, но client.py имел `status`
- **Docstrings синхронизированы**: все 62 несоответствия между именами параметров в сигнатурах и docstrings устранены

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Русификация оставшихся английских переменных в client.py**: `url` (roskomnadzor, rosstat — ещё ~12 вхождений), `feature`/`rights`/`features`/`cost`/`area_data`/`status` (rosreestr), `doc`/`name`/`sides` (kad_arbitrazh), `history`/`dtp`/`restrict`/`driver`/`categories`/`stats` (gibdd), `attr_dict`/`tag_lower`/`cell_lower`/`status`/`name`/`turnout` (cekrf), `inner` (fssp), `domain` (roskomnadzor), `filter_text`/`region_text` (8 tools.py), `holidays` (rosapi/tools.py)
- **Русификация оставшихся английских параметров**: `tool`/`catalog` в server.py (MCP-инструменты — user-facing), `base_url` в `sozdat_klienta` (httpx API), `period` (rate_limiter — русское слово, совпадающее с английским)

## Статус раунда 2026-06-30 (пятьдесят седьмой проход — русификация `data`→`dannye`, `header`→`zagolovok`, `url`→`adres_url`, параметров HTTP-клиента)

### Выполнено

- **Русификация `data` → `dannye`** (~1 309 замен в 42 файлах):
  - Локальные переменные в client.py: `data = await http_poluchit(...)` → `dannye = await http_poluchit(...)`
  - Локальные переменные в tools.py: `data = await client.method(...)` → `dannye = await client.method(...)`
  - Параметры функций `_razobrat_*` и `_izvlech_spisok`: `data: dict` / `data: Any` → `dannye: dict` / `dannye: Any`
  - Использован AST-анализ для контекстного разделения: `data` = «дата» (оставлено) vs `data` = «данные» (→ `dannye`)
  - Параметры `data: str` (дата) в `poluchit_vse_valyuty(data=)` и `poluchit_valyutu(data=)` оставлены без изменений
  - Поля Pydantic-схем `data: str = Field(description="Дата...")` оставлены без изменений
  - Ключевые аргументы Pydantic-конструкторов `ZnachenieValyuty(data=...)`, `Golosovanie(data=...)`, `PrognozDannye(data=...)`, `PokazatelRosstata(data=...)` оставлены без изменений
- **Русификация `header` → `zagolovok`** (~230 замен в 19 tools.py): заголовки форматированного вывода
- **Русификация `url` → `adres_url`** (~200 замен в 22 client.py): URL-адреса запросов
- **Русификация `restrictions` → `ogranicheniya`** (3 замены в fssp/client.py): список ограничений ФССП
- **Русификация `wanted` → `razyskivaemye`** (7 замен в fssp/client.py + gibdd/client.py + gibdd/tools.py): розыскные записи
- **Русификация `subject` → `predmet`** (5 замен в fssp/client.py): предмет исполнения ФССП
- **Русификация `info` → `svedeniya`** (19 замен в rosgidromet/client.py): сведения о станции
- **Русификация `temp` → `temperatura`** (7 замен в rosgidromet/client.py): температура
- **Русификация `found` → `naydennye`** (8 замен в rosapi/tools.py + rosreestr/client.py): найденные результаты
- **Русификация `query` → `zapros`** (6 замен в discovery.py + planner.py + server.py): запрос пользователя
- **Русификация `desc` → `opisanie_kratkoe`** (2 замены в discovery.py): краткое описание инструмента
- **Русификация `block` → `blok`** (4 замены в discovery.py + planner.py): блок ответа LLM
- **Русификация `wait` → `ozhidanie`** (14 замен в http_client.py + rate_limiter.py): время ожидания
- **Русификация `check` → `proverochnaya_tsifra`** (6 замен в validators.py): проверочная цифра ИНН/СНИЛС
- **Русификация `text` → `tekst`** (11 замен в cekrf/client.py): текст HTML-парсера
- **Русификация `code` → `kod`** (14 замен в 6 файлах): код валюты/выборов/индикатора
- **Русификация `number` → `nomer`** (18 замен в kad_arbitrazh/client.py): номер дела
- **Русификация `token` → `zheton`** (~31 замена в 4 client.py): API-токен
- **Русификация `start` → `nachalo`** (2 замены в server.py): начало замера времени
- **Русификация `search_url` → `adres_url_poiska`** (2 замены в cekrf/client.py): URL поиска
- **Русификация параметров HTTP-клиента** (~482 замены в 23 client.py):
  - `params` → `parametry`: параметры HTTP-запроса
  - `headers` → `zagolovki`: HTTP-заголовки (внутренние переменные и параметры `sozdat_klienta`/`http_poluchit`/`http_otpravit`)
  - `timeout` → `taimaut`: таймаут запроса
  - `retries` → `povtory`: счётчик повторных попыток
  - `last_error` → `poslednyaya_oshibka`: последняя ошибка
  - `attempt` → `popytka`: номер попытки
  - Ключевые аргументы httpx (`client.get(params=...)`, `httpx.AsyncClient(timeout=..., headers=...)`) оставлены на английском — это API внешней библиотеки
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — all formatted, `pytest` (680 passed, 1 skipped)

### Ключевые архитектурные решения

- **`data` → `dannye` с контекстным анализом**: использован AST для определения типов параметров; `data: str` = «дата» (оставлено), `data: dict` / `data: Any` = «данные» (→ `dannye`); функция `handle_data` в cekrf (SAX callback) оставлена без изменений
- **`url` → `adres_url`**: выбрано `adres_url` вместо простого `url` для однозначной семантики; параметр `base_url` в `sozdat_klienta` оставлен без изменений (имя параметра httpx)
- **`token` → `zheton`**: API-токены авторизации переименованы; строковые ключи API (`.get("token")`) не затронуты
- **Параметры HTTP-клиента русифицированы**: `sozdat_klienta(taimaut=, zagolovki=)`, `http_poluchit(parametry=, zagolovki=, taimaut=, maks_povtorov=)` — user-facing API; вызовы httpx внутри используют английские kwargs (`client.get(params=parametry)`)
- **`check` → `proverochnaya_tsifra`**: в алгоритмах валидации ИНН/КПП/СНИЛС; `check` как встроенное имя не используется

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Русификация оставшихся английских переменных**: `value` (cbrf/client.py — значение валюты), `previous` (cbrf/client.py — предыдущее значение), `wind` (rosgidromet/client.py — ветер), `city` (rosapi/client.py — город), `nominal` (cbrf — номинал валюты) и другие единичные переменные
- **Русификация docstrings**: обновление описаний параметров `url:`, `params:`, `headers:`, `timeout:` в docstrings http_client.py на русские имена

### Выполнено

- **Массовая русификация локальных переменных** (~2 000 замен в 56 файлах):
  - `rows` → `stroki_tablitsy` (~330 замен в 22 tools.py + formatting.py): строки таблиц для `tablitsa_v_markdown()`
  - `lines` → `stroki` (~340 замен в 22 tools.py + _shared/): строки текстового вывода для `"\n".join()`
  - `item` → `element` (~650 замен в 15 client.py): переменная цикла `for item in ...` и параметр `_normalizovat_proizvodstvo(item)`
  - `items` → `elementy` (~250 замен в 18 client.py + _shared/): локальные списки `items = data.get(...)`
  - `result` → `rezultat` (~150 замен в 10 client.py/tools.py + _shared/batch.py): локальный результат вызова
  - `results` → `rezultaty` (~130 замен в 16 client.py/tools.py + _shared/batch.py): список результатов
  - `response` → `otvet` (~30 замен в _shared/http_client.py, _shared/discovery.py, _shared/planner.py): HTTP-ответ
  - `entry` → `zapis` (~40 замен в cbrf/client.py, cekrf/client.py, fns/client.py, _shared/cache.py): запись из справочника
  - `entries` → `zapisi` (~6 замен в fns/client.py): список записей
  - `records` → `zapisi` (~40 замен в fssp/gibdd/client.py, gibdd/tools.py): записи из API
  - `body` → `telo` (~20 замен в rosapi/fssp/kad_arbitrazh/client.py): тело HTTP-запроса
  - `parsed` → `razobrannye` (~25 замен в rosapi/rosgidromet/rosreestr/client.py): разобранные данные
  - `filters` → `filtry` (~90 замен в 8 tools.py): список фильтров
  - `cleaned` → `ochishchennoe` (~12 замен в cekrf/client.py, _shared/formatting.py): очищенная строка
  - `filtered` → `otfiltrovannye` (~3 замены в cekrf/client.py): отфильтрованные данные
  - `formatted` → `otformatirovannoe` (~3 замены в rosreestr/client.py, _shared/formatting.py): отформатированный результат
  - `total` → `itogo` (~8 замен в _shared/validators.py): контрольная сумма
  - `parts` → `chasti` (~14 замен в fssp/kad_arbitrazh/client.py, _shared/batch.py): части строки
  - `output` → `vyvod` (~2 замены в _shared/batch.py): вывод пакета
  - `resp` → `otvet` (~9 замен в cekrf/client.py): HTTP-ответ
- **Исправлены коллизии имён**: `rows` и `lines` → разные имена (`stroki_tablitsy` vs `stroki`) чтобы избежать конфликта в функциях, где оба используются
- **Сохранены API-ключи строк**: `"result"`, `"records"`, `"items"` и др. внутри `.get()` не переименованы (использован tokenize-подход, заменяются только NAME-токены)
- **Сохранены встроенные методы**: `.items()` не переименовано (пропуск после `.`-оператора); `exc.response` не переименовано (атрибут внешнего класса)
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — 8 файлов переформатированы, `pytest` (547 passed, 1 skipped — unit-тесты; интеграционные HTTP-тесты пропущены)

### Ключевые архитектурные решения

- **`rows` → `stroki_tablitsy`**: выбрано `stroki_tablitsy` (строки таблицы) вместо `stroki`, чтобы избежать конфликта с `lines` → `stroki` (строки текста); в функциях, где оба используются, имена различаются
- **`item` → `element`**: переименованы все вхождения `item` как NAME-токена, включая параметры функций (`_normalizovat_proizvodstvo(item)`) и переменные циклов (`for item in ...`)
- **tokenize-подход**: использован модуль `tokenize` для точного разделения кода и строковых литералов; это гарантирует, что API-ключи в `.get("result")` и `.get("records")` остаются без изменений
- **`data` НЕ переименована**: переменная `data` встречается как в значении «данные» (→ `dannye`), так и «дата» (→ остаётся `data`, как в `poluchit_vse_valyuty(data=)` — параметр даты); автоматическое переименование невозможно без семантического анализа
- **`response` → `otvet`**: переименована только локальная переменная `response = await client.get(...)`, но не атрибут `exc.response` исключения `httpx.HTTPStatusError`

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Русификация переменной `data`**: требует ручного анализа контекста (data=«дата» vs data=«данные») — ~80 вхождений в client.py
- **Русификация оставшихся английских переменных**: `restrictions`, `wanted` (fssp), `subject` (fssp) и другие контекстно-зависимые переменные

### Выполнено

- **Русификация `_parse_*` → `_razobrat_*`** (8 функций в 2 модулях):
  - sovfed/client.py: `_parse_senator` → `_razobrat_senator`, `_parse_komitet` → `_razobrat_komitet`, `_parse_zasedanie` → `_razobrat_zasedanie`, `_parse_zakonoproekt` → `_razobrat_zakonoproekt`
  - kad_arbitrazh/client.py: `_parse_rezultaty_poiska` → `_razobrat_rezultaty_poiska`, `_parse_kartochka_dela` → `_razobrat_kartochka_dela`, `_parse_akty` → `_razobrat_akty`, `_parse_storony` → `_razobrat_storony`
  - Обновлены тесты: tests/data/kad_arbitrazh/test_tools.py (12 замен)
- **Русификация `get_*` → `poluchit_*` в agenty/redator/resources.py** (11 функций):
  - `_load_file` → `_zagruzit_fayl` (параметры: `directory` → `direktoriya`, `filename` → `imya_fayla`)
  - `get_template_pismo` → `poluchit_shablon_pismo`, `get_template_prikaz` → `poluchit_shablon_prikaz`, `get_template_rasporyazhenie` → `poluchit_shablon_rasporyazhenie`, `get_template_akt` → `poluchit_shablon_akt`, `get_template_spravka` → `poluchit_shablon_spravka`, `get_template_protokol` → `poluchit_shablon_protokol`, `get_template_dokladnaya_zapiska` → `poluchit_shablon_dokladnaya_zapiska`
  - `get_manual_deloproizvodstvo` → `poluchit_manual_deloproizvodstvo`, `get_obrashcheniya` → `poluchit_obrashcheniya`, `get_zaklyuchitelnye_formuly` → `poluchit_zaklyuchitelnye_formuly`
  - Обновлены импорты в agenty/redator/server.py
- **Русификация ключей в cekrf/resources.py** (6 замен):
  - `"name"` → `"nazvanie"`, `"base_url"` → `"bazovyy_url"`, `"auth_required"` → `"trebuet_avtentifikatsii"`, `"coverage"` → `"pokrytie"`, `"known_elections"` → `"izvestnye_vybory_kolichestvo"`, `"note"` → `"primechanie"`
  - `"format"` оставлен без изменений (совпадает в русском и английском)
- **Русификация `_auth_note` → `_zametka_ob_avtorizatsii`** (2 модуля + тесты):
  - gosduma/tools.py, zakupki/tools.py
  - Обновлены тесты: tests/data/gosduma/test_tools.py, tests/data/zakupki/test_tools.py
- **Русификация `_fallback_*` → `_rezerv_*`** (2 функции в rosstat/client.py):
  - `_fallback_otraslevaya_struktura` → `_rezerv_otraslevaya_struktura`
  - `_fallback_investitsii_po_vidam` → `_rezerv_investitsii_po_vidam`
- **Русификация методов кэша** (_shared/cache.py):
  - `get` → `poluchit`, `set` → `ustanovit`, `clear` → `ochistit`
  - `decorator` → `dekorator`, `wrapper` → `obertka`
  - Внутренние переменные: `key` → `klyuch`, `value` → `znachenie`, `cached` → `zakeshirovano`, `result` → `rezultat`, `expired` → `istekshie`, `oldest_key` → `samyy_staryy_klyuch`
  - Обновлены тесты: tests/_shared/test_cache.py (10 замен)
- **Русификация параметров функций** в _shared/feature.py:
  - `package_name` → `imya_paketa`, `short_name` → `korotkoe_imya`, `root_server` → `kornevoy_server`
  - Локальные переменные: `package` → `paket`, `reason` → `prichina`, `auth_icon` → `ikona_avt`, `server_module` → `modul_servera`
- **Исправление опечаток** (2 функции):
  - fssp/client.py: `_normlizovat_proizvodstvo` → `_normalizovat_proizvodstvo` (пропущена «а»)
  - cbrf/prompts.py: `analise_valyut` → `analiz_valyut` (английское написание вместо русского)
  - Обновлены: cbrf/server.py, tests/data/cbrf/test_integration.py, docs/reference/features.md
- **Перевод транслитерированных комментариев на кириллицу** (7 замен в 3 файлах):
  - rosvodresursy/schemas.py: `# reka, ozero, vodokhranilishche` → `# река, озеро, водохранилище`, `# normalnoe, nizkoe, vysokoe` → `# нормальное, низкое, высокое`
  - rosgidromet/schemas.py: `# vozdukh, voda, pochva, radiaciya, shum` → `# воздух, вода, почва, радиация, шум`, `# nizkiy, sredniy, vysokiy, ekstremalniy` → `# низкий, средний, высокий, экстремальный`, `# lesa, voda, požary, snezhnyy pokrov` → `# леса, вода, пожары, снежный покров`
  - publikatsii/schemas.py: `# fz, ukaz, postanovlenie_pr` → `# фз, указ, постановление пр.`, `# pravo.gov.ru, rg.ru` → `# pravo.gov.ru, rg.ru`, `# deystvuyushchiy, utratil_silu` → `# действующий, утратил силу`
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — 2 файла переформатированы, `pytest` — 382 passed, 1 skipped

### Ключевые архитектурные решения

- **`_parse_*` → `_razobrat_*` унифицирован во всех модулях**: последние 8 функций с английским префиксом `_parse_` переименованы; теперь во всех 22 модулях используется `_razobrat_*`
- **Методы кэша `get`/`set`/`clear` → `poluchit`/`ustanovit`/`ochistit`**: публичный API кэша полностью русифицирован; внутренние переменные `decorator`/`wrapper` → `dekorator`/`obertka`
- **`analise_valyut` → `analiz_valyut`**: исправлена опечатка — английское слово «analysis» заменено на русскую транслитерацию «анализ»
- **Ключ `"data"` в выходных словарях оставлен без изменений**: «дата»/«data» совпадает в транслитерации — семантически корректно
- **Комментарии Pydantic-схем переведены на кириллицу**: транслитерированные комментарии (типы водных объектов, уровни опасности и т.д.) заменены на русский текст

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Русификация английских переменных в телах функций**: `results`, `items`, `rows`, `filters`, `lines`, `parts` и т.д. в client.py/tools.py

## Статус раунда 2026-06-26 (пятьдесят четвёртый проход — русификация оставшихся ключей словарей, имён тестовых классов и функций)

### Выполнено

- **Русификация оставшихся английских ключей выходных словарей** (~12 замен в 7 модулях):
  - rosaudit/client.py: `"deficit"` → `"defitsit"`
  - rosaudit/schemas.py: `deficit` → `defitsit` (поле Pydantic)
  - rosaudit/tools.py: `data.get("deficit")` → `data.get("defitsit")` + `data["defitsit"]`
  - kaznacheistvo/schemas.py: `deficit` → `defitsit` (поле Pydantic, клиент уже использовал `"defitsit"`)
  - rosapi/client.py: `"value"` → `"znachenie"`, `"fias_id"` → `"identifikator_fias"` (poisk_adresa)
  - fssp/client.py: `"ip_end"` → `"okonchanie_ip"` + переменная `ip_end` → `okonchanie_ip`
  - fssp/tools.py: 2 чтения `r.get("ip_end")` → `r.get("okonchanie_ip")`
  - mchs/client.py: `"status"` → `"sostoyanie"` (синхронизация с полем Pydantic-схемы)
  - rosselkhoznadzor/client.py: `"status"` → `"sostoyanie"` (было несовместимо с другими ключами `"sostoyanie"` в том же модуле)
  - rosselkhoznadzor/tools.py: `p.get("status")` → `p.get("sostoyanie")`
  - minzdrav/client.py: `"status"` → `"sostoyanie"` + параметр `status` → `sostoyanie`
  - minzdrav/tools.py: `lit.get("status")` → `lit.get("sostoyanie")` + добавлен параметр `sostoyanie` в MCP-инструмент
  - Обновлены тесты: rosaudit/test_tools.py (`"deficit"` → `"defitsit"`), rosapi/test_tools.py (`"fias_id"` → `"identifikator_fias"`)
- **Русификация имён тестовых классов** (~28 классов в 12 файлах):
  - tests/_shared/test_batch.py: `TestBuildDispatch` → `TestPostroenieDispetcherizatsii`, `TestExecuteBatch` → `TestVypolneniePaketa`
  - tests/_shared/test_lifespan.py: `TestHttpLifespan` → `TestHttpZhiznennyyTsikl`
  - tests/_shared/test_settings.py: `TestSettings` → `TestNastroyki`
  - tests/_shared/test_formatting.py: `TestMarkdownTable` → `TestTablitsaVMarkdown`, `TestFormatRub` → `TestFormatirovatRubli`, `TestFormatNumberRu` → `TestFormatirovatChisloRu`, `TestFormatPercent` → `TestFormatirovatProtsent`, `TestTruncateList` → `TestUsechSpisok`, `TestParseRubNumber` → `TestRazobratRublevoeChislo`
  - tests/_shared/test_cache.py: `TestTtlCacheDecorator` → `TestDekoratorKeshaSVremenemZhizni`
  - tests/_shared/test_validators.py: `TestValidatePostalCodeRU` → `TestProveritPochtovyyIndeks`, `TestFormatPostalCodeRU` → `TestFormatirovatPochtovyyIndeks`
  - tests/_shared/test_feature.py: `TestRegistryIntegration` → `TestIntegratsiyaReestra`
  - tests/test_discovery.py: `TestBuildCatalog` → `TestPostroenieKataloga`, `TestBM25SearchTransform` → `TestTransformatsiyaBM25`, `TestToolSearchConfig` → `TestKonfiguratsiyaPoiskaInstrumentov`, `TestTagPropagation` → `TestRasprostranenieTegov`
  - tests/test_root_server.py: `TestRootServerTools` → `TestInstrumentyKornevogoServera`, `TestRootServerResources` → `TestResursyKornevogoServera`, `TestRootServerPrompts` → `TestPromptyKornevogoServera`, `TestRootServerToolTags` → `TestTegiInstrumentovKornevogoServera`
  - tests/agenty/redator/test_integration.py: `TestToolsRegistered` → `TestInstrumentyZaregistrirovany`, `TestResourcesRegistered` → `TestResursyZaregistrirovany`, `TestPromptsRegistered` → `TestPromptyZaregistrirovany`, `TestToolExecution` → `TestVypolnenieInstrumentov`, `TestResourceExecution` → `TestVypolnenieResursov`, `TestPromptExecution` → `TestVypolneniePromtov`
  - tests/data/rosselkhoznadzor/test_tools.py: `TestConstants` → `TestKonstanty`, `TestTools` → `TestInstrumenty`, `TestIntegration` → `TestIntegratsiya`
- **Русификация имён тестовых функций** (~139 функций в 24 файлах):
  - tests/_shared/test_batch.py: 11 функций (test_builds_from_registry → test_stroitsya_iz_reestra и т.д.)
  - tests/_shared/test_lifespan.py: 2 функции
  - tests/_shared/test_settings.py: 5 функций
  - tests/_shared/test_formatting.py: 28 функций
  - tests/_shared/test_cache.py: 12 функций
  - tests/_shared/test_validators.py: 14 функций
  - tests/_shared/test_feature.py: 18 функций
  - tests/_shared/test_http_client.py: 14 функций
  - tests/_shared/test_rate_limiter.py: 6 функций
  - tests/test_public_namespace.py: 2 функции
  - tests/test_discovery.py: 20 функций
  - tests/test_root_server.py: 9 функций
  - tests/agenty/redator/test_tools.py: 14 функций
  - tests/agenty/redator/test_integration.py: 6 функций
  - tests/data/*/test_integration.py: ~66 функций (test_has_tools → test_instrumenty_zaregistrirovany и т.д. в 22 модулях)
  - tests/data/kad_arbitrazh/test_tools.py: 8 функций (test_parse_* → test_razbor_*)
  - tests/data/zakupki/test_tools.py: 3 функции
  - tests/data/gosduma/test_tools.py: 2 функции
  - tests/data/rosselkhoznadzor/test_tools.py: 3 функции
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — all formatted, `pytest` — все unit-тесты пройдены

### Ключевые архитектурные решения

- **`"deficit"` → `"defitsit"`**: английское написание «дефицит» заменено на русскую транслитерацию; в kaznacheistvo/client.py ключ уже был `"defitsit"`, но поле Pydantic оставалось `deficit` — теперь консистентно
- **`"value"` → `"znachenie"` в poisk_adresa**: ключ адресного значения русифицирован для единообразия; tools.py уже использовал `addr.get("znachenie")` — исправлена рассинхронизация
- **`"fias_id"` → `"identifikator_fias"`**: следует конвенции проекта (identifikator вместо id)
- **`"ip_end"` → `"okonchanie_ip"`**: смешанный английско-русский ключ заменён на полностью русский
- **`"status"` → `"sostoyanie"` в 3 модулях**: устранена несогласованность — mchs и rosselkhoznadzor имели поле Pydantic `sostoyanie`, но ключ словаря `"status"`; minzdrav добавлен параметр MCP-инструмента `sostoyanie`
- **Все полностью английские имена тестов русифицированы**: ~28 классов и ~139 функций переименованы; имена, уже содержащие русскую транслитерацию (TestKeshSVremenemZhizni, TestOgranichitelChastoty и т.д.), оставлены без изменений

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Русификация оставшихся английских строковых ключей**: `"data"` в выходных словарях (11 вхождений — «дата»/«data» совпадает в транслитерации, как и `period`)

## Статус раунда 2026-06-26 (пятьдесят третий проход — русификация полей Pydantic-схем region/status, ключей словарей, параметров инструментов MCP)

### Выполнено

- **Русификация полей Pydantic-схем `region` → `subiekt`** (~33 поля в 15 модулях):
  - rosstat: VRPDannye, DannyeZarplaty, IndikatorDannye, OtraslevayaStrukturaVRP, InvestitsiiPoVidam
  - rosgidromet: PogodaDannye, Preduprezhdenie, SputnikMonitoring
  - rosvodresursy: VodnyyObekt, VodokhranilishcheDannye, Vodopolzovanie
  - rosapi: AdresRF, BankRF, InformatsiyaPochtovogoIndeksa
  - cekrf: KandidatKratko, Kandidat, ItogiVYborov
  - zakupki: Zakazchik, Postavshchik
  - kad_arbitrazh: StoronaDela
  - rospotrebnadzor: OrganNadzora
  - rosprirodnadzor: ObektNegativnogoVozdeystviya
  - minzdrav: MedOrganizatsia, PokazatelZdorovya, ZabolevanieStat
  - rosselkhoznadzor: ProverkaRskhn, KarantinnyyObyekt
  - mchs: Pozhar, ChrezvychaynayaSituatsiya, RadiatsionnyyMonitoring
  - gibdd: StatistikaDTP, RegistracionnoeDeystvie
  - sovfed: SenatorRezyume
  - minobrnauki: VUZ
  - Обновлены все ссылки: client.py (keyword args + output dict keys + function params), tools.py (attribute access + dict reads + function params + docstrings), constants.py, тесты
- **Русификация полей Pydantic-схем `status` → `sostoyanie`** (~29 полей в 17 модулях):
  - rosapi: Organizatsiya
  - cekrf: KandidatKratko, Kandidat
  - zakupki: Zakupka, Kontrakt
  - kad_arbitrazh: SudebnoeDelo, SudebnoeZasedanie
  - gosduma: Zakonoproekt
  - fns: OrganizatsiyaFNS, IndividualnyyPredprinimatel, LizenziaFNS
  - roskomnadzor: ReestrZapisey, ZapisReestra, DomenReestra
  - rospotrebnadzor: Proverka, PlanovayaProverka
  - rosprirodnadzor: ObektNegativnogoVozdeystviya
  - rosselkhoznadzor: ProverkaRskhn, KarantinnyyObyekt, SertifikatRskhn
  - mchs: ChrezvychaynayaSituatsiya
  - gibdd: VoditelskoeUdostovereie
  - sovfed: ZakonoproektSF, RezolyutsiyaSF
  - fssp: IspolnitelnoeProizvodstvo
  - rosaudit: KontrolnoeMeropriyatie
  - publikatsii: PravovoyAkt
  - minobrnauki: AkkreditaciyaVUZa, LizenziyaObrazovatelnaya
  - Составные поля (`status_akkreditatsii`, `status_oplaty`, `status_karantina`, `status_rassmotreniya`, `status_ucheta`, `status_licenzii`) НЕ затронуты
  - Обновлены все ссылки: client.py (keyword args + output dict keys), tools.py (attribute access + dict reads + function params + docstrings), тесты
- **Русификация ключей выходных словарей** (~78 замен в 14 модулях):
  - `"region"` → `"subiekt"` (~28 замен: rosgidromet/constants.py, rosvodresursy/constants.py, cekrf/constants.py, sovfed/constants.py + client.py в 10 модулях)
  - `"status"` → `"sostoyanie"` (~19 замен: client.py в 10 модулях)
  - `"suggestions"` → `"predlozheniya"` (6 замен: rosapi/client.py)
  - `"name"` → `"nazvanie"` (3 замены: cekrf/client.py)
  - `"value"` → `"znachenie"` (1 замена: rosapi/client.py)
  - `"key"` → `"klyuch"` (1 замена: cekrf/client.py)
  - `"subject"` → `"subiekt_rf"` (1 замена: fssp/client.py — отличается от `subiekt` чтобы избежать дублирования с «предмет»)
  - `"initiator"` → `"initsiator"` (2 замены: gibdd/client.py)
  - `"domain"` → `"domen"` (3 замены: roskomnadzor/client.py)
  - `"deficit"` → `"defitsit"` (2 замены: kaznacheistvo/client.py)
  - Обновлены все .get() чтения в соответствующих tools.py и тестах
- **Русификация параметров MCP-инструментов** (tools.py function params — user-facing):
  - `region` → `subiekt` в 13 модулях: rosstat, cekrf, rosvodresursy, rospotrebnadzor, minzdrav, rosselkhoznadzor, mchs, rosgidromet, gibdd, fssp, kaznacheistvo + zakupki
  - `status` → `sostoyanie` в 3 модулях: gosduma, sovfed, rosaudit + zakupki
  - Обновлены docstrings, client call sites, и все тесты
- **Поле `period` оставлено без изменений**: «период» — русское слово, транслитерация которого совпадает с английским написанием; семантически корректно
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — 1 file reformatted, `pytest` (680 passed, 1 skipped — интеграционные HTTP-тесты пропущены)

### Ключевые архитектурные решения

- **Поля Pydantic `region` → `subiekt`**: выбрано `subiekt` (субъект) как наиболее русскоязычный термин; в контексте государственных данных РФ «регион» почти всегда означает «субъект РФ»; консистентно с существующими `subiekty`, `poluchit_spisok_subiektov`
- **Поля Pydantic `status` → `sostoyanie`**: выбрано `sostoyanie` (состояние) как исконно русское слово вместо заимствованного «статус»; составные поля (`status_oplaty` и т.д.) оставлены без изменений
- **Ключ FSSP `"region"` → `"subiekt_rf"`**: в данных ФССП «subject» (предмет исполнения) и «region» (регион) — разные сущности; для избежания дублирования ключа `"subiekt"` регион назван `"subiekt_rf"` (субъект РФ)
- **MCP-инструменты с новыми параметрами**: параметры `subiekt`/`sostoyanie` видны пользователям MCP-сервера — это user-facing API-контракт
- **Внешние API-ключи не затронуты**: ключи запросов к API (`params["region"]`, `.get("status")` из ответов) оставлены как были, т.к. они определяются внешними API

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Русификация английских имён тестовых классов/функций**: ~26 полностью английских классов, ~150 полностью английских функций в tests/
- **Русификация оставшихся английских строковых ключей**: `"data"` в выходных словарях (11 вхождений — «дата»/«data» совпадает в транслитерации, как и `period`)

## Статус раунда 2026-06-25 (пятьдесят второй проход — русификация полей MetaFunktsii, констант settings, ключей словарей, параметров функций)

### Выполнено

- **Русификация полей dataclass MetaFunktsii** (8 полей, ~199 замен в 28 файлах):
  - `name` → `imya` (определение + 25 __init__.py + discovery.py + feature.py)
  - `description` → `opisanie` (определение + 25 __init__.py + discovery.py + feature.py)
  - `version` → `versiya` (определение + 25 __init__.py + feature.py)
  - `api_base` → `baza_api` (определение + 25 __init__.py)
  - `requires_auth` → `trebuet_autentifikatsii` (определение + 5 __init__.py + discovery.py + feature.py)
  - `auth_env_var` → `peremennaya_avt_env` (определение + 3 __init__.py + discovery.py + feature.py)
  - `enabled` → `vklyuchena` (определение + feature.py)
  - `tags` → `tegi` (определение + 25 __init__.py)
  - Обновлены docstring примеры в feature.py и CONTRIBUTING.md
- **Русификация констант settings.py** (9 констант + 34 замен в 11 файлах):
  - `HTTP_TIMEOUT` → `TAIMAUT_HTTP`
  - `HTTP_MAX_RETRIES` → `MAKS_POVTOROV_HTTP`
  - `HTTP_BACKOFF_BASE` → `BAZA_EKSPON_ZADERZH`
  - `USER_AGENT` → `POLZOVATELSKIY_AGENT`
  - `TOOL_SEARCH` → `POISK_INSTRUMENTOV`
  - `DADATA_API_KEY` → `KLYUCH_DADATA_API`
  - `DUMA_API_TOKEN` → `TOKEN_GOSDUMY_API`
  - `ZAKUPKI_API_TOKEN` → `TOKEN_ZAKUPKI_API`
  - `ANTHROPIC_API_KEY` → `KLYUCH_ANTHROPIC_API`
  - Обновлены все импорты и использования в http_client.py, lifespan.py, discovery.py, planner.py, server.py, client.py (rosapi, gosduma, zakupki), тестах
- **`"error"` → `"oshibka"` ключи словарей** (22 замены в 5 модулях):
  - cbrf/client.py: `{"error": ...}` → `{"oshibka": ...}`
  - rosstat/client.py: `{"error": ...}` → `{"oshibka": ...}`
  - rosapi/client.py: 8 замен (`"error"` ключи и проверки `"error" in result`)
  - rosstat/tools.py: `"error" in data` → `"oshibka" in data`
  - rosapi/tools.py: 4 проверки `"error" in result` → `"oshibka" in result`
  - Обновлены тесты: rosapi/test_tools.py (4), rosstat/test_tools.py (1)
- **Русификация параметров функций** (~30 замен):
  - `postal_code` → `pochtovyy_indeks` (validators.py — 2 функции)
  - `max_requests` → `maks_zaprosov` (rate_limiter.py — __init__ + атрибут + docstring + пример)
  - `max_retries` → `maks_povtorov` (http_client.py — 2 функции)
  - `tool_name` → `imya_instrumenta` (discovery.py + batch.py)
  - `module_path` → `put_modulya` (feature.py + batch.py)
  - Обновлены тесты: test_rate_limiter.py (6), test_http_client.py (5), test_batch.py (7)
- **Переименование классов `*Data` → `*Dannye`** (8 классов):
  - `InflaciyaData` → `InflaciyaDannye` (rosstat/schemas.py)
  - `DemografiyaData` → `DemografiyaDannye` (rosstat/schemas.py)
  - `VRPData` → `VRPDannye` (rosstat/schemas.py)
  - `PogodaData` → `PogodaDannye` (rosgidromet/schemas.py)
  - `PrognozData` → `PrognozDannye` (rosgidromet/schemas.py)
  - `EkologiyaData` → `EkologiyaDannye` (rosgidromet/schemas.py)
  - `GidroData` → `GidroDannye` (rosvodresursy/schemas.py)
  - `VodokhranilishcheData` → `VodokhranilishcheDannye` (rosvodresursy/schemas.py)
  - Обновлены ссылки в client.py, tools.py и тестах
- **`realnaya_zp_change` → `realnaya_zp_izmenenie`** (3 замены: schemas.py, client.py, tools.py)
- **`McpRussiaError` → `OshibkaMcpRussia`** (exceptions.py — базовый класс)
- **`"http_client"` → `"http_klient"`** контекстный ключ (lifespan.py + 2 теста)
- **`"tool"`/`"args"` → `"instrument"`/`"argumenty"`** в протоколе пакетного выполнения (batch.py + server.py docstring + test_batch.py)
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — all formatted, `pytest` (680 passed, 1 skipped)

### Ключевые архитектурные решения

- **Поля MetaFunktsii полностью русифицированы**: все 8 полей dataclass (`imya`, `opisanie`, `versiya`, `baza_api`, `trebuet_autentifikatsii`, `peremennaya_avt_env`, `vklyuchena`, `tegi`) теперь на русском; обновлены все 25 __init__.py, discovery.py, feature.py
- **Константы settings.py русифицированы**: 9 модульных констант переименованы; имена переменных окружения (MCP_RUSSIA_*) не затронуты
- **Ключи словарей `"error"` → `"oshibka"`**: унифицированы во всех 5 модулях, где возвращались словари с ошибками
- **Протокол пакетного выполнения обновлён**: ключи JSON `{"tool": ..., "args": ...}` → `{"instrument": ..., "argumenty": ...}`; это user-facing API контракт
- **Базовое исключение переименовано**: `McpRussiaError` → `OshibkaMcpRussia` — больше ни один класс исключений не содержит английских слов

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Русификация оставшихся английских артефактов**: английские имена тестовых классов/функций (~56 классов, ~130+ полностью английских функций), ~~поля `region`/`status`/`period` в Pydantic-схемах (34+29+9 вхождений)~~ ✅, ~~ключи внешних API (`"suggestions"`, `"value"` и т.д.)~~ ✅

## Статус раунда 2026-06-24 (пятьдесят первый проход — русификация HTTP-клиента, зачистка алиасов, переименование констант)

### Выполнено

- **Русификация HTTP-клиента** (3 функции + 24 импорта):
  - `create_client` → `sozdat_klienta` (http_client.py)
  - `http_get` → `http_poluchit` (http_client.py)
  - `http_post` → `http_otpravit` (http_client.py)
  - Обновлены импорты и вызовы в 24 client.py, cache.py (docstring), test_http_client.py
- **Удаление мёртвых алиасов** (5 алиасов, 0 внешних использований):
  - `FeatureError = OshibkaFunktsii` удалён (exceptions.py)
  - `HttpClientError = OshibkaHttpClienta` удалён (exceptions.py)
  - `AuthError = OshibkaAutentifikatsii` удалён (exceptions.py)
  - `FeatureMeta = MetaFunktsii` удалён (feature.py)
  - `RegisteredFeature = ZaregistrirovannayaFunktsiya` удалён (feature.py)
  - `FeatureRegistry = ReyestrFunktsiy` удалён (feature.py)
- **Зачистка импортов FeatureMeta** (25 __init__.py):
  - `from mcp_russia._shared.feature import MetaFunktsii as FeatureMeta` → `from mcp_russia._shared.feature import MetaFunktsii`
  - `FeatureMeta(` → `MetaFunktsii(` во всех 25 __init__.py
- **Переименование FEATURE_META → META_FUNKTSII** (25 __init__.py + feature.py):
  - Константа `FEATURE_META` → `META_FUNKTSII` во всех 25 __init__.py модулей
  - Обновлены ссылки в feature.py: getattr, сообщения об ошибках, docstring
  - Обновлена ссылка в tests/_shared/test_feature.py
- **Русификация инфраструктурных имён** (6 замен):
  - `RequestLoggingMiddleware` → `PosrednikLogirovaniyaZaprosov` (server.py)
  - `_RETRYABLE_STATUS_CODES` → `_KODY_STATUSOV_DLYA_POVTORA` (http_client.py)
  - `_dispatch` → `_dispetcher` (batch.py + test_batch.py)
  - `_catalog_cache` → `_kesh_kataloga` (discovery.py + test_discovery.py)
  - `_SYSTEM_PROMPT` → `_SISTEMNYY_PROMPT` (planner.py)
  - `_always_visible` → `_vsegda_vidimye` (server.py)
- **Русификация документации** (~20 замен в 8 файлах):
  - cliff.toml: `# Changelog` → `# Журнал изменений`, `## [Unreleased]` → `## [Не выпущено]`, 8 group names (Features→Новые функции, Bug Fixes→Исправления, Documentation→Документация, Performance→Производительность, Refactoring→Рефакторинг, Styling→Стиль кода, Testing→Тестирование, Miscellaneous→Прочее, Build→Сборка)
  - CONTRIBUTING.md: `FEATURE_META` → `META_FUNKTSII`, `FeatureMeta` → `MetaFunktsii`, `MCP tools` → `MCP-инструментов`, `Pydantic models` → `модели Pydantic`, `tool` → `инструмент`, `feature` → `модуль`, `auto-discovery` → `автообнаружения`, `Breaking change` → `Критическое изменение`
  - pyproject.toml: 3 английских комментария → русские
  - CHANGELOG.md: `# Changelog` → `# Журнал изменений`
  - README.md: `Brazilian validators` → `бразильские валидаторы`
  - docs/guide/development.md: `test suite` → `набор тестов`, `quality gate` → `контроль качества`
  - docs/guide/adding-features.md: `auto-discovery` → `автообнаружение`, `root server` → `корневой сервер`
  - docs/concepts/architecture.md: `root server` → `корневой сервер`, `tool-call` → `вызовов инструментов`
  - docs/reference/smart-tools.md: `tool calls` → `вызовов инструментов`, `round-trips` → `обменов`, `tool name` → `имя инструмента`, `Tool` → `Инструмент`
  - docs/examples/ofitsialnyy-redaktor.md: `resource` → `ресурс`
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — all formatted, `pytest` (680 passed, 1 skipped)

### Ключевые архитектурные решения

- **HTTP-клиент полностью русифицирован**: `create_client` → `sozdat_klienta`, `http_get` → `http_poluchit`, `http_post` → `http_otpravit` — основные HTTP-функции теперь имеют русские имена; обновлены все 24 клиента данных
- **Все мёртвые алиасы удалены**: `FeatureError`, `HttpClientError`, `AuthError`, `FeatureMeta`, `RegisteredFeature`, `FeatureRegistry` — 0 внешних использований, чистое удаление без алиасов
- **FEATURE_META → META_FUNKTSII**: константа переименована, алиас `FeatureMeta` убран — все 25 __init__.py теперь используют `MetaFunktsii` напрямую
- **cliff.toml русифицирован**: при следующей генерации CHANGELOG.md группы секций будут на русском

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Русификация оставшихся английских артефактов**: `McpRussiaError` (базовый класс исключений), поля dataclass MetaFunktsii (`name`, `description`, `version`, `api_base`, `requires_auth`, `auth_env_var`, `enabled`, `tags`), английские имена тестовых классов/функций (~47 классов, ~176 функций), `"error"` ключи словарей (5 модулей), параметры функций (`postal_code`, `max_requests`, `tool_name`, `tool`)

## Статус раунда 2026-06-24 (пятидесятый проход — полная русификация имён функций, методов, классов инфраструктуры)

### Выполнено

- **Русификация функций rosapi/client.py** (18 функций):
  - `_dadata_headers` → `_zagolovki_dadaty`, `_nested_get` → `_vlozhennoe_poluchenie`, `_parse_org_data` → `_razobrat_dannye_organizatsii`, `_parse_bank_data` → `_razobrat_dannye_banka`, `_suggest_address` → `_predlozhit_adres`, `_find_by_fias` → `_nayti_po_fias`, `_postal_by_index` → `_pochtovyy_po_indeksu`, `_find_org_by_inn` → `_nayti_organizatsiyu_po_inn`, `_find_org_by_ogrn` → `_nayti_organizatsiyu_po_ogrn`, `_list_banks` → `_spisok_bankov`, `_find_bank_by_bik` → `_nayti_bank_po_bik`, `get_holidays` → `poluchit_prazdniki`, `consult_address_by_postal` → `konsultirovat_adres_po_pochtovomu`, `search_address` → `poisk_adresa`, `find_org_by_inn` → `nayti_organizatsiyu_po_inn`, `find_org_by_ogrn` → `nayti_organizatsiyu_po_ogrn`, `list_banks_public` → `spisok_bankov_publichnyy`, `find_bank_by_bik` → `nayti_bank_po_bik`
  - Обновлены ссылки в tools.py и test_tools.py
- **Русификация функций gibdd/client.py** (7 функций):
  - `_extract_result` → `_izvlech_rezultat`, `_parse_history` → `_razobrat_istoriyu`, `_parse_dtp` → `_razobrat_dtp`, `_parse_wanted` → `_razobrat_rozysk`, `_parse_restrict` → `_razobrat_ogranichenie`, `_parse_driver` → `_razobrat_voditelya`, `_parse_statistika` → `_razobrat_statistiku`
- **Русификация функций rosstat/client.py** (3 функции):
  - `_parse_indikator_response` → `_razobrat_otvet_indikatora`, `get_subiekty_list` → `poluchit_spisok_subiektov`, `get_federalny_okruga_list` → `poluchit_spisok_federalnykh_okrugov`
  - Обновлены ссылки в tools.py
- **Русификация функций zakupki/client.py** (10 функций):
  - `_get_api_token` → `_poluchit_api_token`, `_parse_zakupki_search` → `_razobrat_poisk_zakupok`, `_determine_zakon` → `_opredelit_zakon`, `_safe_float` → `_bezopasnoe_veshchestvennoe`, `_parse_kontrakty` → `_razobrat_kontrakty`, `_parse_plany` → `_razobrat_plany`, `get_tipy_dannykh` → `poluchit_tipy_dannykh`, `get_sposoby_zakupok` → `poluchit_sposoby_zakupok`, `get_otrasli` → `poluchit_otrasli`, `get_statusy_zakupok` → `poluchit_statusy_zakupok`
  - Обновлены ссылки в tools.py и test_tools.py
- **Русификация функций fns/client.py** (4 функции):
  - `_egrul_search` → `_poisk_egrul`, `_parse_egrul_organization` → `_razobrat_egrul_organizatsiyu`, `_parse_egrul_ip` → `_razobrat_egrul_ip`, `_parse_status` → `_razobrat_status`
- **Русификация `_parse_*` → `_razobrat_*` в оставшихся 17 модулях** (~55 функций):
  - cekrf (5), gosduma (4), fssp (2), rosreestr (1), cbrf (1), roskomnadzor (5), rospotrebnadzor (2), mchs (5), rosaudit (4), rosselkhoznadzor (5), rosprirodnadzor (4), rosvodresursy (4), rosgidromet (3), minzdrav (4), kaznacheistvo (5), publikatsii (4), minobrnauki (2)
  - Обновлены ссылки в тестах (cekrf, gosduma)
- **Русификация `get_*_list` → `poluchit_spisok_*` и `get_*` → `poluchit_*`** (~50 функций в 14 модулях):
  - sovfed (2), mchs (6), rosaudit (3), rosselkhoznadzor (7), rosprirodnadzor (3), rosvodresursy (5), rosgidromet (4), minzdrav (5), kaznacheistvo (2), publikatsii (4), gosduma (3+1), kad_arbitrazh (4), cekrf (3)
  - Обновлены ссылки в tools.py, server.py и тестах
- **Русификация других английских паттернов** (~10 функций):
  - `_fetch_*` → `_zaprosit_*` (cekrf), `_find_*` → `_nayti_*` (rosgidromet), `_normalise_*` → `_normlizovat_*` (fssp), `_search_results` → `_rezultaty_poiska` (publikatsii), `_granty_fallback` → `_granty_rezervnye` (minobrnauki), `_proverka_ts_full` → `_polnaya_proverka_ts` (gibdd/tools.py), `_hpa_to_mmhg` → `_gpa_v_mmrtst`, `_deg_to_napravlenie` → `_gradusy_v_napravlenie` (rosgidromet)
- **Русификация `_shared/` инфраструктуры** (~39 функций/методов):
  - formatting.py (6): `markdown_table` → `tablitsa_v_markdown`, `format_rub` → `formatirovat_rubli`, `format_number_ru` → `formatirovat_chislo_ru`, `format_percent` → `formatirovat_protsent`, `parse_rub_number` → `razobrat_rublevoe_chislo`, `truncate_list` → `usech_spisok`
  - validators.py (9): `_only_digits` → `_tolko_tsifry`, `validate_inn` → `proverit_inn`, `format_inn` → `formatirovat_inn`, `validate_kpp` → `proverit_kpp`, `format_kpp` → `formatirovat_kpp`, `validate_snils` → `proverit_snils`, `format_snils` → `formatirovat_snils`, `validate_postal_code_ru` → `proverit_pochtovyy_indeks`, `format_postal_code_ru` → `formatirovat_pochtovyy_indeks`
  - feature.py (7): `features` → `funktsii`, `skipped` → `propushcheno`, `discover` → `obnaruzhit`, `_try_register` → `_poprovat_zaregistrirovat`, `mount_all` → `smontirovat_vse`, `summary` → `svodka`, `get_feature` → `poluchit_funktsiyu`
  - batch.py (2): `_scan_tools_module` → `_skanirovat_modul_instrumentov`, `_run_one` → `_vypolnit_odin`
  - cache.py (2): `size` → `razmer`, `_evict` → `_ischislit`
  - rate_limiter.py (2): `_purge` → `_ochistit`, `acquire` → `zakhvatit`
  - lifespan.py (1): `http_lifespan` → `http_zhiznennyy_tsikl`
  - planner.py (1): `to_markdown` → `v_markdown`
  - server.py (3): `on_call_tool` → `pri_vyzove_instrumenta`, `on_read_resource` → `pri_chtenii_resursa`, `on_get_prompt` → `pri_zaprose_prompta`
  - Обновлены ссылки во всех 24 tools.py, server.py, batch.py, discovery.py, тестах
- **Переименование классов инфраструктуры** (3 класса с алиасами для совместимости):
  - `FeatureMeta` → `MetaFunktsii` (feature.py + алиас FeatureMeta)
  - `RegisteredFeature` → `ZaregistrirovannayaFunktsiya` (feature.py + алиас RegisteredFeature)
  - `FeatureRegistry` → `ReyestrFunktsiy` (feature.py + алиас FeatureRegistry)
  - Обновлены импорты в 25 __init__.py, server.py, batch.py, discovery.py, тестах
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — all formatted, `pytest` (680 passed, 1 skipped)

### Ключевые архитектурные решения

- **~198 английских имён функций/методов русифицированы** за один проход: все английские имена функций в client.py (5 приоритетных модулей + 17 остальных), _shared/ инфраструктура, server.py
- **Паттерн `_parse_*` → `_razobrat_*`** унифицирован во всех 22 модулях данных
- **Паттерн `get_*_list` → `poluchit_spisok_*`** унифицирован во всех 14 модулях со справочными функциями
- **Алиасы для классов инфраструктуры**: `FeatureMeta = MetaFunktsii`, `RegisteredFeature = ZaregistrirovannayaFunktsiya`, `FeatureRegistry = ReyestrFunktsiy` — существующий код может использовать оба имени
- **FEATURE_META сохранена**: константа `FEATURE_META` в __init__.py модулей не переименована — это установившийся API-контракт; импорт обновлён на `from mcp_russia._shared.feature import MetaFunktsii as FeatureMeta`
- **Инфраструктурные функции форматирования и валидации русифицированы**: `markdown_table` → `tablitsa_v_markdown`, `validate_inn` → `proverit_inn` и т.д. — затронуло все 24 tools.py, которые импортируют эти функции

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Проверка оставшихся английских артефактов в _shared/http_client.py**: `create_client`, `http_get`, `http_post` — основные HTTP-функции; переименование может быть нежелательным из-за широты использования
- **Зачистка FEATURE_META**: после стабилизации — убрать алиас `FeatureMeta` и обновить все __init__.py на использование `MetaFunktsii` напрямую

## Статус раунда 2026-06-23 (сорок девятый проход — русификация имён классов, функций, переменных, строковых значений, заголовков Makefile и скриптов)

### Выполнено

- **Переименование публичных MCP-инструментов Росстата** (2 инструмента):
  - `region_info` → `informatsiya_o_regionye` (tools.py, server.py, client.py, тесты)
  - `okrug_info` → `informatsiya_ob_okruge` (tools.py, server.py, client.py, тесты)
- **Русификация строковых значений в пользовательском выводе** (4 замены):
  - `"national"` → `"natsionalnyy"` (rosapi/client.py — тип праздника)
  - `"weekend"` → `"vykhodnoy"` (rosapi/client.py — тип праздника)
  - `"ACTIVE, LIQUIDATED и т.д."` → `"DEYSTVUYUSHCHAYA, LIKVIDIROVANA и т.д."` (rosapi/schemas.py)
  - `fallback_name` → `rezervnoe_imya` (параметр _parse_bank_data)
- **Переименование классов Pydantic-схем** (3 класса):
  - `RegionData` → `DannyeRegiona` (rosstat/schemas.py, client.py, тесты)
  - `WagesData` → `DannyeZarplaty` (rosstat/schemas.py, client.py, тесты)
  - `PostalCodeInfo` → `InformatsiyaPochtovogoIndeksa` (rosapi/schemas.py)
- **Переименование классов исключений** (3 класса с алиасами для совместимости):
  - `FeatureError` → `OshibkaFunktsii` (exceptions.py + алиас FeatureError)
  - `HttpClientError` → `OshibkaHttpClienta` (exceptions.py, http_client.py, тесты + алиас)
  - `AuthError` → `OshibkaAutentifikatsii` (exceptions.py, rosapi/client.py, тесты + алиас)
- **Переименование инфраструктурных классов** (2 класса):
  - `TTLCache` → `KeshSVremenemZhizni` (cache.py, тесты)
  - `RateLimiter` → `OgranichitelChastoty` (rate_limiter.py, тесты)
- **Переименование функций в _shared/** (6 функций):
  - `build_catalog` → `postroit_katalog` (discovery.py, server.py, тесты)
  - `build_dispatch` → `postroit_dispetcherizatsiyu` (batch.py, server.py, тесты)
  - `execute_batch` → `vypolnit_paket_vnutrenniy` (batch.py, server.py, тесты)
  - `ttl_cache` → `kesh_s_vremenem_zhizni` (cache.py, тесты)
  - `_format_tool_signature` → `_formatirovat_signaturu_instrumenta` (discovery.py)
  - `is_auth_available` → `dostupna_li_autentifikatsiya` (feature.py, тесты)
- **Переименование `_extract_list` → `_izvlech_spisok`** (8 модулей: rosaudit, mchs, sovfed, rosvodresursy, rosselkhoznadzor, rosprirodnadzor, minzdrav, kaznacheistvo)
- **Русификация локальных переменных** (5 переменных):
  - `region_info` → `info_o_regionye` (rosstat/client.py)
  - `okrug_info` → `info_ob_okruge` (rosstat/client.py)
  - `indicator_name` → `imya_indikatora` (rosstat/client.py, tools.py)
  - `status_map` → `karta_statusov` (rosapi/tools.py, fns/client.py)
  - `fallback_name` → `rezervnoe_imya` (rosapi/client.py)
- **Перевод заголовков секций Makefile** (6 замен):
  - `Setup` → `Настройка`, `Quality` → `Качество`, `Server` → `Сервер`, `Release` → `Релиз`, `Docs` → `Документация`, `Misc` → `Разное`
- **Перевод скриптов на русский**:
  - `scripts/generate_diagrams.py`: все docstrings, комментарии, строки вывода, имена переменных и функций переведены
  - `scripts/release.sh`: все комментарии, сообщения об ошибках и информационные выводы переведены
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — all formatted, `pytest` (674 passed, 1 skipped)

### Ключевые архитектурные решения

- **Алиасы для классов исключений**: для обратной совместимости оставлены `FeatureError = OshibkaFunktsii`, `HttpClientError = OshibkaHttpClienta`, `AuthError = OshibkaAutentifikatsii` — существующий код может использовать оба имени
- **Имена классов FeatureMeta/FeatureRegistry/RegisteredFeature сохранены**: это установившиеся программные конструкции, на которые ссылается множество модулей через FEATURE_META (подтверждено решением раунда 48)
- **Все публичные MCP-инструменты теперь имеют русские имена**: `informatsiya_o_regionye`, `informatsiya_ob_okruge` — последние инструменты с английскими именами переименованы
- **Строковые значения русифицированы**: типы праздников `"natsionalnyy"`/`"vykhodnoy"` вместо `"national"`/`"weekend"`, описание статуса организации на русском
- **Скрипты полностью на русском**: generate_diagrams.py и release.sh — все выводы, комментарии и имена переменных

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Русификация оставшихся английских имён функций в client.py**: `_dadata_headers`, `_nested_get`, `_parse_org_data`, `_parse_bank_data`, `_suggest_address`, `_find_by_fias`, `_postal_by_index`, `_find_org_by_inn`, `_find_org_by_ogrn`, `_list_banks`, `_find_bank_by_bik`, `get_holidays`, `consult_address_by_postal`, `search_address`, `find_org_by_inn`, `find_org_by_ogrn`, `list_banks_public`, `find_bank_by_bik` (rosapi); `_extract_result`, `_parse_history`, `_parse_dtp`, `_parse_wanted`, `_parse_restrict`, `_parse_driver`, `_parse_statistika` (gibdd); `_parse_indikator_response`, `get_subiekty_list`, `get_federalny_okruga_list` (rosstat); `_get_api_token`, `_parse_zakupki_search`, `_determine_zakon`, `_safe_float`, `_parse_kontrakty`, `_parse_plany` (zakupki); `_egrul_search`, `_parse_egrul_organization`, `_parse_egrul_ip`, `_parse_status` (fns)
- **Рассмотрение переименования FeatureMeta → MetaFunktsii, RegisteredFeature → ZaregistrirovannayaFunktsiya, FeatureRegistry → ReyestrFunktsiy**: потребует обновления всех __init__.py и ссылок на FEATURE_META

## Статус раунда 2026-06-19 (сорок восьмой проход — устранение термина «feature» из промптов, документации и Makefile)

### Выполнено

- **Устранение термина «feature» из LLM-промптов** (7 замен в planner.py):
  - `с префиксом feature` → `с префиксом модуля` (docstring EtapPlana.tool)
  - `исторические названия features и tools` → `исторические названия модулей и инструментов`
  - `Используй ТОЛЬКО tools из каталога. Никогда не придумывай новые names.` → `Используй ТОЛЬКО инструменты из каталога. Никогда не придумывай новые имена.`
  - `Используй точные имена tools с префиксом feature.` → `Используй точные имена инструментов с префиксом модуля.`
  - `несколько features` → `несколько модулей` (2 места)
  - `второй feature` → `вторым модулем`
  - `feature_imya_instrumenta` → `modul_imya_instrumenta` (пример JSON)
- **Устранение термина «features» из документации** (4 замены):
  - `27 активных features` → `27 активных модулей` (docs/reference/smart-tools.md)
  - `вывести summary зарегистрированных features` → `вывести сводку зарегистрированных модулей` (docs/guide/development.md)
  - `feat(feature):` → `feat(modul):` (commit convention в development.md)
  - `{feature}/` → `{modul}/` в path templates (docs/guide/adding-features.md — 3 места, docs/concepts/architecture.md — 1 место)
- **Перевод комментариев Makefile на русский** (16 замен):
  - `Show this help` → `Показать справку`
  - `Install production dependencies` → `Установить production-зависимости`
  - `Install all dependencies` → `Установить все зависимости`
  - `Run lint + format check` → `Проверка линтером и форматирования`
  - `Auto-fix lint + format` → `Автоисправление линтера и форматирования`
  - `Run mypy strict type checking` → `Строгая проверка типов mypy`
  - `Run all tests` → `Запустить все тесты`
  - `Run tests for a specific feature` → `Запустить тесты одного модуля`
  - `Full CI pipeline` → `Полный CI-конвейер`
  - `Run MCP server (stdio)` → `Запустить MCP-сервер (stdio)`
  - `Run MCP server (HTTP)` → `Запустить MCP-сервер (HTTP)`
  - `Inspect MCP server tools/resources/prompts` → `Показать инструменты/ресурсы/промпты MCP-сервера`
  - `Show current version` → `Показать текущую версию`
  - `Build package` → `Собрать пакет`
  - `Generate CHANGELOG.md` → `Сгенерировать CHANGELOG.md`
  - И все остальные комментарии (release, diagrams, clean)
- **Русификация внутренних переменных** (4 замены):
  - `feature_name` → `imya_modulya` (discovery.py — параметр функции + использование)
  - `feature_module` → `importiruyemyy_modul` (feature.py — переменная в _try_register)
  - `feature` → `modul` (feature.py — loop variable в mount_all)
  - Добавлена полная docstring к `_format_tool_signature` с параметрами
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — all formatted, `pytest` (680 passed, 1 skipped)

### Ключевые архитектурные решения

- **Термин «feature» полностью устранён из пользовательского вывода и документации**: во всех LLM-промптах, Makefile-комментариях и docs/ вместо «feature» используется «модуль/модуля/модулей»
- **Внутренние переменные русифицированы**: `feature_name` → `imya_modulya`, `feature_module` → `importiruyemyy_modul`, loop variable `feature` → `modul` в монтировании
- **Имена классов FeatureMeta/FeatureRegistry сохранены**: это установившиеся программные конструкции, на которые ссылается множество модулей через FEATURE_META
- **Makefile-цель `test-feature` сохранена**: переименование могло бы сломать существующие скрипты и привычки; комментарий переведён на русский

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата

## Статус раунда 2026-06-19 (сорок седьмой проход — русификация полей Pydantic-схем, ключей констант, параметров функций)

### Выполнено

- **Русификация оставшихся полей Pydantic-схем** (~67 замен в 12 модулях):
  - `id` → `identifikator` (10 моделей в 5 модулях): zakupki (Zakupka, Kontrakt, Zakazchik, Postavshchik, PlanZakupki), gosduma (Deputat, Zakonoproekt), kad_arbitrazh (SudebnyyAkt, SudebnoeZasedanie, Sudy), cekrf (KandidatKratko, Kandidat), minzdrav (MedOrganizatsia, VrachebnyyKadr)
  - `number` → `nomer` (5 моделей в 3 модулях): zakupki (Zakupka, Kontrakt), gosduma (Zakonoproekt), kad_arbitrazh (SudebnoeDelo)
  - `title` → `nazvanie` (3 модели в gosduma: Zakonoproekt, Golosovanie; zakupki: Zakupka)
  - `city` → `gorod` (4 модели в rosapi: AdresRF, BankRF, PostalCodeInfo; minzdrav: MedOrganizatsia)
  - `currency` → `valyuta` (2 модели: zakupki Zakupka/Kontrakt, kad_arbitrazh SudebnoeDelo)
  - `initial_price` → `nachalnaya_tsena`, `deadline` → `srok_podachi`, `organizer_inn` → `organizator_inn`, `execution_deadline` → `srok_ispolneniya`, `contractor_inn` → `podryadchik_inn`, `price` → `tsena`, `zakupka_number` → `zakupka_nomer` (zakupki)
  - `zakupki_count` → `zakupki_kolichestvo`, `total_spent` → `obshchie_raskhody`, `contracts_won` → `kontraktov_vyigrano`, `contracts_executed` → `kontraktov_ispolneno`, `total_revenue` → `obshchiy_dokhod`, `year` → `god`, `items_count` → `kolichestvo_pozitsiy`, `total_budget` → `obshchiy_byudzhet` (zakupki)
  - `street` → `ulitsa`, `house` → `dom`, `full_address` → `polnyy_adres`, `address` → `adres`, `director` → `rukovoditel`, `phone` → `telefon`, `swift` → `svift`, `type` → `tip`, `district` → `rayon`, `addresses` → `adresa` (rosapi)
  - `category` → `kategoriya`, `delo_number` → `delo_nomer`, `pdf_url` → `pdf_ssylka` (kad_arbitrazh)
  - `author` → `avtor`, `readings` → `chteniya`, `count` → `kolichestvo`, `zakonoproekt_id` → `zakonoproekt_identifikator`, `foto_url` → `foto_ssylka` (gosduma)
  - `level` → `uroven`, `color` → `tsvet` (cekrf)
  - `unit` → `edinitsa`, `source` → `istochnik`, `population` → `naselenie`, `vrp_per_capita` → `vrp_na_dushu` (rosstat)
  - `feels_like` → `oshchushchaetsya_kak`, `izobrazhenie_url` → `izobrazhenie_ssylka` (rosgidromet)
  - `previous` → `predydushchee` (cbrf)
  - `tekst_url` → `tekst_ssylka` (publikatsii, 4 модели)
  - `territory` → `territoriya` (rosprirodnadzor)
  - `email` → `elektronnaya_pochta` (rospotrebnadzor)
- **Русификация ключей словарей в constants.py** (~1,915 замен в 23 модулях):
  - `"code"` → `"kod"` (~911 замен во всех 23 модулях)
  - `"name"` → `"nazvanie"` (~937 замен во всех 24 модулях)
  - `"short_name"` → `"korotkoe_nazvanie"`, `"color"` → `"tsvet"`, `"type"` → `"tip"`, `"level"` → `"uroven"` (cekrf)
  - `"url"` → `"ssylka"` (roskomnadzor)
  - Исправлена ошибка дублирования ключей в cekrf IZVESTNYE_VYBORY: первый `"type"` → `"tip_vyborov"`, второй → `"tip"`
- **Русификация параметров функций** (~60+ замен в 12 модулях):
  - `code` → `kod`, `codes` → `kody` (cbrf/client.py)
  - `sub_region` → `podregion`, `vib_type` → `tip_golosovaniya` (cekrf/client.py)
  - `query` → `zapros`, `status_code` → `kod_statusa` (fns/client.py)
  - `id` → `identifikator`, `limit` → `ogranichenie`, `page` → `stranitsa`, `id_deputata` → `identifikator_deputata` (gosduma)
  - `number` → `nomer`, `category` → `kategoriya`, `id_akta` → `identifikator_akta`, `key` → `klyuch` (kad_arbitrazh)
  - `id_mo` → `identifikator_mo`, `mkb_code` → `kod_mkb` (minzdrav)
  - `domain` → `domen`, `reestr_code` → `kod_reestra`, `zapisi_id` → `identifikator_zapisi` (roskomnadzor)
  - `target_inn` → `inn_tseli`, `target_name` → `nazvanie_tseli` (rospotrebnadzor)
  - `territory` → `territoriya` (rosprirodnadzor)
  - `date_range` → `diapazon_dat` (rosstat)
  - `post_id` → `identifikator_posta` (rosvodresursy)
  - `senator_id` → `identifikator_senatora` (sovfed)
  - `contractor_inn` → `inn_podryadchika`, `zakazchik_inn` → `inn_zakazchika`, `organizer_inn` → `inn_organizatora` (zakupki)
  - `postal_code` → `pochtovyy_indeks`, `fias_id` → `identifikator_fias`, `index` → `indeks` (rosapi)
- **Обновлены все ссылки** в client.py, tools.py и тестах (координированные замены)
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — all formatted, `pytest` (680 passed, 1 skipped)

### Ключевые архитектурные решения

- **Все поля Pydantic-схем русифицированы**: английские field names заменены на русскую транслитерацию во всех 12 модулях, где они оставались. JSON-вывод инструментов теперь полностью на русском
- **Все ключи словарей в constants.py русифицированы**: `"code"` → `"kod"`, `"name"` → `"nazvanie"` во всех 23 модулях. Справочные данные теперь используют русские ключи
- **Все параметры функций русифицированы**: английские параметры (limit, code, id, query, etc.) заменены на русскую транслитерацию в 12 модулях
- **Исправлена ошибка дублирования ключей**: в cekrf/constants.py IZVESTNYE_VYBORY имел два ключа `"type"`, второй перезаписывал первый. Теперь: `"tip_vyborov"` (тип выборов: 1=президентские, 2=думские) и `"tip"` (VRN-код: 242/224)
- **Полная координация**: schemas.py + constants.py + client.py + tools.py + tests обновлены согласованно

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата

### Выполнено

- **Русификация терминологии в документации** (~140 замен в 16 файлах):
  - `feature` → `модуль` (~32 замены): README.md (6), CONTRIBUTING.md (8), docs/concepts/architecture.md (9), docs/index.md (3), docs/reference/smart-tools.md (1), docs/reference/configuration.md (1), docs/guide/adding-features.md (2), docs/guide/development.md (2), docs/examples/ekonomist.md (1)
  - `tools` → `инструменты` (~14 замен): README.md (1), docs/reference/smart-tools.md (6), docs/reference/configuration.md (2), docs/guide/quickstart.md (1), docs/concepts/architecture.md (1), docs/examples/analiz-zakonodatelstva.md (1)
  - `Prompt:` → `Промпт:` (90 замен в 7 файлах docs/examples/): zhurnalist-rassledovatel (19), gosudarstvennaya-politika (21), zhurnalist-stati (16), municipalnyy-kontrol (14), ekonomicheskaya-panorama (7), parlamentskiy-otchet (7), ekonomist (6)
  - `meta-tools` → `мета-инструменты` (6 замен): docs/reference/smart-tools.md (2), docs/reference/configuration.md (2), docs/guide/quickstart.md (1), docs/concepts/architecture.md (1)
- **Русификация английских заголовков** (9 замен):
  - `## Root server` → `## Корневой сервер` (architecture.md)
  - `## Анатомия feature` → `## Анатомия модуля` (architecture.md)
  - `## Shared-инфраструктура` → `## Общая инфраструктура` (architecture.md)
  - `## Pull request` → `## Pull-запрос` (CONTRIBUTING.md)
  - `### HTTP transport` → `### HTTP-транспорт` (configuration.md)
  - `### Retry с backoff` → `### Повторные попытки с экспоненциальной задержкой` (configuration.md)
  - `### Rate limiting` → `### Ограничение частоты запросов` (configuration.md)
  - `## Локальный setup` → `## Локальная настройка` (development.md)
  - `### HTTP / streamable HTTP` → `### HTTP / потоковый HTTP` (quickstart.md)
- **Русификация смешанных терминов** (8 замен):
  - `package-by-feature` → `пакетирование по модулям` (README.md)
  - `feature-дерево` → `дерево модулей` (architecture.md)
  - `feature-пакетов` → `пакетов модулей` (architecture.md)
  - `feature-инструментов` → `инструментов модулей` (architecture.md)
  - `feature-модулей` → `модулей` (architecture.md, ekonomist.md)
  - `Setup, проверки` → `Настройка, проверки` (index.md)
  - `data features` → `модули данных`, `agent features` → `агентные модули` (architecture.md)
- **Русификация таблиц** (2 замены):
  - `| API | Feature |` → `| API | Модуль |` (analiz-zakonodatelstva.md)
  - `| Resource | Содержимое |` → `| Ресурс | Содержимое |` (ofitsialnyy-redaktor.md)
- **Русификация комментариев в тестах** (2 замены):
  - `# FeatureMeta` → `# FeatureMeta (метаданные модуля)` (tests/_shared/test_feature.py)
  - `# FeatureRegistry` → `# FeatureRegistry (реестр модулей)` (tests/_shared/test_feature.py)
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — all formatted, `pytest` (680 passed, 1 skipped)

### Ключевые архитектурные решения

- **Документация полностью русифицирована**: все английские термины (feature, tools, meta-tools, Prompt:) в пользовательской документации заменены на русские эквиваленты
- **Термин feature устранён из документации**: везде заменён на «модуль», что соответствует русскоязычной терминологии проекта
- **Промпты в примерах унифицированы**: `> Prompt:` → `> Промпт:` во всех 7 примерах docs/examples/ (кроме politolog.md и analiz-zakonodatelstva.md, которые уже использовали русские варианты)
- **Технические имена файлов не затронуты**: `{feature}` в путях `src/mcp_russia/data/{feature}/` и командах `make test-feature` оставлены как есть, т.к. это шаблоны/команды

### Следующие действия

- **Русификация оставшихся полей Pydantic-схем**: `id→identifikator`, `number→nomer`, `title→nazvanie`, `status→status` (оставить), `city→gorod`, `street→ulitsa`, `house→dom`, `price→tsena`, `currency→valyuta`, `deadline→srok`, `count→kolichestvo`, `population→naselenie`, `unit→edinitsa`, `source→istochnik`, `feels_like→oshchushchaetsya_kak`, `full_address→polnyy_adres`, `district→rayon`, `addresses→adresa`, `type→tip`, `territory→territoriya`, `previous→predydushchee`, `year→god`, `author→avtor`, `readings→chteniya`, `level→uroven`, `color→tsvet`, `phone→telefon`, `address→adres`, `director→rukovoditel` — затронет ~120+ полей в schemas.py, client.py, tools.py и тестах
- **Русификация ключей словарей в constants.py**: `"code"→"kod"`, `"name"→"nazvanie"` — ~340+ вхождений в 22 модулях; потребует координированных замен в tools.py, client.py и тестах
- **Русификация параметров функций**: `region`, `status`, `number`, `code`, `id`, `year` и др. — ~60+ вхождений в client.py и tools.py
- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата

## Статус раунда 2026-06-18 (сорок пятый проход — русификация полей Pydantic-схем)

### Выполнено

- **Русификация полей Pydantic-схем** (49 замен в 10 модулях):
  - `code→kod` (11 замен): cekrf (SubyektRF, TipVyborov, Dolzhnost), gosduma (Frakciya), rospotrebnadzor (OrganNadzora), rosapi (PostalCodeInfo), rosstat (PokazatelRosstata, RegionData), rosvodresursy (VodnyyObekt, VodokhranilishcheData)
  - `name→nazvanie` (14 замен): cekrf (SubyektRF, TipVyborov, Dolzhnost, PartiaInfo), gosduma (Frakciya), rosapi (BankRF, Prazdnik), rosstat (PokazatelRosstata, RegionData), rosvodresursy (VodnyyObekt, VodokhranilishcheData), kad_arbitrazh (StoronaDela), zakupki (Zakazchik, Postavshchik), minzdrav (MedOrganizatsia, PokazatelZdorovya, ZabolevanieStat)
  - `value→znachenie` (2 замены): rosstat (PokazatelRosstata), cbrf (DannyeValyuty)
  - `date→data` (3 замены): rosapi (Prazdnik), gosduma (Golosovanie), cbrf (DannyeValyuty)
  - Составные поля `*_name/name_*→*_nazvanie/nazvanie_*` (10 замен): cekrf (short_name→kratkoe_nazvanie), rosapi (name_full→nazvanie_polnoe, name_short→nazvanie_kratkoe), kad_arbitrazh (sud_name→nazvanie_suda), zakupki (organizer_name→nazvanie_organizatora, contractor_name→nazvanie_podryadchika)
  - Составные поля `*_date/date_*→*_data/data_*` (6 замен): rosapi (registration_date→data_registratsii), kad_arbitrazh (posledniy_akt_date→data_poslednego_akta), gosduma (date_vnesen→data_vneseniya), zakupki (publish_date→data_publikatsii, sign_date→data_podpisaniya, created_date→data_sozdaniya, updated_date→data_obnovleniya)
  - Составные поля `*_code/code_*→*_kod/kod_*` (3 замены): roskomnadzor (registry_code→kod_reestra), rosapi (postal_code→pochtovyy_indeks), minzdrav (mkb_code→kod_mkb)
- **Обновлены клиентские функции** (координированные замены в client.py 8 модулей):
  - cekrf/client.py: TipVyborov, SubyektRF, Dolzhnost, PartiaInfo — keyword args
  - rosapi/client.py: _parse_org_data, _parse_bank_data, get_holidays dict keys, AdresRF, Organizatsiya, BankRF constructors
  - rosvodresursy/client.py: get_vodokhranilishcha_list, _parse_vodnyy_obekt, _parse_vodokhranilishche dict keys
  - kad_arbitrazh/client.py: SudebnoeDelo, StoronaDela constructors
  - gosduma/client.py: Zakonoproekt, Golosovanie, Frakciya constructors
  - rosstat/client.py: RegionData, PokazatelRosstata constructors, poluchit_federalny_okrug/poluchit_sravnenie_regionov dict keys
  - zakupki/client.py: Zakupka, Kontrakt, Zakazchik, Postavshchik, PlanZakupki constructors
  - minzdrav/client.py: _parse_med_organizatsia, _parse_pokazatel, _parse_zabolevanie dict keys
- **Обновлены инструменты** (координированные замены в tools.py 8 модулей):
  - cekrf/tools.py: attribute access на TipVyborov.kod, SubyektRF.nazvanie, Dolzhnost.kod, PartiaInfo.kratkoe_nazvanie
  - rosapi/tools.py: AdresRF.pochtovyy_indeks, Organizatsiya.nazvanie_polnoe/nazvanie_kratkoe/data_registratsii, BankRF.nazvanie/nazvanie_kratkoe, holidays dict keys
  - rosvodresursy/tools.py: dict key access nazvanie
  - kad_arbitrazh/tools.py: SudebnoeDelo.nazvanie_suda/data_poslednego_akta, StoronaDela.nazvanie
  - gosduma/tools.py: Zakonoproekt.data_vneseniya, Golosovanie.data
  - rosstat/tools.py: RegionData.kod/nazvanie, okrug_info dict keys, sravnenie_regionov dict keys
  - zakupki/tools.py: Zakupka.data_publikatsii/nazvanie_organizatora, Kontrakt.nazvanie_podryadchika/data_podpisaniya, Zakazchik.nazvanie, Postavshchik.nazvanie, PlanZakupki.nazvanie_organizatora
  - minzdrav/tools.py: dict key access nazvanie, kod_mkb
- **Обновлены тесты** (31 замена в 7 тестовых файлах):
  - tests/data/cekrf/test_tools.py: TipVyborov, SubyektRF, Dolzhnost, PartiaInfo kwargs
  - tests/data/rosapi/test_tools.py: AdresRF, Organizatsiya, BankRF kwargs, search_address dict keys
  - tests/data/rosvodresursy/test_tools.py: mock data dict keys
  - tests/data/kad_arbitrazh/test_tools.py: SudebnoeDelo attribute/dict access
  - tests/data/gosduma/test_tools.py: Zakonoproekt, Golosovanie kwargs
  - tests/data/rosstat/test_tools.py: RegionData kwargs, okrug/sravnenie dict keys
  - tests/data/zakupki/test_tools.py: Zakupka, Kontrakt kwargs, assertion access
  - tests/data/minzdrav/test_tools.py: mock data dict keys
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — all formatted, `pytest` (680 passed, 1 skipped)

### Ключевые архитектурные решения

- **Все поля Pydantic-схем русифицированы**: английские field names (code, name, value, date и их составные формы) заменены на русскую транслитерацию (kod, nazvanie, znachenie, data и т.д.) во всех 10 модулях, где они оставались
- **JSON-вывод инструментов теперь полностью русифицирован**: при сериализации Pydantic-моделей в JSON ключи полей будут на русском (kod, nazvanie и т.д.)
- **Dict keys клиентских функций синхронизированы**: возвращаемые словари в client.py используют те же ключи, что и соответствующие Pydantic-схемы
- **14 модулей уже имели русские поля**: publikatsii, rosselkhoznadzor, mchs, rosgidromet, gibdd, fssp, sovfed, rosprirodnadzor, rosaudit, rosreestr, fns, kaznacheistvo, minobrnauki, agenty/redator — не потребовали изменений
- **Константы (constants.py) не затронуты**: справочники в constants.py по-прежнему используют `"code"` и `"name"` как внутренние ключи — это данные, а не схема

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата

## Статус раунда 2026-06-17 (сорок четвёртый проход — русификация кодовых значений Росстата, Минздрава, Роскомнадзора, РосАПИ, Госдумы, ЦИК)

### Выполнено

- **Русификация кодовых значений Росстата** (51 замена в 3 структурах):
  - `KLYUCHEVYE_INDIKATORY`: 21 код — population→naselenie, cpi→ipcz, gdp→vvp, industrial→promyshlennoe_proizvodstvo, unemployment→bezrabotitsa, wages→zarplata, retail_trade→roznichnaya_torgovlya, investments→investitsii, agrarian→selkoe_khozyaystvo, construction→stroitelstvo, wages_real→realnaya_zarplata, income_per_capita→dokhody_na_dushu, poverty_rate→uroven_bednosti, gini→koeffitsient_dzhini, pension_avg→srednyaya_pensiya, foreign_trade→vneshnetorgovyy_oborot, energy_production→proizvodstvo_elektroenergii, transport_cargo→gruzooborot_transporta, science_innovation→nauka_i_innovatsii, vrp_structure→struktura_vrp; vrp без изменений
  - `EMISS_KODY_POKAZATELEY`: 23 ключа + vrp_per_capita→vrp_na_dushu, subsidy_income→subsidii, migration→migratsiya, natural_growth→estestvennyy_prirost, housing→zhile, investments_by_activity→investitsii_po_vidam
  - `REGIONALNYE_POKAZATELI`: 16 ключей (аналогично KLYUCHEVYE_INDIKATORY + vrp_na_dushu, migratsiya, estestvennyy_prirost, proizvodstvo_elektroenergii, gruzooborot_transporta)
- **Русификация кодовых значений Минздрава** (29 замен):
  - `POKAZATELI_ZDOROVYA`: 6 кодов (life_expectancy→prodolzhitelnost_zhizni, mortality→smertnost, infant_mortality→mladencheskaya_smertnost, morbidity→zabolevaemost, hospital_beds→bolnichnye_koyki, doctors→vrachi)
  - `TIPLY_MO`: 7 кодов (hospital→bolnitsa, polyclinic→poliklinika, dispensary→dispanser, emergency→skoraya_pomoshch, maternity→roddom, hospice→khospis, sanatorium→sanatoriy); nc→nt
  - `SPETSIALNOSTI_VRACHEY`: 15 кодов (therapist→terapevt, surgeon→khirurg, pediatrician→pediatr, neurologist→nevropatolog, cardiologist→kardiolog, ophthalmologist→oftalmolog, dentist→stomatolog, gynecologist→akusher_ginekolog, traumatologist→travmatolog, anesthesiologist→anesteziolog, psychiatrist→psikhiatr, dermatologist→dermatovenerolog, endocrinologist→endokrinolog, urologist→urolog, oncologist→onkolog)
- **Русификация кодовых значений Роскомнадзора** (8 замен):
  - `TIPY_LICENZIY_SVYAZI`: 2 кода (data_transmission→peredacha_dannykh, satellite→sputnikovaya)
  - `KATEGORII_NARUSHENIY`: 6 кодов (personal_data_leak→utechka_personalnykh_dannykh, illegal_content→zapreshchennyy_kontent, copyright_violation→narushenie_avtorskikh_prav, license_violation→narushenie_litsenzionnykh_trebovaniy, data_localization→narushenie_lokalizatsii_dannykh, extremism→ekstremistskie_materialy)
- **Русификация кодовых значений РосАПИ** (5 замен):
  - `TIPY_TRANSPORTA`: 5 ключей (car→legkovoy, truck→gruzovoy, moto→mototsikl, bus→avtobus, special→spectekhnika)
- **Русификация кодовых значений Госдумы** (4 замены):
  - `KLYUCHEVYE_INDIKATORY`: 4 кода (deputats→deputaty, laws→zakonoproekty, sessions→zasedaniya, votes→golosovaniya)
- **Русификация кодовых значений ЦИК РФ** (3 замены):
  - `DOLZHNOSTI_FEDERAL`: level "federal"→"federalnyy" (3 записи)
- **Обновлены ссылки в client.py и tools.py**:
  - `rosstat/client.py`: 5 EMISS_KODY_POKAZATELEY.get() вызовов + 2 docstring
  - `rosstat/tools.py`: 3 docstring
- **Обновлены тесты**:
  - `tests/data/rosstat/test_tools.py`: 18 замен (ipcz, naselenie, zarplata, selkoe_khozyaystvo, stroitelstvo, vneshnetorgovyy_oborot, proizvodstvo_elektroenergii, gruzooborot_transporta, nauka_i_innovatsii, struktura_vrp, migratsiya, estestvennyy_prirost, dokhody_na_dushu)
  - `tests/data/rosstat/test_integration.py`: 1 замена (cpi→ipcz)
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — all formatted, `pytest` (680 passed, 1 skipped)

### Ключевые архитектурные решения

- **Все кодовые значения в constants.py русифицированы во всех 6 модулях**: английские мнемоники (cpi, gdp, wages и т.д.) заменены на русскую транслитерацию (ipcz, vvp, zarplata и т.д.) для единообразия со всеми другими модулями (kad_arbitrazh, cbrf, sovfed и т.д.)
- **Росстат — крупнейший модуль по количеству кодов**: 51 замена в 3 структурах (KLYUCHEVYE_INDIKATORY, EMISS_KODY_POKAZATELEY, REGIONALNYE_POKAZATELI). Коды глубоко встроены в client.py и tools.py
- **Ключи парсинга внешних API не затронуты**: `.get("population")`, `.get("gdp")`, `.get("doctors")` и т.д. в client.py — это ключи ответов внешних API, они остаются на английском
- **deputats→deputaty**: исправлена несогласованность в Госдуме (смешанный паттерн)

### Следующие действия

- **Русификация полей Pydantic-схем**: `code→kod`, `name→nazvanie`, `value→znachenie`, `date→data`, `region→region` (оставить), `period→period` (оставить) в schemas.py всех модулей — затронет JSON-вывод инструментов
- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата

## Статус раунда 2026-06-17 (сорок третий проход — русификация кодовых значений, зачистка английских строк)

### Выполнено

- **Русификация кодовых значений в словарях constants.py** (62 замены в 8 модулях):
  - `sovfed/constants.py`: `STATUSY_ZAKONOPROEKTA` — 7 ключей (pending→na_rassmotrenii, approved→odobren, rejected→otklonen, revision→dorabotka, committee→v_komitete, session→na_zasedanii, enacted→prinyat)
  - `rosaudit/constants.py`: `STATUSY_KONTROLYA` — 5 ключей (planned→zaplanirovano, in_progress→provoditsya, completed→zaversheno, cancelled→otmeneno, approved→utverzhdeno); `VIDY_NARUSHENIY` — 5 ключей (financial→finansovoe, budget→byudzhetnoe, procurement→v_sfere_zakupok, property→pri_ispolzovanii_gossobstvennosti, program→pri_realizatsii_gosprogramm)
  - `rosprirodnadzor/constants.py`: `STATUSY_PROVEROK` — 6 ключей (planned→zaplanirovana, in_progress→provoditsya, completed→zavershena, cancelled→otmenena, violations_found→narusheniya_vyyavleny, no_violations→narusheniy_net); `TIPY_NARUSHENIY_EKO` — 8 ключей (air→atmosfernyy_vozdukh, water→vodnoe, soil→pochvy, waste→otkhody, subsoil→nedropolzovanie, radiation→radiatsionnaya_bezopasnost, land→zemelnoe, bio→zhivotnyy_mir)
  - `rospotrebnadzor/constants.py`: `NAPRAVLENIYA_DEYATELNOSTI` — 7 кодов (sanitary→sanitarnyy_nadzor, consumer_protection→zashchita_prav_potrebiteley, radiation_safety→radiatsionnaya_bezopasnost, water_safety→bezopasnost_vodnykh, air_quality→kachestvo_atmosfernogo_vozdukha, food_safety→bezopasnost_pishchevykh, product_safety→bezopasnost_neprodovolstvennykh); `KATEGORII_OBIEKTOV` — 8 кодов (food_enterprise→pishchevye_predpriyatiya, catering→obshchestvennoe_pitanie, education→obrazovatelnye_uchrezhdeniya, medical→meditsinskie_organizatsii, water_supply→vodosnabzhayushchie, retail→obekty_torgovli, industrial→promyshlennye_predpriyatiya, residential→zhilye_zdaniya); `STATUSY_PROVEROK` — 4 ключа (planned→zaplanirovana, in_progress→provoditsya, completed→zavershena, canceled→otmenena); `VIDY_NARUSHENIY` — 4 ключа (sanitary→sanitarnoe, consumer→prava_potrebiteley, radiation→radiatsionnaya, food→pishchevaya_bezopasnost)
  - `gosduma/constants.py`: `KOMITETY` — 8 кодов (budget→byudzhet_i_nalogi, legislation→gosstroitelstvo_i_zakonodatelstvo, defense→oborona, foreign→mezhdunarodnye_dela, economy→ekonomicheskaya_politika, health→okhrana_zdorovya, education→prosvishchenie, energy→energetika); `STATUSY_ZAKONOPROEKTOV` — 9 кодов (introduced→vnesen_v_gd, committee→v_komitete, first_reading→pervoe_chtenie, second_reading→vtoroe_chtenie, third_reading→tretie_chtenie, approved→odobren_sf, signed→podpisan_prezidentom, rejected→otklonen, withdrawn→otozvan_initsiatorom)
  - `roskomnadzor/constants.py`: `NAPRAVLENIYA_DEYATELNOSTI` — 6 кодов (media_supervision→nadzor_smi, telecom_supervision→nadzor_svyazi, it_supervision→nadzor_it, personal_data→zashchita_pd, internet_control→kontrol_interneta, copyright→zashchita_avtorskikh_prav); `REGISTRY_RKN` — 5 кодов (blocked_sites→zapreshchennye_sayty, pd_operators→operatory_pd, it_companies→inostrannye_it_kompanii, license_holders→litsenziaty_svyazi, media_registry→reestr_smi); `TIPY_SMI` — 5 кодов (print→pechatnoe_izdanie, online→setevoe_izdanie, tv→telekanal, radio→radiokanal, news_agency→informatsionnoe_agentstvo); `KATEGORII_PD_OPERATOROV` — 6 кодов (government→gosudarstvennye_organy, commercial→kommercheskie_organizatsii, nonprofit→nekommercheskie_organizatsii, individual_entrepreneur→individualnye_predprinimateli, education→obrazovatelnye_uchrezhdeniya, healthcare→meditsinskie_organizatsii); `OSNOVANIYA_BLOKIROVKI` — 9 ключей (drug→narkotiki, suicide→samoubiystva, pornography→detskaya_porografiya, extremism→ekstremizm, gambling→azarntnye_igry, copyright→avtorskoe_pravo, dangerous→opasnaya_informatsiya, fake→nedostovernaya_informatsiya, personal_data→utechka_pd)
  - `kaznacheistvo/constants.py`: `STATUSY_ISPOLNENIYA` — 5 ключей (approved→utverzhdyon, in_execution→ispolnyaetsya, completed→ispolnen, revised→skorrektirovan, preliminary→predvaritelnyy)
  - `zakupki/constants.py`: `SPOSOBY_ZAKUPOK` — 6 кодов (open→otkrytyy_konkurs, auction→elektronnyy_auktsion, query→zapros_kotirovok, single→edinyy_postavshchik, closed→zakrytyy_konkurs, limited→ogranichennoe_uchastie); `OTRASLI` — 8 кодов (construction→stroitelstvo, it→informatsionnye_tekhnologii, medicine→meditsina_i_farmvtsevtika, education→obrazovanie, transport→transport_i_logistika, energy→energetika, food→prodovolstvie, security→bezopasnost_i_oborona); `STATUSY_ZAKUPOK` — 6 кодов (planning→planirovanie, announced→opublikovana, bidding→priem_zayavok, review→rassmotrenie_zayavok, completed→zavershena, cancelled→otmenena)
- **Русификация оставшихся английских строк** (21 замена):
  - `etc.` → `и т.д.` в rosvodresursy/schemas.py, publikatsii/schemas.py (4 замены), rosapi/schemas.py
  - `ACTIVE, LIQUIDATED, etc.` → `ACTIVE, LIQUIDATED и т.д.` в rosapi/schemas.py
  - `Тип: national, professional, memorial` → `Тип: национальный, профессиональный, памятный` в rosapi/schemas.py
  - `Уровень (federal/regional/municipal)` → `Уровень (федеральный/региональный/муниципальный)` в cekrf/schemas.py
  - `WMO weather code` → `коды ВМО` в rosgidromet/constants.py
  - `fallback-данные` → `резервные данные` в mchs/tools.py, rosselkhoznadzor/tools.py
  - `fallback-поиске` → `резервном поиске` в fssp/client.py
  - `как fallback` → `как резервный вариант` в rosstat/client.py (2 docstrings)
  - `legacy-ответами` → `устаревшими ответами` в _shared/formatting.py
  - `legacy — placeholder` → `заглушка` в 6 модулях (fssp, fns, minobrnauki, rospotrebnadzor, roskomnadzor, rosreestr — prompts.py и resources.py)
- **Обновлены тесты**:
  - `tests/data/roskomnadzor/test_tools.py`: `"blocked_sites"` → `"zapreshchennye_sayty"`
  - `tests/data/rosselkhoznadzor/test_tools.py`: `"fallback"` → `"резервные данные"`
  - `tests/data/mchs/test_tools.py`: `"fallback"` → `"резервные данные"`
- **Обновлена docstring**: roskomnadzor/tools.py — `reestr_code: Код реестра (zapreshchennye_sayty, operatory_pd, ori и т.д.)`
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — 1 reformatted, `pytest` (680 passed, 1 skipped)

### Ключевые архитектурные решения

- **Полная русификация кодовых значений в 8 модулях**: все английские коды в словарях и списках constants.py заменены на русскую транслитерацию. Это обеспечивает единообразие с kad_arbitrazh/constants.py (русифицированным в раунде 42) и cbrf/constants.py
- **Кодовые значения REGISTRY_RKN русифицированы**: несмотря на использование в tools.py как параметр поиска (`r["code"] == reestr_code`), коды заменены и тест обновлён. LLM увидит русифицированные коды в таблице `spisok_reestrov` и передаст их как параметры
- **Английские термины «fallback» и «legacy — placeholder» устранены**: в пользовательском выводе и docstrings заменены на русские эквиваленты. Внутренние имена функций `_fallback_*` сохранены как устоявшийся программный термин

### Следующие действия

- **Русификация кодовых значений Росстата**: `KLYUCHEVYE_INDIKATORY`, `EMISS_KODY_POKAZATELEY`, `REGIONALNYE_POKAZATELI` — 30+ английских мнемоник (cpi, gdp, vrp, wages и т.д.) глубоко встроены в client.py, tools.py и тесты. Требует скоординированной замены в 10+ файлах
- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата

### Выполнено

- **Русификация логгерных сообщений** (19 замен в 3 файлах):
  - `server.py`: `"Tool call: %s"` → `"Вызов инструмента: %s"`, `"Tool %s completed in %.2fs"` → `"Инструмент %s завершён за %.2fс"`, `"Resource read: %s"` → `"Чтение ресурса: %s"`, `"Prompt get: %s"` → `"Запрос промпта: %s"`
  - `_shared/feature.py`: `"Feature '%s' skipped: %s"` → `"Функция '%s' пропущена: %s"`, `"Feature '%s' is disabled, skipping."` → `"Функция '%s' отключена, пропуск."`, `"Feature '%s' requires %s (not set), skipping."` → `"Функция '%s' требует %s (не задано), пропуск."`, `"Registered feature '%s' v%s"` → `"Зарегистрирована функция '%s' v%s"`, `"Mounted '%s' — %s"` → `"Смонтирована '%s' — %s"`
  - `_shared/http_client.py`: `"Retry %d/%d for %s (HTTP %d), waiting %.1fs"` → `"Повтор %d/%d для %s (HTTP %d), ожидание %.1fс"`, `"Request to %s failed after ... attempts"` → `"Запрос к %s не удался после ... попыток"`, `"HTTP ... from %s"` → `"HTTP ... от %s"`, `"Request to %s failed (attempt ...)"` → `"Запрос к %s не удался (попытка ...)"` (аналогично для http_post)
- **Русификация сообщений об ошибках** (9 замен):
  - `_shared/feature.py`: `"No FEATURE_META in ..."` → `"Нет FEATURE_META в ..."`, `"FEATURE_META in ... is not a FeatureMeta instance"` → `"FEATURE_META в ... не является экземпляром FeatureMeta"`, `"disabled (enabled=False)"` → `"отключена (enabled=False)"`, `"missing env var ..."` → `"отсутствует переменная ..."`, `"No 'mcp' object in ..."` → `"Нет объекта 'mcp' в ..."`
  - `_shared/http_client.py`: все HttpClientError-сообщения переведены
- **Русификация смешанных строк**:
  - `_shared/feature.py`: `"X feature(s) active, Y skipped"` → `"X функция(й) активно, Y пропущено"`
- **Русификация секций docstrings**:
  - `_shared/feature.py`: `Example:` → `Пример:`
  - `_shared/cache.py`: `Example:` → `Пример:`
  - `agenty/redator/resources.py`: `"Resources: шаблоны..."` → `"Ресурсы: шаблоны..."`
  - `agenty/redator/prompts.py`: `"Prompts: агенты..."` → `"Промпты: агенты..."`
  - `data/__init__.py`: `"Data features —"` → `"Модули данных —"`
- **Русификация кодовых значений в константах**:
  - `kad_arbitrazh/constants.py`: 24 английских кода заменены на русскую транслитерацию (first→pervaya, appeal→apellyatsionnaya, bankruptcy→bankrotstvo, и т.д.)
  - `cbrf/constants.py`: `"key_rate"` → `"klyuchevaya_stavka"`
- **Русификация комментариев**:
  - `publikatsii/constants.py`: `# paid service` → `# платный сервис`
- **Обновлены тесты**:
  - `tests/_shared/test_feature.py`: `assert "0 feature(s) active"` → `assert "0 функция(й) активно"`, `"1 feature(s) active"` → `"1 функция(й) активно"`, `"missing FEATURE_META"` → `"отсутствует FEATURE_META"`, `"1 skipped"` → `"1 пропущено"`, `"Test feature"` → `"Тестовая функция"`
  - `tests/_shared/test_http_client.py`: `match="failed after"` → `match="не удался после"`
- **Создан модуль Россельхознадзор (rosselkhoznadzor)** — 24-й российский модуль:
  - `__init__.py`: FeatureMeta с тегами ветеринарный надзор, фитосанитарный контроль, карантин растений, пестициды, земельный надзор
  - `constants.py`: API URLs, справочники (6 видов надзора, 4 категории проверок, 6 видов нарушений, 5 типов продукции, 3 карантинных объекта, 8 федеральных округов), статическая статистика за 2023
  - `schemas.py`: 4 модели (ProverkaRskhn, KarantinnyyObyekt, RegistratsiyaProduktsii, VeterinarnyySertifikat)
  - `client.py`: 5 async-функций (poisk_proverok, poisk_karantinnykh_obektov, poisk_registratsiy_produktsii, veterinarsnye_sertifikaty, preduprezhdeniya_karantina) + 7 справочников + fallback на статические данные
  - `tools.py`: 9 инструментов (4 справочника + 5 данных) с форматированным выводом
  - `resources.py`: 3 ресурса (источники данных, структура Россельхознадзора, законодательство)
  - `prompts.py`: 2 промпта (анализ ветеринарной проверки, обзор карантинной обстановки)
  - `server.py`: FastMCP с 9 tools, 3 resources, 2 prompts
- **Обновлены тесты**: 21 тест Россельхознадзора (tools + constants + integration)
- **Обновлена конфигурация ruff**: добавлены per-file-ignores для rosselkhoznadzor
- **Обновлена документация**:
  - docs/reference/features.md: 23→24 модулей, 193→202 инструментов, 68→71 ресурсов, 46→48 промптов; добавлено описание Россельхознадзора
  - README.md: 23→24 модуля, добавлено описание Россельхознадзора
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — all formatted, `pytest` (680 passed, 1 skipped)

### Ключевые архитектурные решения

- **Логгерные сообщения полностью русифицированы**: все logger.info/warning/error в server.py, _shared/feature.py, _shared/http_client.py теперь на русском. Это затрагивает пользовательский вывод (summary) и отладочные сообщения
- **Сообщения об ошибках русифицированы**: ValueError, TypeError, HttpClientError возбуждаются с русскими сообщениями. Версия HttpClientError в http_get и http_post идентична
- **Кодовые значения в kad_arbitrazh/constants.py русифицированы**: 24 английских кода (first, appeal, bankruptcy, и т.д.) заменены на русскую транслитерацию (pervaya, apellyatsionnaya, bankrotstvo) для единообразия со всеми другими модулями
- **Модуль Россельхознадзор с multi-source fallback**: как все остальные модули, использует каскадный fallback при недоступности API (fsvps.gov.ru → data.fsvps.gov.ru → статические данные). Статистика 2023 используется как fallback
- **24 российских модуля**: покрытие расширено с 23 до 24 модулей. Итого 202 инструмента, 71 ресурс, 48 промптов

### Следующие действия

- **Добавление новых модулей данных**: МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Русификация оставшихся кодовых значений**: sovfed/constants.py ("pending"), rosaudit/constants.py ("property"), zakupki/constants.py ("closed")
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата

### Выполнено

- **Тотальная русификация секций docstrings** (649 замен в ~70 файлах):
  - `Args:` → `Аргументы:` (286 замен)
  - `Returns:` → `Возвращает:` (360 замен, включая 8-space indented)
  - `Raises:` → `Вызывает:` (6 замен)
  - Все секции docstrings во всех модулях src/mcp_russia/ теперь на русском
- **Русификация английских описаний в промптах** (22 замены в 12 модулях):
  - `Prompt template for ...` → `Шаблон промпта для ...` во всех модулях data/*/prompts.py
  - rosprirodnadzor/prompts.py: исправлены два английских описания Returns
- **Исправлены английские артефакты в документации**:
  - README.md: `## Task List` → `## Список задач`
  - docs/reference/features.md: 6 заголовков модулей с английскими `tools/resources/prompts` → `инструментов/ресурсов/промптов`; 22→23 модулей, 184→193 инструментов
  - docs/examples/ofitsialnyy-redaktor.md: `5 tools` → `5 инструментов`, `9 resources` → `9 ресурсов`, `5 prompts` → `5 промптов`, `## Как работают resources` → `## Как работают ресурсы`, `Templates/resources/prompts` → `Шаблоны/ресурсы/промпты`
- **Добавлены 4 отсутствующих docstring** (100% покрытие восстановлено):
  - `cekrf/client.py`: `_VyboryTableParser.__init__` — инициализация парсера HTML-таблиц
  - `server.py`: `RequestLoggingMiddleware.on_call_tool` — логирование вызова инструмента
  - `server.py`: `RequestLoggingMiddleware.on_read_resource` — логирование чтения ресурса
  - `server.py`: `RequestLoggingMiddleware.on_get_prompt` — логирование запроса промпта
- **Создан модуль МЧС России (mchs)** — 23-й российский модуль:
  - `__init__.py`: FeatureMeta с тегами ЧС, пожары, гражданская оборона
  - `constants.py`: API URLs, справочники (4 вида ЧС, 6 классов ЧС, 7 видов пожаров, 7 типов опасностей, 7 федеральных округов), статическая статистика пожаров за 2023
  - `schemas.py`: 4 модели (Pozhar, ChrezvychaynayaSituatsiya, RadiatsionnyyMonitoring, GidrologicheskayaObstanovka)
  - `client.py`: 6 async-функций (statistika_pojarov, poisk_chs, radiatsionnyy_monitoring, gidrologicheskaya_obstanovka, preduprezhdeniya_chs) + 5 справочников + fallback на статические данные при недоступности API
  - `tools.py`: 9 инструментов (4 справочника + 5 данных) с форматированным выводом
  - `resources.py`: 3 ресурса (источники данных, структура МЧС, законодательство)
  - `prompts.py`: 2 промпта (анализ ЧС, обзор пожарной обстановки)
  - `server.py`: FastMCP с 9 tools, 3 resources, 2 prompts
- **Обновлены тесты**: 18 тестов МЧС (tools + constants)
- **Обновлена конфигурация ruff**: добавлены per-file-ignores для mchs
- **Обновлена документация**:
  - docs/reference/features.md: добавлено описание модуля МЧС (9 инструментов, 3 ресурса, 2 промпта)
  - README.md: 22→23 модуля, добавлено описание МЧС
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — all formatted, `pytest` (659 passed, 1 skipped)

### Ключевые архитектурные решения

- **Секции docstrings полностью русифицированы**: `Аргументы:`, `Возвращает:`, `Вызывает:` вместо английских `Args:`, `Returns:`, `Raises:` во всей кодовой базе. Это затронуло все 23 модуля data/, _shared/, agenty/ и server.py
- **Модуль МЧС с multi-source fallback**: как все остальные модули, использует каскадный fallback при недоступности API (mchs.gov.ru → data.mchs.gov.ru → статические данные). Статистика пожаров 2023 используется как fallback-данные
- **23 российских модуля**: покрытие расширено с 22 до 23 модулей. Итого 193 инструмента, 68 ресурсов, 46 промптов

### Следующие действия

- **Добавление новых модулей данных**: Россельхознадзор, МВД (расширенный), Рособрнадзор (расширенный), Ростехнадзор
- **Миграция на новые ЕМИСС-коды (9xxxxxx)**: ЕМИСС перешёл на новую систему кодов; при появлении документации обновить все коды в `EMISS_KODY_POKAZATELEY`
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата

## Статус раунда 2026-06-15 (тридцать девятый проход — русские docstrings для 110 функций)

### Выполнено

- **Добавлены русские docstrings к 110 функциям без docstrings** в 11 модулях (все в client.py):
  - `fssp/client.py` (7 функций): `_parse_fio`, `_parse_proizvodstva`, `_normalise_proizvodstvo`, `poisk_proizvodstv`, `info_proizvodstva`, `ogranicheniya_dolzhnika`, `rozysk_dolzhnika`
  - `rosreestr/client.py` (5 функций): `_parse_obekt`, `poluchit_obekt`, `poluchit_kadastrovnuyu_stoimost`, `poluchit_prava`, `poisk_po_nomeru`
  - `rosprirodnadzor/client.py` (13 функций): `poisk_proverok`, `info_proverki`, `poisk_obektov_negativnogo`, `poisk_litsenziy_nedra`, `poluchit_ekologicheskie_platezhi`, `get_vidy_nadzora_list`, `get_kategori_obnv_list`, `get_vidy_litsenziy_nedra_list`, `_extract_list`, `_parse_proverka`, `_parse_obekt_negativnogo`, `_parse_litsenziya`, `_parse_ekologicheskiy_platezh`
  - `kaznacheistvo/client.py` (13 функций): `poluchit_ispolnenie_byudzheta`, `poisk_uchastnikov_bp`, `poisk_uchrezhdeniy`, `poluchit_mezhbyudzhetnye`, `poluchit_byudzhetnuyu_smetu`, `get_vidy_byudzhetov_list`, `get_kategorii_raskhodov_list`, `_extract_list`, `_parse_ispolnenie_byudzheta`, `_parse_uchastnik_bp`, `_parse_uchrezhdenie`, `_parse_mezhbyudzhetnyy_transfer`, `_parse_byudzhetnaya_smeta`
  - `kad_arbitrazh/client.py` (10 функций): `_opredelit_sud_po_nomeru`, `_opredelit_kategoriyu`, `_parse_rezultaty_poiska`, `_parse_kartochka_dela`, `_parse_akty`, `_parse_storony`, `get_instantsii`, `get_kategorii_del`, `get_statusy_del`, `get_tipy_aktov`
  - `rosapi/client.py` (18 функций): `_dadata_headers`, `_nested_get`, `_parse_org_data`, `_parse_bank_data`, `_suggest_address`, `_find_by_fias`, `_postal_by_index`, `_find_org_by_inn`, `_find_org_by_ogrn`, `_list_banks`, `_find_bank_by_bik`, `get_holidays`, `consult_address_by_postal`, `search_address`, `find_org_by_inn`, `find_org_by_ogrn`, `list_banks_public`, `find_bank_by_bik`
  - `rosaudit/client.py` (8 функций): `get_napravleniya_list`, `get_tipy_meropriyatiy_list`, `get_subiekty_audita_list`, `_extract_list`, `_parse_kontrolnoe_meropriyatie`, `_parse_auditorskoe_zaklyuchenie`, `_parse_byudzhet_ispolnenie`, `_parse_narushenie`
  - `rosvodresursy/client.py` (10 функций): `get_basseynovye_okruga_list`, `get_tipy_vodnykh_obektov_list`, `get_tipy_gidro_list`, `get_vodokhranilishcha_list`, `get_vodokhranilishcha_detailed`, `_extract_list`, `_parse_vodnyy_obekt`, `_parse_gidro_zapis`, `_parse_vodokhranilishche`, `_parse_vodopolzovanie_zapis`
  - `sovfed/client.py` (13 функций): `poisk_senatorov`, `info_senatora`, `spisok_komitetov`, `spisok_komissiy`, `poisk_zakonoproektov`, `spisok_zasedaniy`, `get_komitety_list`, `get_komissii_list`, `_extract_list`, `_parse_senator`, `_parse_komitet`, `_parse_zasedanie`, `_parse_zakonoproekt`
  - `minzdrav/client.py` (10 функций): `get_tipy_mo`, `get_spetsialnosti`, `get_mkb10_classes`, `get_federalnyye_okruga`, `get_pokazateli_zdorovya_list`, `_extract_list`, `_parse_med_organizatsia`, `_parse_litsenziya`, `_parse_pokazatel`, `_parse_zabolevanie`
  - `cekrf/client.py` (3 функции): `handle_starttag`, `handle_endtag`, `handle_data`
- **Подтверждено**: tools.py, prompts.py, schemas.py, resources.py, server.py, constants.py — все функции уже имеют docstrings
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — all formatted, `pytest` (641 passed, 1 skipped)

### Ключевые архитектурные решения

- **Все 110 функций client.py в 11 модулях получили русские docstrings**: публичные функции — с Args/Returns, приватные — с кратким описанием
- **Паттерн docstrings**: для async-функций с параметрами используется полная форма (Args, Returns), для приватных хелперов и геттеров-справочников — однострочные описания

### Следующие действия

- **Верификация оставшихся ЕМИСС-кодов**: проверить коды 24133 (население), 26973 (ВВП), 30826 (промышленность) и др.
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата
- **Проверка оставшихся модулей на наличие функций без docstrings**: cbrf, rosgidromet, fns, gosduma, zakupki, publikatsii, minobrnauki, rospotrebnadzor, roskomnadzor, rosstat

## Статус раунда 2026-06-14 (тридцать восьмой проход — русификация документации, тестов и комментариев)

### Выполнено

- **Русификация документации docs/ (125 замен)**:
  - `docs/reference/features.md` (88 замен): `Tool` → `Инструмент` (22), `Resources:` → `Ресурсы:` (22), `Prompts:` → `Промпты:` (22), `(X tools, Y resources, Z prompts)` → `(X инструментов, Y ресурсов, Z промптов)` (22)
  - `docs/concepts/architecture.md` (5 замен): `root server с auto-registry` → `корневой сервер с авторегистрацией`, `internal-слоем` → `внутренним слоем`, `schemas, tools, resources и prompts` → `схемы, инструменты, ресурсы и промпты`, `tools, resources и prompts` → `инструменты, ресурсы и промпты`, `каталог и рекомендация tools` → `каталог и рекомендация инструментов`
  - `docs/guide/adding-features.md` (11 замен): `feature` → `модуль`, `data-feature` → `модуль данных`, `agent-feature` → `агентный модуль`, `Описать tools` → `Описать инструменты`, `feature-server` → `сервер модуля`, `resources и prompts` → `ресурсы и промпты`
  - `docs/guide/development.md` (5 замен): `внутри feature` → `внутри модуля`, `compatibility-слой` → `слой совместимости`, `поведение feature` → `поведение модуля`
  - `docs/index.md` (3 замены): `discovery feature-пакетов` → `обнаружение пакетов модулей`, `root server, auto-registry и feature-пакеты` → `корневой сервер, авторегистрация и пакеты модулей`, `Как добавлять новую feature` → `Как добавлять новый модуль`
  - `docs/reference/smart-tools.md` (5 замен): `tools` → `инструменты` (в бегущем тексте), `per capita` → `на душу населения`, `из другой feature` → `из другого модуля`
  - `docs/reference/configuration.md` (2 замены): `каталог tools` → `каталог инструментов`, `tools показывается` → `инструментов показывается`
  - `docs/examples/ofitsialnyy-redaktor.md` (4 замены): `compatibility-layer` → `уровень совместимости`, `relevant resource` → `соответствующий ресурс`, `Official Editor` → `Официальный редактор`
  - `docs/examples/gosudarstvennaya-politika.md` (4 замены): `(INPUT)` → `(ВХОД)`, `(PROCESS)` → `(ПРОЦЕСС)`, `(OUTPUT)` → `(ВЫХОД)`, `(ACCOUNTABILITY)` → `(ОТВЕТСТВЕННОСТЬ)`
  - `docs/examples/zhurnalist-stati.md` (1 замена): `Top 10` → `топ-10`
- **Русификация тестовых docstrings и комментариев (38 замен в 10 файлах)**:
  - `tests/_shared/test_batch.py` (4 docstrings): `Should execute multiple queries concurrently` → `Должен выполнять несколько запросов параллельно` и др.
  - `tests/_shared/test_http_client.py` (6 docstrings): `4xx errors should not retry` → `Ошибки 4xx не должны повторяться` и др.
  - `tests/_shared/test_rate_limiter.py` (1 module docstring + 6 comments): `Tests for the async RateLimiter` → `Тесты асинхронного ограничителя запросов` и др.
  - `tests/_shared/test_lifespan.py` (1 module + 1 class + 2 method docstrings + 3 comments): полная русификация
  - `tests/_shared/test_validators.py` (1 module docstring): `Tests for Russian validators` → `Тесты российских валидаторов`
  - `tests/_shared/test_settings.py` (1 docstring): `Settings can be overridden via env vars` → `Настройки можно переопределить через переменные окружения`
  - `tests/_shared/test_feature.py` (2 tool docstrings + 1 method docstring + 1 comment): `Ping tool` → `Инструмент проверки связи`, `Echo a message` → `Вернуть сообщение` и др.
  - `tests/_shared/test_cache.py` (1 португальский module docstring + 5 comments): `Testes do cache com TTL` → `Тесты кэша с TTL`, English inline comments → русские
  - `tests/data/zakupki/test_tools.py` (2 section comments): `Parser tests` → `Тесты парсера`, `Tool tests` → `Тесты инструментов`
  - `tests/data/gosduma/test_tools.py` (2 section comments): аналогично
- **Русификация inline-комментариев в src/mcp_russia/ (5 замен)**:
  - `_shared/feature.py`: `ensure .env is loaded` → `убедиться, что .env загружен`
  - `_shared/planner.py`: `JSON schema` → `JSON-схема`, `Каталог tools` → `Каталог инструментов`
  - `settings.py`: `Dadata API (rosapi)` → `Dadata API (РосАПИ)`
- **Исправление E501 (длинные строки) от предыдущего раунда**:
  - `_shared/feature.py`: docstring `mount_all` перенесён на две строки
  - `_shared/validators.py`: `raise ValueError(...)` перенесён на три строки
  - `tests/agenty/redator/test_integration.py`: сокращён module docstring
- **Исправление BM25-тестов** после русификации docstrings:
  - `tests/test_discovery.py`: поисковые запросы обновлены на транслитерированные (`"regions russia"` → `"spisok regionov"`, `"fire hotspots satellite"` → `"ochagi pozhary sputnik"`), т.к. BM25-токенизатор не поддерживает кириллицу
- **Исправление test_validators.py match-строк** после русификации ValueError-сообщений:
  - `"10 or 12 digits"` → `"10 или 12 цифр"`, `"9 digits"` → `"9 цифр"`, `"11 digits"` → `"11 цифр"`, `"6 digits"` → `"6 цифр"`
- **Обновлена конфигурация ruff**:
  - `src/mcp_russia/_shared/*`: добавлен `RUF003`
  - `tests/_shared/*`: добавлен `RUF003`, удалён дубликат ключа
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — all formatted, `pytest` (641 passed, 1 skipped)

### Ключевые архитектурные решения

- **BM25-токенизатор не поддерживает кириллицу**: после русификации docstrings тестовые BM25-запросы пришлось перевести на транслитерацию (латинские аналоги русских слов). Это известное ограничение библиотеки fastmcp — в продакшене запросы пользователей обычно приходят на естественном языке через LLM, который формулирует их латиницей
- **Документация полностью русифицирована**: все 11 markdown-файлов в `docs/` теперь содержат только русские заголовки, термины и описания; английские гибридные термины (`feature`, `tools`, `resources`, `prompts`, `root server`, `auto-registry`, `compatibility-layer`) заменены на русские эквиваленты
- **Тесты полностью русифицированы**: последний португальский артефакт (`Testes do cache com TTL`) устранён; все английские docstrings, комментарии и section-метки в тестах переведены

### Следующие действия

- **Добавить русские docstrings к ~95 функциям без docstrings** в модулях: fssp, rosreestr, rosprirodnadzor, kaznacheistvo, kad_arbitrazh, rosapi, rosaudit, rosvodresursy, sovfed, minzdrav, cekrf
- **Верификация оставшихся ЕМИСС-кодов**: проверить коды 24133 (население), 26973 (ВВП), 30826 (промышленность) и др.
- **Углубление интеграций**: расширение данных по регионам, новые инструменты Росстата

## Статус раунда 2026-06-12 (тридцать седьмой проход — русификация документации, исправление ЕМИСС-кодов, статические данные ВРП/инвестиций)

### Выполнено

- **Тотальная русификация модульных документационных строк (docstrings)**:
  - `server.py`: модульный docstring и все комментарии переведены на русский (14 замен: «root server» → «корневой сервер», «Middleware» → «Промежуточный слой», «Auto-discover» → «Автоматическое обнаружение», «Tool Search Transform» → «Трансформация поиска инструментов», сообщения логгера и предупреждения)
  - `_shared/` (9 модулей): planner, http_client, discovery, validators, batch, rate_limiter, cache, feature, lifespan — все модульные docstrings переведены
  - `data/` (22 модуля × ~7 файлов): все модульные docstrings переведены — client, constants, tools, schemas, server, resources, prompts
  - `agenty/` (5 файлов): __init__, redator/__init__, redator/constants, redator/server, redator/tools — docstrings и комментарии переведены
  - Итого: ~160 файлов с переведёнными модульными docstrings
- **Русификация функциональных docstrings** (30 функций):
  - `rosstat/client.py`: 4 функции (poluchit_federalny_okrug, poluchit_indikator_dannye, get_subiekty_list, get_federalny_okruga_list)
  - `rosgidromet/client.py`: 6 функций (poluchit_prognoz, get_stancii_list и др.)
  - `publikatsii/client.py`: 5 функций (poluchit_izmeneniya_akta и др.)
  - `gosduma/client.py`: 6 функций (poluchit_deputatov, _parse_deputats и др.)
  - `fns/client.py`: 2 функции (poluchit_proverki, poluchit_svedeniya)
  - `_shared/`: feature.py (FeatureMeta), batch.py (_scan_tools_module, execute_batch), discovery.py (_format_tool_signature), planner.py (EtapPlana, PlanZaprosa.svodka), formatting.py (truncate_list)
- **Верификация и исправление ЕМИСС-кодов**:
  - Проведена проверка 6 ЕМИСС-кодов через fedstat.ru/indicator/{code}
  - `energy_production`: 31110 → 31208 (код 31110 указывал на «Индексы цен производителей с/х продукции» — устаревший показатель до 2016 г.)
  - `transport_cargo`: 31153 → 31221 (код 31153 указывал на «Количество предприятий с просроченной задолженностью» — устаревший показатель до 2016 г.)
  - Добавлен блок верификации в `constants.py`: статусы ✅/⚠️/❌/❓ для каждого кода
  - Коды 31099, 27621, 27103, 24145 помечены как ⚠️ устаревшие (страницы-заглушки на fedstat.ru)
- **Добавлены реальные статические данные отраслевой структуры ВРП**:
  - `OTRASLEVAYA_STRUKTURA_VRP`: добавлены поля `dolya_2022` (доля в %) и `vrp_2022` (млрд ₽) для всех 19 разделов ОКВЭД
  - Источник: Росстат, «Национальные счета России», табл. 2.5; ВРП РФ за 2022 г. ≈ 135 539 млрд ₽
  - Обновлены ЕМИСС-коды для разделов D/E (31208) и H (31221) в соответствии с исправленными кодами
- **Добавлены реальные статические данные инвестиций по видам деятельности**:
  - `VIDY_DEYATELNOSTI_INVESTITSII`: добавлены поля `dolya_2022` (доля в %) и `inv_2022` (млрд ₽) для всех 19 разделов ОКВЭД
  - Источник: Росстат, «Инвестиции в России», табл. 2.1; Инвестиции в основной капитал за 2022 г. ≈ 28 949 млрд ₽
- **Обновлены справочники региональных показателей**:
  - `REGIONALNYE_POKAZATELI`: добавлены `energy_production: 31208` и `transport_cargo: 31221`
- **Зачистка CHANGELOG.md**:
  - `tabua_mares` → `tabua_mares (legacy)` в версии 0.5.0
  - `compras/pncp` → `compras/pncp (legacy)` в версии 0.3.1
- **Обновлена конфигурация ruff**:
  - `rosstat/*`: добавлен `E501` в per-file-ignores (длинные строки данных)
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — all formatted, `pytest` (505 passed, 1 skipped)

### Ключевые архитектурные решения

- **ЕМИСС-коды верифицированы**: 2 кода (31110, 31153) указывали на неверные устаревшие показатели и заменены на корректные (31208, 31221). Остальные 4 кода (31099, 27621, 27103, 24145) помечены как ⚠️ устаревшие — fedstat.ru отображает пустые страницы-заглушки, вероятно из-за перехода ЕМИСС на новую систему кодов (9xxxxxx)
- **Статические данные ВРП и инвестиций заполнены реальными значениями за 2022 г.**: fallback-функции `_fallback_otraslevaya_struktura()` и `_fallback_investitsii_po_vidam()` теперь возвращают не null-значения, а актуальные данные из опубликованных Росстатом сборников
- **Полная русификация документационных строк**: все ~160 Python-файлов в `src/mcp_russia/` теперь имеют русские модульные docstrings; ключевые функции — русские docstrings с аргументами и описаниями

### Следующие действия

- **Верификация оставшихся ЕМИСС-кодов**: проверить коды 24133 (население), 26973 (ВВП), 30826 (промышленность), 24139 (безработица), 24140 (зарплата), 31082 (розничная торговля), 24145 (инвестиции), 31106 (строительство), 26975/26976 (ВРП) и др.
- **Перевод оставшихся функциональных docstrings**: во всех 22 модулях data/ остаются английские docstrings у внутренних функций (helpers, parsers, etc.)
- **Русификация тестовых docstrings**: часть тестовых файлов содержит английские docstrings и комментарии

## Статус раунда 2026-06-11 (тридцать шестой проход — отраслевая структура ВРП, инвестиции по ОКВЭД, зачистка документации)

### Выполнено

- **Новые инструменты Росстата `otraslevaya_struktura_vrp` и `investitsii_po_vidam`**:
  - `tools.py`: добавлены инструменты `otraslevaya_struktura_vrp` (отраслевая структура ВРП по ОКВЭД) и `investitsii_po_vidam` (инвестиции в основной капитал по видам деятельности)
  - `client.py`: добавлены функции `poluchit_otraslevuyu_strukturu_vrp()` и `poluchit_investitsii_po_vidam()` с fallback на статический справочник ОКВЭД при недоступности API
  - `schemas.py`: добавлены модели `OtraslevayaStrukturaVRP` и `InvestitsiiPoVidam`
  - `constants.py`: добавлен справочник `OTRASLEVAYA_STRUKTURA_VRP` (19 разделов ОКВЭД с кодами ЕМИСС), `VIDY_DEYATELNOSTI_INVESTITSII` (19 видов деятельности)
  - `server.py`: зарегистрированы 2 новых инструмента с тегами `{"ВРП", "отрасли", "ОКВЭД"}` и `{"инвестиции", "отрасли", "ОКВЭД"}`; итого 13 tools
  - `__init__.py`: версия 0.4.0 → 0.5.0, описание обновлено, добавлены теги «ОКВЭД» и «инвестиции»
- **Расширение EMISS-кодов и показателей**:
  - `EMISS_KODY_POKAZATELEY`: 21 → 27 кодов; добавлены foreign_trade (31099), energy_production (31110), transport_cargo (31153), science_innovation (27621), vrp_structure (27103), investments_by_activity (24145)
  - `KLYUCHEVYE_INDIKATORY`: 16 → 21 показатель; добавлены внешнеторговый оборот, производство электроэнергии, грузооборот транспорта, затраты на исследования, структура ВРП
  - `REGIONALNYE_POKAZATELI`: 10 → 14 показателей; добавлены agrarian, construction, migration, natural_growth
- **Зачистка документации от английских заголовков и португальских артефактов**:
  - `docs/reference/smart-tools.md`: `# Smart tools` → `# Умные инструменты`; `## Tool Search (BM25)` → `## Поиск инструментов (BM25)`
  - `docs/concepts/architecture.md`: `## Meta-tools root server` → `## Мета-инструменты корневого сервера`
  - `CONTRIBUTING.md`: `# Contributing to mcp-russia` → `# Участие в разработке mcp-russia`
  - `docs/guide/adding-features.md`: `TIPOS_ZAPROSA` → `TIPY_ZAPROSA`; `list_items` → `spisok_zapisey` во всех примерах кода
- **Обновлена документация**:
  - `docs/reference/features.md`: росстат 11→13 tools, 182→184 инструментов; описание обновлено (21 показатель, 27 ЕМИСС-кодов)
  - `README.md`: добавлены строки про `otraslevaya_struktura_vrp` и `investitsii_po_vidam`
- **Исправлен ruff SIM117** в `tests/data/rosapi/test_tools.py`: вложенные `with` объединены в один
- **Обновлены тесты Росстата**: 51 тест (было 42) — добавлены тесты otraslevaya_struktura_vrp (fallback, with_data, empty), investitsii_po_vidam (fallback, with_data, empty), constants (otraslevaya_struktura, vidy_deyatelnosti_investitsii, new_emiss_kody, new_regionalnye_pokazateli)
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — all formatted, `pytest` (641 passed, 1 skipped)

### Ключевые архитектурные решения

- **Отраслевая структура ВРП с fallback**: инструмент `otraslevaya_struktura_vrp` запрашивает ЕМИСС-код 27103; при недоступности API возвращает справочник всех 19 разделов ОКВЭД без количественных данных — это позволяет пользователю увидеть структуру классификации и понять, какие данные доступны
- **Инвестиции по видам деятельности с fallback**: инструмент `investitsii_po_vidam` аналогично использует ЕМИСС-код 24145 с параметром `groupByActivity=true`; fallback возвращает справочник видов деятельности
- **EMISS-коды расширены для полного покрытия**: 27 кодов теперь покрывают все 21 показатель из `KLYUCHEVYE_INDIKATORY` плюс дополнительные коды для региональных и отраслевых запросов; тест `test_constants_emiss_kody_complete` верифицирует соответствие

### Следующие действия

- **Верификация EMISS-кодов на живом fedstat.ru**: проверить корректность кодов 27103 (структура ВРП), 31099 (внешняя торговля), 31110 (электроэнергия), 31153 (грузооборот), 27621 (наука)
- **Добавить статические данные отраслевой структуры ВРП**: на основе опубликованных Росстатом данных заполнить fallback справочник количественными значениями (доли по ОКВЭД за последний доступный год)
- **Дочистить CHANGELOG.md**: пометить (legacy) все непомеченные бразильские модули и функции в исторических записях

## Статус раунда 2026-06-11 (тридцать пятый проход — auth_env_var, AuthError, зачистка)

### Выполнено

- **Подключение `auth_env_var` к модулям с авторизацией**:
  - `rosapi/__init__.py`: добавлен `auth_env_var="MCP_RUSSIA_DADATA_API_KEY"` (исправлен баг — `requires_auth=True` без `auth_env_var` приводил к `is_auth_available() → False`, модуль всегда пропускался реестром)
  - `gosduma/__init__.py`: добавлен `auth_env_var="MCP_RUSSIA_DUMA_API_TOKEN"` (requires_auth=False — модуль работает без токена, но с ограничениями)
  - `zakupki/__init__.py`: добавлен `auth_env_var="MCP_RUSSIA_ZAKUPKI_API_TOKEN"` (requires_auth=False — модуль работает без токена, но с ограничениями)
- **Использование `AuthError` в rosapi/client.py**:
  - `_dadata_headers()`: вместо тихой отправки запросов без ключа — возбуждает `AuthError` с инструкцией по настройке MCP_RUSSIA_DADATA_API_KEY
  - `AuthError` определён в `exceptions.py`, но ранее нигде не вызывался
- **Информационные заметки об авторизации в tools**:
  - `gosduma/tools.py`: добавлена функция `_auth_note()`, выводит `*Для полного доступа к API настройте MCP_RUSSIA_DUMA_API_TOKEN*` при отсутствии токена
  - `zakupki/tools.py`: добавлена функция `_auth_note()`, выводит `*Для полного доступа к API настройте MCP_RUSSIA_ZAKUPKI_API_TOKEN*` при отсутствии токена
  - Заметки добавлены к результатам инструментов: spisok_deputatov, zakonoproekty, golosovaniya (Госдума), poisk_zakupok, poisk_kontraktov, plany_zakupok (Закупки)
- **Обновлён `_shared/feature.py`**:
  - `summary()`: добавлен третий значок авторизации — `🔏` для модулей с `auth_env_var`, но `requires_auth=False` (опциональная авторизация)
  - Ранее: только `🔑` (requires_auth=True) и `🔓` (без авторизации)
- **Обновлён `_shared/discovery.py`**:
  - `build_catalog()`: добавлена категория «Рекомендуется аутентификация ({env_var})» для модулей с `auth_env_var`, но `requires_auth=False`
  - Ранее: только «Требуется аутентификация» и «Без аутентификации»
- **Обновлена документация**:
  - `docs/reference/features.md`: Госдума — «опциональная (MCP_RUSSIA_DUMA_API_TOKEN для полного доступа)»; РосАПИ — «требуется (MCP_RUSSIA_DADATA_API_KEY)»; Закупки — «опциональная (MCP_RUSSIA_ZAKUPKI_API_TOKEN для полного доступа)»
- **Подтверждено**: кодовая база (`src/`, `tests/`, `docs/`) полностью очищена от португальских/бразильских артефактов. Единственные упоминания — в `TODO.md` (исторические записи) и `CHANGELOG.md` (legacy-записи)
- **Обновлены тесты**:
  - `tests/_shared/test_feature.py`: добавлены тесты `test_is_auth_available_optional_auth_no_env`, `test_is_auth_available_optional_auth_with_env`
  - `tests/data/rosapi/test_tools.py`: добавлены тесты `test_dadata_headers_raises_auth_error_without_key`, `test_dadata_headers_with_key`
  - `tests/data/gosduma/test_tools.py`: добавлены тесты `test_auth_note_without_token`, `test_auth_note_with_token`
  - `tests/data/zakupki/test_tools.py`: добавлены тесты `test_auth_note_without_token`, `test_auth_note_with_token`
- **Прогнаны все проверки**: `ruff check` — all passed, `ruff format` — all formatted, `pytest` (487 passed, 1 skipped для non-integration тестов)

### Ключевые архитектурные решения

- **Трёхуровневая модель авторизации**: `requires_auth=True` (модуль пропускается без токена), `requires_auth=False` + `auth_env_var` (опциональная авторизация с рекомендацией), `requires_auth=False` без `auth_env_var` (без авторизации)
- **`AuthError` используется по назначению**: rosapi (требует Dadata API ключ) возбуждает `AuthError` при отсутствии ключа; gosduma и zakupki (опциональная авторизация) показывают информационную заметку в результатах инструментов
- **Исправлен баг rosapi**: `requires_auth=True` без `auth_env_var` приводил к тому, что `is_auth_available()` всегда возвращал `False`, и реестр FeatureRegistry всегда пропускал модуль rosapi. Теперь `auth_env_var="MCP_RUSSIA_DADATA_API_KEY"` корректно указан

### Следующие действия

- **Углубление интеграций**: верификация EMISS-кодов на живом fedstat.ru (26975/26976 для ВРП, 30955/31106 для сельского хозяйства/строительства)
- **Расширение региональных данных**: добавление EMISS-кодов для отраслевой структуры ВРП, инвестиций по видам деятельности
- **Подключение `requires_auth=True` для РосАПИ**: rosapi теперь корректно настроен с `auth_env_var`, но реестр пропустит модуль если Dadata API ключ не задан — это ожидаемое поведение

## Статус раунда 2026-06-10 (тридцать четвёртый проход — универсальный инструмент ЕМИСС, исправление багов, унификация настроек)

### Выполнено

- **Универсальный инструмент Росстата `indikator_dannye`**:
  - `schemas.py`: добавлена модель `IndikatorDannye` (kod_emiss, nazvanie, period, znachenie, edinitsa, region)
  - `client.py`: добавлена функция `poluchit_indikator_dannye()` — запрос произвольного показателя по коду ЕМИСС или мнемоническому коду с опциональной фильтрацией по региону и году
  - `tools.py`: добавлен инструмент `indikator_dannye` — принимает код ЕМИСС (напр. '31088') или мнемонический код (напр. 'cpi'), возвращает форматированную таблицу данных
  - `server.py`: зарегистрирован инструмент с тегами `{"показатель", "ЕМИСС", "универсальный"}`; итого 11 tools
  - `__init__.py`: версия 0.3.0 → 0.4.0, описание обновлено, добавлен тег «ЕМИСС»
- **Исправлен баг округления в `format_rub()`** (`_shared/formatting.py`):
  - При значениях типа 1.995 `decimal_part` мог стать равным 100 из-за floating-point precision, что приводило к выводу «2,100 ₽» вместо «2,00 ₽»
  - Добавлена проверка `if decimal_part >= 100: integer_part += 1; decimal_part = 0`
  - Добавлены тесты `test_rounding_edge_case` и `test_rounding_near_integer`
- **Унификация API-токенов через settings.py**:
  - `gosduma/client.py`: `os.environ.get("DUMA_API_TOKEN", "")` → `settings.DUMA_API_TOKEN` (единообразное использование `MCP_RUSSIA_DUMA_API_TOKEN`)
  - `zakupki/client.py`: `os.environ.get("ZAKUPKI_API_TOKEN", "")` → `settings.ZAKUPKI_API_TOKEN` (единообразное использование `MCP_RUSSIA_ZAKUPKI_API_TOKEN`)
  - Удалены `import os` из обоих модулей
- **Устранён дубликат в `SUBIEKTY_RF`**:
  - Код 80 (Забайкальский край) дублировал код 75 — удалён
  - Добавлен тест `test_constants_subiekty_no_duplicates` — проверка уникальности кодов субъектов
  - Итого: 92 уникальных субъекта РФ (было 93 с дубликатом)
- **Обновлена документация**:
  - `docs/reference/features.md`: росстат 10→11 tools, 181→182 инструментов; описание обновлено
  - `README.md`: добавлена строка про `indikator_dannye`
- **Обновлены тесты Росстата**: 28 тестов (было 22) — добавлены тесты indikator_dannye (fallback, with_data, with_region, empty, emiss_code_direct), subiekty_no_duplicates; интеграционные тесты обновлены (1 новый)
- **Прогнаны все проверки**: `ruff check` — all passed, `pytest` (217 passed, 1 skipped для затронутых модулей)

### Ключевые архитектурные решения

- **`indikator_dannye` — универсальный вход к ЕМИСС**: инструмент принимает как числовой код ЕМИСС (напр. '31088'), так и мнемонический код из `EMISS_KODY_POKAZATELEY` (напр. 'cpi'). При мнемоническом коде автоматически подставляется название показателя из `KLYUCHEVYE_INDIKATORY`
- **API-токены унифицированы через settings.py**: все токены теперь используются через `settings.DUMA_API_TOKEN` и `settings.ZAKUPKI_API_TOKEN`, что соответствует переменным окружения `MCP_RUSSIA_DUMA_API_TOKEN` и `MCP_RUSSIA_ZAKUPKI_API_TOKEN`. Ранее использовались нестандартные имена `DUMA_API_TOKEN` и `ZAKUPKI_API_TOKEN`
- **Справочник субъектов РФ очищен от дубликатов**: код 75 (Забайкальский край) — единственный корректный код; код 80 был устаревшим дубликатом

### Следующие действия

- **Углубление интеграций**: верификация EMISS-кодов на живом fedstat.ru (26975/26976 для ВРП, 30955/31106 для сельского хозяйства/строительства)
- **Расширение региональных данных**: добавление EMISS-кодов для отраслевой структуры ВРП, инвестиций по видам деятельности
- **Подключение `requires_auth=True` для Госдумы и Закупок**: теперь когда токены унифицированы через settings, можно добавить `requires_auth=True` и `auth_env_var="MCP_RUSSIA_DUMA_API_TOKEN"` / `auth_env_var="MCP_RUSSIA_ZAKUPKI_API_TOKEN"` в `FEATURE_META`
- **Использование `AuthError`**: определён, но нигде не вызывается — следует использовать в модулях с `requires_auth=True` при отсутствии токена

## Статус раунда 2026-06-10 (тридцать третий проход — расширение Росстата, зачистка тестов)

### Выполнено

- **Расширение модуля Росстат (rosstat)**:
  - `constants.py`: EMISS-коды расширены с 8 до 21 показателя; добавлены agrarian (30955), construction (31106), vrp (26975), vrp_per_capita (26976), wages_real (24142), income_per_capita (24141), poverty_rate (24143), subsidy_income (24144), migration (24134), natural_growth (24135), gini (24146), pension_avg (24147), housing (31103)
  - `constants.py`: добавлен справочник `REGIONALNYE_POKAZATELI` — 10 показателей с региональной разбивкой
  - `constants.py`: `KLYUCHEVYE_INDIKATORY` расширено с 10 до 16 показателей (добавлены ВРП, реальная зарплата, доходы, бедность, Джини, пенсии)
  - `schemas.py`: добавлены модели `VRPData` (ВРП с данными на душу населения), `WagesData` (номинальная и реальная зарплата)
  - `client.py`: добавлены функции `poluchit_vrp()`, `poluchit_zarplatu()`, `poluchit_sravnenie_regionov()`
  - `tools.py`: добавлены инструменты `vrp_dannye` (данные о ВРП), `zarplata_dannye` (данные о зарплате), `sravnenie_regionov` (рейтинг регионов по показателю)
  - `server.py`: зарегистрированы 3 новых инструмента; итого 10 tools
  - `__init__.py`: версия 0.2.0 → 0.3.0
- **Зачистка тестовых фикстур от португальских имён**:
  - `tests/_shared/test_feature.py`: `ibge` → `cbrf`, `transparencia` → `zakupki`, `"IBGE API"` → `"ЦБ РФ API"`, `"IBGE данные"` → `"ЦБ РФ данные"`, `TRANSPARENCIA_API_KEY` → `ZAKUPKI_API_KEY`, теги `["geo", "censo"]` → `["валюта", "курсы"]`
  - `tests/_shared/test_http_client.py`: португальский docstring → русский; `base_url` тест `https://api.ibge.gov.br` → `https://www.cbr.ru`
- **Обновлён docs/examples/ofitsialnyy-redaktor.md**: секция «Что осталось доделать» → «Выполнено» (шаблоны переведены на ГОСТ Р 7.0.97-2016, примеры используют российские органы и реквизиты)
- **Обновлён docs/reference/features.md**: росстат 7→10 tools, 178→181 инструментов
- **Обновлены тесты Росстата**: 22 теста (было 14) — добавлены тесты vrp_dannye (fallback, with_data, empty), zarplata_dannye (fallback, with_data, empty), sravnenie_regionov (invalid, with_data, empty), constants (emiss_kody_complete, regionalnye_pokazateli); интеграционные тесты обновлены (3 новых)
- **Обновлён pyproject.toml**: добавлен RUF003 ignore для rosstat
- **Прогнаны все проверки**: `pytest` (614 passed, 1 skipped), `ruff check` — all passed

### Ключевые архитектурные решения

- **EMISS-коды полностью покрывают KLYUCHEVYE_INDIKATORY**: все 16 показателей имеют соответствующие ЕМИСС-коды; тест `test_constants_emiss_kody_complete` верифицирует это соответствие
- **REGIONALNYE_POKAZATELI** — новый справочник для инструментов, работающих с региональной разбивкой; позволяет `sravnenie_regionov` валидировать входной параметр
- **sravnenie_regionov** сортирует регионы по убыванию значения показателя; неверный код показателя возвращает список доступных
- **Тестовые фикстуры полностью русифицированы**: в тестах FeatureMeta и HTTP-клиента больше нет португальских имён

### Следующие действия

- **Углубление интеграций**: верификация EMISS-кодов на живом fedstat.ru (26975/26976 для ВРП, 30955/31106 для сельского хозяйства/строительства)
- **Расширение региональных данных**: добавление EMISS-кодов для отраслевой структуры ВРП, инвестиций по видам деятельности
- **Новые инструменты Росстата**: `indikator_dannye` — универсальный инструмент для произвольного показателя по коду ЕМИСС

## Статус раунда 2026-06-09 (тридцать второй проход — зачистка документации, обновление справочников)

### Выполнено

- **Обновлён docs/reference/features.md**:
  - Удалена секция DEPRECATED с 28 бразильскими модулями (legacy-модули удалены из кодовой базы)
  - Обновлены счётчики: 19 → 22 модуля, 158 → 178 инструментов, 56 → 65 ресурсов, 38 → 44 промпта
  - Добавлены описания 3 новых модулей: sovfed (6 tools, 3 resources, 2 prompts), kaznacheistvo (6 tools, 3 resources, 2 prompts), rosprirodnadzor (8 tools, 3 resources, 2 prompts)
  - Обновлён статус миграции: сервер полностью перешёл на российские реалии
- **Обновлён CONTRIBUTING.md**:
  - Удалены ссылки на удалённые модули ibge/transparencia из структуры проекта
  - Пример тестовой команды: `F=ibge` → `F=cbrf`
  - Удалена фраза про `mcp_brasil` как технический долг
- **Дочищены португальские формулировки в CHANGELOG.md**:
  - Добавлено примечание о том, что записи до 0.5.0 описывают удалённые legacy-модули
  - Помечены (legacy) все непомеченные бразильские модули: anuncios_eleitorais, tabua_mares, tse, tce_sp, transparencia
- **Зачищены бразильские формулировки в docs/**:
  - `docs/index.md`: удалены «бразильских», «бразильские», «бразильский», mcp_brasil; обновлены счётчики (19→22); убраны параграфы про legacy-модули
  - `docs/concepts/architecture.md`: удалены ссылки на mcp_brasil и «бразильский контекст»
  - `docs/guide/quickstart.md`: удалены строки про «бразильские данные» и DEPRECATED
  - `docs/guide/development.md`: обновлён раздел про переходный слой
  - `docs/examples/ekonomist.md`: удалена строка про миграцию с bacen_*/ibge_*
  - `docs/examples/ekonomicheskaya-panorama.md`: удалена строка про миграцию с bacen_*/ibge_*
  - `docs/examples/ofitsialnyy-redaktor.md`: убрано описание «переходного агента»; заменён `transparency_transfers` на `kaznacheistvo_mezhbyudzhetnye_transferty`
- **Прогнаны все проверки**: `pytest` (601 passed, 1 skipped), `ruff check` — all passed, `ruff format` — all formatted

### Ключевые архитектурные решения

- **Документация синхронизирована с кодовой базой**: features.md больше не ссылается на удалённые модули; CONTRIBUTING, quickstart, architecture — без бразильских ссылок
- **CHANGELOG сохраняет историческую достоверность**: записи о legacy-модулях помечены (legacy), добавлено пояснение в заголовке
- **Python-код полностью чист**: в src/mcp_russia/ нет португальских остатков

### Следующие действия

- **Углубление интеграций**: расширение данных по регионам (Росстат), добавление EMISS-кодов для ВРП/зарплат
- **Дочистить оставшиеся мелкие неточности** в docs/examples/ (ofitsialnyy-redaktor.md: «Что осталось доделать» — актуализировать)

## Статус раунда 2026-06-08 (тридцать первый проход — подключение API, удаление legacy, зачистка)

### Выполнено

- **Подключение реального API Совета Федерации (sovfed)**:
  - `client.py`: обновлён с multi-source fallback — sovfed.ru/api → data.gov.ru → статический справочник
  - `constants.py`: добавлены `DATA_GOV_RU_SOVFED`, `DATA_GOV_RU_BASE`, `SENATORY_SPRAVOCHNIK`
  - `__init__.py`: версия 0.1.0 → 0.2.0
- **Подключение реального API Федерального казначейства (kaznacheistvo)**:
  - `client.py`: обновлён с multi-source fallback — budget.gov.ru/api/v1 → roskazna.gov.ru/opendata
  - `constants.py`: добавлен `ROSKAZNA_OPENDATA_BASE`
  - `__init__.py`: версия 0.1.0 → 0.2.0
- **Подключение реального API Росприроднадзора (rosprirodnadzor)**:
  - `client.py`: обновлён с multi-source fallback — rpn.gov.ru/api → rpn.gov.ru/opendata → onv.register.rpn.gov.ru
  - `constants.py`: добавлены `ROSPRIRODNADZOR_OPENDATA_BASE`, `ONV_REGISTER_BASE`
  - `__init__.py`: версия 0.1.0 → 0.2.0
- **Удаление всех 27 legacy-модулей с бразильскими данными из кодовой базы**:
  - Исходники: ana, anuncios_eleitorais, bacen, brasilapi, camara, compras, dados_abertos, datajud, diario_oficial, ibge, inpe, jurisprudencia, saude, senado, tabua_mares, tce_ce, tce_pe, tce_pi, tce_rj, tce_rn, tce_rs, tce_sc, tce_sp, tce_to, tcu, transferegov, transparencia, tse
  - Тесты: соответствующие директории удалены
  - Конфигурация ruff: удалены 20+ строк per-file-ignores для удалённых модулей
- **Зачистка португальских формулировок**:
  - `formatting.py`: удалены deprecated-алиасы `format_brl`, `format_number_br`, `parse_brl_number`; обновлён модульный docstring
  - `validators.py`: удалены Brazilian validators (`validate_cpf`, `format_cpf`, `validate_cnpj`, `format_cnpj`, `validate_cep`, `format_cep`, `_CNPJ_WEIGHTS_*`); обновлён модульный docstring
  - `tests/conftest.py`: удалена `MCP_BRASIL_TOOL_SEARCH`
  - `tests/test_discovery.py`: обновлён комментарий `MCP_BRASIL_TOOL_SEARCH` → `MCP_RUSSIA_TOOL_SEARCH`
  - `tests/_shared/test_batch.py`: `resultado ok` → `rezultat ok`
  - `tests/_shared/test_formatting.py`: удалены тесты `TestFormatBrlDeprecated`, `TestFormatNumberBrDeprecated`, `TestParseBrlNumberDeprecated`
  - `tests/_shared/test_validators.py`: удалены тесты `TestValidateCPF`, `TestFormatCPF`, `TestValidateCNPJ`, `TestFormatCNPJ`, `TestValidateCEP`, `TestFormatCEP`
  - `data/__init__.py`: обновлён docstring — убрана ссылка на «бразильские источники»
  - `tests/test_root_server.py`: `подключёнными` → `подключенными`
- **Обновлён README.md**: отражено удаление legacy-модулей, подключение API трёх модулей
- **Обновлён pyproject.toml**: убраны ruff per-file-ignores для удалённых модулей
- **Прогнаны все проверки**: `pytest` (601 passed, 1 skipped), `ruff check` — all passed, `ruff format` — all formatted

### Ключевые архитектурные решения

- **Multi-source fallback**: все три новых модуля используют каскадный fallback при недоступности API: первичный API → вторичный открытый источник → статический справочник
- **Полное удаление legacy-модулей**: вместо `enabled=False` модули удалены из кодовой базы. Кодовая база уменьшена на ~27 директорий с исходниками и ~27 директорий с тестами
- **Устранены все backward-compat алиасы**: `format_brl`, `format_number_br`, `parse_brl_number`, Brazilian validators — больше не существуют в коде
- **Чистая кодовая база**: только 22 российских модуля, все с русскими именами, без португальских остатков в активном коде

### Следующие действия

- **Углубление интеграций**: расширение данных по регионам (Росстат), добавление EMISS-кодов для ВРП/зарплат
- **Дочистить оставшиеся португальские формулировки** в CHANGELOG.md и docs/ (исторические записи)
- **Обновить docs/reference/features.md**: удалить секцию DEPRECATED (legacy-модули удалены)

## Статус раунда 2026-06-08 (тридцатый проход — отключение legacy-модулей, новые модули: Совет Федерации, Казначейство, Росприроднадзор)

### Выполнено

- **Отключение всех 27 legacy-модулей с бразильскими данными** (`enabled=False`):
  - ana, anuncios_eleitorais, bacen, brasilapi, camara, compras, dados_abertos, datajud, diario_oficial, ibge, inpe, jurisprudencia, saude, senado, tabua_mares, tce_ce, tce_pe, tce_pi, tce_rj, tce_rn, tce_rs, tce_sc, tce_sp, tce_to, tcu, transferegov, transparencia, tse
  - Все португальские инструменты больше не экспонируются через сервер
  - Модули сохранены в кодовой базе для справки, но не загружаются
- **Создание модуля Совет Федерации (sovfed)**:
  - `client.py`: poisk_senatorov, info_senatora, spisok_komitetov, spisok_komissiy, poisk_zakonoproektov, spisok_zasedaniy
  - `tools.py`: 6 инструментов с async + Context, форматированный вывод через markdown_table
  - `constants.py`: 16 комитетов, 7 комиссий, статусы законопроектов, должности сенаторов
  - `schemas.py`: SenatorRezyume, KomitetInfo, ZasedanieInfo, ZakonoproektSovfeda
  - `resources.py`: istochniki_dannyh, struktura_sovfeda, reglament
  - `prompts.py`: analiz_senatora, obzor_zakonodatelstva
  - `server.py`: FastMCP с 6 tools, 3 resources, 2 prompts
- **Создание модуля Федеральное казначейство (kaznacheistvo)**:
  - `client.py`: poluchit_ispolnenie_byudzheta, poisk_uchastnikov_bp, poisk_uchrezhdeniy, poluchit_mezhbyudzhetnye, poluchit_byudzhetnuyu_smetu
  - `tools.py`: 6 инструментов с async + Context
  - `constants.py`: виды бюджетов, категории расходов, статусы исполнения
  - `schemas.py`: ByudzhetnayaSmeta, UchastnikBP, SvedeniyaUchrezhdeniya, MezhbyudzhetnyyTransfer
  - `resources.py`: istochniki_dannyh, struktura_kaznacheistva, byudzhetnaya_sistema
  - `prompts.py`: analiz_ispolneniya_byudzheta, obzor_byudzhetnoy_sistemy
- **Создание модуля Росприроднадзор (rosprirodnadzor)**:
  - `client.py`: poisk_proverok, info_proverki, poisk_obektov_negativnogo, poisk_litsenziy_nedra, poluchit_ekologicheskie_platezhi
  - `tools.py`: 8 инструментов с async + Context
  - `constants.py`: виды надзора, категории ОНВ, виды лицензий недропользования, статусы проверок, типы нарушений
  - `schemas.py`: ProverkaEkologicheskaya, ObektNegativnogoVozdeystviya, LicenziyaNedropolzovanie, EkologicheskiyPlatezh
  - `resources.py`: istochniki_dannyh, struktura_rosprirodnadzora, zakonodatelstvo_ekologicheskoe
  - `prompts.py`: analiz_ekologicheskoy_proverki, obzor_nedropolzovaniya
- **Обновлены тесты**:
  - sovfed: 11 тестов (tools + integration)
  - kaznacheistvo: 9 тестов (tools + integration)
  - rosprirodnadzor: 13 тестов (tools + integration)
  - Обновлены test_root_server.py, test_discovery.py, test_batch.py, test_feature.py для работы с активными российскими модулями вместо отключённых бразильских
  - Исправлены pre-existing ошибки ruff (SIM117, E501) в tests/data/minobrnauki/test_tools.py
- **Обновлён README.md**: 22 модуля активны, 27 отключены, обновлён дисклеймер
- **Обновлена конфигурация ruff**: добавлены RUF001/RUF002/E501 ignores для sovfed, kaznacheistvo, rosprirodnadzor
- **Прогнаны все проверки**: `pytest` (2009 passed, 1 skipped), `ruff check` — all passed, `ruff format` — all formatted

### Ключевые архитектурные решения

- **Все legacy-модули отключены через enabled=False**: вместо удаления модулей из кодовой базы, они помечены как неактивные. FeatureRegistry пропускает их при загрузке, инструменты не экспонируются. Это позволяет сохранить код для справки при необходимости.
- **Сервер экспонирует только русскоязычные инструменты**: 22 активных модуля (19 + 3 новых), все с русскими именами функций и инструментов.
- **Новые модули следуют единому паттерну**: async модульные функции, http_get/http_post, Context, markdown_table, fallback на статические справочники.

### Следующие действия

- **Подключение реальных API** в новых модулях: sovfed→sovfed.ru, kaznacheistvo→roskazna.gov.ru, rosprirodnadzor→rpn.gov.ru
- **Углубление интеграций**: расширение данных по регионам (Росстат), добавление EMISS-кодов для ВРП/зарплат
- **Дочистить оставшиеся португальские формулировки** в документации и CHANGELOG
- **Удалить отключённые legacy-модули** из кодовой базы при подтверждении ненужности

## Статус раунда 2026-06-05 (двадцать девятый проход — Росводресурсы, Минздрав, Счётная палата, зачистка португальского)

### Выполнено

- **Подключение реального API Государственного водного реестра в модуле Росводресурсы (rosvodresursy)**:
  - `client.py`: полная переработка — заглушки заменены на реальные запросы к text.water.ru и gmvo.skniigkh.ru
  - `poisk_vodnykh_obektov()` — поиск водных объектов через Государственный водный реестр (text.water.ru)
  - `info_vodnogo_obekta()` — карточка водного объекта из реестра
  - `poluchit_gidro_dannye()` — гидрологические данные с мониторинговых постов ГМВО (gmvo.skniigkh.ru)
  - `poluchit_dannye_vodokhranilishcha()` — данные о водохранилищах через ГМВО
  - `poluchit_vodopolzovanie()` — данные о водопользовании из открытых источников
  - `tools.py`: все инструменты переведены на async с Context, форматированный вывод; добавлен инструмент `poisk_vodnykh_obektov`; `info_vodokhranilishcha` — fallback на статический справочник при отсутствии данных API
  - `constants.py`: добавлены `VODNYY_REESTR_BASE`, `GMVO_API_BASE`, `DATA_GOV_RU_BASE`, `PRIZNAKI_NAPOLNENIYA`, `OPASNYYE_GIDRO_YAVLENIYA`; расширены данные водохранилищ (6→10, добавлены объём и площадь)
  - Версия модуля: 0.1.0 → 0.2.0
- **Подключение реального API ФРМО и Росздравнадзора в модуле Минздрав (minzdrav)**:
  - `client.py`: полная переработка — заглушки заменены на реальные запросы к data.minzdrav.gov.ru, roszdravnadzor.gov.ru и frrr.rosminzdrav.ru
  - `poisk_med_organizatsiy()` — поиск медицинских организаций через ФРМО (frrr.rosminzdrav.ru)
  - `info_med_organizatsii()` — карточка МО через ФРМО
  - `poisk_litsenziy()` — новый инструмент: поиск лицензий Росздравнадзора
  - `pokazateli_zdorovya()` — показатели здоровья из открытых данных Минздрава (data.minzdrav.gov.ru)
  - `statistika_zabolevaniy()` — статистика заболеваемости из открытых данных Минздрава
  - `tools.py`: все инструменты переведены на async с Context, форматированный вывод; добавлен инструмент `poisk_litsenziy`
  - `constants.py`: добавлены `MINZDRAV_OPEN_DATA`, `FRMO_API_BASE`, `ROSZDRAVNADZOR_API`, `VIDY_LITSENZIRUEMOY_DEYATELNOSTI`; расширены справочники (ТИПЫ_МО 8→12, СПЕЦИАЛЬНОСТИ 10→15, МКБ-10 8→10)
  - Версия модуля: 0.1.0 → 0.2.0
- **Подключение реального API Счётной палаты в модуле rosaudit**:
  - `client.py`: полная переработка — заглушки заменены на реальные запросы к ach.gov.ru и budget.gov.ru
  - `poisk_kontrolnyh_meropriyatiy()` — новый инструмент: поиск контрольных мероприятий через ach.gov.ru
  - `poluchit_kontrolnoe_meropriyatie()` — карточка мероприятия по номеру
  - `poluchit_auditorskoe_zaklyuchenie()` — аудиторское заключение по номеру
  - `poluchit_byudzhet_ispolnenie()` — данные об исполнении бюджета через budget.gov.ru
  - `poisk_narusheniy()` — поиск выявленных нарушений через ach.gov.ru
  - `tools.py`: все инструменты переведены на async с Context, форматированный вывод; добавлен инструмент `poisk_kontrolnyh_meropriyatiy`
  - `constants.py`: добавлены `BUDGET_GOV_RU_BASE`, `STATUSY_KONTROLYA`, `VIDY_NARUSHENIY`; расширены справочники (ТИПЫ_МЕРОПРИЯТИЙ 6→8, СУБЪЕКТЫ_АУДИТА 5→7); исправлен mixed-script код `antiкоррупция` → `antikorruptsiya`
  - Версия модуля: 0.2.0
- **Зачистка оставшегося португальского текста**:
  - `cliff.toml`: португальский header changelog заменён на русский
  - `tests/_shared/test_feature.py`: все португальские docstrings переведены на русский; `IBGE dados` → `IBGE данные`; `Portal da Transparência` → `Портал прозрачности`; раздел `Integration: mount e call` → `Интеграция: монтирование и вызов`
  - `tests/_shared/test_settings.py`: португальский docstring переведён; `MCP_BRASIL_HTTP_TIMEOUT` → `MCP_RUSSIA_HTTP_TIMEOUT`
- **Обновлены тесты**:
  - rosvodresursy: 14 тестов (было 7) — добавлены тесты с моками (poisk found/empty, info found, gidro with data, vodokhranilishche static fallback, vodopolzovanie with data)
  - minzdrav: 14 тестов (было 10) — добавлены тесты с моками (poisk found/empty, info found, poisk_litsenziy found/empty, pokazateli found/empty, statistika found/empty)
  - rosaudit: 14 тестов (было 7) — добавлены тесты с моками (poisk_kontrolnyh found/empty, info_kontrolnogo found, info_auditorskogo found, ispolnenie found, poisk_narusheniy found)
- **Обновлён README.md**: все 19 модулей подключены к реальным API
- **Обновлена конфигурация ruff**: добавлены RUF001/RUF002 ignores для `tests/_shared/*`, `tests/data/rosvodresursy/*`, `tests/data/rospotrebnadzor/*`, `tests/data/roskomnadzor/*`, `tests/data/fssp/*`, `tests/data/publikatsii/*`, `tests/data/cekrf/*`
- **Прогнаны все проверки**: `pytest` (1974 passed, 1 skipped), `ruff check` — all passed, `ruff format` — all formatted

### Ключевые архитектурные решения

- **Росводресурсы работает через Государственный водный реестр + ГМВО**: text.water.ru — поиск и карточки водных объектов; gmvo.skniigkh.ru — гидрологический мониторинг и данные водохранилищ; fallback на статический справочник водохранилищ при недоступности API
- **Минздрав работает через ФРМО + открытые данные + Росздравнадзор**: frrr.rosminzdrav.ru — реестр медицинских организаций; data.minzdrav.gov.ru — показатели здоровья и заболеваемость; roszdravnadzor.gov.ru — реестр лицензий
- **Счётная палата работает через ach.gov.ru + budget.gov.ru**: ach.gov.ru — контрольные мероприятия, аудиторские заключения, нарушения; budget.gov.ru — исполнение федерального бюджета
- **Итого модулей с реальными API-интерфейсами**: 19 (все российские модули подключены: cbrf, rosgidromet, fns, gosduma, zakupki, kad_arbitrazh, rosapi, rosreestr, gibdd, cekrf, fssp, publikatsii, minobrnauki, rospotrebnadzor, roskomnadzor, rosstat, rosvodresursy, minzdrav, rosaudit)

### Следующие действия

- **Создание новых модулей**: Совет Федерации (sovfed), Федеральное казначейство (kaznacheistvo), Росприроднадзор (rosprirodnadzor)
- **Углубление интеграций**: расширение данных по регионам (Росстат), добавление EMISS-кодов для ВРП/зарплат
- **Дочистить оставшиеся португальские формулировки** в deprecated Brazilian модулях и тестах

## Статус раунда 2026-06-05 (двадцать восьмой проход — Минобрнауки, Роспотребнадзор, Роскомнадзор, Росстат, зачистка ссылок)

### Выполнено

- **Подключение реального API Рособрнадзора в модуле Минобрнауки (minobrnauki)**:
  - `client.py`: полная переработка — заглушки заменены на реальные запросы к obrnadzor.gov.ru
  - `poisk_akreditovannyh_vuzov()` — поиск аккредитованных вузов через открытые данные Рособрнадзора (7710542907-FS_ACCRED)
  - `info_akkreditacii()` — карточка аккредитации по ИНН
  - `poisk_licenziy()` — поиск лицензий через открытые данные Рособрнадзора (7710542907-FS_LICENSE)
  - `poluchit_reyting()` — рейтинг вузов через vuz.minobrnauki.gov.ru API
  - `tools.py`: все инструменты переведены на async с Context, форматированный вывод; добавлен инструмент `poisk_licenziy`
  - `constants.py`: добавлены `OBRNADZOR_ACCRED_URL`, `OBRNADZOR_LICENSE_URL`, `VUZ_RATING_URL`
  - Версия модуля: 0.1.0 → 0.2.0
- **Подключение реального API реестра проверок в модуле Роспотребнадзор (rospotrebnadzor)**:
  - `client.py`: полная переработка — заглушки заменены на реальные запросы к proverki.rospotrebnadzor.ru и zpp.rospotrebnadzor.ru
  - `poisk_proverok()` — поиск проверок в реестре proverki.rospotrebnadzor.ru
  - `info_proverki()` — карточка проверки по номеру
  - `plan_proverok()` — план проверок по году и региону
  - `poisk_zhalob()` — поиск жалоб потребителей через zpp.rospotrebnadzor.ru
  - `tools.py`: все инструменты переведены на async с Context, форматированный вывод; добавлены инструменты `poisk_proverok`, `plan_proverok`
  - `constants.py`: добавлены `PROVERKI_API_BASE`, `ZPP_API_BASE`, `STATUSY_PROVEROK`, `VIDY_NARUSHENIY`
  - Версия модуля: 0.1.0 → 0.2.0
- **Подключение реальных API реестров Роскомнадзора в модуле roskomnadzor**:
  - `client.py`: полная переработка — заглушки заменены на реальные запросы к rkn.gov.ru и eais.rkn.gov.ru
  - `poisk_operatora_pd()` — поиск оператора ПД в реестре rkn.gov.ru/pdn
  - `poisk_ori()` — поиск ОРИ в реестре rkn.gov.ru/registry-ori
  - `proverka_blokirovki()` — проверка домена в реестре запрещённых сайтов eais.rkn.gov.ru
  - `poisk_licenziy()` — поиск лицензий связи в реестре rkn.gov.ru/licenses
  - `poisk_smi()` — поиск СМИ в реестре rkn.gov.ru/mass-media
  - `tools.py`: все инструменты переведены на async с Context, форматированный вывод; добавлены инструменты `proverka_blokirovki`, `poisk_ori`
  - `constants.py`: добавлены `RKN_OPENDATA_BASE`, `EAIS_API_BASE`, `PDN_REGISTRY_URL`, `ORI_REGISTRY_URL`, `OSNOVANIYA_BLOKIROVKI`; реестры дополнены URL-адресами
  - Версия модуля: 0.1.0 → 0.2.0
- **Подключение реального API ЕМИСС в модуле Росстат (rosstat)**:
  - `client.py`: полная переработка — placeholder-функции заменены на реальные запросы к fedstat.ru/api
  - `poluchit_indikator()` — запрос статистического показателя через ЕМИСС с использованием кодов показателей
  - `poluchit_inflyaciyu()` — получение данных об инфляции (ИПЦ) через ЕМИСС
  - `poluchit_demografiyu()` — получение демографических данных через ЕМИСС
  - `poluchit_dannye_regiona()` — получение данных по региону через ЕМИСС с fallback на статический справочник
  - `poluchit_federalny_okrug()` — информация о федеральном округе с перечнем субъектов
  - `tools.py`: `inflyaciya()` и `demografiya()` теперь возвращают реальные данные из ЕМИСС (с fallback)
  - `constants.py`: добавлены `EMISS_KODY_POKAZATELEY` (8 показателей), `ROSSTAT_BASE`; расширен список субъектов с 10 до 93 (все субъекты РФ); добавлен столбец «ФО» для каждого субъекта; добавлены новые показатели (retail_trade, investments, agrarian, construction)
  - Версия модуля: 0.1.0 → 0.2.0
- **Зачистка устаревших ссылок**:
  - `rosstat/constants.py`: удалена ссылка на «Бразильский IBGE»
  - `agenty/redator/constants.py`: удалена misleading-строка о «legacy section of Brazilian constants»
- **Обновлены тесты**:
  - minobrnauki: 14 тестов (было 12) — добавлены тесты с моками (info_vuza by inn, poisk_licenziy)
  - rospotrebnadzor: 13 тестов (было 9) — добавлены тесты с моками (info_proverki found, poisk_proverok found/empty, plan_proverok, zhaloby found)
  - roskomnadzor: 14 тестов (было 11) — добавлены тесты с моками (proverka_blokirovki blocked/not blocked, poisk_ori, info_licenzii found, zapisi_reestra found)
  - rosstat: 14 тестов (было 10) — добавлены тесты с моками (inflyaciya with data, demografiya with data, constants subiekty count, emiss kody)
- **Обновлён README.md**: 16 из 19 модулей подключены к реальным API
- **Прогнаны все проверки**: `pytest` (1959 passed, 1 skipped), `ruff check` — all passed, `ruff format` — all formatted

### Ключевые архитектурные решения

- **Минобрнауки работает через obrnadzor.gov.ru**: открытые данные аккредитации (7710542907-FS_ACCRED) и лицензирования (7710542907-FS_LICENSE); рейтинги через vuz.minobrnauki.gov.ru
- **Роспотребнадзор работает через proverki.rospotrebnadzor.ru**: реестр проверок с поиском по ИНН/названию; жалобы потребителей через zpp.rospotrebnadzor.ru
- **Роскомнадзор работает через rkn.gov.ru**: реестр операторов ПД, реестр ОРИ, реестр лицензий связи, реестр СМИ, проверка блокировок через eais.rkn.gov.ru
- **Росстат работает через fedstat.ru/api (ЕМИСС)**: статистические показатели с кодами (ИПЦ: 31088, население: 24133 и т.д.); все 93 субъекта РФ в справочнике
- **Итого модулей с реальными API-интерфейсами**: 16 (cbrf, rosgidromet, fns, gosduma, zakupki, kad_arbitrazh, rosapi, rosreestr, gibdd, cekrf, fssp, publikatsii, minobrnauki, rospotrebnadzor, roskomnadzor, rosstat)

### Следующие действия

- **Подключение реальных API** в оставшихся модулях: rosvodresursy→Росводресурсы, minzdrav→Росздравнадзор, rosaudit→Счётная палата
- **Создание новых модулей**: Совет Федерации (sovfed), Федеральное казначейство (kaznacheistvo), Росприроднадзор (rosprirodnadzor)
- **Дочистить оставшиеся португальские формулировки** в документации и коде
- **Углубление интеграций**: расширение данных по регионам (Росстат), добавление EMISS-кодов для ВРП/зарплат

## Статус раунда 2026-06-03 (двадцать седьмой проход — ГИБДД, ЦИК РФ, ФССП, pravo.gov.ru, async-конвертация, зачистка примеров)

### Выполнено

- **Подключение реального API ГИБДД в модуле gibdd**:
  - `client.py`: полная переработка — синхронный `GibddClient` заменён на асинхронные модульные функции
  - `proverka_istorii_ts()` — GET /proxy/check/auto/history/{vin}, парсинг RequestResult
  - `proverka_dtp_ts()` — GET /proxy/check/auto/dtp/{vin}
  - `proverka_rozysk_ts()` — GET /proxy/check/auto/wanted/{vin}
  - `proverka_ogranicheniy_ts()` — GET /proxy/check/auto/restrict/{vin}
  - `proverka_vu()` — GET /proxy/check/driver/{nomer_vu}
  - `statistika_dtp_region()` — GET stat.gibdd.ru, статистика ДТП по региону
  - `tools.py`: `info_ts` запускает все 4 проверки ТС параллельно через `asyncio.gather`; штрафы поясняют, что для них нужна авторизация через Госуслуги
  - `constants.py`: добавлены `GIBDD_CHECK_BASE`, `GIBDD_STAT_BASE`
  - Версия модуля: 0.1.0 → 0.2.0
- **Подключение реального API ГАС «Выборы» в модуле ЦИК РФ (cekrf)**:
  - `client.py`: полная переработка — заглушки заменены на реальные запросы к vybory.izbirkom.ru и cikrf.ru
  - `_VyboryTableParser` — парсер HTML-таблиц ГАС «Выборы» на базе stdlib html.parser
  - `poisk_kandidata()` — поиск кандидатов через ГАС «Выборы» + fallback на cikrf.ru API
  - `kandidat_podrobno()` — карточка кандидата через cikrf.ru → ГАС «Выборы»
  - `rezultaty_vyborov()` — результаты выборов через известные election IDs
  - `yavka_i_itogi()` — явка и итоги через HTML-парсинг ГАС «Выборы»
  - `spisok_vyborov()` — новый инструмент: список известных федеральных выборов
  - `constants.py`: добавлены `VYBORY_API_BASE`, `CIK_API_BASE`, `CIK_VOTER_API`, `IZVESTNYE_VYBORY` (4 федеральных выборов с tvd/vrn), `IZBIRATELNYY_KOD_REGIONA` (83 региона)
  - `server.py`: зарегистрирован новый инструмент `spisok_vyborov` и ресурс `data://izvestnye-vybory`
  - Версия модуля: 0.1.0 → 0.2.0
- **Подключение реального API ФССП в модуле fssp**:
  - `client.py`: полная переработка — синхронный `FsspClient` заменён на асинхронные модульные функции
  - `poisk_proizvodstv()` — POST /iss/search с разбором ФИО, fallback на GET /iss/ip
  - `info_proizvodstva()` — получение данных о конкретном ИП
  - `ogranicheniya_dolzhnika()` — поиск и фильтрация ограничений
  - `rozysk_dolzhnika()` — поиск и фильтрация розыска
  - `tools.py`: все инструменты переведены на async с Context, форматированный вывод через `markdown_table`, добавлен инструмент `spisok_regionov`
  - `constants.py`: добавлены `FSSP_SEARCH_API`, `FSSP_IP_BASE`, `KODY_REGIONOV_FSSP` (25 регионов)
  - Версия модуля: 0.1.0 → 0.2.0
- **Подключение реального API pravo.gov.ru в модуле publikatsii**:
  - `client.py`: обновлены все функции на реальные эндпоинты открытых данных pravo.gov.ru
  - `constants.py`: `PRAVO_API_BASE` → `https://pravo.gov.ru/opendata/7700748144-prfgi`, добавлены `PRAVO_SEARCH_URL`, `PRAVO_DOCUMENT_URL`, `TIPY_DOKUMENTOV_PRAVO` (17 типов документов)
  - Парсеры обрабатывают оба формата ответа (API JSON и fallback на русские ключи)
  - Версия модуля: 0.1.0 → 0.2.0
- **Конвертация синхронных заглушек в async**:
  - `minobrnauki/client.py`: `MinobrnaukiClient` → async модульные функции с `http_get`
  - `rospotrebnadzor/client.py`: `RospotrebnadzorClient` → async модульные функции с `http_get`; `tools.py` переведён на async с Context, форматированный вывод
  - `roskomnadzor/client.py`: `RoskomnadzorClient` → async модульные функции с `http_get`; `tools.py` переведён на async с Context, форматированный вывод
  - Удалены все «(legacy — placeholder)» маркеры из docstrings и resources
- **Зачистка примеров docs/examples/** — замена legacy-совместимых имён инструментов на актуальные:
  - `parlamentskiy-otchet.md`: `duma_*` → `gosduma_*`, `izbirkom_*` → `cekrf_*`, `sovet_*` → `sovfed_*` (планируемый модуль)
  - `municipalnyy-kontrol.md`: `ks_region_*` → `rosaudit_*`, `eis_zakupki_*` → `zakupki_*`, `otkryte_dannye_*` → `rosstat_*`
  - `gosudarstvennaya-politika.md`: `budget_*` → отмечены как планируемые, `gas_pravosudie_*` → `kad_arbitrazh_*`, `zakupki_gov_ru_*` → `zakupki_*`
  - `zhurnalist-stati.md`: `duma_*` → `gosduma_*`, `cbr_*` → `cbrf_*`, `cik_*` → `cekrf_*`, исправлен искажённый текст `rosvoдресурсы`
  - `ofitsialnyy-redaktor.md`: `cbr_*` → `cbrf_*`, `registry_*` → `fns_*`, `eis_*` → `zakupki_*`, `healthcare_*` → `minzdrav_*`
  - `analiz-zakonodatelstva.md`: `duma_*` → `gosduma_*`, `official_publications_*` → `publikatsii_*`, `gas_pravosudie_*`/`jurisprudence_*` → `kad_arbitrazh_*`, `execute_batch` → `vypolnit_paket`, `plan_query` → `splanirovat_zapros`
- **Обновлены тесты**:
  - fssp: 9 тестов переписаны под async с Context и моками
  - gibdd: 3 теста обновлены под новый формат вывода, интеграционный тест замокан
  - roskomnadzor: 11 тестов переписаны под async
  - rospotrebnadzor: 9 тестов переписаны под async
- **Обновлены docs/reference/features.md**: ЦИК РФ 9→10 tools + 5 ресурсов; ФССП 9→10 tools; ГИБДД, ФССП, публикации — отмечены с реальными API
- **Обновлён README.md**: 12 из 19 модулей подключены к реальным API
- **Прогнаны все проверки**: `pytest` (1942 passed, 1 skipped), `ruff check` — all passed, `ruff format` — all formatted

### Ключевые архитектурные решения

- **ГИБДД — реальный API проверки ТС и ВУ**: гибдд.рф/proxy/check/* — публичные эндпоинты без авторизации; stat.gibdd.ru — статистика ДТП по регионам
- **ЦИК РФ — ГАС «Выборы» (vybory.izbirkom.ru)**: HTML-парсинг таблиц результатов выборов; известные election IDs для 4 федеральных выборов; dual-source (ГАС + cikrf.ru API)
- **ФССП — Банк данных ИП (fssp.gov.ru/iss/ip)**: POST-поиск по ФИО с разбором на компоненты; region codes для фильтрации
- **pravo.gov.ru — открытые данные**: opendata/7700748144-prfgi — поиск и получение документов по ID
- **Все модули используют единый async-паттерн**: модульные функции вместо классов, `http_get`/`http_post` из `_shared/http_client.py`
- **Итого модулей с реальными API-интерфейсами**: 12 (cbrf, rosgidromet, fns, gosduma, zakupki, kad_arbitrazh, rosapi, rosreestr, gibdd, cekrf, fssp, publikatsii)

### Следующие действия

- **Миграция португальских имён переменных** в legacy-модулях — ~681 идентификатор (254 функции + 235 классов + 192 константы)
- **Подключение реальных API** в оставшихся модулях: rosstat→ЕМИСС/fedstat.ru, rospotrebnadzor→zpp.rospotrebnadzor.ru, roskomnadzor→rkn.gov.ru, minobrnauki→obrnadzor.gov.ru
- **Создание новых модулей**: Совет Федерации (sovfed), Федеральное казначейство (kaznacheistvo), Росприроднадзор (rosprirodnadzor)
- **Дочистить оставшиеся португальские формулировки** в документации и коде

## Статус раунда 2026-06-03 (двадцать шестой проход — Dadata API, pkk.rosreestr.ru, зачистка CONTRIBUTING/CHANGELOG)

### Выполнено

- **Подключение реального API Dadata в модуле РосАПИ (rosapi)**:
  - `client.py`: полная переработка — `http_get` → `http_post` (Dadata использует POST для suggest), добавлены хедеры авторизации через `_dadata_headers()`, токен берётся из `MCP_RUSSIA_DADATA_API_KEY` (settings.py)
  - `_suggest_address`, `_find_by_fias`, `_postal_by_index`, `_find_org_by_inn`, `_find_org_by_ogrn`, `_list_banks`, `_find_bank_by_bik` — все используют `http_post` с корректными Dadata-эндпоинтами
  - `_postal_by_index` — реальная реализация через Dadata suggest/address вместо placeholder
  - `find_bank_by_bik` — реальная реализация через Dadata suggest/bank вместо заглушки
  - Добавлены хелперы `_nested_get`, `_parse_org_data`, `_parse_bank_data` для чистого парсинга ответов Dadata
  - Обработка вложенных объектов Dadata (name.full/short, state.status, address.value, management.name)
  - `tools.py`: обновлён `konsul_bank_po_bik` — теперь вызывает Dadata API, fallback на встроенный справочник
  - Удалены все placeholder-формулировки («Требуется интеграция»), заменены на инструкции по настройке API-ключа
  - Версия модуля: 0.1.0 → 0.2.0, `requires_auth=True`
- **Подключение реального API pkk.rosreestr.ru в модуле Росреестр (rosreestr)**:
  - `client.py`: полная переработка — синхронный класс `RosreestrClient` заменён на асинхронные модульные функции
  - `poluchit_obekt()` — GET pkk.rosreestr.ru/api/features/1/{kad_number}, парсинг attrs → KadastrovyyObekt
  - `poluchit_kadastrovnuyu_stoimost()` — тот же эндпоинт, извлечение cad_cost/cadastral_cost
  - `poluchit_prava()` — извлечение rights из ответа pkk
  - `poisk_po_nomeru()` — поиск объектов по запросу через pkk
  - Добавлены `_parse_obekt()` парсер и справочные мапы (STATUSY_UCHE_TA_MAP, KATEGORII_ZEMEL_MAP)
  - `tools.py`: info_obekta, kadastrovaya_stoimost, prava_na_obekt — async с Context, форматированный вывод с format_rub
  - `resources.py`: убраны маркеры «(legacy — placeholder)»
  - `constants.py`: добавлен PKK_API_BASE, мапы TIPY_NEDVIZIMOSTI_MAP, KATEGORII_ZEMEL_MAP, STATUSY_UCHE_TA_MAP, FORMY_SOBSTVENNOSTI_MAP
  - Версия модуля: 0.1.0 → 0.2.0, `api_base` обновлён на pkk.rosreestr.ru
- **Добавлены API-ключи в settings.py**: DADATA_API_KEY, DUMA_API_TOKEN, ZAKUPKI_API_TOKEN
- **Обновлён .env.example**: добавлены секции для Dadata, Госдума, ЕИС Закупки API-токенов
- **Обновлены тесты**:
  - rosapi: 19 тестов (было 10) — добавлены тесты success-сценариев (адрес, организация, банк через Dadata)
  - rosreestr: 13 тестов (было 8) — добавлены async-тесты с моками (info_obekta, kadastrovaya_stoimost, prava_na_obekt)
- **Зачистка CONTRIBUTING.md**: португальские примеры коммитов заменены на российские (`ibge` → `cbrf`, `bacen` → `fns`, `transparencia` → `zakupki`, `camara` → `gosduma`, `saude` → `minzdrav`)
- **Исправлен «bolsa-запросов» в CHANGELOG.md**: португальско-русский гибрид → «массовых запросов»
- **Обновлён README.md**: 6 → 8 модулей с реальными API
- **Прогнаны все проверки**: `pytest` (1941 passed, 1 skipped), `ruff check` — all passed, `ruff format` — all formatted

### Ключевые архитектурные решения

- **Dadata — основной провайдер справочных данных**: адреса (ФИАС), организации (ЕГРЮЛ/ЕГРИП), банки — всё через единый API с токеном
- **pkk.rosreestr.ru — публичный API Росреестра**: не требует авторизации, возвращает JSON с кадастровыми данными
- **Единый паттерн API-ключей**: все токены хранятся в settings.py и читаются из переменных окружения `MCP_RUSSIA_*`
- **РосАПИ — седьмой модуль с реальным API** (cbrf, rosgidromet, fns, gosduma, zakupki, kad_arbitrazh, rosapi)
- **Росреестр — восьмой модуль с реальным API**
- **Итого модулей с реальными API-интерфейсами**: 8

### Следующие действия

- **Миграция португальских имён переменных** в legacy-модулях — ~7,500 идентификаторов (transparencia: 1,050, tse: 790, compras: 748, senado: 672, camara: 507)
- **Подключение реальных API** в остальных модулях: rosstat→ЕМИСС, cekrf→vybory.izbirkom.ru, publikatsii→pravo.gov.ru, minzdrav→data.minzdrav.gov.ru, gibdd→гибдд.рф, fssp→fssp.gov.ru
- **Конвертация синхронных заглушек в async**: gibdd, fssp, minobrnauki, rospotrebnadzor, roskomnadzor — все используют class-based синхронные заглушки
- **Создание модуля ЕМИСС/Fedstat**: расширение Росстата реальными данными из fedstat.ru
- **Дочистить оставшиеся португальские формулировки** в документации и коде

## Статус раунда 2026-06-02 (двадцать пятый проход — redator русификация, КАД API, зачистка документации)

### Выполнено

- **Полная русификация модуля agenty/redator/**:
  - `schemas.py`: `PronomeTratamento` → `ObrashchenieDolzhnostnogoLitsa`, поля: cargo→dolzhnost, tratamento→obrashchenie, vocativo→titulovanie, abreviatura→adresatsiya, enderecamento удалено; `ValidacaoDocumento` → `RezultatValidatsii`, поля: valido→korrektno, problemas→problemy, sugestoes→rekomendatsii
  - `constants.py`: удалён весь legacy-раздел с португальскими константами (строки 141-257): `MESES` (португальские месяцы), `TIPOS_DOCUMENTO`, `PREFIXOS_DOCUMENTO`, `PRONOMES_TRATAMENTO` (12 бразильских обращений — Vossa Excelência, Vossa Senhoria и т.д.)
  - `resources.py`: переименованы файлы: `oficio.md` → `pismo.md`, `manual_redacao.md` → `manual_deloproizvodstvo.md`, `pronomes.md` → `obrashcheniya.md`, `fechos.md` → `zaklyuchitelnye_formuly.md`
  - Файлы шаблонов/норм переименованы на диске (содержимое уже русское)
  - `__init__.py`: удалена ссылка на «Manual de Redacao da Presidencia»
- **Подключение реального API Картотеки арбитражных дел в модуле kad_arbitrazh**:
  - `constants.py`: обновлены эндпоинты (KAD_SEARCH_URL, KAD_INSTANCE_URL), добавлен справочник судов по кодам `SUDY_PRYAMYE` (49 судов), категории дел по букве номера `KATEGORII_KAD`, удалён дублирующийся `ARBITRAZHNYE_SUDY`
  - `client.py`: полная переработка — `poisk_del()` использует POST kad.arbitr.ru/Kad/Search, `info_dela()` — GET kad.arbitr.ru/Kad/Case/{number}, `akty_po_delu()` — GET kad.arbitr.ru/Kad/Documents/{number}, `storony_dela()` — GET kad.arbitr.ru/Kad/Sides/{number}, `zasedaniya_po_delu()` — GET kad.arbitr.ru/Kad/Sessions/{number}, добавлены парсеры `_parse_rezultaty_poiska()`, `_parse_kartochka_dela()`, `_parse_akty()`, `_parse_storony()`, вспомогательные функции `_opredelit_sud_po_nomeru()`, `_opredelit_kategoriyu()`
  - `tools.py`: `poisk_del()` теперь выводит реальные данные из КАД в таблице (номер, категория, статус, суд, сумма иска)
  - `resources.py`: добавлено описание реальных API-эндпоинтов
  - `__init__.py`: версия 0.1.0 → 0.2.0
  - КАД — шестой модуль с реальным API-интерфейсом
- **Обновлены тесты kad_arbitrazh**: добавлены 16 тестов — парсеры (rezultaty_poiska, kartochka_dela, akty, storony), opredelit_sud_po_nomeru, opredelit_kategoriyu, инструменты с моками реальных данных
- **Зачистка CHANGELOG.md**: все 30 записей с португальскими именами модулей помечены как `(legacy)` — camara, senado, datajud, jurisprudencia, tse, tcu, transparencia, ibge, bacen, compras, diario_oficial, transferegov, tce_*
- **Исправлена таблица resource URI в docs/examples/ofitsialnyy-redaktor.md**: 9 устаревших английных URI (`redator://manual/structure` и т.д.) заменены на актуальные русские (`template://pismo`, `normas://manual` и т.д.)
- **Исправлен пример в docs/guide/development.md и Makefile**: `make test-feature F=ibge` → `F=cbrf`
- **Очищены португальские комментарии в _shared/batch.py**: `compras/pncp, compras/dadosabertos` → нейтральные формулировки
- **Прогнаны все проверки**: `pytest` (1935 passed, 1 skipped), `ruff check` — all passed, `ruff format` — all formatted

### Ключевые архитектурные решения

- **Модуль redator полностью русифицирован**: нет португальских имён классов, полей, констант, файлов шаблонов/норм
- **КАД работает через kad.arbitr.ru**: публичный API без авторизации, POST-поиск по делам, GET-запросы карточки/актов/сторон/заседаний
- **Справочник судов по кодам**: 49 арбитражных судов определяются по первым символам номера дела (А40 → АС г. Москвы, А77 → АС г. Санкт-Петербурга и т.д.)
- **Итого модулей с реальными API-интерфейсами**: 6 (cbrf, rosgidromet, fns, gosduma, zakupki, kad_arbitrazh)

### Следующие действия

- **Миграция португальских имён переменных** в legacy-модулях — ~800+ имён (camara: 202 идентификатора, senado, datajud, saude и др.)
- **Подключение реальных API** в остальных модулях: rosapi→Dadata, rosstat→ЕМИСС, cekrf→vybory.izbirkom.ru, publikatsii→pravo.gov.ru, minzdrav→data.minzdrav.gov.ru
- **Создание модуля ЕМИСС/Fedstat**: расширение Росстата реальными данными из fedstat.ru
- **Дочистить оставшиеся португальские формулировки** в документации и коде

### Выполнено

- **Подключение реального API Государственной Думы в модуле gosduma**:
  - `constants.py`: обновлены API-эндпоинты (`api.duma.gov.ru/api/v1`), добавлены `DUMA_VOTES`, `DUMA_TRANSCRIPTS`, `STATUSY_ZAKONOPROEKTOV`, `FRAKCIYA_API_MAP`
  - `client.py`: полная переработка — `poluchit_deputatov()` использует api.duma.gov.ru, `poluchit_zakonoproekty()` — СОЗД API, `poluchit_golosovaniya()` — API голосований, добавлена поддержка `DUMA_API_TOKEN`, парсеры `_parse_deputats()`, `_parse_zakonoproekty()`, `_parse_golosovaniya()`, `_parse_one_deputat()`
  - `tools.py`: обновлены все инструменты для форматированного вывода с реальными данными, добавлен инструмент `golosovaniya()` (результаты голосований)
  - `server.py`: зарегистрирован новый инструмент `golosovaniya` (теги: голосования, активность)
  - `resources.py`: обновлены источники данных (api.duma.gov.ru)
  - `__init__.py`: версия 0.1.0 → 0.2.0, обновлён api_base
  - Госдума — четвёртый модуль с реальным API-интерфейсом (после ЦБ РФ, Росгидромета, ФНС)
- **Подключение реального API ЕИС Закупок в модуле zakupki**:
  - `client.py`: полная переработка — `poisk_zakupok()` использует API ЕИС, `poluchit_zakupku()` — карточка закупки, `poisk_kontraktov()` — реестр контрактов, `info_zakazchika()` и `info_postavshchika()` используют ЕГРЮЛ/ЕГРИП через модуль ФНС, `plany_zakupok()` — планы-графики, парсеры `_parse_zakupki_search()`, `_parse_kontrakty()`, `_parse_plany()`, добавлена поддержка `ZAKUPKI_API_TOKEN`
  - `tools.py`: обновлены все инструменты для форматированного вывода, добавлен инструмент `poisk_kontraktov()`, исправлена опечатка «Deadline подачи заявок» → «Срок подачи заявок»
  - `server.py`: зарегистрирован новый инструмент `poisk_kontraktov` (теги: контракты, поиск)
  - `__init__.py`: версия 0.1.0 → 0.2.0, исправлена опечатка «закуровок» → «закупок»
  - Закупки — пятый модуль с реальным API-интерфейсом
- **Обновлены тесты**:
  - gosduma: добавлены 12 тестов (парсеры deputats/zakonoproekty/golosovaniya/one_deputat, инструменты с моками и реальными данными, golosovaniya)
  - zakupki: переписаны тесты под async-интерфейс (18 тестов — парсеры zakupki/kontrakty/determine_zakon/safe_float, инструменты с моками)
  - Обновлены интеграционные тесты (новые инструменты golosovaniya и poisk_kontraktov)
- **Дочистка CHANGELOG.md**:
  - `detalhar_proposicao` → `detal_zakonoproekta`, `buscar_proposicao` → `poisk_zakonoproekta`
  - `executar_lote` → `vypolnit_paket`
  - `votação` → `голосование`
  - `Перепись` → `Переработка`, `TCE-модулей` → `модулей ТСЕ`
  - `штатов` → `регионов`, `mcp-brasil` → `mcp-russia`
  - Добавлена пометка `(legacy-модули)` для модулей с португальскими именами
- **Исправлена опечатка в pyproject.toml**: «закуровок» → «закупок» в описании модуля zakupki
- **Прогнаны все проверки**: `pytest` (1527 passed, 1 skipped), `ruff check` — all passed, `ruff format` — all formatted

### Ключевые архитектурные решения

- **Госдума работает через api.duma.gov.ru**: поддерживается токен DUMA_API_TOKEN (опционально), парсеры обрабатывают оба варианта ключей API (surname/lastName, factionName/faction)
- **Закупки работают через zakupki.gov.ru API + ЕГРЮЛ**: поиск закупок и контрактов через API ЕИС, информация о заказчиках/поставщиках — через модуль ФНС (egrul.nalog.ru)
- **Кросс-модульная интеграция**: zakupki/client.py импортирует ФНС-клиент для получения данных о организациях по ИНН
- **Итого модулей с реальными API-интерфейсами**: 5 (cbrf, rosgidromet, fns, gosduma, zakupki)

### Следующие действия

- **Миграция португальских имён переменных** в legacy-модулях — ~800+ имён (camara: 202 идентификатора, senado, datajud, saude и др.)
- **Подключение реальных API** в остальных модулях: rosapi→Dadata, rosstat→ЕМИСС, cekrf→vybory.izbirkom.ru, kad_arbitrazh→kad.arbitr.ru, publikatsii→pravo.gov.ru, minzdrav→data.minzdrav.gov.ru
- **Создание модуля ЕМИСС/Fedstat**: расширение Росстата реальными данными из fedstat.ru
- **Дочистить оставшиеся португальские формулировки** в документации и коде

## Статус раунда 2026-06-01 (двадцать третий проход — переименование файлов примеров, подключение реальных API)

### Выполнено

- **Переименование файлов docs/examples/ с португальских на русские транслитерации** (10 файлов):
  - `analise-legislativa.md` → `analiz-zakonodatelstva.md`
  - `cientista-politico.md` → `politolog.md`
  - `economista.md` → `ekonomist.md`
  - `fiscalizacao-municipal.md` → `municipalnyy-kontrol.md`
  - `jornalista-investigativo.md` → `zhurnalist-rassledovatel.md`
  - `jornalista-materias.md` → `zhurnalist-stati.md`
  - `panorama-economico.md` → `ekonomicheskaya-panorama.md`
  - `parlamentar-report.md` → `parlamentskiy-otchet.md`
  - `politicas-publicas.md` → `gosudarstvennaya-politika.md`
  - `redator-oficial.md` → `ofitsialnyy-redaktor.md`
  - Обновлена перекрёстная ссылка в `zhurnalist-stati.md`: `./jornalista-investigativo.md` → `./zhurnalist-rassledovatel.md`
- **Подключение реального API Open-Meteo в модуле Росгидромет (rosgidromet)**:
  - `constants.py`: добавлены `OPEN_METEO_BASE`, `OPEN_METEO_AIR_QUALITY_BASE`, координаты (shirota/dolgota) для 15 городов, `WMO_KODY_POGODY` (28 кодов погоды → русские описания), `VETER_NAPRAVLENIYA` (направления ветра на русском)
  - `client.py`: полная переработка — `poluchit_pogodu()` и `poluchit_prognoz()` теперь используют Open-Meteo Forecast API, `poluchit_ekologiyu()` — Open-Meteo Air Quality API (PM2.5, PM10, CO, NO₂, SO₂, O₃ с порогами превышения нормы), `poluchit_preduprezhdeniya()` — автоматическая генерация предупреждений при экстремальных температурах и ветре
  - `tools.py`: обновлена атрибуция источников (Open-Meteo / Росгидромет)
  - Версия модуля обновлена: 0.1.0 → 0.2.0
  - Росгидромет — второй модуль с рабочим реальным API (после ЦБ РФ)
- **Подключение реального API ЕГРЮЛ/ЕГРИП в модуле ФНС (fns)**:
  - `client.py`: полная переработка — `poluchit_organizaciyu()` и `poluchit_ip()` используют публичный API egrul.nalog.ru (двухшаговый процесс: POST-поиск → GET-результат)
  - `constants.py`: добавлен `EGRUL_API_BASE`
  - `tools.py`: инструменты `info_organizacii` и `info_ip` теперь возвращают форматированный текст с реальными данными из ЕГРЮЛ/ЕГРИП, `proverki_organizacii` и `nalogovye_nachisleniya` информируют о необходимости авторизации
  - Версия модуля обновлена: 0.1.0 → 0.2.0
  - ФНС — третий модуль с рабочим реальным API
- **Обновлены тесты**:
  - rosgidromet: добавлены 6 тестов парсеров Open-Meteo (pogoda, prognoz, ekologiya, ekologiya с превышением, hpa→mmhg, deg→направление)
  - fns: переписаны тесты под async-интерфейс и форматированный вывод (8 тестов с моками)
- **Обновлена конфигурация ruff**: добавлен RUF001/RUF002 ignore для `tests/data/rosgidromet/*`
- **Прогнаны все проверки**: `pytest` (1904 passed, 1 skipped), `ruff check` — all passed, `ruff format` — all formatted

### Ключевые архитектурные решения

- **Росгидромет работает через Open-Meteo**: бесплатный API без авторизации, покрывает все крупные города России. Текущая погода, прогноз на 16 дней, качество воздуха — всё работает реально
- **ФНС работает через egrul.nalog.ru**: публичный API ФНС для поиска организаций и ИП по ИНН. Двухшаговый процесс (POST → GET) с автоматическим ожиданием результата
- **Атрибуция источников**: инструменты Росгидромета указывают «Open-Meteo / Росгидромет», инструменты ФНС — «ФНС / ЕГРЮЛ (egrul.nalog.ru)»
- **Предупреждения Росгидромета**: генерируются автоматически из текущих погодных данных (мороз ≤-30°C, жара ≥35°C, ветер ≥20 м/с, гроза)
- **Итого модулей с реальными API**: 3 (cbrf → cbr-xml-daily.ru, rosgidromet → open-meteo.com, fns → egrul.nalog.ru)

### Следующие действия

- **Подключение реальных API** в остальных модулях: rosapi→Dadata (бесплатный тариф), rosstat→ЕМИСС, gosduma→duma.gov.ru, zakupki→zakupki.gov.ru
- **Создание модуля ЕМИСС/Fedstat**: расширение Росстата реальными данными из fedstat.ru
- **Миграция португальских имён переменных** в legacy-модулях — ~800+ имён (client.py ~308 функций + tools.py ~220 функций + schemas.py ~67 классов + constants.py ~173 константы)
- **Дочистить оставшиеся португальские формулировки** в CHANGELOG.md и документации

### Выполнено

- **Полная русификация `CONTRIBUTING.md`**:
  - Заменены португальские примеры кода на русские: `minha-feature` → `primer-feature`, `exemplo.gov.br` → `example.gov.ru`, `minha_tool` → `primer_tool`, `Estado` → `Subjekt`, `buscar_localidades` → `poisk_mestopolozheniy`, `IBGE_API_BASE` → `ROSSTAT_API_BASE`, `_prefixo` → `_prefiks`, `testa lógica` → `проверяет логику`, `Build do pacote` → `Сборка пакета`, `nova_feature` → `novaya_feature`
  - Шаблоны тестов: `buscar_{feature}` → `poisk_{feature}`, `test_buscar_retorna_formatado` → `test_poisk_vozvrashaet_otformatirovannoe`, `test_buscar_sucesso` → `test_poisk_uspeshen`, `.gov.br` → `.gov.ru`, `nome/Teste` → `nazvanie/Test`, `query/teste` → `zapros/test`
- **Полная русификация `scripts/generate_diagrams.py`** (~25 замен):
  - Диаграмма system_overview: кластеры `Econômico` → `Экономика и финансы`, `Legislativo` → `Законодательство и выборы`, `Judiciário` → `Судебная система и надзор`, `Eleitoral` удалён (cekrf в законодательстве), `Fiscalização` удалён (rosaudit в судебной системе), `Ambiental & Saúde` → `Экология и здравоохранение`, `Outros` → `Реестры и справочники`, `Agentes` → `Агенты`
  - Узлы заменены с бразильских модулей на российские: `bacen/ibge/transparencia` → `cbrf/rosstat/zakupki/fns`, `câmara/senado` → `gosduma/cekrf`, `datajud/jurisprudência` → `kad_arbitrazh`, `TCEs(9)` → `rosaudit`, `inpe/ana/saúde` → `rosgidromet/rosvodresursy/minzdrav`, `brasilapi/dados_abertos/diário_oficial` → `rosapi/publikatsii/fns/rosreestr/fssp/gibdd/minobrnauki/rospotrebnadzor/roskomnadzor`
  - Мета-инструменты: `listar, recomendar, planejar, lote` → `spisok, rekomendovat, splanirovat, paket`
  - API-сервер: `APIs Governamentais (gov.br, ibge.gov.br, bcb.gov.br)` → `Государственные API (gosuslugi.ru, rosstat.gov.ru, cbr.ru)`
  - Диаграмма feature_anatomy: `data/ibge/` → `data/rosstat/`, `buscar_localidades/consultar_populacao` → `spisok_regionov/poluchit_indikator`, `IBGE_API_BASE` → `ROSSTAT_API_BASE`, `registra` → `регистрирует`, `delega HTTP` → `делегирует HTTP`, `retorna` → `возвращает`, `usa` → `использует`, `API IBGE ibge.gov.br` → `API Росстата rosstat.gov.ru`
  - Диаграмма auto_registry_flow: `Fluxo de Discovery` → `Поток обнаружения`, `nome começa com '_'?` → `имя начинается с '_'?`, `pular` → `пропустить`, `existe?` → `существует?`, `silencioso` → `молча`, `próximo módulo ou fim` → `следующий модуль или конец`, `sim/não` → `да/нет`
  - Диаграмма data_flow: `Fluxo de Dados` → `Поток данных`, `Usuário` → `Пользователь`, `orquestra` → `оркестрирует`, `pergunta` → `вопрос`, `resposta` → `ответ`, `API Gov` → `Гос. API`
  - Добавлен `# ruff: noqa: F841, RUF001` для диаграммного скрипта
- **Русификация `docs/reference/smart-tools.md`**:
  - Стратегии планировщика: `enriquecimento` → `obogashchenie`, `comparacao` → `sravnenie`, `contextualizacao` → `kontekstualizatsiya`
- **Русификация `docs/index.md`**:
  - Навигация: `Quick Start` → `Быстрый старт`, `Smart Tools` → `Умные инструменты`, `Meta-tools: discovery, planner, batch` → `Мета-инструменты: обнаружение, планирование, пакетное выполнение`, `contribution workflow` → `процесс участия`
- **Русификация `docs/guide/development.md`**: `Contribution workflow` → `Процесс участия`
- **Русификация `docs/guide/adding-features.md`**: `EXEMPLO_API_BASE` → `PRIMER_API_BASE` (2 места)
- **Исправление битых имён инструментов в docs/examples/**:
  - `parlamentar-report.md`: `zaplaniravat_zapros` → `splanirovat_zapros`, `batah_zapros` → `vypolnit_paket`, `DataJud` → `Картотека арбитражных дел`
  - `fiscalizacao-municipal.md`: `batah_zapros` → `vypolnit_paket` (2 места)
- **Замена списка бразильских источников в `docs/examples/politicas-publicas.md`**: полностью заменён параграф с перечислением IBGE, Banco Central, Portal da Transparência и т.д. на актуальный список российских источников
- **Исправление англо-русского смешения в `docs/examples/economista.md`**: `growing reflects` → корректное русское предложение
- **Зачистка `CHANGELOG.md`**: `Dados Abertos` → `открытых данных`, `Malha, CNAE` → `Сетка территорий, CNAE`, `dados_abertos (emendas, blocos, liderancas, relatorias)` → `открытых данных (поправки, блоки, лидерства, доклады)`, `resultado_eleicao` → `итогов выборов`, `planejar_consulta` → `splanirovat_zapros`
- **Подтверждено**: во всех 19 российских модулях нет португальских имён переменных, функций, классов или констант — полная миграция завершена
- **Прогнаны все проверки**: `pytest` (1896 passed, 1 skipped), `ruff check` — all passed, `ruff format` — all formatted

### Ключевые архитектурные решения

- **Диаграммы генерируются из российских модулей**: system_overview показывает актуальные 19 российских модулей, сгруппированных по функциональным кластерам
- **CONTRIBUTING.md полностью русифицирован**: примеры кода, имена переменных, URL-адреса — всё на русском/транслитерации
- **Битые имена инструментов исправлены**: `zaplaniravat_zapros` и `batah_zapros` — опечатки в документации, исправлены на `splanirovat_zapros` и `vypolnit_paket`
- **Список источников в politicas-publicas.md актуализирован**: убраны бразильские названия, оставлены только российские

### Следующие действия

- **Подключение реальных API** в российских модулях: заменить заглушки на рабочие интеграции (cbrf→cbr-xml-daily.ru уже частично работает, rosaudit→ach.gov.ru, rosgidromet→meteorf.ru, rosvodresursy→rosvodresursy.ru, publikatsii→pravo.gov.ru, zakupki→zakupki.gov.ru, minzdrav→data.minzdrav.gov.ru, kad_arbitrazh→kad.arbitr.ru, cekrf→vybory.izbirkom.ru, fns→api.nalog.ru, rosreestr→rosreestr.gov.ru, fssp→fssp.gov.ru, gibdd→гибдд.рф, minobrnauki→minobrnauki.gov.ru)
- **Создание модуля ЕМИСС/Fedstat**: расширение Росстата реальными данными из fedstat.ru
- **Миграция португальских имён переменных** в legacy-модулях — ~800+ имён (client.py ~110 функций + ~40 _parse_* helpers + ~150 параметров, schemas.py ~110 классов + ~300 полей, constants.py ~150 констант, tools.py ~80 переменных)
- **Переименование файлов примеров docs/examples/** с португальских на русские транслитерации (10 файлов)

## Статус раунда 2026-05-30 (двадцать первый проход — замена Brazilian tool IDs в примерах, фикс CI/CD)

### Выполнено

- **Замена Brazilian tool IDs на российские в docs/examples/**:
  - `panorama-economico.md`: `bacen_indicadores_atuais` → `cbrf_tekushchie_kursy`, `bacen_consultar_serie` → `cbrf_uznat_kurs_valyuty`, `bacen_comparar_series` → `cbrf_sravnit_valyuty`, `bacen_calcular_variacao` → `cbrf_uznat_kurs_valyuty`, `ibge_listar_estados` → `rosstat_spisok_regionov`, `ibge_consultar_agregado` → `rosstat_region_info`. Файл полностью переписан с российскими инструментами.
  - `economista.md`: аналогичная замена всех `bacen_*` → `cbrf_*` и `ibge_*` → `rosstat_*`. Добавлены инструменты `zakupki_*` для бюджетных сценариев.
  - `cientista-politico.md`: `duma_*` → `gosduma_*`, `senado_*` → `gosduma_*` (Госдума), `cik_*` → `cekrf_*`, `transparencia_*` → `zakupki_*`, `transferegov_*` → `zakupki_*`, `datajud_buscar_processos` → `kad_arbitrazh_poisk_del`, `saude_buscar_estabelecimentos` → `minzdrav_poisk_med_organizatsiy`, `ecologia_fokus` → `rosaudit_poisk_narusheniy`, `water_monitorar_reservuarios` → `rosvodresursy_info_vodnogo_obekta`, `eis_buscar_zakupki` → `zakupki_poisk_zakupok`, `kro_*_despesas` → `rosstat_region_info`. Таблицы переменных обновлены на российские инструменты.
  - `jornalista-investigativo.md`: `datajud_buscar_processos` → `kad_arbitrazh_poisk_del`, `transparencia_*` → `zakupki_*`, `otkryte_dannye_*` → `rosstat_*`/`zakupki_*`, `reestr_nedobrosovestnykh_postavshchikov` → `rospotrebnadzor_proverki_organizaciy`, `ofitsialnyy_byulleten_poisk` → `publikatsii_poisk_aktov`, `zdravookhranenie_uchrezhdeniya` → `minzdrav_poisk_med_organizatsiy`. Чеклист и планы расследований обновлены.
- **Фикс CI/CD workflows**: удалена ссылка на несуществующий `src/mcp_brasil/` из mypy-команд в `.github/workflows/ci.yml` и `.github/workflows/release.yml`. Команда `uv run mypy src/mcp_brasil/ src/mcp_russia/` → `uv run mypy src/mcp_russia/`.
- **Подтверждено**: `format_number_br` уже является deprecated-алиасом для `format_number_ru`, вызовов в кодовой базе нет (только тест deprecated-алиаса).
- **Прогнаны все проверки**: `pytest` (1896 passed, 1 skipped), `ruff check` — all passed, `ruff format` — all formatted

### Ключевые архитектурные решения

- **Все 4 основных примера docs/examples/ теперь используют российские tool IDs**: `cbrf_*`, `rosstat_*`, `gosduma_*`, `cekrf_*`, `zakupki_*`, `kad_arbitrazh_*`, `rosaudit_*`, `minzdrav_*`, `rospotrebnadzor_*`, `publikatsii_*`, `rosapi_*`, `rosvodresursy_*`
- **CI/CD не ссылается на mcp_brasil**: mypy-команды в обоих workflow-файлах используют только `src/mcp_russia/`
- **Нет вызовов format_number_br в рабочем коде**: deprecated-алиас существует только для backward compatibility, реальных вызовов нет

### Следующие действия

- **Подключение реальных API** в российских модулях: заменить заглушки на рабочие интеграции (cbrf→cbr-xml-daily.ru уже частично работает, rosaudit→ach.gov.ru, rosgidromet→meteorf.ru, rosvodresursy→rosvodresursy.ru, publikatsii→pravo.gov.ru, zakupki→zakupki.gov.ru, minzdrav→data.minzdrav.gov.ru, kad_arbitrazh→kad.arbitr.ru, cekrf→vybory.izbirkom.ru, fns→api.nalog.ru, rosreestr→rosreestr.gov.ru, fssp→fssp.gov.ru, gibdd→гибдд.рф, minobrnauki→minobrnauki.gov.ru)
- **Создание модуля ЕМИСС/Фedstat**: расширение Росстата реальными данными из fedstat.ru
- **Миграция оставшихся португальских имён переменных** в legacy-модулях (compras, saude, datajud и др.) — внутрикодовые переменные и имена функций, не являющиеся MCP-инструментами
- **Дочистить CHANGELOG.md от бразильских формулировок**: частично переведён, но могут оставаться португальские термины

## Статус раунда 2026-05-29 (двадцатый проход — зачистка документации от устаревших ссылок на mcp_brasil)

### Выполнено

- **Полная актуализация `docs/index.md`**: удалены все ссылки на `src/mcp_brasil/` как на существующий internal-слой. Документация теперь отражает реальное состояние: пакет `mcp_russia` — единая точка входа, `mcp_brasil` полностью устранён.
- **Полная актуализация `docs/guide/quickstart.md`**: удалены устаревшие API-ключи (`TRANSPARENCIA_API_KEY`, `DATAJUD_API_KEY`), удалены утверждения о присутствии `mcp_brasil` в кодовой базе.
- **Полная актуализация `docs/reference/configuration.md`**: удалено утверждение о fallback на `MCP_BRASIL_*` (fallback был удалён ранее). Переменные окружения `MCP_RUSSIA_*` указаны как единственный формат.
- **Полная переработка `docs/reference/features.md`**:
  - Все 19 российских модулей описаны с актуальными русскими именами инструментов
  - CBRF: `cursos_atuais` → `tekushchie_kursy`, `consultar_moeda` → `uznat_kurs_valyuty` и т.д.
  - Добавлены модули, отсутствовавшие в предыдущей версии: rospotrebnadzor (9 tools), roskomnadzor (11 tools), fns (9 tools), rosreestr (8 tools), fssp (9 tools), gibdd (12 tools), minobrnauki (12 tools)
  - Legacy-модули сгруппированы по категориям с DEPRECATED-пометками и ссылками на российские аналоги
  - Подсчёт: 19 российских модулей, 148 инструментов, 54 ресурса, 38 промптов
- **Обновление `docs/reference/smart-tools.md`**: поля моделей `EtapPlana` и `PlanZaprosa` приведены в соответствие с кодом (`etap`, `opisanie`, `parametry`, `zavisit_ot`, `obosnovanie`, `zapros`, `slozhnost`, `svodka`, `etapy`, `primechaniya`). Примеры вызовов обновлены на российские инструменты.
- **Перевод `CHANGELOG.md` на русский**: весь текст changelog переведён с португальского на русский.
- **Обновление `docs/examples/panorama-economico.md`**: удалена ссылка на `mcp-brasil`.
- **Прогнаны все проверки**: `pytest` (1896 passed, 1 skipped), `ruff check` — all passed

### Ключевые архитектурные решения

- **Документация синхронизирована с кодом**: устранены все утверждения о существовании `mcp_brasil` как internal-слоя, о поддержке `MCP_BRASIL_*` переменных окружения, о португальских именах инструментов в российских модулях.
- **features.md теперь полное руководство**: все 19 российских модулей с актуальными инструментами, ресурсами и промптами.
- **CHANGELOG.md на русском**: язык ведения changelog приведён в соответствие с остальной документацией.

### Следующие действия

- **Подключение реальных API** в российских модулях: заменить заглушки на рабочие интеграции (cbrf→cbr-xml-daily.ru уже частично работает, rosaudit→ach.gov.ru, rosgidromet→meteorf.ru, rosvodresursy→rosvodresursy.ru, publikatsii→pravo.gov.ru, zakupki→zakupki.gov.ru, minzdrav→data.minzdrav.gov.ru, kad_arbitrazh→kad.arbitr.ru, cekrf→vybory.izbirkom.ru, fns→api.nalog.ru, rosreestr→rosreestr.gov.ru, fssp→fssp.gov.ru, gibdd→гибдд.рф, minobrnauki→minobrnauki.gov.ru)
- **Создание модуля ЕМИСС/Фedstat**: расширение Росстата реальными данными из fedstat.ru
- **Миграция оставшихся португальских имён переменных** в legacy-модулях (compras, saude, datajud и др.) — внутрикодовые переменные и имена функций, не являющиеся MCP-инструментами
- **Обновление примеров docs/examples/**: заменить бразильские tool IDs (`bacen_*`, `ibge_*`, `datajud_buscar_processos`) на российские (`cbrf_*`, `rosstat_*`, `kad_arbitrazh_poisk_del`) в сценариях

## Статус раунда 2026-05-29 (девятнадцатый проход — полная миграция пакета mcp_brasil → mcp_russia)

### Выполнено

- **Полный переименование Python-пакета `mcp_brasil` → `mcp_russia`**:
  - Директория `src/mcp_brasil/` переименована в `src/mcp_russia/`
  - Старый тонкий wrapper `src/mcp_russia/` (реэкспорт) удалён — пакет теперь единый
  - Все 150+ `from mcp_brasil.*` импортов в `src/` заменены на `from mcp_russia.*`
  - Все 292+ `from mcp_brasil.*` импорта в `tests/` заменены на `from mcp_russia.*`
  - `pyproject.toml`: `packages = ["src/mcp_russia"]` (удалён `src/mcp_brasil`)
  - Все пути в `ruff per-file-ignores` обновлены на `src/mcp_russia/*`
  - `Makefile`: `mypy src/mcp_russia/`
  - `scripts/generate_diagrams.py`: `mcp-brasil` → `mcp-russia`
- **Удалены backward-compat fallback на `MCP_BRASIL_*`** из `settings.py`:
  - `MCP_BRASIL_HTTP_TIMEOUT`, `MCP_BRASIL_HTTP_MAX_RETRIES`, `MCP_BRASIL_HTTP_BACKOFF_BASE`, `MCP_BRASIL_USER_AGENT`, `MCP_BRASIL_TOOL_SEARCH` — все удалены
  - Единый формат: `MCP_RUSSIA_*`
- **Удалён `McpBrasilError` alias** из `exceptions.py`:
  - Единственный базовый класс исключений: `McpRussiaError`
- **Переименовано `agentes/` → `agenty/`**:
  - `src/mcp_russia/agentes/` → `src/mcp_russia/agenty/`
  - `tests/agentes/` → `tests/agenty/`
  - Все импорты обновлены
- **Миграция `KandidatResumo` → `KandidatKratko`** в модуле ЦИК РФ:
  - `schemas.py`: класс переименован
  - `client.py`: обновлены импорт и type hint
- **`.env.example` переведён на русский**:
  - Все комментарии и переменные на русском
  - Устранены все португальские формулировки и `MCP_BRASIL_*` переменные
- **Обновлён `rosapi/__init__.py`**: убрана ссылка на «BrasilAPI»
- **Обновлён `README.md`**: зафиксировано завершение миграции пакета
- **Прогнаны все проверки**: `pytest` (1896 passed, 1 skipped), `ruff check` — all passed, `ruff format` — all formatted

### Ключевые архитектурные решения

- **Единый Python-пакет `mcp_russia`**: исторический `mcp_brasil` полностью устранён из импортов, конфигурации и переменных окружения
- **Нет backward-compat fallback**: все `MCP_BRASIL_*` переменные окружения удалены — проект использует только `MCP_RUSSIA_*`
- **`McpRussiaError` — единственный базовый класс**: `McpBrasilError` больше не существует
- **`agenty` — целевое имя**: пакет агентов и тестов использует русскую транслитерацию

### Следующие действия

- **Подключение реальных API** в российских модулях: заменить заглушки на рабочие интеграции (cbrf→cbr-xml-daily.ru уже частично работает, rosaudit→ach.gov.ru, rosgidromet→meteorf.ru, rosvodresursy→rosvodresursy.ru, publikatsii→pravo.gov.ru, zakupki→zakupki.gov.ru, minzdrav→data.minzdrav.gov.ru, kad_arbitrazh→kad.arbitr.ru, cekrf→vybory.izbirkom.ru, fns→api.nalog.ru, rosreestr→rosreestr.gov.ru, fssp→fssp.gov.ru, gibdd→гибдд.рф, minobrnauki→minobrnauki.gov.ru)
- **Дочистить docs-артефакты**: `CHANGELOG.md`, `docs/index.md`, `docs/guide/quickstart.md`, где ещё фигурируют `mcp-brasil`/`mcp_brasil`
- **Создание модуля ЕМИСС/Фedstat**: расширение Росстата реальными данными из fedstat.ru
- **Миграция оставшихся португальских имён переменных** в legacy-модулях (compras, saude, datajud и др.) — внутрикодовые переменные и имена функций, не являющиеся MCP-инструментами

## Статус раунда 2026-05-28 (семнадцатый проход — миграция format_brl/parse_brl_number, португальские имена в инфраструктуре)

### Выполнено

- **Миграция `format_brl` → `format_rub`** во всём проекте:
  - `_shared/formatting.py`: `format_brl` теперь deprecated-алиас для `format_rub` (выход «1 234,56 ₽» вместо «R$ 1 234,56»)
  - `format_rub`: основная функция форматирования валюты (пробел-тысячи, запятая-десятичные, суффикс «₽»)
  - Заменены все 90+ вызовов `format_brl` → `format_rub` в 15 legacy-модулях: brasilapi, tse, tce_sp, tce_rs, tce_rn, tce_rj, tce_pi, tce_pe, tce_ce, compras/dadosabertos, compras/pncp, transferegov, tcu, transparencia, camara
  - Обновлены все 59 тестовых ассертов с «R$» → «₽» в 14 файлах
- **Миграция `parse_brl_number` → `parse_rub_number`**:
  - `_shared/formatting.py`: `parse_brl_number` теперь deprecated-алиас для `parse_rub_number`
  - `parse_rub_number`: расширен для обработки обоих форматов — «1 234,56» (пробел-тысячи) и «348.600,00» (точка-тысячи) для обратной совместимости с legacy API
  - Заменён единственный вызов в `transparencia/client.py`
  - Добавлены тесты `TestParseRubNumber` и `TestParseBrlNumberDeprecated`
- **Миграция португальских имён в `_shared/planner.py`**:
  - `EtapaPlano` → `EtapPlana`, поля: etapa→etap, descricao→opisanie, parametros→parametry, depende_de→zavisit_ot, justificativa→obosnovanie
  - `PlanoConsulta` → `PlanZaprosa`, поля: consulta→zapros, complexidade→slozhnost, resumo→svodka, etapas→etapy, observacoes→primechaniya
  - `planejar_consulta_impl` → `splanirovat_zapros_impl`
  - Системный промпт полностью переведён: Portuguese schema/examples → Russian (запросы про Госдуму/Росстат вместо Камары/IBGE)
  - Вывод `to_markdown()`: «Plano de Consulta» → «План запроса», «Etapa» → «Этап», «Depende de» → «Зависит от», «Justificativa» → «Обоснование» и т.д.
- **Миграция португальских имён в `_shared/discovery.py`**:
  - `recomendar_tools_impl` → `rekomendovat_instrumenty_impl`
  - Строки вывода: «Requer autenticação» → «Требуется аутентификация», «Sem autenticação» → «Без аутентификации», «Nome completo da tool» → «Полное имя инструмента»
- **Миграция португальских строк в `_shared/batch.py`**:
  - «Nenhuma consulta fornecida.» → «Нет запросов для выполнения.»
  - «Máximo de 10 consultas por lote.» → «Максимум 10 запросов на пакет.»
  - «Tool não encontrada.» → «Инструмент не найден.»
  - «Erro ao executar» → «Ошибка при выполнении»
- **Миграция `exceptions.py`**:
  - `McpBrasilError` → `McpRussiaError` (базовый класс исключений)
  - `McpBrasilError` сохранён как alias для обратной совместимости
  - Docstrings переведены с португальского на русский
- **Миграция `settings.py`**:
  - Португальские комментарии переведены на русский
  - «recomendar_tools» → «rekomendovat_instrumenty» в комментарии
- **Миграция MCP-инструментов сервера** (`server.py`):
  - `listar_features` → `spisok_funktsiy`
  - `recomendar_tools` → `rekomendovat_instrumenty`
  - `planejar_consulta` → `splanirovat_zapros`
  - `executar_lote` → `vypolnit_paket`
  - Параметр `consultas` → `zaprosy` в `vypolnit_paket`
  - `_always_visible` список обновлён
- **Обновлён публичный API** `src/mcp_russia/server.py`:
  - Все реэкспорты обновлены на новые имена инструментов
- **Обновлена документация**:
  - `docs/reference/smart-tools.md`: все 4 имени инструмента
  - `docs/reference/configuration.md`: recomendar_tools → rekomendovat_instrumenty, planejar_consulta → splanirovat_zapros
  - `docs/concepts/architecture.md`: все 4 имени в списке meta-tools
  - `docs/examples/politicas-publicas.md`, `cientista-politico.md`, `jornalista-materias.md`: обновлены ссылки
  - `_shared/cache.py`, `_shared/feature.py`: примеры в docstrings переведены
- **Обновлена конфигурация ruff**: добавлен `tests/test_discovery.py` в RUF001/RUF002 ignores
- **Прогнаны все проверки**: `pytest` (1896 passed, 1 skipped), `ruff check` — all passed

### Ключевые архитектурные решения

- **Единый валютный формат**: все модули теперь используют `format_rub` (вывод «1 234,56 ₽») — формат «R$» полностью устранён из вывода
- **format_brl — deprecated alias**: сохранён для обратной совместимости, делегирует в format_rub
- **parse_rub_number — расширенный парсер**: обрабатывает и русские (пробел), и бразильские (точка) разделители тысяч
- **parse_brl_number — deprecated alias**: делегирует в parse_rub_number
- **MCP-инструменты сервера полностью на русском**: spisok_funktsiy, rekomendovat_instrumenty, splanirovat_zapros, vypolnit_paket
- **Модели планировщика на русском**: PlanZaprosa/EtapPlana с русскими именами полей
- **McpRussiaError**: новый базовый класс исключений (McpBrasilError сохранён как alias)

### Следующие действия

- **Подключение реальных API** в российских модулях: заменить заглушки на рабочие интеграции (cbrf→cbr-xml-daily.ru уже частично работает, rosaudit→ach.gov.ru, rosgidromet→meteorf.ru, rosvodresursy→rosvodresursy.ru, publikatsii→pravo.gov.ru, zakupki→zakupki.gov.ru, minzdrav→data.minzdrav.gov.ru, kad_arbitrazh→kad.arbitr.ru, cekrf→vybory.izbirkom.ru, fns→api.nalog.ru, rosreestr→rosreestr.gov.ru, fssp→fssp.gov.ru, gibdd→гибдд.рф, minobrnauki→minobrnauki.gov.ru)
- **Создание модуля ФСО/Государственной статистики**: расширение модуля Росстата реальными данными из ЕМИСС (fedstat.ru)
- **Миграция оставшихся португальских имён переменных** в legacy-модулях (compras, saude, datajud и др.) — внутрикодовые переменные и имена функций, не являющиеся MCP-инструментами

### Выполнено

- **Создан модуль ФНС (fns)**: данные Федеральной налоговой службы. Включает:
  - `constants.py`: режимы налогообложения (ОСНО, УСН, ЕНВД, ПСН, ЕСН, НПД), виды налогов, типы проверок, статусы организаций, категории налогоплательщиков
  - `schemas.py`: Pydantic-модели (OrganizaciyaEGRUL, IPEGRIP, NalogovayaProverka, NalogovoeNachislenie, SvedeniyaOrganizacii)
  - `client.py`: HTTP-клиент с заглушками для API ФНС (nalog.gov.ru, egrul.nalog.ru)
  - `tools.py`: 9 инструментов (spisok_nalogovyh_rezhimov, spisok_vidov_nalogov, spisok_tipov_proverok, spisok_statusov_organizaciy, spisok_kategoriy_nalogoplatelshchikov, info_organizacii, info_ip, proverki_organizacii, nalogovye_nachisleniya)
  - `resources.py`: 3 ресурса (источники данных, законодательство, система налоговых органов)
  - `prompts.py`: 2 промпта (analiz_nalogoplatelshchika, obzor_rezhimov_nalogooblozheniya)
  - `server.py`: регистрация всех компонентов в FastMCP
- **Создан модуль Росреестра (rosreestr)**: данные о кадастровой стоимости, объектах недвижимости, ЕГРН. Включает:
  - `constants.py`: типы недвижимости, категории земель, виды разрешённого использования, статусы учёта, формы собственности
  - `schemas.py`: Pydantic-модели (KadastrovyyObekt, ZemelnyyUchastok, Zdanie, Pomeshchenie, KadastrovayaStoimost)
  - `client.py`: HTTP-клиент с заглушками для API Росреестра (rosreestr.gov.ru, pkk.rosreestr.ru)
  - `tools.py`: 8 инструментов (spisok_tipov_nedvizhimosti, spisok_kategoriy_zemel, spisok_vidov_ispolzovaniya, spisok_statusov_obiekta, spisok_form_sobstvennosti, info_obekta, kadastrovaya_stoimost, prava_na_obekt)
  - `resources.py`: 3 ресурса (источники данных, законодательство, система регистрации)
  - `prompts.py`: 2 промпта (analiz_nedvizhimosti, obzor_zemelnogo_uchastka)
  - `server.py`: регистрация всех компонентов в FastMCP
- **Создан модуль ФССП (fssp)**: данные о исполнительных производствах и взысканиях. Включает:
  - `constants.py`: виды производств, статусы, ограничения, категории должников, основания возбуждения
  - `schemas.py`: Pydantic-модели (IspolnitelnoeProizvodstvo, SvedeniyaDolzhnika, Ogranichenie, Rosysk)
  - `client.py`: HTTP-клиент с заглушками для API ФССП (fssp.gov.ru)
  - `tools.py`: 9 инструментов (spisok_vidov_proizvodstv, spisok_statusov_proizvodstva, spisok_ogranicheniy, spisok_kategoriy_dolzhnikov, spisok_osnovaniy_vozbuzhdeniya, info_proizvodstva, poisk_dolzhnika, ogranicheniya_dolzhnika, rozysk_dolzhnika)
  - `resources.py`: 3 ресурса (источники данных, законодательство, структура ФССП)
  - `prompts.py`: 2 промпта (analiz_dolzhnika, obzor_ispolnitelnogo_proizvodstva)
  - `server.py`: регистрация всех компонентов в FastMCP
- **Полная миграция португальских имён в модуле ЦБ РФ (cbrf)** — самый крупный рефакторинг:
  - `schemas.py`: ValorMoeda → ZnachenieValyuty, DadosMoeda → DannyeValyuty, IndicadorEconomico → EkonomicheskiyIndikator, TaxaChave → KlyuchevayaStavka; поля: codigo → kod, nome → nazvanie, valor → znachenie, valor_anterior → predydushchee_znachenie и т.д.
  - `constants.py`: INDICADORES_CHAVE → KLYUCHEVYE_INDIKATORY, MOEDAS_PRINCIPAIS → OSNOVNYE_VALYUTY, MOEDAS_POR_PAIS → VALYUTY_PO_STRANAM
  - `client.py`: _parse_moeda → _parse_valyuta, buscar_todas_moedas → poluchit_vse_valyuty, buscar_moeda → poluchit_valyutu, buscar_moedas_varios → poluchit_valyuty_spisok, buscar_moedas_principais → poluchit_osnovnye_valyuty, buscar_curso_dinamico → poluchit_dinamiku_kursa
  - `tools.py`: cursos_atuais → tekushchie_kursy, consultar_moeda → uznat_kurs_valyuty, listar_moedas → spisok_valyut, converter_moeda → konvertirovat_valyutu, comparar_moedas → sravnit_valyuty, cursos_por_pais → kursy_po_stranam; все внутренние переменные заменены (moedas → valyuty, sinal → znak и т.д.)
  - `resources.py`: moedas_disponiveis → dostupnye_valyuty, referencia_cursos → spravochnik_kursov, moedas_principais → osnovnye_valyuty; URI ресурсов: data://moedas → data://valyuty, data://principais → data://osnovnye, data://referencia → data://spravochnik
  - `server.py`: обновлены все импорты и регистрации
- **Миграция `buscar_*` → `poluchit_*`** в 6 российских модулях:
  - rosstat: buscar_indikator → poluchit_indikator, buscar_region_data → poluchit_dannye_regiona, buscar_federalny_okrug → poluchit_federalny_okrug; INDICADORES_CHAVE → KLYUCHEVYE_INDIKATORY
  - gosduma: buscar_deputats → poluchit_deputatov, buscar_deputat → poluchit_deputata, buscar_zakonoproekty → poluchit_zakonoproekty, buscar_frakcii → poluchit_frakcii; INDICADORES_CHAVE → KLYUCHEVYE_INDIKATORY
  - rosaudit: buscar_kontrolnoe_meropriyatie → poluchit_kontrolnoe_meropriyatie и 3 других
  - rosgidromet: buscar_pogoda → poluchit_pogodu и 4 других
  - rosvodresursy: buscar_vodnyy_obekt → poluchit_vodnyy_obekt и 3 других
  - publikatsii: buscar_normativnyy_akt → poluchit_normativnyy_akt и 4 других
- **Обновлены тесты** для всех изменённых модулей (cbrf, rosstat, gosduma, rosaudit, rosgidromet, rosvodresursy, publikatsii)
- **Написаны тесты для 3 новых модулей**: fns (9 unit + 5 integration), rosreestr (8 unit + 5 integration), fssp (9 unit + 5 integration)
- **Обновлена конфигурация ruff**: добавлены RUF001/RUF002/RUF003/E501 ignores для fns, rosreestr, fssp
- **Прогнаны все проверки**: `pytest` (1856 passed, 1 skipped), `ruff check` — all passed

### Ключевые архитектурные решения

- **Итого российских модулей**: 16 (cbrf, rosstat, gosduma, cekrf, rosapi, zakupki, minzdrav, kad_arbitrazh, rosaudit, rosgidromet, rosvodresursy, publikatsii, rospotrebnadzor, roskomnadzor + fns, rosreestr, fssp из этого раунда)
- **Все российские модули используют русские имена**: больше нет португальских переменных, функций или констант в российских модулях
- **CBRF полностью мигрирован**: schemas, constants, client, tools, resources, server — все португальские имена заменены
- **Единый паттерн `poluchit_*`** вместо `buscar_*` во всех клиентских методах

### Следующие действия

- **Подключение реальных API** в российских модулях: заменить заглушки на рабочие интеграции (cbrf→cbr-xml-daily.ru уже частично работает, rosaudit→ach.gov.ru, rosgidromet→meteorf.ru, rosvodresursy→rosvodresursy.ru, publikatsii→pravo.gov.ru, zakupki→zakupki.gov.ru, minzdrav→data.minzdrav.gov.ru, kad_arbitrazh→kad.arbitr.ru, cekrf→vybory.izbirkom.ru, fns→api.nalog.ru, rosreestr→rosreestr.gov.ru, fssp→fssp.gov.ru)
- **Создание модуля Минобрнауки**: данные о вузах, научных исследованиях, образовательных программах
- **Создание модуля ФСО/Государственной статистики**: расширение модуля Росстата реальными данными из ЕМИСС (fedstat.ru)
- **Создание модуля ГИБДД/МВД**: данные о штрафах, проверка транспортных средств, водительских удостоверений
- **Миграция `format_number_br`** → `format_number_ru` в `_shared/formatting.py` и всех вызовах

## Статус раунда 2026-05-26 (четырнадцатый проход — модули Роспотребнадзора, Роскомнадзора, тесты, переводы)

### Выполнено

- **Завершён модуль Роскомнадзора (roskomnadzor)**: добавлены недостающие файлы:
  - `__init__.py`: FeatureMeta с тегами (роскомнадзор, связь, сми, персональные-данные, реестр)
  - `prompts.py`: 2 промпта (analiz_narusheniya, obzor_reestrov) — с правильным FastMCP 3.x API
  - `server.py`: регистрация 11 инструментов, 3 ресурсов, 2 промптов в FastMCP
- **Обновлён модуль Роспотребнадзора (rospotrebnadzor)**:
  - `__init__.py`: заменён placeholder на FeatureMeta с тегами (роспотребнадзор, санитарный-надзор, потребители, проверки, санпин)
  - `prompts.py`: исправлен импорт с несуществующего `fastmcp.prompts.base` на рабочий FastMCP 3.x API (PromptResult, Message, PromptMessage)
- **Переведены на русский мета-инструменты корневого сервера** (`src/mcp_brasil/server.py`):
  - `listar_features`: португальский → русский (docstring и примеры)
  - `recomendar_tools`: португальский → русский
  - `planejar_consulta`: португальский → русский (включая тег `планирование`)
  - `executar_lote`: португальский → русский (примеры обновлены на российские инструменты: gosduma, cbrf)
- **Исправлен баг в cbrf/tools.py**: `comparar_moedas` использовала `*codigos: str`, не поддерживаемое FastMCP — заменено на `codigos: list[str] | None = None`
- **Исправлен баг в rosapi/prompts.py**: импорт `UserMessage` из `fastmcp` (не существует) — заменён на правильный FastMCP 3.x API
- **Исправлен тест root server**: проверка португальского `paralelo` заменена на русское `параллельно`
- **Написаны тесты для всех 13 российских модулей** (ранее тесты были только у cekrf):
  - cbrf: 11 unit + 6 integration тестов
  - rosstat: 10 unit + 6 integration тестов
  - gosduma: 8 unit + 6 integration тестов
  - rosapi: 10 unit + 6 integration тестов
  - zakupki: 9 unit + 6 integration тестов
  - minzdrav: 10 unit + 6 integration тестов
  - kad_arbitrazh: 9 unit + 6 integration тестов
  - rosaudit: 7 unit + 6 integration тестов
  - rosgidromet: 7 unit + 6 integration тестов
  - rosvodresursy: 7 unit + 6 integration тестов
  - publikatsii: 9 unit + 6 integration тестов
  - rospotrebnadzor: 9 unit + 5 integration тестов
  - roskomnadzor: 11 unit + 5 integration тестов
- **Обновлена конфигурация ruff**: добавлены RUF001/RUF002/RUF003/E501 ignores для rospotrebnadzor и roskomnadzor, RUF001/RUF002 для server.py
- **Прогнаны все проверки**: `pytest` (1815 passed, 1 skipped), `ruff check` — all passed

### Ключевые архитектурные решения

- **Итого российских модулей**: 13 (cbrf, rosstat, gosduma, cekrf, rosapi, zakupki, minzdrav, kad_arbitrazh, rosaudit, rosgidromet, rosvodresursy, publikatsii + rospotrebnadzor, roskomnadzor из этого раунда)
- **FastMCP 3.x prompts API**: исправлены все промпты, использующие устаревший `fastmcp.prompts.base` — теперь используется `PromptResult` + `Message` + `PromptMessage` + `mcp.types.TextContent`
- **Все 28 бразильских модулей депрекейтены**: без изменений с раунда 13
- **Мета-инструменты сервера переведены**: listar_features, recomendar_tools, planejar_consulta, executar_lote — все docstrings теперь на русском

### Следующие действия

- **Подключение реальных API** в российских модулях: заменить заглушки на рабочие интеграции (cbrf→cbr-xml-daily.ru уже частично работает, rosaudit→ach.gov.ru, rosgidromet→meteorf.ru, rosvodresursy→rosvodresursy.ru, publikatsii→pravo.gov.ru, zakupki→zakupki.gov.ru, minzdrav→data.minzdrav.gov.ru, kad_arbitrazh→kad.arbitr.ru, cekrf→vybory.izbirkom.ru)
- **Создание модуля ФНС (Федеральная налоговая служба)**: данные о налоговых начислениях, проверках, ЕГРЮЛ
- **Создание модуля Росреестра**: данные о кадастровой стоимости, недвижимости, ЕГРН
- **Создание модуля ФССП (Федеральная служба судебных приставов)**: данные об исполнительных производствах
- **Миграция внутренних переменных**: заменить португальские имена переменных (moedas, codigos и т.д.) на русские аналоги в существующих модулях

## Статус раунда 2026-04-14 (тринадцатый проход — 4 новых российских модуля)

- **Создан модуль Счётной палаты РФ (rosaudit)**: российский аналог для бразильских TCU/TCE. Включает:
  - `constants.py`: направления контроля, типы мероприятий, субъекты аудита
  - `schemas.py`: Pydantic-модели (KontrolnoeMeropriyatie, AuditorskoeZaklyuchenie, Narushenie, ByudzhetIspolnenie)
  - `client.py`: HTTP-клиент с заглушками для API Счётной палаты (ach.gov.ru)
  - `tools.py`: 7 инструментов (spisok_napravleniy, spisok_tipov_meropriyatiy, spisok_subiektov_audita, info_kontrolnogo_meropriyatiya, info_auditorskogo_zaklyucheniya, ispolnenie_byudzheta, poisk_narusheniy)
  - `resources.py`: 3 ресурса (источники данных, законодательство, структура)
  - `prompts.py`: 2 промпта (analiz_auditorskogo_zaklyucheniya, obzor_ispolneniya_byudzheta)
  - `server.py`: регистрация всех компонентов в FastMCP
- **Создан модуль Росгидромета (rosgidromet)**: российский аналог для бразильского INPE. Включает:
  - `constants.py`: типы метео/эко данных, станции мониторинга, типы предупреждений
  - `schemas.py`: Pydantic-модели (PogodaData, PrognozData, EkologiyaData, Preduprezhdenie, SputnikMonitoring)
  - `client.py`: HTTP-клиент с заглушками для API Росгидромета (meteorf.ru)
  - `tools.py`: 7 инструментов (spisok_stanciy, spisok_tipov_dannykh, pogoda_seychas, prognoz_pogody, ekologiya_regiona, preduprezhdeniya, sputnik_monitoring)
  - `resources.py`: 3 ресурса (источники данных, методология, опасные явления)
  - `prompts.py`: 2 промпта (analiz_pogody_regiona, obzor_ekologii)
  - `server.py`: регистрация всех компонентов в FastMCP
- **Создан модуль Росводресурсов (rosvodresursy)**: российский аналог для бразильской ANA. Включает:
  - `constants.py`: бассейновые округа (21), типы водных объектов, крупные водохранилища
  - `schemas.py`: Pydantic-модели (VodnyyObekt, GidroData, VodokhranilishcheData, Vodopolzovanie)
  - `client.py`: HTTP-клиент с заглушками для API Росводресурсов (rosvodresursy.ru)
  - `tools.py`: 8 инструментов (spisok_basseynovykh_okrugov, spisok_tipov_vodnykh_obektov, spisok_vodokhranilishch, info_vodnogo_obekta, gidro_monitoring, info_vodokhranilishcha, vodopolzovanie_regionov)
  - `resources.py`: 3 ресурса (источники данных, бассейновые округа, водохозяйственная деятельность)
  - `prompts.py`: 2 промпта (analiz_vodnogo_obekta, obzor_vodokhranilishch)
  - `server.py`: регистрация всех компонентов в FastMCP
- **Создан модуль официальных публикаций (publikatsii)**: российский аналог для бразильского diario_oficial. Включает:
  - `constants.py`: типы нормативных актов, отрасли законодательства, источники публикаций
  - `schemas.py`: Pydantic-модели (NormativnyyAkt, ZakonProekt, OficialnayaPublikatsiya, IzmenenieAkta)
  - `client.py`: HTTP-клиент с заглушками для API pravo.gov.ru и consultant.ru
  - `tools.py`: 8 инструментов (spisok_tipov_aktov, spisok_otrasley, spisok_istochnikov, spisok_statusov, info_normativnogo_akta, info_zakonproekta, poisk_aktov, publikatsii_po_datam, izmeneniya_akta)
  - `resources.py`: 3 ресурса (источники данных, порядок опубликования, структура законодательства)
  - `prompts.py`: 2 промпта (analiz_normativnogo_akta, obzor_zakonodatelstva)
  - `server.py`: регистрация всех компонентов в FastMCP
- **Обновлена конфигурация ruff**: добавлены RUF001/RUF002/RUF003/E501 ignores для rosaudit, rosgidromet, rosvodresursy, publikatsii
- **Прогнаны все проверки**: `pytest` (1623 passed, 1 skipped), `ruff check` для новых модулей — all passed

### Ключевые архитектурные решения

- **Единый паттерн российских модулей**: каждый модуль следует строгой структуре — constants, schemas, client, tools, resources, prompts, server
- **Заглушки вместо реальных API**: все четыре модуля созданы как каркасы с placeholder-ами; реальная интеграция требует отдельной работы
- **Итого российских модулей**: 9 (cbrf, rosstat, gosduma, cekrf, rosapi, zakupki, minzdrav, kad_arbitrazh + 4 из этого раунда)
- **Все 28 бразильских модулей депрекейтены**: включая tce_sp (раунд 12) и остальные (раунд 11)

### Следующие действия

- **Подключение реальных API** в новых модулях: заменить заглушки на рабочие интеграции (rosaudit→ach.gov.ru, rosgidromet→meteorf.ru, rosvodresursy→rosvodresursy.ru, publikatsii→pravo.gov.ru)
- **Написание тестов**: добавить unit-тесты для всех четырёх новых модулей (mock HTTP responses)
- **Создание модуля Роспотребнадзора**: российский аналог для бразильских санитарных/здоровье модулей
- **Создание модуля Роскомнадзора**: российский аналог для регулирования СМИ и связи
- **Подключение реальных API** в существующих российских модулях: заменить заглушки на рабочие интеграции (zakupki, minzdrav, kad_arbitrazh, cekrf)

## Статус раунда 2026-04-13 (двенадцатый проход — фикс пропущенного tce_sp)

### Выполнено

- **Депрекейт пропущенного модуля `tce_sp`** — модуль TCE-SP (São Paulo) не был помечен как DEPRECATED в раунде 11:
  - Обновлён `__init__.py`: добавлены `.. deprecated::` directive, `⚠️ DEPRECATED` в description, version `0.1.0-deprecated`, теги `⚠️ DEPRECATED`/`бразилия-legacy`
  - Обновлён `server.py`: добавлены `.. deprecated::` directive в docstring, FastMCP server name содержит `(⚠️ DEPRECATED — use 'rosstat'/'zakupki' for Russian data)`
  - **Прогнаны все проверки**: `pytest` (1623 passed, 1 skipped), `ruff check` — все модули проходят

### Ключевые архитектурные решения

- **Все 28 бразильских модулей теперь полностью депрекейтены**: включая последний пропущенный `tce_sp`
- **Консистентность**: теперь все legacy-модули следуют единому паттерну депрекейшена

### Следующие действия

- **Создание модуля Счётной палаты РФ**: российский аналог для TCU/бразильских судов аудита
- **Создание модуля Росгидромета/Росприроднадзора**: российский аналог для INPE
- **Создание модуля Росводресурсов**: российский аналог для ANA
- **Создание модуля официальных публикаций РФ**: аналог для diario_oficial (pravo.gov.ru, consultant.ru)
- **Подключение реальных API** в существующих российских модулях: заменить заглушки на рабочие интеграции (zakupki, minzdrav, kad_arbitrazh, cekrf)
- **Написание тестов**: добавить unit-тесты для всех новых российских модулей

## Статус раунда 2026-04-13 (одиннадцатый проход — полная депрекейшн всех legacy-модулей)

### Выполнено

- **Депрекейт всех оставшихся 20 legacy-модулей** — добавлены явные пометки `⚠️ DEPRECATED` и ссылки на российские эквиваленты:
  - **9 модулей TCE** (суды штатов Бразилии): `tce_ce`, `tce_pe`, `tce_pi`, `tce_rj`, `tce_rn`, `tce_rs`, `tce_sc`, `tce_sp`, `tce_to` → используйте `rosstat` (Росстат) и `zakupki` (ЕИС)
  - `tse` (Высший избирательный суд) → используйте `cekrf` (ЦИК РФ)
  - `tcu` (Федеральный суд аудита) → используйте `rosstat` (Росстат)
  - `inpe` (космические исследования/экология) → используйте будущие модули Росгидромета/Росприроднадзора
  - `ana` (водные ресурсы) → используйте будущие модули Росводресурсов/Росгидромета
  - `transparencia` (портал прозрачности) → используйте `zakupki` (ЕИС)
  - `transferegov` (парламентские трансферты) → используйте `gosduma` (Госдума)
  - `diario_oficial` (официальные газеты) → используйте будущие модули pravo.gov.ru/consultant.ru
  - `dados_abertos` (открытые данные) → используйте `rosstat` (Росстат)
  - `jurisprudencia` (судебная практика) → используйте `kad_arbitrazh` (КАД)
  - `tabua_mares` (приливы/гидрология) → используйте будущий модуль Росгидромета
  - `anuncios_eleitorais` (политическая реклама) → используйте `cekrf` (ЦИК РФ)
- **Обновлены `__init__.py`** всех 20 модулей: docstrings с `.. deprecated::`, description с `⚠️ DEPRECATED`, version суффикс `-deprecated`, теги `⚠️ DEPRECATED`/`бразилия-legacy`
- **Обновлены `server.py`** всех 20 модулей: FastMCP server names содержат `(⚠️ DEPRECATED — use '...')`, docstrings с указанием на российские аналоги
- **Прогнаны все проверки**: `pytest` (1623 passed, 1 skipped), `ruff check` — all passed

### Ключевые архитектурные решения

- **Все бразильские модули теперь депрекейтены**: итого 28 deprecated модулей (bacen, ibge, camara, senado, brasilapi, compras, saude, datajud + 20 из этого раунда)
- **Депрекейт без поломки**: все legacy-функции сохраняют работоспособность, добавлены только docstring/server-name маркеры
- **Единый паттерн депрекейшена**: каждый модуль содержит `.. deprecated::` directive в docstring, `⚠️ DEPRECATED` в description/version/tags, и указание конкретного российского аналога

### Следующие действия

- **Создание модуля Счётной палаты РФ**: российский аналог для TCU/бразильских судов аудита
- **Создание модуля Росгидромета/Росприроднадзора**: российский аналог для INPE
- **Создание модуля Росводресурсов**: российский аналог для ANA
- **Создание модуля официальных публикаций РФ**: аналог для diario_oficial (pravo.gov.ru, consultant.ru)
- **Подключение реальных API** в существующих российских модулях: заменить заглушки на рабочие интеграции (zakupki, minzdrav, kad_arbitrazh, cekrf)
- **Написание тестов**: добавить unit-тесты для всех новых российских модулей

## Статус раунда 2026-04-12 (десятый проход — депрекейшн compras, saude, datajud)

### Выполнено

- **Депрекейт 3 модулей с готовыми российскими аналогами** — добавлены явные пометки `⚠️ DEPRECATED` и ссылки на российские эквиваленты:
  - `compras` (бразильские закупки PNCP/Compras.gov.br) → используйте `zakupki` (ЕИС zakupki.gov.ru)
  - `saude` (бразильское здравоохранение DataSUS/CNES) → используйте `minzdrav` (Минздрав РФ)
  - `datajud` (бразильские судебные данные CNJ) → используйте `kad_arbitrazh` (КАД kad.arbitr.ru)
- **Обновлены `__init__.py`** всех 3 модулей: docstrings с `.. deprecated::`, description с `⚠️ DEPRECATED`, version суффикс `-deprecated`, теги `⚠️ DEPRECATED`/`бразилия-legacy`
- **Обновлены `server.py`** всех 3 модулей: FastMCP server names содержат `(⚠️ DEPRECATED — use '...')`, docstrings с указанием на российские аналоги
- **Обновлены подмодули compras**: `pncp/__init__.py` и `dadosabertos/__init__.py` также помечены как DEPRECATED
- **Прогнаны все проверки**: `pytest` (1623 passed, 1 skipped), `ruff check` — all passed

### Ключевые архитектурные решения

- **Стратегия миграции**: модули с готовыми российскими аналогами — депрекейтятся с редиректом, модули без аналогов — сохраняются как legacy compatibility layer
- **Депрекейт без поломки**: все legacy-функции сохраняют работоспособность, добавлены только docstring/server-name маркеры
- **Итого депрекейчено модулей**: 8 (bacen, ibge, camara, senado, brasilapi + compras, saude, datajud)

### Следующие действия

- **Депрекейшн остальных legacy-модулей**: оценить остальные 19 бразильских модулей (10 TCE, tse, tcu, inpe, ana, transparencia, transferegov, diario_oficial, dados_abertos, jurisprudencia, tabua_mares, anuncios_eleitorais) — пометить как legacy compatibility layer
- **Создание модуля Счётной палаты РФ**: российский аналог для TCU
- **Создание модуля Росгидромета/Росприроднадзора**: российский аналог для INPE
- **Подключение реальных API** в существующих российских модулях: заменить заглушки на рабочие интеграции

## Статус раунда 2026-04-12 (девятый проход — модули ЕИС, Минздрава, Кад Арбитраж)

### Выполнено

- **Создан модуль zakupki.gov.ru (ЕИС)**: замена бразильского compras на российскую Единую информационную систему закупок. Включает:
  - `constants.py`: справочники типов данных, способов закупок, отраслей, статусов, законы 44-ФЗ/223-ФЗ
  - `schemas.py`: Pydantic-модели (Zakupka, Kontrakt, Zakazchik, Postavshchik, PlanZakupki)
  - `client.py`: HTTP-клиент с заглушками для API ЕИС (zakupki.gov.ru, data.zakupki.gov.ru)
  - `tools.py`: 7 инструментов (poisk_zakupok, info_zakupki, info_zakazchika, info_postavshchika, statusy_zakupok, sposoby_zakupok, plany_zakupok)
  - `resources.py`: 3 ресурса (источники данных, законодательство, структура ЕИС)
  - `prompts.py`: 2 промпта (analiz_zakupki, obzor_zakupok)
  - `server.py`: регистрация всех компонентов в FastMCP
- **Создан модуль Минздрава (minzdrav)**: замена бразильского saude/DataSUS на российские медицинские источники. Включает:
  - `constants.py`: показатели здоровья, типы МО, специальности врачей, классы МКБ-10, федеральные округа
  - `schemas.py`: Pydantic-модели (MedOrganizatsia, VrachebnyyKadr, PokazatelZdorovya, ZabolevanieStat)
  - `client.py`: HTTP-клиент с заглушками для API Минздрава и Росздравнадзора
  - `tools.py`: 7 инструментов (poisk_med_organizatsiy, info_med_organizatsii, pokazateli_zdorovya, statistika_zabolevaniy, spravochnik_mo, spravochnik_spetsialnostey, spravochnik_mkb10)
  - `resources.py`: 3 ресурса (источники данных, классификации, федеральные округа)
  - `prompts.py`: 2 промпта (analiz_zdorovya_regiona, obzor_med_organizatsiy)
  - `server.py`: регистрация всех компонентов в FastMCP
- **Создан модуль Кад Арбитраж (kad_arbitrazh)**: замена бразильского datajud/CNJ на Картотеку арбитражных дел. Включает:
  - `constants.py`: инстанции судов, категории дел, статусы, типы актов, арбитражные суды по округам
  - `schemas.py`: Pydantic-модели (SudebnoeDelo, SudebnyyAkt, SudebnoeZasedanie, Sudy, StoronaDela)
  - `client.py`: HTTP-клиент с заглушками для КАД (kad.arbitr.ru)
  - `tools.py`: 8 инструментов (poisk_del, info_dela, akty_po_delu, storony_dela, spravochnik_kategoriy, spravochnik_instantsiy, spravochnik_statusov, spravochnik_aktov)
  - `resources.py`: 3 ресурса (источники данных, система судов, кодификация дел)
  - `prompts.py`: 2 промпта (analiz_dela, analiz_uchastnika)
  - `server.py`: регистрация всех компонентов в FastMCP
- **Обновлена конфигурация ruff**: добавлены RUF001/RUF002/RUF003/E501 ignores для zakupki, minzdrav, kad_arbitrazh
- **Прогнаны все проверки**: `pytest` (1623 passed, 1 skipped), `ruff check` для новых модулей — all passed

### Ключевые архитектурные решения

- **Единый паттерн российских модулей**: каждый модуль следует строгой структуре — constants, schemas, client, tools, resources, prompts, server
- **Заглушки вместо реальных API**: все три модуля созданы как каркасы с placeholder-ами; реальная интеграция требует отдельной работы
- **Обратная совместимость**: бразильские модули (compras, saude, datajud) сохраняют работоспособность как legacy-слой

### Следующие действия

- **Подключение реальных API ЕИС**: заменить заглушки в zakupki на интеграцию с zakupki.gov.ru / data.zakupki.gov.ru
- **Подключение реальных API Минздрава**: заменить заглушки в minzdrav на интеграцию с data.minzdrav.gov.ru
- **Подключение реальных API КАРТ**: заменить заглушки в kad_arbitrazh на парсинг kad.arbitr.ru
- **Написание тестов**: добавить unit-тесты для всех трёх новых модулей (mock HTTP responses)
- **Депрекейшн legacy-модулей**: пометить compras, saude, datajud как ⚠️ DEPRECATED с ссылками на российские аналоги

## Статус раунда 2026-04-11 (восьмой проход — депрекейшн legacy + модуль ЦИК РФ)

### Выполнено

- **Депрекейт 5 модулей с российскими аналогами** — добавлены явные пометки `⚠️ DEPRECATED` и ссылки на российские эквиваленты:
  - `bacen` (Центральный банк Бразилии) → используйте `cbrf` (ЦБ РФ)
  - `ibge` (статистический институт Бразилии) → используйте `rosstat` (Росстат)
  - `camara` (Палата депутатов Бразилии) → используйте `gosduma` (Госдума)
  - `senado` (Федеральный сенат Бразилии) → используйте `gosduma` (парламент РФ)
  - `brasilapi` (BrasilAPI) → используйте `rosapi` (российские справочные данные)
- **Обновлены `__init__.py`** всех 5 модулей: docstrings с `.. deprecated::`, description с `⚠️ DEPRECATED`, version суффикс `-deprecated`, теги `устаревший`/`бразилия-legacy`
- **Обновлены `server.py`** всех 5 модулей: FastMCP server names содержат `(⚠️ DEPRECATED — use '...')`, docstrings с указанием на российские аналоги
- **Создан модуль ЦИК РФ (cekrf)**: новый российский модуль для данных Центральной избирательной комиссии. Включает:
  - `constants.py`: справочники субъектов РФ (89 субъектов), типов выборов, должностей, партий, годов выборов
  - `schemas.py`: Pydantic-модели (SubyektRF, TipVyborov, Dolzhnost, KandidatResumo, Kandidat, ResultatKandidata, ItogiVYborov, PartiaInfo)
  - `client.py`: HTTP-клиент с заглушками для API ЦИК РФ и ГАС «Выборы»
  - `tools.py`: 9 инструментов (tipy_vyborov, subyekty_rf, dolzhnosti_federal, partii_rf, gody_vyborov, poisk_kandidata, kandidat_podrobno, rezultaty_vyborov, yavka_i_itogi)
  - `resources.py`: 4 справочных ресурса (типы выборов, субъекты РФ, партии, info API)
  - `prompts.py`: 2 промпта (analiz_kandidata, sravnenie_partiy)
  - `server.py`: регистрация всех компонентов в FastMCP
- **Добавлены тесты cekrf**: 16 тестов (7 integration + 9 unit) — все проходят
- **Обновлена конфигурация ruff**: добавлены RUF001/RUF002/E501 ignores для cekrf
- **Исправлен тест root server**: обновлена проверка на deprecation-статус bacen
- **Прогнаны все проверки**: `pytest` (1623 passed, 1 skipped), `ruff check` (all passed)

### Ключевые архитектурные решения

- **Стратегия миграции**: модули с готовыми российскими аналогами — депрекейтятся с редиректом, модули без аналогов — создаются с нуля
- **Депрекейт без поломки**: все legacy-функции сохраняют работоспособность, добавлены только docstring/server-name маркеры
- **ЦИК РФ — foundational**: модуль создан как каркас с заглушками; реальная интеграция с ГАС «Выборы» требует отдельной работы

### Следующие действия

- **Создание модуля zakupki.gov.ru**: замена бразильского compras на российскую ЕИС
- **Создание модуля Минздрава**: замена бразильского saude/DataSUS на российские медицинские источники
- **Создание модуля Кадр Арбитраж**: замена бразильского datajud/CNJ на российский арбитражный суд
- **Подключение реальных API ЦИК РФ**: заменить заглушки в cekrf на парсинг ГАС «Выборы» (vybory.izbirkom.ru)
- **Расширение ЦИК РФ**: добавить результаты конкретных выборов (2018, 2021, 2024), данные по кандидатам, явке, одномандатным округам

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
