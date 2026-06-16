<div align="center">

<img src="docs/assets/logo.png" alt="mcp-russia logo" width="100">

# mcp-russia

**Русскоязычная адаптация MCP-репозитория для работы с государственными и публичными данными**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

## Статус

Репозиторий полностью переведён на российские и русскоязычные реалии.

Python-пакет `mcp_russia` является единой точкой входа. Все 27 legacy-модулей с бразильскими данными удалены из кодовой базы.

22 российских модуля активны и подключены к реальным API. Сервер экспонирует только русскоязычные инструменты и ресурсы.

## Что уже сделано

- Python-пакет полностью перенесён в `mcp_russia` (исторический `mcp_brasil` устранён).
- Переменные окружения унифицированы: `MCP_RUSSIA_*` (fallback на `MCP_BRASIL_*` удалён).
- Корневой сервер автообнаруживает features из `mcp_russia.data` и `mcp_russia.agenty`.
- Мета-инструменты сервера на русском: `spisok_funktsiy`, `rekomendovat_instrumenty`, `splanirovat_zapros`, `vypolnit_paket`.
- Базовый класс исключений: `McpRussiaError` (устаревший `McpBrasilError` удалён).
- 23 российских модуля данных, подключённых к реальным API-интеграциям.
- Все 27 legacy-модулей с бразильскими данными удалены из кодовой базы.
- Устранены deprecated-алиасы: `format_brl`, `format_number_br`, `parse_brl_number` удалены.
- Устранены Brazilian validators: `validate_cpf`, `validate_cnpj`, `validate_cep` удалены.
- Российские модули: ЦБ РФ (cbr-xml-daily.ru), Росгидромет (open-meteo.com), ФНС (egrul.nalog.ru), Госдума (api.duma.gov.ru), Закупки (zakupki.gov.ru), Картотека арбитражных дел (kad.arbitr.ru), РосАПИ (Dadata), Росреестр (pkk.rosreestr.ru), ГИБДД (гибдд.рф), ЦИК РФ (vybory.izbirkom.ru), ФССП (fssp.gov.ru), Официальные публикации (pravo.gov.ru), Минобрнауки (obrnadzor.gov.ru), Роспотребнадзор (proverki.rospotrebnadzor.ru), Роскомнадзор (rkn.gov.ru), Росстат (fedstat.ru), Росводресурсы (text.water.ru, gmvo.skniigkh.ru), Минздрав (data.minzdrav.gov.ru, roszdravnadzor.gov.ru), Счётная палата (ach.gov.ru, budget.gov.ru), Совет Федерации (sovfed.ru, data.gov.ru), Федеральное казначейство (roskazna.gov.ru, budget.gov.ru), Росприроднадзор (rpn.gov.ru), МЧС России (mchs.gov.ru, data.mchs.gov.ru, fires.ru).
- Универсальный инструмент Росстата `indikator_dannye` для запроса данных по произвольному коду ЕМИСС.
- Инструменты отраслевой структуры ВРП (`otraslevaya_struktura_vrp`) и инвестиций по видам деятельности (`investitsii_po_vidam`).

## Что здесь есть

- Архитектура MCP-сервера на Python с auto-registry для features.
- 22 активных российских модуля с реальными интеграциями: курсы валют ЦБ РФ, погода и качество воздуха (Open-Meteo), ЕГРЮЛ/ЕГРИП (egrul.nalog.ru), депутаты и законопроекты Госдумы (api.duma.gov.ru), закупки и контракты (zakupki.gov.ru), арбитражные дела (kad.arbitr.ru), адреса и организации (Dadata), кадастровые данные (pkk.rosreestr.ru), проверки ТС и ВУ (гибдд.рф), выборы и кандидаты (vybory.izbirkom.ru), исполнительные производства (fssp.gov.ru), правовые акты (pravo.gov.ru), аккредитация вузов (obrnadzor.gov.ru), проверки Роспотребнадзора (proverki.rospotrebnadzor.ru), реестры Роскомнадзора (rkn.gov.ru), статистические показатели (fedstat.ru), водные объекты и гидрология (text.water.ru, gmvo.skniigkh.ru), медицинские организации и лицензии (data.minzdrav.gov.ru, roszdravnadzor.gov.ru), контрольные мероприятия и бюджет (ach.gov.ru, budget.gov.ru), Совет Федерации (sovfed.ru, data.gov.ru), Федеральное казначейство (roskazna.gov.ru, budget.gov.ru), Росприроднадзор (rpn.gov.ru).
- МЧС России (mchs.gov.ru, data.mchs.gov.ru, fires.ru): статистика пожаров, чрезвычайные ситуации, радиационный мониторинг, гидрологическая обстановка, предупреждения о ЧС.
- Инструменты разработки: `uv`, `pytest`, `ruff`, `mypy`, `Makefile`.

## Текущее направление адаптации

- углубить существующие интеграции (расширение данных по регионам, EMISS-коды);
- дочистить документацию от исторических бразильских формулировок;
- обновить примеры, тесты и справочные материалы под российские сценарии использования.

## Список задач

Живой список задач и статусов текущей миграции ведется в [TODO.md](TODO.md).

## Быстрый старт для разработки

```bash
git clone git@github.com:denis-gordeev/mcp-russia.git
cd mcp-russia
make dev
```

Локальные команды:

```bash
make test             # Запустить все тесты
make test-feature F=cbrf
make lint
make types
make ci
make run
make serve
make inspect
```

Часть документации ещё содержит бразильский контекст. Рабочая точка входа для запуска и разработки — `mcp_russia`.

## Архитектура

Проект использует подход package-by-feature:

```text
src/mcp_russia/
├── server.py
├── settings.py
├── exceptions.py
├── _shared/
├── data/
└── agenty/
```

Каждая feature инкапсулирует:

- `client.py` для HTTP-интеграции;
- `tools.py` для MCP tools;
- `schemas.py` для моделей;
- `resources.py` и `prompts.py` при необходимости;
- `server.py` с `FastMCP`-регистрацией.

## Документация

Актуализируйте существующую документацию с учётом фактической структуры `src/mcp_russia/`. Часть файлов в `docs/` и `CHANGELOG.md` содержит исторические бразильские формулировки и требует отдельного прохода.

## Разработка и вклад

1. Работайте в небольших, изолированных изменениях.
2. Если меняете поведение кода, запускайте релевантные проверки.
3. Если переводите существующую feature на российский контекст, обновляйте одновременно код, тесты и документацию.
4. Для внешних изменений используйте pull request.

В репозитории отключены GitHub Issues, поэтому для предложений и исправлений ориентируйтесь на pull request и сопроводительное описание изменений.

## Дисклеймер

Проект прошёл полную миграцию на российские реалии. 23 модуля активны и подключены к реальным российским API. Legacy-модули с бразильскими данными удалены из кодовой базы.

Сервер не создаёт видимости официального государственного источника. При подключении интеграций явно указывается происхождение данных, ограничения покрытия и условия использования каждого внешнего API.

## Лицензия

MIT
