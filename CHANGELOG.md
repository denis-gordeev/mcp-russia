# Changelog

Все заметные изменения mcp-russia документируются в этом файле.

> **Примечание:** записи до версии 0.5.0 относятся к периоду, когда проект ещё содержал бразильские legacy-модули. Все эти модули удалены из кодовой базы (см. TODO.md). Записи с пометкой `(legacy)` описывают модули, которые больше не существуют.

## [0.5.0] - 2026-03-27

### Исправления

- **anuncios_eleitorais (legacy):** Синхронизация клиента с форматом Meta Graph API

### Документация

- Удалены ссылки на ADR и раздел документации из CONTRIBUTING
- Обновление README: добавлен модуль tabua_mares (legacy) и исправлены подсчёты
- Удалён пример raio-x-parlamentar

### Новые функции

- **anuncios_eleitorais (legacy):** Модуль Meta Ad Library с 6 инструментами, 3 ресурсами и 3 промптами

## [0.4.0] - 2026-03-26

### Новые функции

- **tabua_mares (legacy):** Модуль таблиц приливов с 7 инструментами, ресурсами и промптами

## [0.3.4] - 2026-03-26

### Новые функции

- **legacy-модуль (camara):** Инструмент detal_zakonoproekta и улучшение poisk_zakonoproekta

## [0.3.3] - 2026-03-26

### Исправления

- **legacy-модули (transparencia,dados_abertos,diario_oficial):** Учёт ограничений API

## [0.3.2] - 2026-03-26

### Прочее

- Добавлены PyPI-ключевые слова и классификаторы

## [0.3.1] - 2026-03-26

### Исправления

- **code-mode:** Корректный fallback на BM25 при отсутствии pydantic-monty
- **legacy-модуль compras/pncp (legacy):** Переработка клиента под реальную спецификацию API
- **.gitignore:** Удаление временных файлов из каталога Claude
- **batch:** Исправление AsyncMock-спецификации для ctx inspection в тесте

### Сборка

- **deps:** Добавлен fastmcp[code-mode] extra в зависимости
- **deps:** Перенос anthropic в основные зависимости

### Документация

- Переработка README для публичного запуска и добавление лицензии MIT
- **examples:** Добавлено 11 руководств по использованию для разных профессий
- **readme:** Обновлён подсчёт инструментов с 205 до 204

### Новые функции

- **batch:** Инструмент vypolnit_paket для параллельного выполнения нескольких запросов
- **planner:** Инструмент splanirovat_zapros со структурированными планами выполнения

### Прочее

- Обновление конфигурации сборки и документации по архитектуре
- Добавление логотипа, обновление README и .gitignore
- Удаление внутренних файлов из отслеживания git
- Добавление белого варианта логотипа

### Производительность

- **tse (legacy):** Кеширование данных регионов в _enrich_candidate_names

## [0.3.0] - 2026-03-23

### Исправления

- **legacy-модуль tse:** Разрешение CDN-кодов выборов по типу должности
- **tests:** Установка TOOL_SEARCH=none в conftest.py до любого импорта

### Документация

- **contributing:** Добавлены правила релиза, CI/CD, шаблоны тестирования и информация о стеке
- Добавлены переменные tool search и LLM discovery в .env.example
- **tech-debt:** Добавлена депрекация comprasnet и статус модулей ТСЕ (legacy)

### Новые функции

- **compras (legacy):** Модуль открытых данных Compras.gov.br с 8 инструментами
- **tse (legacy):** Результаты выборов через CDN с 4 новыми инструментами
- **tcu (legacy):** TCU с 8 инструментами, 1 ресурсом и 1 промптом
- **tce_rj (legacy):** TCE-RJ с 7 инструментами, 1 ресурсом и 1 промптом
- **tools:** Добавлены семантические теги ко всем инструментам
- **tce_sp (legacy):** TCE-SP с 3 инструментами, 1 ресурсом и 1 промптом
- **tce_sp (legacy):** TCE-SP с 3 инструментами, 1 ресурсом и 1 промптом
- **legacy-модуль tse:** Результаты федеральных выборов через формат CDN
- **discovery:** BM25-поиск, code_mode и recomendar_tools
- **tce_ce (legacy):** TCE-CE с 4 инструментами, 1 ресурсом и 1 промптом
- **tce_pe (legacy):** TCE-PE с 5 инструментами, 1 ресурсом и 1 промптом
- **tce_rs (legacy):** TCE-RS с 5 инструментами, 1 ресурсом и 1 промптом
- **tce_sc (legacy):** TCE-SC с 2 инструментами, 1 ресурсом и 1 промптом
- **tce_rn (legacy):** TCE-RN с 5 инструментами, 1 ресурсом и 1 промптом
- **tce_to (legacy):** TCE-TO с 3 инструментами, 1 ресурсом и 1 промптом
- **tce_pi (legacy):** TCE-PI с 5 инструментами, 1 ресурсом и 1 промптом

## [0.2.2] - 2026-03-23

### Документация

- **release:** Добавлены правила релиза в CLAUDE.md и AGENTS.md

### Тестирование

- **compras (legacy):** Обновление тестов для подмодуля pncp

## [0.2.0] - 2026-03-23

### Исправления

- **transparencia (legacy):** Безопасный парсинг, rate limiting и защита от массовых запросов
- **senado (legacy):** Миграция эндпоинтов голосования на новый API
- **datajud (legacy):** Замена try-except-pass на contextlib.suppress
- **transferegov,transparencia (legacy):** Исправление маппинга API и парсинга чисел
- **diario_oficial (legacy):** Очистка HTML-тегов из выдержек
- **ibge (legacy):** Исправление ID агрегатов для pib_per_capita и area_territorial
- **datajud,transparencia (legacy):** Удаление STF из DataJud, исправление эндпоинта PEP

### Документация

- **tech-debt:** Обновление решённых позиций и исправление опечатки в заголовке
- Добавлены правила commit-on-green и tech-debt
- **adrs,skills:** Обновление шаблонов с ресурсами, промптами, контекстом и middleware
- Добавлен CONTRIBUTING.md

### Новые функции

- **shared:** HTTP-клиент и утилиты форматирования
- **core:** TTL-cache и миграция на dependency-groups
- **ibge,bacen (legacy):** Модули ibge и bacen
- **ibge,bacen,transparencia (legacy):** Сетка территорий, CNAE, клиент bacen и модуль transparencia
- Добавлены lifespan, context, resources, prompts и middleware
- **transparencia (legacy):** Ресурсы, промпты и интеграционные тесты
- **_shared:** Асинхронный RateLimiter со скользящим окном
- **transparencia (legacy):** Подсказки по пагинации в ответах инструментов
- **camara (legacy):** Инструменты для депутатов и законодательства
- **senado (legacy):** Инструменты для сенаторов и законодательства
- **legislativo (legacy):** Rate limiting для клиентов camara и senado
- **senado (legacy):** Инструменты partidos_senado и ufs_senado
- **judiciario (legacy):** Модули datajud, tse и jurisprudencia
- **phase4 (legacy):** Модули brasilapi (legacy), diario_oficial (legacy) и compras (legacy)
- **tse (legacy):** Дополнительные инструменты выборов
- **datajud (legacy):** TREs, TJMs, логические запросы и пагинация search_after
- **transparencia,transferegov (legacy):** Расширение до 18 инструментов + новый модуль transferegov
- **senado (legacy):** 4 инструмента открытых данных (поправки, блоки, лидерства, доклады)
- **tse (legacy):** Инструмент итогов выборов с тотализацией голосов
- Завершение mcp-russia с 4 новыми модулями (legacy) + расширение 3 существующих
- **tse (legacy):** Результаты выборов через CDN с 4 новыми инструментами
- **release:** Инфраструктура управления релизами

### Прочее

- Начальная структура проекта
- Добавлены claude code skills (commit, fastmcp, skill-creator)
- **config:** Переход с justfile на Makefile
- Обновление Makefile, README, .gitignore и .env.example
- Все tech-debt позиции transparencia (legacy) отмечены как решённые
- Добавлены тесты ibge, удалена конфигурация cursor
- Позиция пагинации tech-debt отмечена как by-design
- **transparencia (legacy):** Новые схемы и константы
- Автоматическая загрузка .env через dotenv

### Рефакторинг

- Переименование docs/ в plan/ и создание пустого docs/
- **registry:** Исправление mount API и добавление базовых модулей
- Реорганизация features в пакеты data/ и agentes/

### Тестирование

- **shared:** Набор тестов для базовых и общих модулей
- Добавлены интеграционные тесты для ресурсов, промптов и полного сервера
- **redator:** Интеграционные тесты для официальных документов (письмо, обращения)

<!-- generated by git-cliff -->
