# TODO

Живой список задач по миграции `mcp-russia` на российские и русскоязычные реалии.

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
